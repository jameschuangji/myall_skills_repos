---
title: Session Management
url: https://geminicli.com/docs/cli/session-management
source: crawler
fetched_at: 2026-01-13T19:15:40.172853772-03:00
rendered_js: false
word_count: 526
summary: This document explains how Gemini CLI automatically saves and manages conversation sessions, including how to resume, list, delete, and configure session retention policies.
tags:
    - session-management
    - conversation-history
    - cli-commands
    - configuration
    - session-retention
category: guide
---

Gemini CLI includes robust session management features that automatically save your conversation history. This allows you to interrupt your work and resume exactly where you left off, review past interactions, and manage your conversation history effectively.

Every time you interact with Gemini CLI, your session is automatically saved. This happens in the background without any manual intervention.

- **What is saved:** The complete conversation history, including:
  
  - Your prompts and the model’s responses.
  - All tool executions (inputs and outputs).
  - Token usage statistics (input/output/cached, etc.).
  - Assistant thoughts/reasoning summaries (when available).
- **Location:** Sessions are stored in `~/.gemini/tmp/<project_hash>/chats/`.
- **Scope:** Sessions are project-specific. Switching directories to a different project will switch to that project’s session history.

## Resuming Sessions

[Section titled “Resuming Sessions”](#resuming-sessions)

You can resume a previous session to continue the conversation with all prior context restored.

### From the Command Line

[Section titled “From the Command Line”](#from-the-command-line)

When starting the CLI, you can use the `--resume` (or `-r`) flag:

- **Resume latest:**
  
  This immediately loads the most recent session.
- **Resume by index:** First, list available sessions (see [Listing Sessions](#listing-sessions)), then use the index number:
- **Resume by ID:** You can also provide the full session UUID:
  
  ```
  
  gemini--resumea1b2c3d4-e5f6-7890-abcd-ef1234567890
  ```

### From the Interactive Interface

[Section titled “From the Interactive Interface”](#from-the-interactive-interface)

While the CLI is running, you can use the `/resume` slash command to open the **Session Browser**:

This opens an interactive interface where you can:

- **Browse:** Scroll through a list of your past sessions.
- **Preview:** See details like the session date, message count, and the first user prompt.
- **Search:** Press `/` to enter search mode, then type to filter sessions by ID or content.
- **Select:** Press `Enter` to resume the selected session.

## Managing Sessions

[Section titled “Managing Sessions”](#managing-sessions)

To see a list of all available sessions for the current project from the command line:

Output example:

```

Available sessions for this project (3):
1. Fix bug in auth (2 days ago) [a1b2c3d4]
2. Refactor database schema (5 hours ago) [e5f67890]
3. Update documentation (Just now) [abcd1234]
```

### Deleting Sessions

[Section titled “Deleting Sessions”](#deleting-sessions)

You can remove old or unwanted sessions to free up space or declutter your history.

**From the Command Line:** Use the `--delete-session` flag with an index or ID:

```

gemini--delete-session2
```

**From the Session Browser:**

1. Open the browser with `/resume`.
2. Navigate to the session you want to remove.
3. Press `x`.

You can configure how Gemini CLI manages your session history in your `settings.json` file.

### Session Retention

[Section titled “Session Retention”](#session-retention)

To prevent your history from growing indefinitely, you can enable automatic cleanup policies.

```

{
"general": {
"sessionRetention": {
"enabled": true,
"maxAge": "30d", // Keep sessions for 30 days
"maxCount": 50// Keep the 50 most recent sessions
}
}
}
```

- **`enabled`** : (boolean) Master switch for session cleanup. Default is `false`.
- **`maxAge`** : (string) Duration to keep sessions (e.g., “24h”, “7d”, “4w”). Sessions older than this will be deleted.
- **`maxCount`** : (number) Maximum number of sessions to retain. The oldest sessions exceeding this count will be deleted.
- **`minRetention`** : (string) Minimum retention period (safety limit). Defaults to `"1d"`; sessions newer than this period are never deleted by automatic cleanup.

You can also limit the length of individual sessions to prevent context windows from becoming too large and expensive.

```

{
"model": {
"maxSessionTurns": 100
}
}
```

- **`maxSessionTurns`** : (number) The maximum number of turns (user + model exchanges) allowed in a single session. Set to `-1` for unlimited (default).
  
  **Behavior when limit is reached:**
  
  - **Interactive Mode:** The CLI shows an informational message and stops sending requests to the model. You must manually start a new session.
  - **Non-Interactive Mode:** The CLI exits with an error.