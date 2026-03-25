---
title: Trusted Folders
url: https://geminicli.com/docs/cli/trusted-folders
source: crawler
fetched_at: 2026-01-13T19:15:30.075462114-03:00
rendered_js: false
word_count: 560
summary: This document explains the Gemini CLI's Trusted Folders feature, a security setting that requires user approval for folders to ensure potentially malicious code is not executed. It covers how to enable the feature, the trust dialog options, the implications of untrusted workspaces, and how to manage trust settings.
tags:
    - gemini-cli
    - security
    - trusted-folders
    - workspace-settings
    - cli-configuration
category: guide
---

The Trusted Folders feature is a security setting that gives you control over which projects can use the full capabilities of the Gemini CLI. It prevents potentially malicious code from running by asking you to approve a folder before the CLI loads any project-specific configurations from it.

## Enabling the feature

[Section titled “Enabling the feature”](#enabling-the-feature)

The Trusted Folders feature is **disabled by default**. To use it, you must first enable it in your settings.

Add the following to your user `settings.json` file:

```

{
"security": {
"folderTrust": {
"enabled": true
}
}
}
```

## How it works: The trust dialog

[Section titled “How it works: The trust dialog”](#how-it-works-the-trust-dialog)

Once the feature is enabled, the first time you run the Gemini CLI from a folder, a dialog will automatically appear, prompting you to make a choice:

- **Trust folder**: Grants full trust to the current folder (e.g., `my-project`).
- **Trust parent folder**: Grants trust to the parent directory (e.g., `safe-projects`), which automatically trusts all of its subdirectories as well. This is useful if you keep all your safe projects in one place.
- **Don’t trust**: Marks the folder as untrusted. The CLI will operate in a restricted “safe mode.”

Your choice is saved in a central file (`~/.gemini/trustedFolders.json`), so you will only be asked once per folder.

## Why trust matters: The impact of an untrusted workspace

[Section titled “Why trust matters: The impact of an untrusted workspace”](#why-trust-matters-the-impact-of-an-untrusted-workspace)

When a folder is **untrusted**, the Gemini CLI runs in a restricted “safe mode” to protect you. In this mode, the following features are disabled:

1. **Workspace settings are ignored**: The CLI will **not** load the `.gemini/settings.json` file from the project. This prevents the loading of custom tools and other potentially dangerous configurations.
2. **Environment variables are ignored**: The CLI will **not** load any `.env` files from the project.
3. **Extension management is restricted**: You **cannot install, update, or uninstall** extensions.
4. **Tool auto-acceptance is disabled**: You will always be prompted before any tool is run, even if you have auto-acceptance enabled globally.
5. **Automatic memory loading is disabled**: The CLI will not automatically load files into context from directories specified in local settings.
6. **MCP servers do not connect**: The CLI will not attempt to connect to any [Model Context Protocol (MCP)](https://geminicli.com/docs/tools/mcp-server) servers.
7. **Custom commands are not loaded**: The CLI will not load any custom commands from .toml files, including both project-specific and global user commands.

Granting trust to a folder unlocks the full functionality of the Gemini CLI for that workspace.

## Managing your trust settings

[Section titled “Managing your trust settings”](#managing-your-trust-settings)

If you need to change a decision or see all your settings, you have a couple of options:

- **Change the current folder’s trust**: Run the `/permissions` command from within the CLI. This will bring up the same interactive dialog, allowing you to change the trust level for the current folder.
- **View all trust rules**: To see a complete list of all your trusted and untrusted folder rules, you can inspect the contents of the `~/.gemini/trustedFolders.json` file in your home directory.

## The trust check process (advanced)

[Section titled “The trust check process (advanced)”](#the-trust-check-process-advanced)

For advanced users, it’s helpful to know the exact order of operations for how trust is determined:

1. **IDE trust signal**: If you are using the [IDE Integration](https://geminicli.com/docs/ide-integration), the CLI first asks the IDE if the workspace is trusted. The IDE’s response takes highest priority.
2. **Local trust file**: If the IDE is not connected, the CLI checks the central `~/.gemini/trustedFolders.json` file.