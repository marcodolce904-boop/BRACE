---
name: wargame
description: "Red versus Blue simulation on a plan or a decision: an adversary attacks the plan, a defender adapts it, then a synthesis identifies second-order consequences and the breaking point. Use it when the outcome depends on how others will react (competitors, the market, a counterpart) and the stakes are high, or when the user asks for an adversarial simulation: 'how would competitors react?', 'simulate the other side', 'what would they do if we cut prices?', 'come reagirebbe il mercato?', 'simula la controparte'. Keyword: WARGAME."
argument-hint: "[scenario] [quick]"
---

# Red / Blue Wargame

Scenario: $ARGUMENTS

## Cost check

Do this before anything else, with one exception: if Preparation needs a clarifying question, ask that question first and ask about cost once the scenario is clear.

- **Sub-agents available.** Unless the arguments contain `quick`, say in one line that the agent mode costs several normal answers, offer the quick mode, and wait for a yes. Example: "The agent wargame costs several normal answers; I can run a quick version here instead. Go with agents?" If the user picks quick or does not confirm, use the quick mode.
- **Sub-agents not available.** Go to the quick mode and say so in one line, adding that in Cowork or Claude Code each side would be a separate agent. Example: "Agents aren't available here, so I'll simulate both sides myself; in Cowork or Claude Code each side would be a separate agent."

## Where you are running

Check what you can do here, not which product you are in.

- **Can you delegate to a sub-agent?** If yes, the agent mode uses the `red` and `blue` agents, after the yes in the cost check. If not, the cost check above already sends you to the quick mode with its one-line notice, which must say that in Cowork or Claude Code each side would be a separate agent.
- **Can you read and write a persistent project folder?** That means a file tool on the user's project folder, where files stay after this conversation ends, as in Claude Code or Cowork; a sandbox that is wiped at the end of the chat does not count. This skill writes no state. If a Position Fix exists in `.brace/` (or the older `.vanta/`), use it as context for the BLUE plan.
- **Was state injected at session start?** If a Position Fix was loaded, use it as context and check with the user that it is still valid. If not, and there is no persistent folder, look in the Project knowledge and in uploaded files for `brace-position-fix.md`.

## Preparation

Before launching the agents, set down in a few lines:

- **BLUE plan:** what the user wants to do and with what measurable goal.
- **RED:** who or what reacts (competitor, customer, market, authority, physical reality) and what its incentives are.
- **Horizon:** the simulated period.

If one of these elements is missing and would change the result, ask a single question and stop. Otherwise state the assumptions and proceed.

## Modes

- **With agents (default).** RED and BLUE are separate agents, each with its own context. It costs several times a normal answer: start it only after the yes in the cost check.
- **Quick.** If the arguments contain `quick`, simulate both sides yourself, in this conversation, with the same format. Low cost, but the two sides share the same point of view.

## Procedure with agents

1. **RED turn.** Delegate to the `red` agent. Pass it the BLUE plan, RED's identity and incentives, the horizon. Ask for three moves.
2. **BLUE turn.** Delegate to the `blue` agent. Pass it the BLUE plan and RED's three moves, without your comment. Ask for a response to each move.
3. **Arbitration.** Write the final synthesis yourself, in the format below. You judge the moves, not the sides: if a RED move is implausible or a BLUE response is too optimistic, say so.

## Synthesis format

```markdown
**BLUE:** … · **RED:** … · **Horizon:** …

| RED move | Prob. | Damage to BLUE | BLUE response | Cost | Residual risk |
|---|---|---|---|---|---|

**Second-order consequences:** what happens after the first reactions.
**Breaking point:** the condition under which the plan no longer holds.
**Change that makes BLUE more robust:** …
**Assumptions:** list of what is speculative.
**Confidence:** High/Medium/Low — what would change it.
```

The wargame produces plausible scenarios, not forecasts: label as an assumption anything not grounded in data. If the simulation leads to a choice worth recording, close by offering to record the decision.
