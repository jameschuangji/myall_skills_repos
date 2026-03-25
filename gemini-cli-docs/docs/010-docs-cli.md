---
title: Gemini CLI
url: https://geminicli.com/docs/cli
source: crawler
fetched_at: 2026-01-13T19:15:27.464687655-03:00
rendered_js: false
word_count: 291
summary: This document provides a comprehensive reference for Gemini CLI, covering its commands, customization options, advanced features, and non-interactive usage for scripting and automation.
tags:
    - gemini-cli
    - command-line-interface
    - automation
    - scripting
    - configuration
    - advanced-features
category: reference
---

Within Gemini CLI, `packages/cli` is the frontend for users to send and receive prompts with the Gemini AI model and its associated tools. For a general overview of Gemini CLI, see the [main documentation page](https://geminicli.com/docs).

- **[Commands](https://geminicli.com/docs/cli/commands):** A reference for all built-in slash commands
- **[Custom commands](https://geminicli.com/docs/cli/custom-commands):** Create your own commands and shortcuts for frequently used prompts.
- **[Headless mode](https://geminicli.com/docs/cli/headless):** Use Gemini CLI programmatically for scripting and automation.
- **[Model selection](https://geminicli.com/docs/cli/model):** Configure the Gemini AI model used by the CLI.
- **[Settings](https://geminicli.com/docs/cli/settings):** Configure various aspects of the CLI’s behavior and appearance.
- **[Themes](https://geminicli.com/docs/cli/themes):** Customizing the CLI’s appearance with different themes.
- **[Keyboard shortcuts](https://geminicli.com/docs/cli/keyboard-shortcuts):** A reference for all keyboard shortcuts to improve your workflow.
- **[Tutorials](https://geminicli.com/docs/cli/tutorials):** Step-by-step guides for common tasks.

## Advanced features

[Section titled “Advanced features”](#advanced-features)

- **[Checkpointing](https://geminicli.com/docs/cli/checkpointing):** Automatically save and restore snapshots of your session and files.
- **[Enterprise configuration](https://geminicli.com/docs/cli/enterprise):** Deploying and manage Gemini CLI in an enterprise environment.
- **[Sandboxing](https://geminicli.com/docs/cli/sandbox):** Isolate tool execution in a secure, containerized environment.
- **[Telemetry](https://geminicli.com/docs/cli/telemetry):** Configure observability to monitor usage and performance.
- **[Token caching](https://geminicli.com/docs/cli/token-caching):** Optimize API costs by caching tokens.
- **[Trusted folders](https://geminicli.com/docs/cli/trusted-folders):** A security feature to control which projects can use the full capabilities of the CLI.
- **[Ignoring files (.geminiignore)](https://geminicli.com/docs/cli/gemini-ignore):** Exclude specific files and directories from being accessed by tools.
- **[Context files (GEMINI.md)](https://geminicli.com/docs/cli/gemini-md):** Provide persistent, hierarchical context to the model.
- **[System prompt override](https://geminicli.com/docs/cli/system-prompt):** Replace the built‑in system instructions using `GEMINI_SYSTEM_MD`.

## Non-interactive mode

[Section titled “Non-interactive mode”](#non-interactive-mode)

Gemini CLI can be run in a non-interactive mode, which is useful for scripting and automation. In this mode, you pipe input to the CLI, it executes the command, and then it exits.

The following example pipes a command to Gemini CLI from your terminal:

```

echo"What is fine tuning?"|gemini
```

You can also use the `--prompt` or `-p` flag:

```

gemini-p"What is fine tuning?"
```

For comprehensive documentation on headless usage, scripting, automation, and advanced examples, see the [**Headless mode**](https://geminicli.com/docs/cli/headless) guide.