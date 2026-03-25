---
title: Uninstalling the CLI
url: https://geminicli.com/docs/cli/uninstall
source: crawler
fetched_at: 2026-01-13T19:15:30.458834892-03:00
rendered_js: false
word_count: 145
summary: 'This document explains how to uninstall the gemini-cli tool, providing instructions for two different installation methods: using npx, which involves clearing the npx cache, and a global npm installation, which uses the standard npm uninstall command.'
tags:
    - uninstall
    - gemini-cli
    - npx
    - npm
    - global-install
    - cache-clearing
category: tutorial
---

Your uninstall method depends on how you ran the CLI. Follow the instructions for either npx or a global npm installation.

## Method 1: Using npx

[Section titled “Method 1: Using npx”](#method-1-using-npx)

npx runs packages from a temporary cache without a permanent installation. To “uninstall” the CLI, you must clear this cache, which will remove gemini-cli and any other packages previously executed with npx.

The npx cache is a directory named `_npx` inside your main npm cache folder. You can find your npm cache path by running `npm config get cache`.

**For macOS / Linux**

```

# The path is typically ~/.npm/_npx
rm-rf"$(npm config get cache)/_npx"
```

**For Windows**

*Command Prompt*

```

:: The path is typically %LocalAppData%\npm-cache\_npx
rmdir /s /q "%LocalAppData%\npm-cache\_npx"
```

*PowerShell*

```

# The path is typically $env:LocalAppData\npm-cache\_npx
Remove-Item-Path (Join-Path $env:LocalAppData "npm-cache\_npx") -Recurse -Force
```

## Method 2: Using npm (global install)

[Section titled “Method 2: Using npm (global install)”](#method-2-using-npm-global-install)

If you installed the CLI globally (e.g., `npm install -g @google/gemini-cli`), use the `npm uninstall` command with the `-g` flag to remove it.

```

npmuninstall-g@google/gemini-cli
```

This command completely removes the package from your system.