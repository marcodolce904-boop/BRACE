# BRACE

**Bias · Risks · Assumptions · Confidence · Evidence**

[Italiano](README.it.md) · **English**

BRACE is a plugin for Claude that turns it into an analytical decision advisor: it checks premises, looks for the strongest objection, states its confidence, stress-tests plans and keeps track of what you decided so you can later compare it with what actually happened. It works in chat (claude.ai, desktop app), in Cowork and in Claude Code.

This repository is a plugin marketplace with two versions of the same plugin, with equivalent content:

| Version | Folder | Plugin id | Skills |
|---|---|---|---|
| English | [`plugins/brace`](plugins/brace) | `brace` | `method`, `position-fix`, `stress-test`, `wargame`, `decision`, `review` |
| Italiano | [`plugins/brace-it`](plugins/brace-it) | `brace-it` | `metodo`, `punto-nave`, `stress-test`, `wargame`, `decisione`, `revisione` |

Install **only one**: both have a startup hook and use the same `.brace/` folder, so installed together they would do the work twice.

> Status: version 0.2.0, experimental. The method follows Anthropic's current prompting recommendations and the research on personas, brevity and self-correction, but it has not yet been measured in the field. The [Checking that it works](#checking-that-it-works) section explains how to do that.

## Install in chat

For claude.ai and the Claude desktop app:

1. Open **Customize → Plugins**.
2. Add the marketplace from GitHub: `marcodolce904-boop/BRACE`
3. Install `brace` (English) or `brace-it` (Italian).

The steps can change: the current ones are in the official article [Manage plugins, skills and connectors from one Plugins page](https://support.claude.com/en/articles/17740565-manage-plugins-skills-and-connectors-from-one-plugins-page).

In chat, sub-agents and hooks do not run, so the independent critic and the wargame run inside the conversation (and say so), and memory lives in a Claude Project: see [Memory in chat](#memory-in-chat).

## Install in Claude Code

```
/plugin marketplace add marcodolce904-boop/BRACE
/plugin install brace@brace
```

For the Italian version, use `/plugin install brace-it@brace` as the second command. Remember: install only one.

To try it locally, or to check the structure before publishing:

```bash
claude --plugin-dir ./plugins/brace
claude plugin validate ./plugins/brace
```

## Just talk to it

You do not need commands. Describe what you need; the right skill starts, or is offered when it costs more. For example:

- "I'm not sure whether to accept this offer." (starts `method`)
- "How could this go wrong? Poke holes in this plan." (starts `stress-test`)
- "Let's go with the second option, note this down." (starts `decision`)
- "Where are we? Sum up where we stand." (starts `position-fix`)
- "How would competitors react if we cut our price?" (offers `wargame`, after a cost check)

Italian works in both plugins, whichever one you installed. Keywords still work as extra triggers: `BRACE`, `POSITION FIX` (or `PUNTO NAVE`, or `STOP`), `STRESS TEST`, `WARGAME`, `DECISION`, `REVIEW`. Slash commands are available too (`/brace:method`, `/brace:position-fix`, `/brace:stress-test`, `/brace:wargame`, `/brace:decision`, `/brace:review`).

Routine technical questions ("library X or Y?", "is this code OK?") get a normal answer: the method is for decisions, plans and choices that are hard to undo.

## What it contains

| Component | Purpose |
|---|---|
| `method` skill | Critical analysis with explicit priorities (accuracy > usefulness > form), reasoning checklist, High/Medium/Low confidence. It is the entry point and proposes the next tool when one adds value |
| `position-fix` skill | Snapshot of the work status, saved to `.brace/position-fix.md` |
| `stress-test` skill | Pre-mortem: five causes of failure with early signals and countermeasures; an independent mode with a separate critic |
| `wargame` skill | Red versus Blue simulation with a final synthesis; asks for a yes before the costly agent mode |
| `decision` skill | Decision log with a verifiable prediction and a review date |
| `review` skill | Compares predictions with outcomes, with calibration by confidence level |
| `nemesis` agent (Opus) | Independent critic with a clean context |
| `red` and `blue` agents (Sonnet) | Adversary and defender in the wargame |
| `BRACE` output style | The method's dry tone and priorities in every answer, opt-in: `/config` → Output style |
| Startup hook | Reloads the latest Position Fix and reminds you of decisions due for review |

## Three levels, one plugin

Each skill detects what the environment can do and uses the richest path available. When it falls back, it tells you in one line.

| | Chat (web, app) | Cowork | Claude Code |
|---|---|---|---|
| Method, stress test, decision, review | yes | yes | yes |
| Independent critic | in-conversation, stated | agent | agent |
| Wargame | quick, stated | agents | agents |
| Memory | Project knowledge | `.brace/` | `.brace/` |
| Automatic resume and due-review reminder | no | yes | yes |
| Output style, slash commands | slash only | slash only | both |

## Memory in chat

Chat has no project folder, so BRACE keeps its memory in a Claude Project:

1. Create a Project (or open an existing one) and work inside it.
2. When `position-fix`, `decision` or `review` produce something to keep, BRACE shows the result and then the **full updated file** in a single code block, with a one-line instruction.
3. Add that content to the Project knowledge, or replace the existing file, as `brace-position-fix.md` (Italian: `brace-punto-nave.md`) and `brace-decisions.md` (Italian: `brace-decisioni.md`). The file is always given in full, so you replace one file instead of merging fragments.
4. In later chats of the same Project, BRACE looks for those files, uses them, and confirms with you that the Position Fix is still valid. `review` reads the decision log from there and computes calibration by counting from the file.

Outside a Project, BRACE says once that memory lasts only for that chat and still shows the content, so you can keep it. The files use the same format as `.brace/`: you can move them into a folder later and Claude Code picks them up. Claude's own memory feature is not used, because its format cannot be controlled and calibration would become unreliable.

### Files created in the project (Claude Code, Cowork)

```
.brace/
├── position-fix.md          current status
├── position-fix-history.md  previous versions
└── decisions.md             decision log
```

If the log contains personal or confidential information, add `.brace/` to the project's `.gitignore`.

## Upgrading from V.A.N.T.A.

BRACE 0.2.0 is the new name of V.A.N.T.A. 0.1.0. The renames are breaking:

- Plugin ids: `vanta-en` is now `brace`, `vanta` is now `brace-it`; the marketplace is `brace`. Uninstall the old plugin and install the new one (`/plugin install brace@brace`), only one of the two.
- Commands: `/vanta-en:method` is now `/brace:method`, and likewise for the other skills; Italian `/vanta:metodo` is now `/brace-it:metodo`. Skill and agent names are unchanged.
- Output style: `V.A.N.T.A.` is now `BRACE` (`"outputStyle": "brace:BRACE"`).
- State folder: `.vanta/` is now `.brace/`. You do not need to move anything: BRACE reads `.vanta/` if `.brace/` does not exist, and the first time it writes state it renames `.vanta/` to `.brace/` and tells you in one line. If you added `.vanta/` to `.gitignore`, add `.brace/` too.
- The repository moved from `marcodolce904-boop/V.A.N.T.A.` to `marcodolce904-boop/BRACE`. GitHub redirects the old address, but re-add the marketplace with the new one: `/plugin marketplace remove vanta`, then the install lines above.

## Indicative costs

| Action | Cost compared with a normal answer |
|---|---|
| Method, Position Fix, decision, review | about 1x |
| Standard stress test | about 1x |
| Independent stress test | about 2-3x (one extra Opus call) |
| Quick wargame | about 1-2x |
| Wargame with agents | about 3-6x |

These are estimates to be checked in use: `/cost` in Claude Code shows the session's real usage. The independent stress test and the agent wargame always wait for your yes.

## Design choices

The plugin comes from a revision of a longer system prompt. What changed and why:

- **No decorative identity.** Personas in the prompt do not improve model accuracy (Zheng et al., 2024; Wharton Generative AI Labs, 2025). The operating rules remain.
- **Modules turned into checklists.** Names such as Sophia, Nemesis and Kairos became concrete check questions.
- **Brevity subordinate to accuracy.** Conciseness instructions increase wrong answers when the question contains a false premise (Giskard, Phare benchmark, 2025).
- **Confidence in levels, not percentages.** Percentages verbalised by models are systematically overconfident (Xiong et al., ICLR 2024).
- **Critique separate from the author.** Without an external signal, self-correction is unreliable (Huang et al., ICLR 2024): hence the clean-context `nemesis` agent.
- **Multi-agent only on request.** Multi-agent systems use far more tokens than a chat (Anthropic, *How we built our multi-agent research system*, 2025) and agent debate does not reliably beat simpler methods: so it is reserved for the wargame, where a genuine adversarial point of view is needed, and it waits for your yes.
- **Pre-mortem.** Gary Klein's technique rests on research into "prospective hindsight" (Mitchell, Russo and Pennington, 1989). The evidence concerns the number of causes identified more than their quality.

## Checking that it works

Each version contains 14 test cases in `evals/`: six on the method (false premise, forced objection, user under pressure, unknown data, insistence without arguments, Position Fix) and eight `route-*` cases that check natural-language routing (the right skill starts or is offered, a vague request enters `method`, a routine coding question does not). Run them with:

```bash
claude plugin eval ./plugins/brace
```

The command compares answers with and without the plugin and scores them with a judge model. Each case runs several times, so it uses credits: for a first pass use `--runs 1`, or pick a single case with `--case false-premise`.

The repository also has structural checks that need no credits and run in CI (`.github/workflows/ci.yml`):

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_plugin.py plugins/brace en
python3 scripts/check_plugin.py plugins/brace-it it
python3 scripts/check_parity.py
sh tests/test_hooks.sh
```

## Repository layout

```
.claude-plugin/marketplace.json   lists both versions
plugins/
├── brace/      English version
└── brace-it/   Italian version
scripts/        checkers (check_plugin.py, check_parity.py)
tests/          unit and hook tests
```

## License

MIT. See [LICENSE](LICENSE).
