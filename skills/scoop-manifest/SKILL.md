---
name: scoop-manifest
version: 1.3.0
description: >
  Generate, update and lint Scoop bucket app manifests (bucket/*.json). Three
  trigger commands: generate builds a skeleton from one of 16 built-in recipes and
  fills in version, URL, hash, checkver, autoupdate and shortcuts, optionally
  syncing the README summary table; update edits fields by dotted path, bumps the
  version while rewriting hard-coded URLs, recomputes hashes and probes upstream
  for the latest release (batch sweep supported); lint runs 22 rules against this
  repo's CI and .editorconfig conventions and repairs formatting with
  --fix-format.
  Triggers: generate manifest, new manifest, update manifest, lint manifest,
  scoop manifest, bucket manifest, checkver, autoupdate, hash verification,
  version bump, Excavator, Scoop bucket maintenance, lint bucket.
display_name: "Scoop Manifest Forge"
visibility: "public"
agent_created: true
---

# Scoop Manifest Forge

Turn "upstream shipped something new" or "upstream shipped a new version" into a
single command. All three trigger commands -- **generate / update / lint** --
share the recipe catalog and the rule engine. Python standard library only, and
everything runs offline except `--checkver`, `--fetch-hash` and `--rehash`.

Package layout:

- `scripts/sm_lib.py` shared layer: paths, serialization, the 15 builders,
  checkver, rule engine, README table sync
- `scripts/scoop_manifest.py` the three-command CLI
- `scripts/sm_selftest.py` self-check: recipes <-> builders, docs <-> code,
  repo round-trip, lint baseline
- `references/manifest-fields.md` manifest field reference (this repo's rules)
- `references/recipes.md` when each of the 16 recipes applies, and what it emits
- `references/lint-rules.md` the 22 rules and how to fix each one
- `references/coverage.md` the upstream survey behind the catalog, and the gaps
- `assets/recipes.catalog` the single source of truth for recipes (JSON, but
  deliberately not named `.json` -- see "1. Hard constraints")

Scripts derive the package root themselves, so **they run from any cwd**:

```bash
python scripts/scoop_manifest.py <command> [options]
python scripts/sm_selftest.py
```

Managed interpreter on this machine:
`C:\Users\msain\.workbuddy\binaries\python\versions\3.13.12\python.exe`.

## 1. Hard constraints

- **Output**: `<repo>/bucket/<app>.json`, optionally plus a README summary row.
  Never write to `bin/`, `scripts/` or `.github/` -- those belong to Scoop's
  official scripts and to this repo's CI.
- **Preserve existing order**: `update` only slots **new** fields into their
  canonical position; existing fields keep their place. A full reorder needs an
  explicit `--reorder`.
- **Self-check before writing**: the result goes through the rule engine first,
  and error-level findings block the write (`--force` overrides).
- **Never add a `.json` file to this package.** The bucket CI runs Scoop's
  manifest gate over every `.json` file a commit changes, anywhere in the tree
  (its `-Path` argument locates the repository, it does not filter by
  sub-directory), and validates each one against `schema.json`. The recipe
  catalog is data, not a manifest, so it ships as `assets/recipes.catalog`.
- **README is controlled**: the header must be exactly the three columns
  `App / Auto-Update ? / Note`, and a missing section skips the sync with an
  explanation. Centering already matches this repo's 5 tables byte for byte, so
  inserting a row never disturbs the others.

## 2. The three trigger commands

| Command | Alias | Job | Main options |
| :--- | :--- | :--- | :--- |
| **generate** | `gen` | Build a manifest from a recipe and fill it in, optionally sync README | `--list-recipes`, `--from`, `--recipe`, `--fetch-hash`, `--hash-from-file`, `--section`, `--dry-run` |
| **update** | `upd` | Edit fields / bump version + rewrite URLs / recompute hashes / probe upstream | `--name`, `--all`, `--set`, `--unset`, `--version`, `--rehash`, `--checkver [--apply]` |
| **lint** | `check` | Run the 22 rules, repair formatting | `--name`, `--json`, `--strict`, `--fix-format`, `--rules` |

Shared option `--repo <bucket repo root>`: without it the script walks up from
the cwd looking for a directory holding both `bucket/` and `README.md`.

## 3. generate

**Settle five things first** and ask the user for anything missing; do not guess:

1. Who is upstream: a GitHub repo, or a website / own CDN?
2. What ships: portable archive / NSIS installer / InnoSetup / bare exe / plugin?
3. Version number (without the leading `v`)
4. Where the entry point is: the exe a shortcut should point at (relative to
   `$dir`, backslashes) and any command-line alias
5. README section: `AI Specific` / `General Use` / `Academic Tools` /
   `Development Tools` / `Win-Only`

Unsure about the recipe? Run `--list-recipes` first; it prints when each recipe
applies, the required and optional parameters, and same-kind samples (from this
repo where a manifest of that shape exists, from the upstream bucket otherwise).
Then compare against `references/recipes.md`.

```bash
python scripts/scoop_manifest.py gen --name myapp --recipe github-nsis-7z \
  --version 3.4.5 --desc "Super app for testing the generator" \
  --homepage https://github.com/o/r --license MIT \
  --url64 "https://github.com/o/r/releases/download/v3.4.5/app.exe#/dl.7z" \
  --repo-url https://github.com/o/r \
  --shortcut-exe app.exe --shortcut-name "MyApp" \
  --section "General Use" --dry-run

python scripts/scoop_manifest.py gen --from specs.json --section "General Use"
```

`--from` reads a spec file, which suits batches: an object or an array of
objects whose keys are the `param_docs` names from `recipes.catalog`, plus
`name`, `recipe` and `section`. Command-line options win over the file.

**Pick one of three ways to obtain the hash, never invent it**: `--fetch-hash`
streams the download and computes it; `--hash-from-file <path>` uses a package
already on disk; if neither is given, run `bin/checkhashes.ps1` afterwards (the
command prints that hint).

**Rhythm**: `--dry-run` to preview, then drop it to write and sync the README,
then `lint --name <app>` to confirm.

## 4. update

`--set` takes a dotted path and parses the value as JSON, falling back to a
string. New fields land in their canonical key position (`persist` goes between
`extract_to` and `env_set`, not at the end of the file); `--unset` deletes.

```bash
python scripts/scoop_manifest.py upd --name myapp \
  --set 'description=Portable note taking app' --set 'persist=data' \
  --set 'shortcuts.0.1=MyApp Pro'

python scripts/scoop_manifest.py upd --name myapp --checkver   # report
python scripts/scoop_manifest.py upd --name myapp --checkver --apply --rehash
python scripts/scoop_manifest.py upd --name myapp --version 3.5.0  # manual
python scripts/scoop_manifest.py upd --all --checkver --apply --rehash  # sweep
```

`--version` rewrites the old version hard-coded in every download URL.

`--checkver` understands the `github` string, `{"github": ...}`, bare-string
regex (scraped from `homepage`), `{"url", "regex"}`, `{"url", "jsonpath",
"regex", "replace"}`, `{"url", "xpath", ...}` and `{"sourceforge": ...}`.
**The `{"script": ...}` form needs a Scoop environment and explicitly reports that
it cannot probe offline**; use `bin/checkver.ps1` instead.

Safety net: the rule engine runs after every change and error-level findings
**block the write** (`--force` overrides); `--dry-run` previews and
`--print-json` dumps the result. `upd` leaves the README alone unless `--readme`
is passed, which syncs it and keeps the existing note column (for example
`by @CronusLM`).

## 5. lint

```bash
python scripts/scoop_manifest.py lint                  # full run, about 1 second
python scripts/scoop_manifest.py lint --name aionui    # a single app
python scripts/scoop_manifest.py lint --json           # machine-readable report
python scripts/scoop_manifest.py lint --strict         # warnings fail too
python scripts/scoop_manifest.py lint --fix-format     # formatting only
python scripts/scoop_manifest.py lint --rules          # print the rule catalog
```

`--fix-format` touches formatting only (indent / CRLF / trailing newline) and
never JSON semantics.

Exit code: error-level findings give 1; warnings alone give 0, or 1 with
`--strict`. Rules and their fixes live in `references/lint-rules.md`.

**Baseline (56 manifests)**: 0 errors, 27 warnings, 35 fully clean. Real issues
found so far:

| manifest | Issue | Rule |
| :--- | :--- | :--- |
| `cumora` | `version` says 0.18.4 but the URL and autoupdate both pin `v0.1.64` with no `$version`, so it installs an old build forever | W104 + W110 |
| `voov-meeting` | `hash` written as `md5:03fd...`, a prefix Scoop does not accept | E011 |
| 7 manifests | `architecture` exists but `autoupdate` has only a flat url, so Excavator never refreshes the per-architecture URLs | W103 |
| `isobuster` | the only file in the repo using LF endings | W109 |
| `aionui` / `ecopaste` | the README summary table spells them `aionaui` / `ecopast` | W105 |
| `affinity` | `description` ends with a period (Scoop wants a phrase) | W101 |

## 6. Boundaries

Not for: installers that need interaction, MSI customisation, or packages with
private unpacking logic beyond `$PLUGINSDIR` (hand-writing is easier); archives
over 2GB (aria2 and hash verification degrade); **32bit architecture** — `arch`
takes `64bit` and `arm64` only, so `url32` / `hash32` are neither accepted nor
emitted; and any change under `bin/`, `scripts/` or `.github/`.

## 7. Maintenance

```bash
python scripts/sm_selftest.py            # full self-check (offline)
python scripts/sm_selftest.py --verbose  # print every detail
```

The self-check has 6 groups: recipe catalog shape -> recipe <-> builder coverage
both ways -> virtual rendering of all 16 recipes -> repo serialization round-trip
-> README table round-trip and row-insert idempotence -> docs <-> code
consistency (`lint-rules.md` matches `RULES` word for word, `recipes.md` maps
one-to-one onto `recipes.catalog`, and `SKILL.md`'s `name` equals the directory
name).

**Adding a recipe** (4 steps, and the self-check catches omissions): add an entry
to the `recipes` array in `recipes.catalog` (`id` / `label` / `when` /
`builder` / `required` / `refs`) and document any new parameters in `param_docs`
-> register
a builder of the same name in `BUILDERS` in `sm_lib.py` -> add a `## <recipe id>`
section to `recipes.md` -> run `sm_selftest.py`.

**Adding a rule**: change `RULES` in `sm_lib.py` and the table in
`lint-rules.md` together, keeping the wording identical.

**Editing docs**: all four markdown files pass `rumdl check` at its default
(width <= 80 columns); finish with `rumdl fmt`.
