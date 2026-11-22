---
name: position-fix
description: "Snapshot of the work status (goal, constraints, variables, decisions, open questions, next action), saved to a file and reloaded in later sessions. Use it when the user writes POSITION FIX or STOP (or PUNTO NAVE), when they want to take stock of the situation or pause the work, or when a long conversation has changed direction several times: 'where are we?', 'sum up where we stand', 'let's pick this up tomorrow', 'facciamo il punto', 'riassumi dove siamo'. Keywords: POSITION FIX, PUNTO NAVE, STOP."
argument-hint: "[optional focus]"
---

# Position Fix

Produce a snapshot of the status of the work in this conversation. If the user has given a focus ($ARGUMENTS), limit the Position Fix to that topic.

## Where you are running

Check what you can do here, not which product you are in.

- **Can you delegate to a sub-agent?** Not needed: this skill always runs in this conversation.
- **Can you read and write a persistent project folder?** That means a file tool on the user's project folder, where files stay after this conversation ends, as in Claude Code or Cowork; a sandbox that is wiped at the end of the chat does not count. If yes, save as in "Saving". Read from `.brace/`, or from `.vanta/` if `.brace/` does not exist; a file named `brace-position-fix.md` counts as `position-fix.md`. Before the first write, if `.vanta/` exists and `.brace/` does not, rename `.vanta/` to `.brace/` and tell the user in one line: "I renamed `.vanta/` to `.brace/`." If there is no persistent folder, follow "Memory in chat", which gives the one-line notice.
- **Was state injected at session start?** If a Position Fix was loaded, follow "Resuming". If not, and there is no persistent folder, look for it as described in "Memory in chat".

## Format

Use exactly these items, in this order. Each item is short and self-contained: it must be understandable by someone resuming the work in a new session without having read the conversation.

```markdown
# Position Fix · YYYY-MM-DD

- **Goal:** the real purpose, in one sentence.
- **Constraints:** fixed limits (time, budget, resources, rules).
- **Key variables:** name = current value (with unit), one per line if there are more than two.
- **Decisions made:** what was decided and why, in short.
- **Open questions:** what is still to be decided or verified.
- **Main risks:** at most three, with the signal that would make each visible.
- **Status:** where the work stands.
- **Next action:** exactly one concrete action, with who does it: one verb, no "and" or "then" chains. If several are needed, pick the first and move the others to Open questions.
```

Write "none" for empty items instead of inventing content. Distinguish what the user decided from what you proposed: a proposal of yours that was not accepted goes under "Open questions", not "Decisions made".

## Saving

When you have a persistent project folder:

1. If `.brace/position-fix.md` already exists in the current working folder, append its content to `.brace/position-fix-history.md` (create it if missing), so previous versions remain available.
2. Write the new Position Fix to `.brace/position-fix.md`, replacing the previous one.
3. Show the Position Fix in chat and state in one line where you saved it. At the start of the next sessions in this folder the plugin will reload it automatically.

When you have no persistent project folder, follow "Memory in chat" below.

## Resuming

If a previous Position Fix was loaded at the start of the session and the user resumes the work, use it as the starting point: check with them that it is still valid before building on it.

## Memory in chat

Use this section when there is no persistent project folder. The file format is the same as in `.brace/`, so the user can later move the file into a `.brace/` folder and Claude Code or Cowork will pick it up.

- **Writing.** Show the Position Fix, then the full updated file `brace-position-fix.md` in a single code block. Then give exactly one notice line. If you found Project knowledge or a BRACE file: "Add this file to the Project knowledge as `brace-position-fix.md`, replacing the previous one if there is one." Otherwise use the line in "No Project knowledge found" below. Always give the whole file, never a fragment, so the user replaces one file instead of merging.
- **Reading.** At the start of relevant work, look in the Project knowledge and in any uploaded file for `brace-position-fix.md` (or `position-fix.md`). If you find it, use it as in "Resuming": check with the user that it is still valid before building on it.
- **No Project knowledge found.** If you find no BRACE files and no Project knowledge, do not assert that this chat is outside a Project: an empty Project looks the same. Give this line instead of the Project-knowledge line above, once in this chat: "This memory lasts only for this chat unless you add this file to a Project's knowledge as `brace-position-fix.md` (create a Project if you have none)." Still show the full file so the user can keep it.
