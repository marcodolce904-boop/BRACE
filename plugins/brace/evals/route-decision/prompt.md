---
max_turns: 6
allowed_tools: [Skill, Read, Write, Edit, Glob]
---

I've decided: we're going with the managed database instead of hosting Postgres ourselves. The alternatives were self-hosting on our own servers or a smaller provider with no SLA. Main reason is that nobody on the team wants to be on call for backups. I expect we'll spend less than 15 hours a month on database work by the end of the quarter. I'd like this written down so we can look back on it.
