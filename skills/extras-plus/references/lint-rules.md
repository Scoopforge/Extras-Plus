# Lint rule catalog

`RULES` in `scripts/sm_lib.py` is the source of truth. This document is the
readable version, kept in sync by `scripts/sm_selftest.py` -- change both.

Rules follow this repo's CI: `.github/workflows/ci.yml` (Pester +
Import-Bucket-Tests), `.github/workflows/schedule.yml` (Excavator every
12 hours), `.editorconfig`, and the 56 existing manifests' own baseline.
`references/coverage.md` records which upstream pattern each rule came from.

## Errors (E)

Error-level findings break `scoop install` or fail CI, making `lint` exit 1.

| Rule | Severity | Description                                                                                            |
| :--- | :------- | :----------------------------------------------------------------------------------------------------- |
| E001 | Error    | manifest is not valid JSON / top level is not an object                                                |
| E002 | Error    | file is not UTF-8, or contains a BOM                                                                   |
| E003 | Error    | missing required field (version/description/homepage/license/checkver/autoupdate)                      |
| E004 | Error    | version is missing or not a string                                                                     |
| E005 | Error    | checkver structure is invalid                                                                          |
| E006 | Error    | autoupdate has neither a top-level url nor architecture.url                                            |
| E007 | Error    | architecture exists but has no 64bit entry                                                             |
| E008 | Error    | shortcut entry does not start with [exe, name]                                                         |
| E009 | Error    | file name does not match ^[a-z0-9][a-z0-9-]*$                                                          |
| E010 | Error    | script matches a dangerous pattern (Invoke-Expression / -EncodedCommand / plaintext credentials, etc.) |
| E011 | Error    | hash is not a 64-char lowercase sha256 and no autoupdate hash source is given                          |

## Warnings (W)

Warnings do not affect installation but they slow down maintenance. With
`--strict` they also make `lint` exit 1.

| Rule | Severity | Description                                                                     |
| :--- | :------- | :------------------------------------------------------------------------------ |
| W101 | Warning  | description ends with a period / exceeds 120 chars / starts lowercase           |
| W102 | Warning  | download URL uses plaintext http://                                             |
| W103 | Warning  | architecture exists but autoupdate does not cover per-architecture URLs         |
| W104 | Warning  | version hard-coded in the URL does not match the version field                  |
| W105 | Warning  | app is missing from the README summary table / listed more than once            |
| W106 | Warning  | license is neither an SPDX identifier nor an {identifier,url} object            |
| W107 | Warning  | version contains non-numeric characters, autoupdate may misbehave               |
| W108 | Warning  | top-level url and architecture coexist; redundant field                         |
| W109 | Warning  | formatting does not match .editorconfig (indentation / CRLF / trailing newline) |
| W110 | Warning  | autoupdate URL has no $version, so the download URL stays stale after a bump    |
| W111 | Warning  | checkver.github points at api.github.com, which Scoop turns into a 404          |

## How to fix each rule

### E group

- **E001 / E002**: run `python -c "import json;json.load(open('x.json'))"`
  to see the failing line and column. A BOM needs a re-save; no auto-fix exists.
- **E003 / E004**: add what is missing. `version` must be a string (`"1.2"`).
- **E005**: `github` and `sourceforge` need no `regex`; `url` and `script` must
  have one, and a misspelled key name is reported here too. A bare string is
  the shorthand for "scrape the homepage": Scoop falls back to `homepage` when
  `checkver.url` is absent, so it is only an error when there is no `homepage`
  to scrape.
- **E006**: `autoupdate` needs a top-level `url` or an `architecture.<a>.url`.
- **E007**: `architecture` must contain a `64bit` branch.
- **E008**: each `shortcuts` entry is at least `["exe", "display name"]`; the
  first two items must be strings. Later items (arguments, icon) may follow.
- **E009**: lowercase letters, digits and hyphens only, starting alphanumeric.
- **E010**: the script contains `Invoke-Expression` / `iex` /
  `-EncodedCommand` / a pipe into `powershell` / a plaintext credential /
  `Set-ExecutionPolicy Unrestricted` / a recursive delete of `C:\`. Such
  patterns are a supply-chain risk in an auto-updating flow; review by hand.
- **E011**: `hash` must be 64 lowercase hex chars or an equally long array.
  Scoop rejects an `"md5:..."` prefix; `voov-meeting` currently has one.
  If Excavator should fill it, declare a `hash` source in `autoupdate`.

### W group

- **W101**: Scoop treats `description` as a phrase, not a sentence.
  `affinity` ends with a period.
- **W102**: only `http://` is reported; the `mirror.ctan.org` texlive
  mirror is allow-listed.
- **W103**: `architecture` and `autoupdate.architecture` must come in pairs,
  otherwise Excavator bumps the version but not the per-arch URLs. 7 hit it.
- **W104**: the version in the download URL disagrees with `version`, so the
  release process was hand-edited. `cumora` hits this.
- **W105**: the app is missing from, or duplicated in, the README summary
  table; near-miss names get a hint: `aionaui` for `aionui`, `ecopast`
  for `ecopaste`.
- **W106**: prefer an SPDX identifier for `license` (`MIT`, `Apache-2.0`,
  `GPL-3.0-or-later`); when unsure use `{"identifier": ..., "url": ...}`.
  Extra words such as `MIT license` are flagged.
- **W107**: when `version` has non-numeric chars (`release13`, `4.6.2-1`),
  Excavator's version comparison may misbehave; confirm by hand.
- **W108**: a top-level `url` plus `architecture` is redundant and easy to
  update inconsistently.
- **W109**: disagrees with `.editorconfig`; `--fix-format` repairs it
  (formatting only). Today only `isobuster` uses LF endings.
- **W110**: the download URL has a version but the `autoupdate` URL has no
  `$version`, so the URL never follows a bump. `cumora` hits this.
- **W111**: `Scoop` appends `/releases/latest` to whatever `checkver.github`
  holds. Pointing it at `https://api.github.com/repos/o/r/releases/latest`
  therefore requests `.../releases/latest/releases/latest` and gets a 404, so
  the version is never detected and Excavator silently skips the app. Move the
  API endpoint into `checkver.url` instead. 140 manifests in the upstream
  `ScoopInstaller/Extras` bucket are written this way; `86box` and
  `adventuregamestudio` are two of them.

## Known exceptions (do not "fix" these)

| Symptom                                          | Why it is fine                                          | Sample                                                        |
| :----------------------------------------------- | :------------------------------------------------------ | :------------------------------------------------------------ |
| `autoupdate` uses a fixed URL with no `$version` | upstream serves a permanent link                        | `install-tl.zip` in `texlive`, `redirect` in `claude-desktop` |
| no `hash` at all                                 | the URL content changes, so a pinned hash fails at once | `claude-desktop`                                              |
| plaintext `http://`                              | the official mirror has no https                        | `texlive`                                                     |
| `version` contains letters                       | upstream archives are named `releaseNN`                 | `defender-remover`                                            |

## Usage

```bash
python scripts/scoop_manifest.py lint                  # full run
python scripts/scoop_manifest.py lint --name aionui    # a single app
python scripts/scoop_manifest.py lint --json           # machine-readable report
python scripts/scoop_manifest.py lint --strict         # warnings fail too
python scripts/scoop_manifest.py lint --fix-format     # formatting only
python scripts/scoop_manifest.py lint --rules          # print the rule catalog
```
