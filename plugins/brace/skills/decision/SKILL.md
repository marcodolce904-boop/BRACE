---
name: decision
description: "Records a decision in the decision log (.brace/decisions.md) with rejected alternatives, rationale, verifiable prediction, confidence and review date. Use it when the user asks to record or note a choice, or has just made an important decision and agrees to record it: 'I've decided to...', 'note this down', 'let's go with X', 'log this decision', 'ho deciso di...', 'segnati questa scelta'. Keyword: DECISION."
argument-hint: "[decision]"
---

# Record a decision

Decision: $ARGUMENTS

The log exists to compare, later on, what the user expected with what actually happened. It only works if the prediction is verifiable, so the quality of the "Prediction" item is the most important part.

## Where you are running

Check what you can do here, not which product you are in.

- **Can you delegate to a sub-agent?** Not needed: this skill always runs in this conversation.
- **Can you read and write a persistent project folder?** That means a file tool on the user's project folder, where files stay after this conversation ends, as in Claude Code or Cowork; a sandbox that is wiped at the end of the chat does not count. If yes, save as in "Saving". Read from `.brace/`, or from `.vanta/` if `.brace/` does not exist; a file named `brace-decisions.md` counts as `decisions.md`. Before the first write, if `.vanta/` exists and `.brace/` does not, rename `.vanta/` to `.brace/` and tell the user in one line: "I renamed `.vanta/` to `.brace/`." If there is no persistent folder, follow "Memory in chat" and say so in one line: "There is no project folder here, so the log goes in the Project knowledge."
- **Was state injected at session start?** If decisions due for review were listed, you may remind the user of them after recording. If nothing was injected and there is no persistent folder, look for the log as described in "Memory in chat".

## Procedure

1. Extract the fields from the conversation. For the missing ones ask a single question that collects them all; do not invent rationales or alternatives the user has not expressed.
2. Make the prediction **verifiable**: what must be true, measurable, by what date. "It will go well" is not a prediction; "By 30 November at least 3 of the 10 clients contacted accept the quote" is. If the user's prediction is vague, propose a measurable version and ask for confirmation.
3. The **confidence** belongs to the user (High, Medium or Low), not to you. If you wish, give your own estimate separately, in the text of the reply.
4. The default **review date** is 30 days from today; use the date given by the user or the one when the outcome will be observable.
5. Assign an identifier `D-YYYYMMDD-NN`, where NN is the day's sequence number.

## Saving

Append the entry at the end of `.brace/decisions.md` in the current working folder (create the file and the folder if missing, with the title `# Decision log`). Keep exactly this format, because the plugin reads it to remind the user of overdue reviews:

```markdown
## D-20261004-01 · Short title
- Date: 2026-10-04
- Decision: …
- Rejected alternatives: …
- Rationale: …
- Prediction: …
- Confidence: Medium
- Review: 2026-11-03
- Status: open
- Outcome:
- Prediction correct:
- Lesson:
```

Without a persistent project folder, follow "Memory in chat" below.

Close with one confirmation line stating the identifier and the review date.

## Memory in chat

Use this section when there is no persistent project folder. The file format is the same as in `.brace/`, so the user can later move the file into a `.brace/` folder and Claude Code or Cowork will pick it up.

- **Reading.** Before assigning the identifier, look in the Project knowledge and in any uploaded file for `brace-decisions.md` (or `decisions.md`). Use it as the existing log, so the new entry goes at its end and the day's sequence number is right.
- **Writing.** Show the new entry, then the full updated file `brace-decisions.md` in a single code block: the existing log with the new entry appended, or, if there is none, a new log with the title `# Decision log`. Then give one line: "Add this file to the Project knowledge as `brace-decisions.md`, replacing the previous one if there is one." Always give the whole log, never a fragment, so the user replaces one file instead of merging.
- **Not in a Project.** If there is no Project knowledge to read from or add to, say once in this chat that the memory lasts only for this chat, and suggest creating a Project and adding the file to its knowledge. Still show the full file so the user can keep it.
