---
title: Policy engine
url: https://geminicli.com/docs/core/policy-engine
source: crawler
fetched_at: 2026-01-13T19:15:32.385728704-03:00
rendered_js: false
word_count: 1245
summary: This document explains how to use the Gemini CLI's policy engine to control tool execution with rules based on tool name, arguments, and priority.
tags:
    - gemini-cli
    - policy-engine
    - tool-execution
    - rules
    - configuration
category: guide
---

The Gemini CLI includes a powerful policy engine that provides fine-grained control over tool execution. It allows users and administrators to define rules that determine whether a tool call should be allowed, denied, or require user confirmation.

To create your first policy:

1. **Create the policy directory** if it doesn’t exist:
   
   ```
   
   mkdir-p~/.gemini/policies
   ```
2. **Create a new policy file** (e.g., `~/.gemini/policies/my-rules.toml`). You can use any filename ending in `.toml`; all such files in this directory will be loaded and combined:
   
   ```
   
   [[rule]]
   toolName = "run_shell_command"
   commandPrefix = "git status"
   decision = "allow"
   priority = 100
   ```
3. **Run a command** that triggers the policy (e.g., ask Gemini CLI to `git status`). The tool will now execute automatically without prompting for confirmation.

The policy engine operates on a set of rules. Each rule is a combination of conditions and a resulting decision. When a large language model wants to execute a tool, the policy engine evaluates all rules to find the highest-priority rule that matches the tool call.

A rule consists of the following main components:

- **Conditions**: Criteria that a tool call must meet for the rule to apply. This can include the tool’s name, the arguments provided to it, or the current approval mode.
- **Decision**: The action to take if the rule matches (`allow`, `deny`, or `ask_user`).
- **Priority**: A number that determines the rule’s precedence. Higher numbers win.

For example, this rule will ask for user confirmation before executing any `git` command.

```

[[rule]]
toolName = "run_shell_command"
commandPrefix = "git "
decision = "ask_user"
priority = 100
```

Conditions are the criteria that a tool call must meet for a rule to apply. The primary conditions are the tool’s name and its arguments.

The `toolName` in the rule must match the name of the tool being called.

- **Wildcards**: For Model-hosting-protocol (MCP) servers, you can use a wildcard. A `toolName` of `my-server__*` will match any tool from the `my-server` MCP.

#### Arguments pattern

[Section titled “Arguments pattern”](#arguments-pattern)

If `argsPattern` is specified, the tool’s arguments are converted to a stable JSON string, which is then tested against the provided regular expression. If the arguments don’t match the pattern, the rule does not apply.

There are three possible decisions a rule can enforce:

- `allow`: The tool call is executed automatically without user interaction.
- `deny`: The tool call is blocked and is not executed.
- `ask_user`: The user is prompted to approve or deny the tool call. (In non-interactive mode, this is treated as `deny`.)

### Priority system and tiers

[Section titled “Priority system and tiers”](#priority-system-and-tiers)

The policy engine uses a sophisticated priority system to resolve conflicts when multiple rules match a single tool call. The core principle is simple: **the rule with the highest priority wins**.

To provide a clear hierarchy, policies are organized into three tiers. Each tier has a designated number that forms the base of the final priority calculation.

TierBaseDescriptionDefault1Built-in policies that ship with the Gemini CLI.User2Custom policies defined by the user.Admin3Policies managed by an administrator (e.g., in an enterprise environment).

Within a TOML policy file, you assign a priority value from **0 to 999**. The engine transforms this into a final priority using the following formula:

`final_priority = tier_base + (toml_priority / 1000)`

This system guarantees that:

- Admin policies always override User and Default policies.
- User policies always override Default policies.
- You can still order rules within a single tier with fine-grained control.

For example:

- A `priority: 50` rule in a Default policy file becomes `1.050`.
- A `priority: 100` rule in a User policy file becomes `2.100`.
- A `priority: 20` rule in an Admin policy file becomes `3.020`.

Approval modes allow the policy engine to apply different sets of rules based on the CLI’s operational mode. A rule can be associated with one or more modes (e.g., `yolo`, `autoEdit`). The rule will only be active if the CLI is running in one of its specified modes. If a rule has no modes specified, it is always active.

When a tool call is made, the engine checks it against all active rules, starting from the highest priority. The first rule that matches determines the outcome.

A rule matches a tool call if all of its conditions are met:

1. **Tool name**: The `toolName` in the rule must match the name of the tool being called.
   
   - **Wildcards**: For Model-hosting-protocol (MCP) servers, you can use a wildcard. A `toolName` of `my-server__*` will match any tool from the `my-server` MCP.
2. **Arguments pattern**: If `argsPattern` is specified, the tool’s arguments are converted to a stable JSON string, which is then tested against the provided regular expression. If the arguments don’t match the pattern, the rule does not apply.

Policies are defined in `.toml` files. The CLI loads these files from Default, User, and (if configured) Admin directories.

Here is a breakdown of the fields available in a TOML policy rule:

```

[[rule]]
# A unique name for the tool, or an array of names.
toolName = "run_shell_command"
# (Optional) The name of an MCP server. Can be combined with toolName
# to form a composite name like "mcpName__toolName".
mcpName = "my-custom-server"
# (Optional) A regex to match against the tool's arguments.
argsPattern = '"command":"(git|npm)'
# (Optional) A string or array of strings that a shell command must start with.
# This is syntactic sugar for `toolName = "run_shell_command"` and an `argsPattern`.
commandPrefix = "git "
# (Optional) A regex to match against the entire shell command.
# This is also syntactic sugar for `toolName = "run_shell_command"`.
# Note: This pattern is tested against the JSON representation of the arguments (e.g., `{"command":"<your_command>"}`), so anchors like `^` or `$` will apply to the full JSON string, not just the command text.
# You cannot use commandPrefix and commandRegex in the same rule.
commandRegex = "^git (commit|push)"
# The decision to take. Must be "allow", "deny", or "ask_user".
decision = "ask_user"
# The priority of the rule, from 0 to 999.
priority = 10
# (Optional) An array of approval modes where this rule is active.
modes = ["autoEdit"]
```

### Using arrays (lists)

[Section titled “Using arrays (lists)”](#using-arrays-lists)

To apply the same rule to multiple tools or command prefixes, you can provide an array of strings for the `toolName` and `commandPrefix` fields.

**Example:**

This single rule will apply to both the `write_file` and `replace` tools.

```

[[rule]]
toolName = ["write_file", "replace"]
decision = "ask_user"
priority = 10
```

### Special syntax for `run_shell_command`

[Section titled “Special syntax for run\_shell\_command”](#special-syntax-for-run_shell_command)

To simplify writing policies for `run_shell_command`, you can use `commandPrefix` or `commandRegex` instead of the more complex `argsPattern`.

- `commandPrefix`: Matches if the `command` argument starts with the given string.
- `commandRegex`: Matches if the `command` argument matches the given regular expression.

**Example:**

This rule will ask for user confirmation before executing any `git` command.

```

[[rule]]
toolName = "run_shell_command"
commandPrefix = "git "
decision = "ask_user"
priority = 100
```

### Special syntax for MCP tools

[Section titled “Special syntax for MCP tools”](#special-syntax-for-mcp-tools)

You can create rules that target tools from Model-hosting-protocol (MCP) servers using the `mcpName` field or a wildcard pattern.

**1. Using `mcpName`**

To target a specific tool from a specific server, combine `mcpName` and `toolName`.

```

# Allows the `search` tool on the `my-jira-server` MCP
[[rule]]
mcpName = "my-jira-server"
toolName = "search"
decision = "allow"
priority = 200
```

**2. Using a wildcard**

To create a rule that applies to *all* tools on a specific MCP server, specify only the `mcpName`.

```

# Denies all tools from the `untrusted-server` MCP
[[rule]]
mcpName = "untrusted-server"
decision = "deny"
priority = 500
```

The Gemini CLI ships with a set of default policies to provide a safe out-of-the-box experience.

- **Read-only tools** (like `read_file`, `glob`) are generally **allowed**.
- **Agent delegation** (like `delegate_to_agent`) defaults to **`ask_user`** to ensure remote agents can prompt for confirmation, but local sub-agent actions are executed silently and checked individually.
- **Write tools** (like `write_file`, `run_shell_command`) default to **`ask_user`** .
- In **`yolo`** mode, a high-priority rule allows all tools.
- In **`autoEdit`** mode, rules allow certain write operations to happen without prompting.