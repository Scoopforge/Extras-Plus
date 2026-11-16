# 🍨 Extras-Plus 🍨

[![Excavator](https://github.com/Scoopforge/Extras-Plus/actions/workflows/ci.yml/badge.svg)](https://github.com/Scoopforge/Extras-Plus/actions/workflows/ci.yml)
[![license](https://img.shields.io/github/license/Scoopforge/Extras-Plus)](https://github.com/Scoopforge/Extras-Plus/blob/master/LICENSE)
[![code size](https://img.shields.io/github/languages/code-size/Scoopforge/Extras-Plus.svg)](https://img.shields.io/github/languages/code-size/Scoopforge/Extras-Plus.svg)
[![repo size](https://img.shields.io/github/repo-size/Scoopforge/Extras-Plus.svg)](https://img.shields.io/github/repo-size/Scoopforge/Extras-Plus.svg)

A Bucket for the Best Windows Package Manager [Scoop](https://github.com/ScoopInstaller/Scoop): An Enhancement for the Official CLI Bucket.

> If you would like to be a co-maintainer, feel free to tell me in the Discussion.

For ones familiar with Scoop:

## 🏃 To Start

```powershell
scoop bucket add extras-plus https://github.com/Scoopforge/Extras-Plus
```

## 🚲 Install Scoop

### 💻 Step 1: Enable remote policy in PowerShell

```powershell
Set-ExecutionPolicy RemoteSigned -scope CurrentUser
```

### ⚙️ Step 2: Download and install Scoop

```powershell
irm get.scoop.sh -outfile 'install.ps1'
.\install.ps1 -ScoopDir ['Scoop_Path'] -ScoopGlobalDir ['GlobalScoopApps_Path'] -NoProxy
# for example
.\install.ps1 -ScoopDir 'C:\Scoop' -ScoopGlobalDir 'C:\Program Files' -NoProxy
```

> If you skip this step, all user installed Apps and Scoop itself will live in `c:/users/user_name/scoop`.

### 📖 Step 3: Glance at quick-start by `scoop help`

For more information, please visit 👉 [Scoop official site](https://scoop.sh/) 👈

## 🚗 Install Apps from this bucket

### 🚋 Step 1: Install Aria2 to accelerate downloading

```powershell
scoop install aria2
```

### 🎫 Step 2: Install Git to add new repositories

```powershell
scoop install git
```

### ✈️ Step 3: Add this wonderful bucket and update, mua~ 💋

```powershell
scoop bucket add extras-plus https://github.com/Scoopforge/Extras-Plus
scoop update
```

### 🚀 Step 4: Install App

```powershell
scoop install <app_name>
```

## 📝 Trivial

### Tweaking Parameters of Aria2

```powershell
scoop config aria2-enabled true
scoop config aria2-retry-wait 4
scoop config aria2-split 16
scoop config aria2-max-connection-per-server 16
scoop config aria2-min-split-size 4M
```

## ⭐️ Summary

### AI Specific

|                               App                               | Auto-Update ? | Note                           |
| :-------------------------------------------------------------: | :-----------: | ------------------------------ |
|          [aionui](https://github.com/iOfficeAI/AionUi)          |       ✓       |                                |
|                [buzz](https://buzzcaptions.com)                 |       ✓       |                                |
|               [claude-desktop](https://claude.ai)               |       ✓       |                                |
|         [comfyui](https://github.com/Comfy-Org/ComfyUI)         |       ✓       |                                |
| [comfyui-manager](https://github.com/Comfy-Org/ComfyUI-Manager) |       ✓       |                                |
|                   [cumora](https://cumora.ai)                   |       ✓       |                                |
|        [dsh-official](https://www.deepseek.com/harness)         |       ✓       |                                |
|                [genoffice](https://genoffice.ai)                |       ✓       |                                |
|     [hermes-one](https://github.com/fathah/hermes-desktop)      |       ✓       |                                |
|        [next-ai-drawio](https://next-ai-drawio.jiang.jp)        |       ✓       |                                |
|                 [notegen](https://notegen.top)                  |       ✓       |                                |
|      [open-design](https://github.com/nexu-io/open-design)      |       ✓       |                                |
|           [opencreator](https://www.open-creator.ai)            |       ✓       |                                |
|                  [unsloth](https://unsloth.ai)                  |       ✓       | First run downloads several GB |
|          [vibe](https://github.com/thewh1teagle/vibe)           |       ✓       |                                |
|             [voice-studio](https://voicestudio.sh)              |       ✓       |                                |
|            [wake](https://github.com/iAmCorey/Wake)             |       ✓       | Index in `%LOCALAPPDATA%\wake` |

### General Use

|                            App                            | Auto-Update ? | Note           |
| :-------------------------------------------------------: | :-----------: | -------------- |
|          [affinity](https://www.affinity.studio)          |       ✓       |                |
|     [alexandria](https://github.com/btpf/Alexandria)      |       ✓       |                |
|           [bitcomet](https://www.bitcomet.com)            |       ✓       |                |
|                   [cap](https://cap.so)                   |       ✓       |                |
|        [dingtalk-en](https://www.dingtalk.com/en)         |       ✓       |                |
|    [dorion](https://spikehd.github.io/projects/dorion)    |       ✓       |                |
|     [ecopaste](https://github.com/ayangweb/EcoPaste)      |       ✓       | Needs WebView2 |
|          [elyoffice](https://office.elygpui.com)          |       ✓       |                |
| [filecentipede](https://github.com/filecxx/FileCentipede) |       ✓       | by @CronusLM   |
| [flying-carpet](https://github.com/spieglt/FlyingCarpet)  |       ✓       |                |
|          [isobuster](https://www.isobuster.com)           |       ✓       |                |
|          [kindle](https://amazon.com/kindleapps)          |       ✓       |                |
|           [landrop-latest](https://landrop.app)           |       ✓       |                |
|          [linkandroid](https://linkandroid.com)           |       ✓       |                |
|               [mineru](https://mineru.net)                |       ✓       |                |
|      [musicat](https://github.com/basharovV/musicat)      |       ✓       |                |
|       [normcap](https://github.com/dynobo/normcap)        |       ✓       |                |
|               [p2p-kiwi](https://p2p.kiwi)                |       ✓       |                |
|           [pastemd](https://pastemd.richqaq.cn)           |       ✓       | Bundles Pandoc |
|          [pdf4qt](https://jakubmelka.github.io)           |       ✓       |                |
|          [stirlingpdf](https://stirlingpdf.com)           |       ✓       |                |
|             [veracrypt](https://veracrypt.fr)             |       ✓       |                |
|          [voov-meeting](https://voovmeeting.com)          |       ✓       |                |
|         [ytdownloader](https://ytdn.netlify.app)          |       ✓       |                |

### Academic Tools

|                                  App                                   | Auto-Update ? | Note           |
| :--------------------------------------------------------------------: | :-----------: | -------------- |
|                   [cytoscape](https://cytoscape.org)                   |       ✓       |                |
| [jupyterlab-desktop](https://github.com/jupyterlab/jupyterlab-desktop) |       ✓       |                |
|                       [mogan](https://mogan.app)                       |       ✓       |                |
|            [netlogo](https://ccl.northwestern.edu/netlogo)             |       ✓       |                |
|            [scihubeva](https://github.com/leovan/SciHubEVA)            |       ✓       | by @leovan     |
|          [separatrix](https://github.com/uncrayon/separatrix)          |       ✓       | Needs WebView2 |
|                   [texlive](https://tug.org/texlive)                   |       ✓       |                |
|                   [tylina](https://tylina.github.io)                   |       ✓       |                |
|                       [tropy](https://tropy.org)                       |       ✓       |                |
|                      [zlibrary](https://1lib.sk)                       |       ✓       |                |

### Development Tools

|                                     App                                      | Auto-Update ? | Note |
| :--------------------------------------------------------------------------: | :-----------: | ---- |
|                         [dbgate](https://dbgate.org)                         |       ✓       |      |
|                      [doxygen-gui](https://doxygen.nl)                       |       ✓       |      |
| [navicat-premium-lite](https://navicat.com/en/products/navicat-premium-lite) |       ✓       |      |

### Win-Only

|                                    App                                     | Auto-Update ? | Note |
| :------------------------------------------------------------------------: | :-----------: | ---- |
|               [catime](https://github.com/vladelaina/Catime)               |       ✓       |      |
|     [configure-defender](https://github.com/AndyFul/ConfigureDefender)     |       ✓       |      |
| [defender-remover](https://github.com/ionuttbara/windows-defender-remover) |       ✓       |      |
|               [fancywm](https://github.com/FancyWM/fancywm)                |       ✓       |      |
|                [file-converter](https://file-converter.org)                |       ✓       |      |
|       [watt-toolkit](https://github.com/BeyondDimension/SteamTools)        |       ✓       |      |
|                      [winhance](https://winhance.net)                      |       ✓       |      |
|         [wisecare365](https://wisecleaner.com/wise-care-365.html)          |       ✓       |      |
