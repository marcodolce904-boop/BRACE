---
name: review
description: "Reviews the decisions recorded in .brace/decisions.md whose review date has passed: collects the outcomes, compares predictions with reality and measures calibration by confidence level. Use it when the user wants to look back at past decisions or know how accurate their predictions were: 'how did my past decisions go?', 'was I right?', 'which decisions are due for review?', 'com'è andata con le decisioni?', 'avevo ragione?'. Keyword: REVIEW."
argument-hint: "[decision ID | all]"
---

# Decision review

Arguments: $ARGUMENTS

## Where you are running

Check what you can do here, not which product you are in.

- **Can you delegate to a sub-agent?** Not needed: this skill always runs in this conversation.
- **Can you read and write a persistent project folder?** That means a file tool on the user's project folder, where files stay after this conversation ends, as in Claude Code or Cowork; a sandbox that is wiped at the end of the chat does not count. If yes, follow the procedure on `.brace/decisions.md`. Read from `.brace/`, or from `.vanta/` if `.brace/` does not exist; a file named `brace-decisions.md` counts as `decisions.md`. Before the first write, if `.vanta/` exists and `.brace/` does not, rename `.vanta/` to `.brace/` and tell the user in one line: "I renamed `.vanta/` to `.brace/`." If there is no persistent folder, follow "Memory in chat" and say so in one line: "There is no project folder here, so I'll work on the log from the Project knowledge."
- **Was state injected at session start?** If decisions due for review were listed, start from those, still reading the log for the details. If nothing was injected and there is no persistent folder, look for the log as described in "Memory in chat".

## Procedure

1. Read `.brace/decisions.md` in the current working folder. If it does not exist, say so and suggest `/brace:decision`.
2. Select the decisions to review:
   - with an ID in the arguments, only that one;
   - with `all`, all those with `Status: open`;
   - with no arguments, those with `Status: open` and a review date on or before today.
3. For each, show decision, prediction and confidence, then ask the user for the outcome. Group the questions into a single message when there is more than one decision. Do not infer the outcome on their behalf.
4. With the answers, update each entry, changing only these fields:
   - `Outcome:` what happened, in one sentence;
   - `Prediction correct:` yes, no or partial, comparing the written prediction with the outcome, not with intentions;
   - `Lesson:` what would change in the next similar decision, only if the user shares it or it clearly emerges;
   - `Status:` closed. If the outcome is not yet observable, leave `open` and move `Review:` to the new agreed date.

## Calibration

After the update, compute over all closed decisions in the log the share of correct predictions for each confidence level (count "partial" as half a point). Do the count by reading the file, not from memory.

```markdown
| Confidence | Closed decisions | Correct predictions | Share |
|---|---|---|---|
| High | | | |
| Medium | | | |
| Low | | | |
```

Comment only on what the numbers allow you to say. With fewer than five decisions per level, state that the sample is too small for conclusions. The useful signal is the ordering: high-confidence decisions should turn out correct more often than low-confidence ones; if they don't, the user's confidence is not discriminating, and that is the most important lesson of the log.

## Memory in chat

Use this section when there is no persistent project folder. The file format is the same as in `.brace/`, so the user can later move the file into a `.brace/` folder and Claude Code or Cowork will pick it up.

- **Reading.** In step 1, look in the Project knowledge and in any uploaded file for `brace-decisions.md` (or `decisions.md`) and use it as the log. If you do not find it, say so, ask the user to upload it if they keep it elsewhere, and otherwise suggest recording a decision first.
- **Writing.** After updating the entries, show the full updated file `brace-decisions.md` in a single code block. Then give one line: "Replace `brace-decisions.md` in the Project knowledge with this file." Always give the whole log, never a fragment, so the user replaces one file instead of merging.
- **Not in a Project.** If there is no Project knowledge to read from or add to, say once in this chat that the memory lasts only for this chat, and suggest creating a Project and adding the file to its knowledge. Still show the full file so the user can keep it.
- **Calibration.** Count from the file, entry by entry, not from memory or from the conversation. If a code tool is available, run the count with code on the text of the updated file and build the table from its output.
