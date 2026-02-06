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

### Cross-Platform

#### General Use

|                            App                             | Auto-Update ? |     Note     |
|:----------------------------------------------------------:|:-------------:|:------------:|
|      [alexandria](https://github.com/btpf/Alexandria)      |       ✓       |              |
| [alist-helper](https://github.com/Xmarmalade/alisthelper)  |       ✓       |              |
|             [bananas](https://getbananas.net/)             |       ✓       |              |
|           [bitcomet](https://www.bitcomet.com/)            |       ✓       |              |
|              [buzz](https://buzzcaptions.com)              |       ✓       |              |
|     [ecopast](https://github.com/EcoPasteHub/EcoPaste)     |       ✓       |              |
| [filecentipede](https://github.com/filecxx/FileCentipede)  |       ✓       | by @CronusLM |
| [flying-carpet](https://github.com/spieglt/FlyingCarpet/)  |       ✓       |              |
|          [kindle](https://amazon.com/kindleapps)           |       ✓       |              |
|           [landrop-latest](https://landrop.app)            |       ✓       |              |
| [linkandroid](https://github.com/modstart-lib/linkandroid) |       ✓       |              |
|      [musicat](https://github.com/basharovV/musicat)       |       ✓       |              |
|        [normcap](https://github.com/dynobo/normcap)        |       ✓       |              |
|       [notegen](https://github.com/codexu/note-gen)        |       ✓       |              |
|           [pastemd](https://pastemd.richqaq.cn)            |       ✓       |              |
|           [pdf4qt](https://jakubmelka.github.io)           |       ✓       |              |
|           [stirlingpdf](https://stirlingpdf.com)           |       ✓       |              |
|             [veracrypt](https://veracrypt.fr)              |       ✓       |              |
|        [vibe](https://github.com/thewh1teagle/vibe)        |       ✓       |              |
|          [voov-meeting](https://voovmeeting.com)           |       ✓       |              |
|          [ytdownloader](https://ytdn.netlify.app)          |       ✓       |              |

#### Academic Tools

|                                  App                                   | Auto-Update ? |    Note    |
|:----------------------------------------------------------------------:|:-------------:|:----------:|
|                   [cytoscape](https://cytoscape.org)                   |       ✓       |            |
| [jupyterlab-desktop](https://github.com/jupyterlab/jupyterlab-desktop) |       ✓       |            |
|                       [mogan](https://mogan.app)                       |       ✓       |            |
|            [netlogo](https://ccl.northwestern.edu/netlogo)             |       ✓       |            |
|            [scihubeva](https://github.com/leovan/SciHubEVA)            |       ✓       | by @leovan |
|                   [texlive](https://tug.org/texlive)                   |       ✓       |            |
|                       [tropy](https://tropy.org)                       |       ✓       |            |

#### Development Tools

|                                     App                                      | Auto-Update ? | Note |
|:----------------------------------------------------------------------------:|:-------------:|:----:|
|                         [dbgate](https://dbgate.org)                         |       ✓       |      |
|                       [doxygen-gui](http://doxygen.nl)                       |       ✓       |      |
| [navicat-premium-lite](https://navicat.com/en/products/navicat-premium-lite) |       ✓       |      |

### Win-Only

|                                    App                                     | Auto-Update ? | Note |
|:--------------------------------------------------------------------------:|:-------------:|:----:|
|    [autodarkmode](https://github.com/Armin2208/Windows-Auto-Night-Mode)    |       ✓       |      |
|     [configure-defender](https://github.com/AndyFul/ConfigureDefender)     |       ✓       |      |
| [defender-remover](https://github.com/ionuttbara/windows-defender-remover) |       ✓       |      |
|               [fancywm](https://github.com/FancyWM/fancywm)                |       ✓       |      |
|                [file-converter](https://file-converter.org)                |       ✓       |      |
|             [jigdo](https://einval.com/~steve/software/jigdo)              |       ✓       |      |
|                     [winhance](hhttps://winhance.net)                      |       ✓       |      |
|         [wisecare365](https://wisecleaner.com/wise-care-365.html)          |       ✓       |      |
