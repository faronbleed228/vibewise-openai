# OpenAI compatibility

Documentation reviewed October 4, 2026. Product capabilities and workspace policies
vary. This repository supplies reusable instructions and local scripts; it does
not grant file tools, account features, or marketplace approval.

| Surface | Setup | State |
| --- | --- | --- |
| ChatGPT conversation | Paste `chatgpt/instructions.md`, then describe the project. | Conversation plus a handoff you save and supply later. |
| ChatGPT Project | Put the instructions in project instructions; attach relevant source and the latest handoff. | Shared project sources, with explicit handoffs for learning continuity. |
| Custom GPT, where supported | Use the instructions and conversation starters in its editor. | Supply the latest handoff; don't rely on implicit learning memory. |
| ChatGPT desktop / Work with local plugin support | Install the generated plugin from its local marketplace and select VibeWise. | Local notes when file tools are available; conversation state otherwise. |
| Codex CLI / IDE | Copy `skills/vibewise` to a supported local skill directory and invoke `$vibewise`. | Markdown notes in the user's project. |

The portable `plugin.json` discovers workflows under `skills/`. Its OpenAI extension
points to a SessionStart hook using `${PLUGIN_ROOT}`. Supported local runtimes can
restore active/paused status and pending decisions after startup, resume, clear,
or compaction. Hooks require the runtime's trust review and are not automatically
deployed by a web installation. Without hooks, explicitly invoke VibeWise at the
start of a session. Coaching checkpoints are instruction behavior, not a tool-level
authorization enforcement system.

No API calls, API keys, third-party Python packages, web server, or external database
are required by this package. Your normal ChatGPT/Codex account and data settings
still apply. No particular model or paid plan is hard-coded.

Official references:

- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Projects and chats](https://learn.chatgpt.com/docs/projects)
- [Package plugins and local marketplaces](https://developers.openai.com/plugins/build/plugins)
- [Hooks](https://learn.chatgpt.com/docs/hooks)

This rewrite was informed by the upstream README and its learn/reset instructions,
learning behavior, onboarding, state templates, hook configuration, and license
retrieved through GitHub's web/raw pages. The shell's network access could not clone
the repository. No upstream tests or full Git history were imported; validation is
for this rewritten implementation.
