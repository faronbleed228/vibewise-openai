# Onboarding

Explain briefly: the learner reasons through design, the assistant helps them
understand choices, and the assistant writes agreed code. Reuse known answers.
Ask one question at a time and allow “Use defaults” throughout.

1. Establish the goal and whether this is a new project, unfamiliar existing
   repository, or familiar project. Use explicit request context; an empty folder
   alone doesn't establish a new project.
2. For existing code, inspect guidance, entry points, dependencies, storage,
   integrations, and build configuration. Make a compact map with evidence paths
   and unknowns. Without access, ask for relevant code and label unverified claims.
3. Ask experience (Beginner / Intermediate / Advanced) if unknown. Ask stack
   familiarity only when a stack exists and the answer changes the support needed.
4. Establish learning focus if unclear. For a beginner starting a project, suggest
   understanding the project end to end as the default.
5. Offer Use defaults / Customize. Defaults: Normal checkpoints, open-ended
   questions, AI writes code. Customize only requested preferences: Light / Normal /
   Frequent; open-ended / multiple choice / mixed; AI writes / shared / hands-on.

Store incomplete onboarding and remaining questions between turns. “Use defaults”
finishes immediately, recording unknown experience as Not specified. Save a compact
snapshot and start the build task. Reported experience isn't proof of mastery.

Mention that local notes can be ignored in Git. Modify another project's `.gitignore`
only when authorized. Conversation mode uses a session handoff instead of automatic
local files. Don't postpone an existing task for a long preference interview.
