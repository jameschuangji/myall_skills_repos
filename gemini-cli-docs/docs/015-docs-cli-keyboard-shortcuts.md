---
title: Gemini CLI keyboard shortcuts
url: https://geminicli.com/docs/cli/keyboard-shortcuts
source: crawler
fetched_at: 2026-01-13T19:15:29.928431772-03:00
rendered_js: false
word_count: 629
summary: This document serves as a reference for the default keyboard shortcuts available in the Gemini CLI, covering actions for input editing, history navigation, UI control, and suggestions.
tags:
    - gemini-cli
    - keyboard-shortcuts
    - reference
    - command-line
    - editing
    - navigation
category: reference
---

Gemini CLI ships with a set of default keyboard shortcuts for editing input, navigating history, and controlling the UI. Use this reference to learn the available combinations.

ActionKeysConfirm the current selection or choice.`Enter`Dismiss dialogs or cancel the current focus.`Esc`

ActionKeysMove the cursor to the start of the line.`Ctrl + A`  
`Home`Move the cursor to the end of the line.`Ctrl + E`  
`End`Move the cursor one character to the left.`Left Arrow (no Ctrl, no Cmd)`  
`Ctrl + B`Move the cursor one character to the right.`Right Arrow (no Ctrl, no Cmd)`  
`Ctrl + F`Move the cursor one word to the left.`Ctrl + Left Arrow`  
`Cmd + Left Arrow`  
`Cmd + B`Move the cursor one word to the right.`Ctrl + Right Arrow`  
`Cmd + Right Arrow`  
`Cmd + F`

ActionKeysDelete from the cursor to the end of the line.`Ctrl + K`Delete from the cursor to the start of the line.`Ctrl + U`Clear all text in the input field.`Ctrl + C`Delete the previous word.`Ctrl + Backspace`  
`Cmd + Backspace`  
`Ctrl + ""`  
`Cmd + ""`  
`Ctrl + W`Delete the next word.`Ctrl + Delete`  
`Cmd + Delete`Delete the character to the left.`Backspace`  
`""`  
`Ctrl + H`Delete the character to the right.`Delete`  
`Ctrl + D`Undo the most recent text edit.`Ctrl + Z (no Shift)`Redo the most recent undone text edit.`Ctrl + Shift + Z`

ActionKeysClear the terminal screen and redraw the UI.`Ctrl + L`

ActionKeysScroll content up.`Shift + Up Arrow`Scroll content down.`Shift + Down Arrow`Scroll to the top.`Home`Scroll to the bottom.`End`Scroll up by one page.`Page Up`Scroll down by one page.`Page Down`

ActionKeysShow the previous entry in history.`Ctrl + P (no Shift)`Show the next entry in history.`Ctrl + N (no Shift)`Start reverse search through history.`Ctrl + R`Insert the selected reverse-search match.`Enter (no Ctrl)`Accept a suggestion while reverse searching.`Tab`

ActionKeysMove selection up in lists.`Up Arrow (no Shift)`Move selection down in lists.`Down Arrow (no Shift)`Move up within dialog options.`Up Arrow (no Shift)`  
`K (no Shift)`Move down within dialog options.`Down Arrow (no Shift)`  
`J (no Shift)`

#### Suggestions & Completions

[Section titled “Suggestions & Completions”](#suggestions--completions)

ActionKeysAccept the inline suggestion.`Tab`  
`Enter (no Ctrl)`Move to the previous completion option.`Up Arrow (no Shift)`  
`Ctrl + P (no Shift)`Move to the next completion option.`Down Arrow (no Shift)`  
`Ctrl + N (no Shift)`Expand an inline suggestion.`Right Arrow`Collapse an inline suggestion.`Left Arrow`

ActionKeysSubmit the current prompt.`Enter (no Ctrl, no Shift, no Cmd, not Paste)`Insert a newline without submitting.`Ctrl + Enter`  
`Cmd + Enter`  
`Paste + Enter`  
`Shift + Enter`  
`Ctrl + J`

ActionKeysOpen the current prompt in an external editor.`Ctrl + X`Paste from the clipboard.`Ctrl + V`  
`Cmd + V`

ActionKeysToggle detailed error information.`F12`Toggle the full TODO list.`Ctrl + T`Toggle IDE context details.`Ctrl + G`Toggle Markdown rendering.`Cmd + M`Toggle copy mode when the terminal is using the alternate buffer.`Ctrl + S`Toggle YOLO (auto-approval) mode for tool calls.`Ctrl + Y`Toggle Auto Edit (auto-accept edits) mode.`Shift + Tab`Expand a height-constrained response to show additional lines.`Ctrl + S`Toggle focus between the shell and Gemini input.`Tab (no Shift)`Toggle focus out of the interactive shell and into Gemini input.`Tab (no Shift)`  
`Shift + Tab`

ActionKeysCancel the current request or quit the CLI.`Ctrl + C`Exit the CLI when the input buffer is empty.`Ctrl + D`

## Additional context-specific shortcuts

[Section titled “Additional context-specific shortcuts”](#additional-context-specific-shortcuts)

- `Option+B/F/M` (macOS only): Are interpreted as `Cmd+B/F/M` even if your terminal isn’t configured to send Meta with Option.
- `!` on an empty prompt: Enter or exit shell mode.
- `\` (at end of a line) + `Enter`: Insert a newline without leaving single-line mode.
- `Esc` pressed twice quickly: Clear the current input buffer.
- `Up Arrow` / `Down Arrow`: When the cursor is at the top or bottom of a single-line input, navigate backward or forward through prompt history.
- `Number keys (1-9, multi-digit)` inside selection dialogs: Jump directly to the numbered radio option and confirm when the full number is entered.