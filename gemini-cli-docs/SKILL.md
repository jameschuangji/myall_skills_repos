---
name: gemini-cli-docs
description: |
  Gemini CLI - Google's AI-powered command-line interface for building, debugging, and deploying with AI.
  Use when working with Gemini CLI configuration, commands, tools, extensions, hooks, skills, or MCP servers.
  Keywords: gemini-cli, google-ai, terminal, code-generation, workflow-automation, cli-commands, gemini-md, authentication, configuration, sandboxing, headless-mode, custom-commands, agent-skills, extensions, hooks, mcp-servers, file-system-tools, shell-commands, web-search, ide-integration.
compatibility: Node.js 18+, npm or npx. Works on macOS, Linux, and Windows.
metadata:
  source: https://geminicli.com/
  total_docs: 67
  generated: 2026-01-13T19:17:00Z
---

# Gemini CLI

> Query and edit large codebases, generate apps from images or PDFs, and automate complex workflows - all from your terminal with Gemini AI.

## Quick Start

```bash
# Install globally
npm install -g @google/gemini-cli

# Run (starts interactive session)
gemini

# Or run without install
npx @google/gemini-cli
```

## Authentication

On first run, select authentication method:
1. **Login with Google** - Most common, uses existing Google account
2. **API Key** - For programmatic access via `GEMINI_API_KEY` environment variable
3. **Vertex AI** - Enterprise, requires Google Cloud project

## Key Commands

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/settings` | Open settings editor |
| `/model` | Select Gemini model (Auto, Pro, Flash) |
| `/chat save <tag>` | Save conversation state |
| `/chat resume <tag>` | Resume saved conversation |
| `/restore` | Revert file changes to checkpoint |
| `/memory show` | Display loaded GEMINI.md content |
| `/skills list` | List available agent skills |
| `/mcp list` | List MCP servers and tools |
| `/tools` | Display available tools |
| `!<cmd>` | Execute shell command |
| `@<path>` | Include file/directory in prompt |

## Configuration

Configuration files location: `~/.gemini/` (global) or `.gemini/` (project)

Key files:
- `settings.json` - CLI settings
- `GEMINI.md` - Project context/instructions (hierarchical memory)
- `skills/` - Agent skills directory

## Documentation

Full documentation in `docs/`. Consult `docs/000-index.md` for detailed navigation.

### By Topic

| Topic | Files | Description |
|-------|-------|-------------|
| Installation & Setup | 003-009 | Get Gemini CLI installed and configured |
| Basic Usage | 010-016 | Core commands, settings, and interface |
| Advanced Features | 017-032 | Security, automation, and customization |
| Architecture | 033-037 | Internal design and APIs |
| Tools | 038-045 | Built-in capabilities for files, shell, web, memory |
| Extensions | 046-048 | Creating and managing extensions |
| Hooks | 049-052 | Event-driven automation |
| IDE Integration | 053-054 | Editor integration and plugins |
| Development | 055-058 | Contributing and testing |
| Releases | 059-063 | Version history and updates |
| Reference | 064-067 | FAQ, troubleshooting, pricing, legal |

### By Keyword

| Keyword | File |
|---------|------|
| installation | `docs/004-docs-get-started-installation.md` |
| authentication | `docs/005-docs-get-started-authentication.md` |
| configuration | `docs/006-docs-get-started-configuration.md` |
| commands | `docs/011-docs-cli-commands.md` |
| settings | `docs/012-docs-cli-settings.md` |
| model-selection | `docs/013-docs-cli-model.md` |
| themes | `docs/014-docs-cli-themes.md` |
| keyboard-shortcuts | `docs/015-docs-cli-keyboard-shortcuts.md` |
| session-management | `docs/016-docs-cli-session-management.md` |
| checkpointing | `docs/017-docs-cli-checkpointing.md` |
| sandboxing | `docs/018-docs-cli-sandbox.md` |
| headless-mode | `docs/019-docs-cli-headless.md` |
| custom-commands | `docs/020-docs-cli-custom-commands.md` |
| agent-skills | `docs/021-docs-cli-skills.md` |
| enterprise | `docs/022-docs-cli-enterprise.md` |
| trusted-folders | `docs/023-docs-cli-trusted-folders.md` |
| system-prompt | `docs/024-docs-cli-system-prompt.md` |
| token-caching | `docs/025-docs-cli-token-caching.md` |
| telemetry | `docs/026-docs-cli-telemetry.md` |
| mcp-server | `docs/027-docs-cli-tutorials.md` |
| gemini-md | `docs/029-docs-cli-gemini-md.md` |
| architecture | `docs/033-docs-architecture.md` |
| policy-engine | `docs/035-docs-core-policy-engine.md` |
| tools-api | `docs/036-docs-core-tools-api.md` |
| file-system-tools | `docs/039-docs-tools-file-system.md` |
| shell-command | `docs/040-docs-tools-shell.md` |
| web-search | `docs/041-docs-tools-web-search.md` |
| web-fetch | `docs/042-docs-tools-web-fetch.md` |
| memory-tool | `docs/043-docs-tools-memory.md` |
| todo-tool | `docs/044-docs-tools-todos.md` |
| mcp-servers | `docs/045-docs-tools-mcp-server.md` |
| extensions | `docs/046-docs-extensions.md` |
| hooks | `docs/049-docs-hooks.md` |
| ide-integration | `docs/053-docs-ide-integration.md` |
| faq | `docs/064-docs-faq.md` |
| troubleshooting | `docs/065-docs-troubleshooting.md` |
| pricing | `docs/066-docs-quota-and-pricing.md` |

### Learning Path

1. **Foundation**: Install (004), authenticate (005), configure (006)
2. **Core Usage**: Commands (011), settings (012), model selection (013)
3. **Productivity**: Checkpointing (017), custom commands (020), skills (021)
4. **Advanced**: Extensions (046-048), hooks (049-052), MCP servers (045)

## Common Tasks

### Configure GEMINI.md for project context
-> `docs/006-docs-get-started-configuration.md` (hierarchical memory setup)

### Create custom slash commands
-> `docs/020-docs-cli-custom-commands.md` (TOML-based command definitions)

### Set up agent skills
-> `docs/021-docs-cli-skills.md` (create SKILL.md with frontmatter)

### Run in headless/CI mode
-> `docs/019-docs-cli-headless.md` (automation and JSON output)

### Configure MCP servers
-> `docs/045-docs-tools-mcp-server.md` (Model Context Protocol integration)

### Build CLI extensions
-> `docs/047-docs-extensions-getting-started-extensions.md` (extension development)

### Write automation hooks
-> `docs/050-docs-hooks-writing-hooks.md` (event-driven scripts)

### Sandbox execution for security
-> `docs/018-docs-cli-sandbox.md` (Docker/Podman isolation)

### Troubleshoot common issues
-> `docs/065-docs-troubleshooting.md` (debugging and error resolution)

### Understand pricing and quotas
-> `docs/066-docs-quota-and-pricing.md` (free tier, paid options)
