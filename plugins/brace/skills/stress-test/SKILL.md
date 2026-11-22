---
name: stress-test
description: "Pre-mortem of a plan, a thesis or a decision: assumes it has already failed and reconstructs the causes, with early warning signals and countermeasures. Use it when the user wants to know how a plan could fail or asks to find its weak spots: 'how could this go wrong?', 'poke holes in this', 'what am I missing?', 'what could kill this?', 'come potrebbe andare storto?', 'trova i punti deboli'. Not for code review or debugging. Keywords: STRESS TEST, pre-mortem."
argument-hint: "[plan, thesis or file] [independent]"
---

# Stress Test (pre-mortem)

Object to test: $ARGUMENTS

If the object is not clear from the arguments or the conversation, ask in one sentence which plan or thesis to test and stop.

## Where you are running

Check what you can do here, not which product you are in.

- **Can you delegate to a sub-agent?** If yes, the independent mode delegates to the `nemesis` agent as described below. If not and the independent mode is requested or agreed, run its procedure yourself, in this conversation, judging only the plan text, the success criterion and the stated constraints, and say in one line: "Here the critique is less independent: in Cowork or Claude Code a separate agent would run it." The standard mode needs no sub-agent.
- **Can you read and write a persistent project folder?** That means a file tool on the user's project folder, where files stay after this conversation ends, as in Claude Code or Cowork; a sandbox that is wiped at the end of the chat does not count. This skill writes no state. If a Position Fix exists in `.brace/` (or the older `.vanta/`), use it as context for the plan.
- **Was state injected at session start?** If a Position Fix was loaded, use it as context and check with the user that it is still valid. If not, and there is no persistent folder, look in the Project knowledge and in uploaded files for `brace-position-fix.md`.

## Modes

- **Standard (default).** Run the pre-mortem yourself, in this conversation. Low cost. Limitation: the critique comes from the same context that produced the plan, so it tends to miss the same blind spots.
- **Independent.** If the arguments contain `independent` (or the user asks for an external critic), delegate to the `nemesis` agent. Pass it only the text of the plan, the success criterion and the constraints stated by the user; do not pass it your reasoning or your opinions on the plan, or it loses its independence. Then report its critique and add, separately, your comment on what you agree with and what you don't. Higher cost: warn the user in one line; if the independent mode was not explicitly requested, wait for a yes before starting.

## Procedure

1. **Restate** the plan in one sentence and the measurable success criterion. If there is no criterion, flag it: that is already a first risk.
2. **Assume failure.** "12 months (or the relevant horizon) have passed and the plan has failed." Generate causes in four categories: execution, market and adversaries, resources, wrong assumptions. Use the checklist in `${CLAUDE_PLUGIN_ROOT}/skills/stress-test/references/biases.md` to look for wrong assumptions.
3. **Rank** the causes by probability × impact and keep the top five.
4. For each, give the **early signal** (what you would see soon if it were happening) and the **countermeasure** (what to do now or when the signal appears).
5. **Close** with the change to the plan that most reduces overall risk and with the worst bearable case: if the plan fails, how much is lost and can it be recovered?

## Format

```markdown
**Plan:** …  ·  **Success criterion:** …

| # | Cause of failure | Prob. | Impact | Early signal | Countermeasure |
|---|---|---|---|---|---|

**Recommended change:** …
**Worst case:** …
**Confidence:** High/Medium/Low — what would change it.
```

Probability and impact are expressed as High/Medium/Low, not as invented percentages. If the plan is solid on a point, say so: a cause of failure made up to fill the table is an error.
