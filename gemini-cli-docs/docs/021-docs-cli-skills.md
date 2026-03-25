---
title: Agent Skills
url: https://geminicli.com/docs/cli/skills/
source: crawler
fetched_at: 2026-01-13T19:15:17.623643399-03:00
rendered_js: false
word_count: 798
summary: This document explains Gemini CLI's Agent Skills feature, which allows extending the CLI's capabilities with specialized, on-demand expertise packaged as self-contained directories. It covers how skills are discovered, managed via interactive commands and terminal utilities, and structured with a `SKILL.md` file for metadata and instructions.
tags:
    - gemini-cli
    - agent-skills
    - cli-extensions
    - procedural-guidance
    - skill-discovery
category: guide
---

*Note: This is an experimental feature enabled via `experimental.skills`. You can also search for “Skills” within the `/settings` interactive UI to toggle this and manage other skill-related settings.*

Agent Skills allow you to extend Gemini CLI with specialized expertise, procedural workflows, and task-specific resources. Based on the [Agent Skills](https://agentskills.io) open standard, a “skill” is a self-contained directory that packages instructions and assets into a discoverable capability.

Unlike general context files ([`GEMINI.md`](https://geminicli.com/docs/cli/gemini-md)), which provide persistent project-wide background, Skills represent **on-demand expertise**. This allows Gemini to maintain a vast library of specialized capabilities—such as security auditing, cloud deployments, or codebase migrations—without cluttering the model’s immediate context window.

Gemini autonomously decides when to employ a skill based on your request and the skill’s description. When a relevant skill is identified, the model “pulls in” the full instructions and resources required to complete the task using the `activate_skill` tool.

- **Shared Expertise:** Package complex workflows (like a specific team’s PR review process) into a folder that anyone can use.
- **Repeatable Workflows:** Ensure complex multi-step tasks are performed consistently by providing a procedural framework.
- **Resource Bundling:** Include scripts, templates, or example data alongside instructions so the agent has everything it needs.
- **Progressive Disclosure:** Only skill metadata (name and description) is loaded initially. Detailed instructions and resources are only disclosed when the model explicitly activates the skill, saving context tokens.

## Skill Discovery Tiers

[Section titled “Skill Discovery Tiers”](#skill-discovery-tiers)

Gemini CLI discovers skills from three primary locations:

1. **Project Skills** (`.gemini/skills/`): Project-specific skills that are typically committed to version control and shared with the team.
2. **User Skills** (`~/.gemini/skills/`): Personal skills available across all your projects.
3. **Extension Skills**: Skills bundled within installed [extensions](https://geminicli.com/docs/extensions).

**Precedence:** If multiple skills share the same name, higher-precedence locations override lower ones: **Project &gt; User &gt; Extension**.

### In an Interactive Session

[Section titled “In an Interactive Session”](#in-an-interactive-session)

Use the `/skills` slash command to view and manage available expertise:

- `/skills list` (default): Shows all discovered skills and their status.
- `/skills disable <name>`: Prevents a specific skill from being used.
- `/skills enable <name>`: Re-enables a disabled skill.
- `/skills reload`: Refreshes the list of discovered skills from all tiers.

*Note: `/skills disable` and `/skills enable` default to the `user` scope. Use `--scope project` to manage project-specific settings.*

### From the Terminal

[Section titled “From the Terminal”](#from-the-terminal)

The `gemini skills` command provides management utilities:

```

# List all discovered skills
geminiskillslist
# Install a skill from a Git repository, local directory, or zipped skill file (.skill)
# Uses the user scope by default (~/.gemini/skills)
geminiskillsinstallhttps://github.com/user/repo.git
geminiskillsinstall/path/to/local/skill
geminiskillsinstall/path/to/local/my-expertise.skill
# Install a specific skill from a monorepo or subdirectory using --path
geminiskillsinstallhttps://github.com/my-org/my-skills.git--pathskills/frontend-design
# Install to the workspace scope (.gemini/skills)
geminiskillsinstall/path/to/skill--scopeworkspace
# Uninstall a skill by name
geminiskillsuninstallmy-expertise--scopeworkspace
# Enable a skill (globally)
geminiskillsenablemy-expertise
# Disable a skill. Can use --scope to specify project or user (defaults to project)
geminiskillsdisablemy-expertise--scopeproject
```

A skill is a directory containing a `SKILL.md` file at its root. This file uses YAML frontmatter for metadata and Markdown for instructions.

```

---
name: <unique-name>
description: <what the skill does and when Gemini should use it>
---
<yourinstructionsforhowtheagentshouldbehave/usetheskill>
```

- **`name`** : A unique identifier (lowercase, alphanumeric, and dashes).
- **`description`** : The most critical field. Gemini uses this to decide when the skill is relevant. Be specific about the expertise provided.
- **Body**: Everything below the second `---` is injected as expert procedural guidance for the model.

### Example: Team Code Reviewer

[Section titled “Example: Team Code Reviewer”](#example-team-code-reviewer)

```

---
name: code-reviewer
description:
Expertise in reviewing code for style, security, and performance. Use when the
user asks for "feedback," a "review," or to "check" their changes.
---
# Code Reviewer
You are an expert code reviewer. When reviewing code, follow this workflow:
1.**Analyze**: Review the staged changes or specific files provided. Ensure
that the changes are scoped properly and represent minimal changes required
to address the issue.
2.**Style**: Ensure code follows the project's conventions and idiomatic
patterns as described in the `GEMINI.md` file.
3.**Security**: Flag any potential security vulnerabilities.
4.**Tests**: Verify that new logic has corresponding test coverage and that
the test coverage adequately validates the changes.
Provide your feedback as a concise bulleted list of "Strengths" and
"Opportunities."
```

### Resource Conventions

[Section titled “Resource Conventions”](#resource-conventions)

While you can structure your skill directory however you like, the Agent Skills standard encourages these conventions:

- **`scripts/`** : Executable scripts (bash, python, node) the agent can run.
- **`references/`** : Static documentation, schemas, or example data for the agent to consult.
- **`assets/`** : Code templates, boilerplate, or binary resources.

When a skill is activated, Gemini CLI provides the model with a tree view of the entire skill directory, allowing it to discover and utilize these assets.

## How it Works (Security & Privacy)

[Section titled “How it Works (Security & Privacy)”](#how-it-works-security--privacy)

1. **Discovery**: At the start of a session, Gemini CLI scans the discovery tiers and injects the name and description of all enabled skills into the system prompt.
2. **Activation**: When Gemini identifies a task matching a skill’s description, it calls the `activate_skill` tool.
3. **Consent**: You will see a confirmation prompt in the UI detailing the skill’s name, purpose, and the directory path it will gain access to.
4. **Injection**: Upon your approval:
   
   - The `SKILL.md` body and folder structure is added to the conversation history.
   - The skill’s directory is added to the agent’s allowed file paths, granting it permission to read any bundled assets.
5. **Execution**: The model proceeds with the specialized expertise active. It is instructed to prioritize the skill’s procedural guidance within reason.