# 🍨 Scoop Extras Plus 🍨

[![Excavator](https://github.com/Scoopforge/Extras-Plus/actions/workflows/ci.yml/badge.svg)](https://github.com/Scoopforge/Extras-Plus/actions/workflows/ci.yml)
[![license](https://img.shields.io/github/license/Scoopforge/Extras-Plus)](https://github.com/Scoopforge/Extras-Plus/blob/master/LICENSE)
[![code size](https://img.shields.io/github/languages/code-size/Scoopforge/Extras-Plus.svg)](https://img.shields.io/github/languages/code-size/Scoopforge/Extras-Plus.svg)
[![repo size](https://img.shields.io/github/repo-size/Scoopforge/Extras-Plus.svg)](https://img.shields.io/github/repo-size/Scoopforge/Extras-Plus.svg)

A Bucket for the Best Windows Package Manager [Scoop](https://github.com/ScoopInstaller/Scoop): An Enhancement for the Official CLI Bucket.

> If you would like to be a co-maintainer, feel free to tell me in the Discussion.

For ones familiar with Scoop:

```powershell
scoop bucket add Extras-plus https://github.com/Scoopforge/Extras-Plus
```

Enjoy the fun of command line!

# 🏃 To Start

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

For more information, please visit Scoop official site at 👉 https://scoop.sh/ 👈

## 🚗 Install Apps from this bucket

### 🚋 Step 1: Install Aria2 to accelerate downloading

```powershell
scoop install aria2
```

### 🎫 Step 2: Install Git to add new repositories

```powershell
scoop install git
```

if you are using VPN, you need to turn off aria2 before installing Apps

```powershell
scoop config aria2-enabled false
```

### ✈️ Step 3: Add this wonderful bucket and update, mua~ 💋

```powershell
scoop bucket add Extras-plus https://github.com/Scoopforge/Extras-Plus
scoop update
```

### 🚀 Step 4: Install CLI

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

|                        App                        | Auto-Update ? | Original ? |
| :-----------------------------------------------: | :-----------: | :--------: |
|           [dbgate](https://dbgate.org)            |       ✓       |     ✓      |
| [lrcget](https://github.com/tranxuanthang/lrcget) |       ✓       |     ✓      |
|   [vibe](https://github.com/thewh1teagle/vibe)    |       ✓       |     ✓      |
