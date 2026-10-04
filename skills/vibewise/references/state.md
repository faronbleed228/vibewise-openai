# Learning state

Maintain three Markdown files selected by `scripts/state.py`. Preserve unrelated
notes and backups. Initialization never replaces existing files.

`profile.md`: keep exact lines `Learning mode: active` (or `paused`) and
`Onboarding: incomplete` (or `complete`) near the top. Record project situation,
experience, learning focus, frequency, question style, coding preference, remaining
onboarding, and a compact concept summary. Update entries instead of duplicating them.

`progress.md`: organize by topic. Separate concepts explained, reasoning demonstrated,
and topics to revisit. Pending decisions use a level-two heading
`## Pending decision: <topic>` with Stage, Proposal, Awaiting, and Scope. Stages:
awaiting reasoning, awaiting design confirmation, awaiting implementation authorization.
Search the whole file for pending sections. The restoration helper includes each one
even when it appears late in a long file. Resolve or replace pending entries after
the actual answer.

`project-map.md`: purpose, requirements, components with evidence paths, flows,
access boundaries, build commands, confirmed choices, actual implementation, unknowns.
Label observed, proposed, confirmed, and verified claims where ambiguity matters.
Confirmed design isn't implemented code.

Keep existing `.sensible-vibes/` state in place; don't merge or relocate it.
Each repository or worktree is a separate boundary. Without Git, new notes live
in the requested directory; don't search parent folders. Reject symlinked state
directories or managed files. Never load transcripts, secrets, or backups as active
context. Reset backs up exact note bytes and creates incomplete onboarding templates.
