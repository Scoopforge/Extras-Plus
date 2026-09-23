"""scoop-extras-plus skill self-check: offline, validates the package and repo baseline.

python scripts/sm_selftest.py            # full self-check
python scripts/sm_selftest.py --verbose  # print every detail
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from collections import OrderedDict
from pathlib import Path

# Let the script run from any cwd: the shared library sits next to it
sys.path.insert(0, str(Path(__file__).resolve().parent))

import sm_lib as L

# Windows consoles default to a non-UTF-8 codepage, which mangles non-ASCII output
L.use_utf8_stdio()

DUMMY = {
    "name": "selftest-app",
    "version": "9.9.9",
    "desc": "Selftest placeholder application",
    "homepage": "https://example.com",
    "license": "MIT",
    "url": "https://example.com/app-9.9.9.zip",
    "url64": "https://example.com/app-9.9.9-x64.zip",
    "url_arm64": "https://example.com/app-9.9.9-arm64.zip",
    "hash": "0" * 64,
    "hash64": "0" * 64,
    "hash_arm64": "1" * 64,
    "repo_url": "https://github.com/example/app",
    "shortcut_exe": "app.exe",
    "shortcut_name": "App",
    "bin_exe": "app.exe",
    "bin_alias": "app",
    "persist": "data",
    "notes": "Selftest notes.",
    "suggest": "extras/7zip",
    "depends": "scoopforge/comfyui",
    "installer_script": 'Start-Process -Wait "$dir\\setup.exe"',
    "uninstaller_script": 'Remove-Item "$dir\\leftover" -Recurse -Force',
    "post_install": "Write-Host 'done'",
    "pre_install": 'Remove-Item "$dir\\updater" -Force -Recurse',
    "extract_dir": "app-9.9.9",
    "extract_to": "app",
    "nsis_payload": "app-64.7z",
    "msi_mode": "extract",
    "msi_args": ["/qn"],
    "psmodule_name": "SelftestModule",
    "psmodule_path": "lib",
    "extra_urls": ["https://example.com/helper.ps1"],
    "extra_hashes": ["2" * 64],
    "env_add_path": "bin",
    "env_set": {"APP_HOME": "$dir"},
    "bin_entries": ["a.exe", ["b.exe", "b"]],
    "shortcut_entries": [["a.exe", "App"], ["b.exe", "App\\B"]],
    "comment": "Selftest comment.",
    "checkver_url": "https://example.com/downloads",
    "checkver_regex": "app-([\\d.]+)-x64\\.zip",
    "checkver_jsonpath": "$.tag_name",
    "checkver_xpath": "/pkg/version",
    "checkver_replace": "${version}",
    "checkver_reverse": True,
    "checkver_script": ["return 'app-9.9.9-x64.zip'"],
    "checkver_sourceforge": "example/app",
    "checkver_useragent": "Mozilla/5.0 (selftest)",
    "au_hash_url": "https://example.com/app-9.9.9.sha256",
    "au_hash_regex": "$sha256\\s+$basename",
    "url_au": "https://example.com/app-$version.zip",
}

# A drive-letter path pointing at a Scoop root -- the very thing the package must
# never contain, because the target is read from the environment at run time. The
# lookbehind keeps a URL scheme ("https://...") from counting as a drive letter.
HARDCODED_SCOOP_ROOT = re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/](?![\\/])[^\s]*[Ss]coop")


class Checker:
    def __init__(self, verbose: bool):
        self.verbose = verbose
        self.failures: list[str] = []
        self.warnings: list[str] = []

    def ok(self, title: str, detail: str = "") -> None:
        print(f"  ✓ {title}" + (f"  {detail}" if detail else ""))
        if self.verbose and detail:
            print(f"      {detail}")

    def fail(self, title: str, detail: str = "") -> None:
        self.failures.append(f"{title} {detail}".strip())
        print(f"  ✗ {title}" + (f"  {detail}" if detail else ""))

    def warn(self, title: str, detail: str = "") -> None:
        self.warnings.append(f"{title} {detail}".strip())
        print(f"  ! {title}" + (f"  {detail}" if detail else ""))

    def expect(self, condition: bool, title: str, detail: str = "") -> bool:
        if condition:
            self.ok(title, detail)
        else:
            self.fail(title, detail)
        return condition


def check_recipes(check: Checker) -> None:
    print("\n[1] recipe catalog <-> builders consistency")
    catalog = L.load_recipes()
    param_docs = catalog.get("param_docs", {})
    recipes = catalog["recipes"]
    check.expect(
        bool(recipes), "recipe catalog is not empty", f"{len(recipes)} recipes"
    )

    stray_json = sorted(
        path.relative_to(L.skill_root()).as_posix()
        for path in L.skill_root().rglob("*")
        if path.is_file() and path.suffix == ".json"
    )
    check.expect(
        not stray_json,
        "no .json file in the package (the CI manifest gate would validate it)",
        ", ".join(stray_json) if stray_json else L.CATALOG_NAME,
    )

    ids = [r["id"] for r in recipes]
    check.expect(len(ids) == len(set(ids)), "recipe ids are unique")
    check.expect(
        catalog.get("default_recipe") in ids,
        "default_recipe points at an existing recipe",
        str(catalog.get("default_recipe")),
    )
    check.expect(
        len(catalog.get("summary_sections", [])) > 0, "declares README sections"
    )

    builders_used: set[str] = set()
    structure_ok = True
    for recipe in recipes:
        for field in ("id", "label", "when", "builder", "required", "refs"):
            if field not in recipe:
                check.fail(f"recipe {recipe.get('id')} lacks field {field}")
                structure_ok = False
        builder = recipe.get("builder")
        builders_used.add(builder)
        if builder not in L.BUILDERS:
            check.fail(
                f"recipe {recipe['id']} has no implementation for builder '{builder}'"
            )
            structure_ok = False
        for key in recipe.get("required", []):
            if key not in param_docs:
                check.fail(
                    f"required parameter '{key}' of recipe {recipe['id']} is not documented in param_docs"
                )
                structure_ok = False
    if structure_ok:
        check.ok("every recipe is well-formed and every builder is implemented")

    unimplemented = sorted(set(L.BUILDERS) - builders_used)
    check.expect(
        not unimplemented, "no orphan builders", ", ".join(unimplemented) or "0"
    )


def check_paths(check: Checker) -> None:
    print("\n[2] bucket resolution ($env:Scoop, no hard-coded root)")
    root = L.skill_root()
    text_files = [
        root / "SKILL.md",
        root / "assets" / L.CATALOG_NAME,
        *sorted((root / "references").glob("*.md")),
        *sorted((root / "scripts").glob("*.py")),
    ]
    hard: list[str] = []
    for path in text_files:
        for match in HARDCODED_SCOOP_ROOT.finditer(path.read_text(encoding="utf-8")):
            hard.append(f"{path.name}: {match.group(0)}")
    check.expect(
        not hard,
        "no hard-coded Scoop root in the package ($env:Scoop is read at run time)",
        "; ".join(hard) if hard else f"{len(text_files)} files scanned",
    )

    with tempfile.TemporaryDirectory() as tmp:
        installed = Path(tmp) / L.BUCKETS_SUBDIR / L.BUCKET_NAME
        (installed / "bucket").mkdir(parents=True)
        (installed / "README.md").write_text("# stub\n", encoding="utf-8")
        saved = os.environ.get(L.SCOOP_ENV_VAR)
        os.environ[L.SCOOP_ENV_VAR] = tmp
        try:
            resolved = L.find_repo_root()
            check.expect(
                resolved == installed.resolve(),
                "$env:Scoop/buckets/extras-plus is the default target",
                str(resolved),
            )
            outside = root.parent.parent
            if L.is_bucket_root(outside):
                check.expect(
                    L.find_repo_root(outside) == outside.resolve(),
                    "--repo overrides the environment",
                    str(outside),
                )
            else:
                check.warn(
                    "--repo override not exercised: the package is not inside a bucket repo",
                    str(outside),
                )
            try:
                L.find_repo_root(Path(tmp))
                rejected = False
            except L.SmError:
                rejected = True
            check.expect(
                rejected, "--repo rejects a directory that is not a bucket root"
            )
        finally:
            if saved is None:
                os.environ.pop(L.SCOOP_ENV_VAR, None)
            else:
                os.environ[L.SCOOP_ENV_VAR] = saved


def check_render(check: Checker) -> None:
    print("\n[3] recipe rendering (offline, virtual parameters)")
    catalog = L.load_recipes()
    for recipe in catalog["recipes"]:
        spec = dict(DUMMY)
        spec["recipe"] = recipe["id"]
        try:
            manifest = L.build_manifest(spec)
        except L.SmError as exc:
            check.fail(
                f"{recipe['id']} failed to render", str(exc).replace("\n", " / ")
            )
            continue
        text = L.dumps_manifest(manifest)
        try:
            reparsed = json.loads(text, object_pairs_hook=OrderedDict)
        except json.JSONDecodeError as exc:
            check.fail(f"{recipe['id']} produced invalid JSON", str(exc))
            continue
        findings = L.lint_manifest_text(text, str(spec["name"]))
        errors = [f for f in findings if f.severity == "error"]
        if errors:
            check.fail(
                f"{recipe['id']} output failed self-check",
                "; ".join(f"{f.rule} {f.message}" for f in errors),
            )
            continue
        keys = list(reparsed.keys())
        if keys != L._sorted_by(keys, L.CANONICAL_ORDER):
            check.fail(
                f"{recipe['id']} top-level key order is not canonical", f"{keys}"
            )
            continue
        check.ok(f"{recipe['id']}", f"{len(keys)} top-level fields")


def check_repo(check: Checker, repo: Path) -> None:
    bucket = L.bucket_dir(repo)
    files = sorted(bucket.glob("*.json"))
    print(f"\n[4] repo round-trip consistency ({repo.name})")
    if not files:
        check.fail("no manifests under bucket/")
        return

    drift: list[str] = []
    for path in files:
        if (
            L.dumps_manifest(L.load_manifest(path), preserve_order=True).encode("utf-8")
            != path.read_bytes()
        ):
            drift.append(path.stem)
    if drift:
        check.warn(
            "formatting differs from the standard (update keeps the original order and will not touch them)",
            ", ".join(drift),
        )
    else:
        check.ok(f"{len(files)} manifests round-trip byte-identically")

    print("\n[5] README summary table round-trip")
    readme_path = repo / "README.md"
    if not readme_path.is_file():
        check.warn("no README.md at the repo root, skipping")
        return
    text = readme_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    tables = L.parse_summary(text)
    if not tables:
        check.fail("could not parse any summary table")
        return
    mismatched = []
    for table in tables:
        located = L._locate_summary_table(lines, table.section)
        if located is None:
            mismatched.append(f"{table.section} (not located)")
            continue
        start, _sep, end = located
        if lines[start:end] != L._render_table(table.header, table.rows, table.widths):
            mismatched.append(table.section)
    check.expect(
        not mismatched,
        f"{len(tables)} summary tables round-trip identically",
        "; ".join(mismatched)
        if mismatched
        else "the centering algorithm matches this repo exactly",
    )

    updated, _msg = L.insert_summary_row(
        text, tables[0].section, "__selftest__", "https://example.com"
    )
    check.expect(
        updated != text, "inserting a row changes the text (the write path works)"
    )
    _reverted, _msg2 = L.insert_summary_row(
        updated, tables[0].section, "__selftest__", "https://example.com"
    )
    check.expect(_reverted == updated, "inserting the same row twice is idempotent")


def check_lint_baseline(check: Checker, repo: Path) -> None:
    print("\n[6] full lint baseline")
    readme = (
        (repo / "README.md").read_text(encoding="utf-8")
        if (repo / "README.md").is_file()
        else None
    )
    files = sorted(L.bucket_dir(repo).glob("*.json"))
    errors = 0
    warnings = 0
    error_detail: list[str] = []
    for path in files:
        raw = path.read_bytes().decode("utf-8", "replace")
        findings = L.lint_manifest_text(raw, path.stem, readme_text=readme)
        for finding in findings:
            if finding.severity == "error":
                errors += 1
                error_detail.append(f"{path.stem}: {finding.rule} {finding.message}")
            else:
                warnings += 1
    print(
        f"      baseline: {len(files)} manifests, {errors} errors, {warnings} warnings"
    )
    if errors:
        for line in error_detail[:10]:
            print(f"        · {line}")
    check.expect(
        errors == 0,
        "the existing bucket has no error-level findings",
        f"{errors} errors" if errors else "",
    )


def check_docs(check: Checker) -> None:
    print("\n[7] docs <-> code consistency")
    refs = L.references_dir()
    catalog = L.load_recipes()
    recipe_ids = [r["id"] for r in catalog["recipes"]]

    # lint-rules.md ↔ RULES
    rules_doc = refs / "lint-rules.md"
    if not rules_doc.is_file():
        check.fail("references/lint-rules.md is missing")
    else:
        text = rules_doc.read_text(encoding="utf-8")
        documented: dict[str, tuple[str, str]] = {}
        for match in re.finditer(
            r"^\|\s*([EW]\d{3})\s*\|\s*(Error|Warning)\s*\|\s*(.+?)\s*\|\s*$",
            text,
            re.MULTILINE,
        ):
            documented[match.group(1)] = (match.group(2), match.group(3))
        code_ids = set(L.RULES)
        doc_ids = set(documented)
        check.expect(
            code_ids == doc_ids,
            "lint-rules.md covers every rule",
            f"missing {sorted(code_ids - doc_ids)}; extra {sorted(doc_ids - code_ids)}"
            if code_ids != doc_ids
            else f"{len(code_ids)} rules",
        )
        drift = []
        for rule, (severity, title) in L.RULES.items():
            if rule not in documented:
                continue
            doc_severity, doc_title = documented[rule]
            want = "Error" if severity == "error" else "Warning"
            if doc_severity != want or doc_title != title:
                drift.append(rule)
        check.expect(
            not drift,
            "rule severity and wording match the code",
            "; ".join(drift) if drift else "",
        )

    # recipes.md ↔ recipes.jsonc
    recipes_doc = refs / "recipes.md"
    if not recipes_doc.is_file():
        check.fail("references/recipes.md is missing")
    else:
        text = recipes_doc.read_text(encoding="utf-8")
        headings = re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
        doc_ids = [h for h in headings if h in recipe_ids]
        missing = [rid for rid in recipe_ids if rid not in doc_ids]
        extra = [h for h in headings if h not in recipe_ids and h != "Adding a recipe"]
        check.expect(
            not missing,
            "recipes.md covers every recipe",
            f"missing {missing}" if missing else f"{len(recipe_ids)} recipes",
        )
        check.expect(
            not extra,
            "recipes.md has no extra sections",
            ", ".join(extra) if extra else "",
        )

    # manifest-fields.md exists
    check.expect(
        (refs / "manifest-fields.md").is_file(), "references/manifest-fields.md exists"
    )

    # coverage.md documents where the recipes come from and what is still uncovered
    check.expect((refs / "coverage.md").is_file(), "references/coverage.md exists")

    # SKILL.md frontmatter matches the directory name
    skill_file = L.skill_root() / "SKILL.md"
    if not skill_file.is_file():
        check.fail("SKILL.md is missing")
        return
    text = skill_file.read_text(encoding="utf-8")
    match = re.search(r"^name:\s*(\S+)\s*$", text, re.MULTILINE)
    check.expect(
        match is not None and match.group(1) == L.skill_root().name,
        "SKILL.md name equals the skill directory name",
        f"name={match.group(1) if match else 'missing'}, dir={L.skill_root().name}",
    )
    missing_commands = [
        cmd for cmd in ("generate", "update", "lint") if cmd not in text
    ]
    check.expect(
        not missing_commands,
        "SKILL.md documents the three trigger commands",
        f"missing {missing_commands}" if missing_commands else "",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="sm_selftest.py", description="scoop-extras-plus skill self-check"
    )
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--repo", help="bucket repo root (default: $env:Scoop/buckets/extras-plus)"
    )
    args = parser.parse_args()

    check = Checker(args.verbose)
    print("scoop-extras-plus skill self-check")
    print(f"skill package: {L.skill_root()}")

    check_recipes(check)
    check_paths(check)
    check_render(check)

    try:
        repo = L.find_repo_root(Path(args.repo) if args.repo else None)
    except L.SmError as exc:
        check.warn("no bucket repo found, skipping repo-level checks", str(exc))
        repo = None
    if repo is not None:
        check_repo(check, repo)
        check_lint_baseline(check, repo)

    check_docs(check)

    print("\n" + "-" * 56)
    print(f"{len(check.failures)} failures, {len(check.warnings)} warnings")
    for line in check.failures:
        print(f"  failure: {line}")
    return 1 if check.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
