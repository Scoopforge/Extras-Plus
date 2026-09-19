# Scoop manifest field reference (this repo's conventions)

This document describes the fields the Extras-Plus repo (`bucket/*.json`)
actually uses. It is derived from statistics over the 56 manifests here plus
the existing CI config; nothing is invented about Scoop internals.
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

| Field                              | Type               | Notes                                                                                                                          | Sample in this repo                                 |
| :--------------------------------- | :----------------- | :----------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------- |
| `url`                              | string or string[] | Single-architecture direct download URL. A top-level `url` together with `architecture` is redundant (W108)                    | `veracrypt` uses a top-level `url`                  |
| `hash`                             | string or string[] | sha256 of the download. **Must be 64 lowercase hex chars**; when `url` is an array, `hash` must be an array of the same length | `normcap` and `buzz` use the array form             |
| `architecture`                     | object             | `{"64bit": {...}, "arm64": {...}}`; `64bit` is mandatory                                                                       | 40/56 use it; `claude-desktop` covers 64bit + arm64 |
| `extract_dir`                      | string             | Inner directory name the archive is extracted into                                                                             | `cytoscape`, `comfyui`                              |
| `extract_to`                       | string             | Subdirectory under `$dir` to extract into, usually the same value as `extract_dir`                                             | `bananas`, `aionui`                                 |
| `innosetup`                        | bool               | Declares an InnoSetup payload so Scoop unpacks it natively, **instead of** a hand-written `installer.script`                   | `scihubeva`, `winhance`, `pastemd`                  |
| `installer`                        | object             | `{"script": ...}`, a custom install script (string or string array)                                                            | `vibe`, `texlive`, `cap`                            |
| `uninstaller`                      | object             | `{"script": ...}`, a custom uninstall script                                                                                   | `comfyui-manager`, `linkandroid`                    |
| `pre_install` / `post_install`     | string or string[] | Hooks before and after install                                                                                                 | `veracrypt`, `mogan`                                |
| `pre_uninstall` / `post_uninstall` | string or string[] | Hooks before and after uninstall                                                                                               | `mogan`, `affinity`                                 |

### 2.3 Integration fields

| Field          | Type                       | Notes                                                                                                          | Sample in this repo                            |
| :------------- | :------------------------- | :------------------------------------------------------------------------------------------------------------- | :--------------------------------------------- |
| `bin`          | string or `[exe, alias][]` | Executables to put on PATH                                                                                     | `isobuster` uses a string; `aionui` uses pairs |
| `shortcuts`    | `[exe, name][]`            | Start-menu shortcuts. A third and fourth item (arguments, icon) are allowed; **the first two must be strings** | `dbgate` passes `--user-data-dir`              |
| `persist`      | string or string[]         | Directories / files kept across versions                                                                       | `mogan`, `veracrypt`                           |
| `env_set`      | object                     | Environment variables written on install                                                                       | `TEXMACS_HOME_PATH` in `mogan`                 |
| `env_add_path` | string or string[]         | Directories appended to PATH                                                                                   | `bin\windows` in `texlive`                     |
| `suggest`      | object or string           | Packages suggested alongside                                                                                   | `cytoscape`, `stirlingpdf`                     |
| `depends`      | string or string[]         | Hard dependency                                                                                                | `scoopforge/comfyui` in `comfyui-manager`      |
| `notes`        | string                     | Message printed after install                                                                                  | `dingtalk-en`, `ecopaste`                      |

### 2.4 The `#/` fragment in URLs

The trailing `#/name` in a URL decides the file name on disk and
**therefore which way Scoop processes the download**:

| Form                                 | Effect                                              | Sample in this repo              |
| :----------------------------------- | :-------------------------------------------------- | :------------------------------- |
| `...exe#/dl.7z`                      | unpack the exe as a 7z archive                      | `dingtalk-en`, `mogan`, `aionui` |
| `...exe#/dl.zip`                     | unpack as a zip                                     | `claude-desktop`                 |
| `...exe#/setup.exe`                  | keep it as an exe and hand it to `installer.script` | `veracrypt`                      |
| `...?d=x&v=1#/isobuster_install.exe` | query string and fragment together                  | `isobuster`                      |

## 3. The four checkver forms

| Form          | Structure                                                     | Use when                                               | Sample in this repo                |
| :------------ | :------------------------------------------------------------ | :----------------------------------------------------- | :--------------------------------- |
| string        | `"checkver": "github"`                                        | the GitHub repo can be derived from `url` / `homepage` | `scihubeva`, `alexandria`          |
| github object | `{"github": "https://github.com/o/r"}`                        | the homepage is not GitHub but releases are            | `bananas`, `mogan`                 |
| url + regex   | `{"url": ..., "regex": ...}`                                  | upstream is a website / own CDN (20 of them)           | `veracrypt`, `bitcomet`, `texlive` |
| jsonpath      | `{"url": ..., "jsonpath": ..., "regex": ..., "replace": ...}` | only an API or rolling builds are offered              | `comfyui-manager`, `filecentipede` |
| script        | `{"script": [...], "regex": ...}`                             | a PowerShell request is needed to get the value        | `dingtalk-en` (the only one)       |

Key points:

- The **`github` form needs no `regex`**; `url` and `script` must have one.
- Prefer a `(?<version>...)` named group; without one Scoop takes the first group.
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

Field order produced by `gen`:

```text
version → description → homepage → license → notes → architecture → url → hash
→ pre_install → installer → innosetup → extract_dir → extract_to → post_install
→ bin → shortcuts → persist → env_set → env_add_path → suggest → depends
→ uninstaller → pre_uninstall → post_uninstall → checkver → autoupdate
```

`update` **does not rewrite the whole file** (avoiding huge diffs): existing
fields keep their position and only new fields are inserted in the order
above. Pass `--reorder` to rewrite everything.

## 6. When not to use this skill

- PowerShell build outputs, MSI customisation, or private unpacking logic
  beyond `$PLUGINSDIR` -- writing the manifest by hand is easier.
- Upstream ships an installer that needs interaction and cannot run silently.
- Archives over 2GB (Scoop's `aria2` and hash verification degrade).

## 7. Related files

- Recipe reference: `references/recipes.md`
- Lint rules: `references/lint-rules.md`
- Recipe data (single source of truth): `assets/recipes.json`
