# Scoop manifest field reference (this repo's conventions)

This document describes the fields the Extras-Plus repo (`bucket/*.json`)
actually uses. It is derived from statistics over the 56 manifests here, the
2,389-manifest survey in `references/coverage.md`, and the existing CI config;
nothing is invented about Scoop internals.
[Scoop Wiki · App Manifests](https://github.com/ScoopInstaller/Scoop/wiki/App-Manifests)
as authoritative.

## 1. File-level conventions

| Item          | Convention                                              | Basis                                                                    |
| :------------ | :------------------------------------------------------ | :----------------------------------------------------------------------- |
| File name     | `<app>.json` where `app` matches `^[a-z0-9][a-z0-9-]*$` | 56/56 comply                                                             |
| Encoding      | UTF-8 without BOM                                       | `.editorconfig`'s `charset = utf-8`                                      |
| Indent        | 4 spaces                                                | `.editorconfig`                                                          |
| Line endings  | CRLF                                                    | `.editorconfig`'s `end_of_line = crlf` plus `.gitattributes`' `eol=crlf` |
| Trailing byte | exactly one newline required                            | `.editorconfig`'s `insert_final_newline = true`                          |
| Non-ASCII     | written literally, never \uXXXX-escaped                 | all 56 manifests are plain ASCII today                                   |

Status: of the 56 files only `isobuster.json` uses LF endings, the single
formatting deviation (`lint` reports W109; `lint --fix-format` repairs it).

## 2. Top-level fields

### 2.1 Required fields (CI fails when missing)

| Field         | Type             | Notes                                                                                                 | Sample in this repo                                              |
| :------------ | :--------------- | :---------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------- |
| `version`     | string           | Upstream version, **without the leading `v`**. A github `checkver` strips the tag's `v` automatically | all 56                                                           |
| `description` | string           | One-line English description. Capitalized, **no trailing period**, length <= 120                      | 55/56 comply (`affinity` ends with a period)                     |
| `homepage`    | string           | Upstream homepage or repository URL                                                                   | all 56                                                           |
| `license`     | string or object | Prefer an SPDX identifier; use `{"identifier": ..., "url": ...}` when unsure                          | `veracrypt` uses `"Apache-2.0"`; `bitcomet` uses the object form |
| `checkver`    | string or object | How the version is detected, see section 3                                                            | all 56                                                           |
| `autoupdate`  | object           | How URLs change on a version bump, see section 4                                                      | all 56                                                           |

### 2.2 Download and install fields

| Field                              | Type               | Notes                                                                                                                                | Sample in this repo                                 |
| :--------------------------------- | :----------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------- |
| `url`                              | string or string[] | Single-architecture direct download URL. A top-level `url` together with `architecture` is redundant (W108)                          | `veracrypt` uses a top-level `url`                  |
| `hash`                             | string or string[] | sha256 of the download. **Must be 64 lowercase hex chars**; when `url` is an array, `hash` must be an array of the same length       | `normcap` and `buzz` use the array form             |
| `architecture`                     | object             | `{"64bit": {...}, "arm64": {...}}`; `64bit` is mandatory                                                                             | 40/56 use it; `claude-desktop` covers 64bit + arm64 |
| `extract_dir`                      | string             | Inner directory name the archive is extracted into                                                                                   | `cytoscape`, `comfyui`                              |
| `extract_to`                       | string             | Subdirectory under `$dir` to extract into, usually the same value as `extract_dir`                                                   | `bananas`, `aionui`                                 |
| `innosetup`                        | bool               | Declares an InnoSetup payload so Scoop unpacks it natively, **instead of** a hand-written `installer.script`                         | `scihubeva`, `winhance`, `pastemd`                  |
| `installer`                        | object             | `{"script": ...}` for a custom install script (string or string array), or `{"file": ..., "args": [...]}` to run a bundled setup exe | `vibe`, `texlive`, `cap`                            |
| `uninstaller`                      | object             | `{"script": ...}`, a custom uninstall script                                                                                         | `comfyui-manager`, `linkandroid`                    |
| `pre_install` / `post_install`     | string or string[] | Hooks before and after install                                                                                                       | `veracrypt`, `mogan`                                |
| `pre_uninstall` / `post_uninstall` | string or string[] | Hooks before and after uninstall                                                                                                     | `mogan`, `affinity`                                 |

### 2.3 Integration fields

| Field          | Type                       | Notes                                                                                                          | Sample in this repo                            |
| :------------- | :------------------------- | :------------------------------------------------------------------------------------------------------------- | :--------------------------------------------- |
| `bin`          | string or `[exe, alias][]` | Executables to put on PATH                                                                                     | `isobuster` uses a string; `aionui` uses pairs |
| `shortcuts`    | `[exe, name][]`            | Start-menu shortcuts. A third and fourth item (arguments, icon) are allowed; **the first two must be strings** | `dbgate` passes `--user-data-dir`              |
| `persist`      | string or string[]         | Directories / files kept across versions                                                                       | `mogan`, `veracrypt`                           |
| `env_set`      | object                     | Environment variables written on install                                                                       | `TEXMACS_HOME_PATH` in `mogan`                 |
| `env_add_path` | string or string[]         | Directories appended to PATH                                                                                   | `bin\windows` in `texlive`                     |
| `psmodule`     | object                     | `{"name": ..., "path": ...}` for a PowerShell module package instead of `bin` / `shortcuts`                    | none here; `completionpredictor` upstream      |
| `suggest`      | object or string           | Packages suggested alongside                                                                                   | `cytoscape`, `stirlingpdf`                     |
| `depends`      | string or string[]         | Hard dependency                                                                                                | `scoopforge/comfyui` in `comfyui-manager`      |
| `notes`        | string                     | Message printed after install                                                                                  | `dingtalk-en`, `ecopaste`                      |
| `##`           | string                     | **The documented way to leave a comment inside a manifest.** Scoop ignores it; use it instead of `_comment`    | none here; 54 upstream manifests               |

### 2.4 The `#/` fragment in URLs

The trailing `#/name` in a URL decides the file name on disk and
**therefore which way Scoop processes the download**:

| Form                                 | Effect                                                                                                              | Sample in this repo              |
| :----------------------------------- | :------------------------------------------------------------------------------------------------------------------ | :------------------------------- |
| `...exe#/dl.7z`                      | unpack the exe as a 7z archive                                                                                      | `dingtalk-en`, `mogan`, `aionui` |
| `...exe#/dl.zip`                     | unpack as a zip                                                                                                     | `claude-desktop`                 |
| `...exe#/setup.exe`                  | keep it as an exe and hand it to `installer.script`                                                                 | `veracrypt`                      |
| `...msi#/setup.msi_`                 | keep the MSI as a file; **the trailing `_` hides the extension, so Scoop does not pick `Expand-MsiArchive` for it** | `affinity`, `normcap`            |
| `...?d=x&v=1#/isobuster_install.exe` | query string and fragment together                                                                                  | `isobuster`                      |

`lib/decompress.ps1` chooses the extraction function from the **on-disk file
name**, matching `\.zip$`, `\.msi$` and (`innosetup` only) `\.exe$`, then falling
back to "is this 7z-readable". A name ending in `_` matches none of those, which
is the whole point of the convention: without the underscore an `.msi` download
is silently unpacked with `Expand-MsiArchive` instead of reaching your
`installer.script`.

## 3. checkver forms

| Form          | Structure                                            | Use when                                                      | Sample in this repo                |
| :------------ | :--------------------------------------------------- | :------------------------------------------------------------ | :--------------------------------- |
| string        | `"checkver": "github"`                               | the GitHub repo can be derived from `url` / `homepage`        | `scihubeva`, `alexandria`          |
| github object | `{"github": "https://github.com/o/r"}`               | the homepage is not GitHub but releases are                   | `bananas`, `mogan`                 |
| bare regex    | `"checkver": "Version ([\\d.]+)"`                    | the homepage itself lists the version and a regex can read it | none here; 147 upstream manifests  |
| url + regex   | `{"url": ..., "regex": ...}`, optionally `+ replace` | upstream is a website / own CDN                               | `veracrypt`, `bitcomet`, `texlive` |
| jsonpath      | `{"url": ..., "jsonpath": ..., "regex": ...}`        | only an API or rolling builds are offered                     | `comfyui-manager`, `filecentipede` |
| xpath         | `{"url": ..., "xpath": ..., "regex": ...}`           | the version lives in an XML / RSS document                    | none here; 15 upstream manifests   |
| sourceforge   | `{"sourceforge": "project/path", "regex": ...}`      | upstream is a SourceForge project                             | none here; 15 upstream manifests   |
| script        | `{"script": [...], "regex": ...}`                    | a PowerShell request is needed to get the value               | `dingtalk-en` (the only one)       |

Key points:

- The **`github` and `sourceforge` forms need no `regex`**; `url`, `script`,
  `xpath` and `jsonpath` must have one.
- **`checkver` with no `url` scrapes `homepage`** — `bin/checkver.ps1` sets
  `$url = $json.homepage` under its "Not Specified" branch. A regex on its own
  is the shorthand for exactly that.
- `reverse`, `replace` and `useragent` need the **object** form; a bare string
  cannot carry them.
- A `checkver.github` value must be a repository URL, **never an
  `api.github.com` one**: Scoop appends `/releases/latest` unconditionally, so
  the API path turns into a 404 (W111). Put the API endpoint in `checkver.url`.
- Prefer a `(?<version>...)` named group; without one Scoop takes the first group.
- `jsonpath` may also be spelled `jp`; both are read.
- A leading `v` in the upstream tag needs no handling; Scoop strips it.
- The `script` form needs a Scoop environment, so this skill's `update --checkver`
  cannot probe it offline and says so explicitly.

## 4. Writing autoupdate

`autoupdate` describes what the URL looks like once the version is `$version`.

| Case                      | Form                                                                            | Sample in this repo    |
| :------------------------ | :------------------------------------------------------------------------------ | :--------------------- |
| top-level `url`           | `{"url": ".../v$version/app-$version.zip"}`                                     | `veracrypt`            |
| `architecture`            | `{"architecture": {"64bit": {"url": ...}, "arm64": {"url": ...}}}`              | `aionui`, `tylina`     |
| hash from a checksum file | `{"url": ..., "hash": {"url": "$url.sha256", "regex": "$sha256\\s+$basename"}}` | `veracrypt`, `texlive` |
| hash from a web page      | `{"url": ..., "hash": {"url": ..., "regex": ...}}`                              | `bitcomet`             |

**Two hard constraints (`lint` checks both)**:

1. If a manifest uses `architecture`, `autoupdate` must also supply
   per-architecture URLs (W103); otherwise Excavator will not update them on
   a bump. Seven violate this today:
   `bitcomet`, `comfyui-manager`, `defender-remover`, `hermes-one`, `mineru`,
   `open-design`, `zlibrary`.
2. If the current download URL carries a version, the `autoupdate` URL must
   carry `$version` (W110); otherwise the version rises while the URL stays put
   and the package goes stale forever. `cumora` is exactly that case (URL
   pinned to `v0.1.64` while `version` says 0.18.4).

## 5. Canonical key order

Field order produced by `gen` (`CANONICAL_ORDER` in `sm_lib.py`):

```text
## → version → description → homepage → license → notes → architecture → url
→ hash → pre_install → installer → innosetup → extract_dir → extract_to
→ post_install → psmodule → bin → shortcuts → persist → env_set → env_add_path
→ suggest → depends → uninstaller → pre_uninstall → post_uninstall
→ checkver → autoupdate
```

Nested levels have their own order:

| Parent                      | Order                                                                                                                                          |
| :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| `architecture`              | `64bit` → `arm64`                                                                                                                              |
| `architecture.<arch>`       | `url`, `hash`, `pre_install`, `installer`, `innosetup`, `extract_dir`, `extract_to`, `post_install`, `psmodule`, `bin`, `shortcuts`, `persist` |
| `checkver`                  | `github`, `url`, `sourceforge`, `script`, `jsonpath`, `xpath`, `regex`, `replace`, `reverse`, `useragent`                                      |
| `autoupdate`                | `architecture`, `url`, `hash`, `extract_dir`, `bin`, `shortcuts`                                                                               |
| `installer` / `uninstaller` | `script`, `args`                                                                                                                               |
| `hash`                      | `url`, `regex`, `jsonpath`                                                                                                                     |

Only `64bit` and `arm64` are recognised. `arch` takes one of them, or the two
joined with `+`; anything else is rejected with the list of valid values.
**32bit is out of scope by decision**, so `url32` / `hash32` are neither
accepted nor generated, and `32bit` is not a valid `arch` value.

`update` **does not rewrite the whole file** (avoiding huge diffs): existing
fields keep their position and only new fields are inserted in the order
above. Pass `--reorder` to rewrite everything.

## 6. When not to use this skill

- PowerShell build outputs, MSI customisation, or private unpacking logic
  beyond `$PLUGINSDIR` -- writing the manifest by hand is easier.
- Upstream ships an installer that needs interaction and cannot run silently.
- Archives over 2GB (Scoop's `aria2` and hash verification degrade).

## 7. Related files

- Which recipe applies, and what it emits: `references/recipes.md`
- Where the recipes came from, and what is not covered: `references/coverage.md`
- Lint rules: `references/lint-rules.md`
- Recipe data (single source of truth): `assets/recipes.jsonc`
