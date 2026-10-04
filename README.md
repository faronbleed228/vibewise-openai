# VibeWise for ChatGPT and Codex

**MIT licensed · Python 3.10+ · No third-party dependencies**

Learn how your software works while AI helps you build it.

VibeWise invites your approach, helps you examine the consequences, implements an
agreed step, and explains the result. This is an independent OpenAI adaptation of
[Noah Kim's VibeWise](https://github.com/nykooi1/vibe-wise), with rewritten packaging
and helpers for ChatGPT and Codex.

## Start in ChatGPT

1. Open [chatgpt/instructions.md](chatgpt/instructions.md) and copy its full contents.
2. Paste it into a new ChatGPT conversation, or use it as a ChatGPT Project's instructions.
3. Describe your project and attach relevant code. Try: **“Help me build a notes app.
   I want to understand how it works. Use defaults.”**

For a custom GPT editor, where available, use the same instructions and
[conversation starters](chatgpt/conversation-starters.md). The instructions are
generated from the shared learning guides, so ChatGPT and Codex use the same workflow.

At the end, say **“Export my VibeWise session handoff.”** Save the response and supply
it in your next chat. [A handoff template](chatgpt/session-handoff.md) is included.
File edits, execution, and persistent local notes depend on the tools your current
ChatGPT surface provides; the instructions do not add tools.

## Start in Codex

Requires Python 3.10+ for local state helpers. No additional packages or API key.

From this repository, copy the skill into your user skill directory:

```sh
mkdir -p ~/.agents/skills
cp -R ./skills/vibewise ~/.agents/skills/vibewise
```

If that destination already exists, back it up before replacing it; do not nest a
new copy inside the old folder. For project-scoped use, copy to your project's
`.agents/skills/vibewise` instead. Keep the entire skill folder, including references
and scripts. Open Codex in the project you want to build and say:

```text
Use $vibewise to help me learn as I build this project. Use defaults.
```

Invoke `$vibewise` again at the start of future sessions to resume local notes.
Standalone skill installation does not install lifecycle hooks.

## Install as an OpenAI plugin

`plugin.json` packages the skill and a read-only session restoration hook. Build
the packages from this repository:

```sh
python3 scripts/build.py
```

The generated **`dist/vibewise-openai.zip`** includes a local marketplace catalog.
Extract it to a folder, open that folder as a trusted local project in the ChatGPT desktop
app, restart the app, and install VibeWise from **VibeWise Local** in the Plugins
Directory where local plugins are supported. Review and trust the hook definition
in your runtime if you want automatic restoration.

The ZIP is a local package, not a publicly published plugin. A web-only installation
doesn't deploy local scripts. Use the ChatGPT instructions directly when local
plugins aren't available. See [compatibility and official references](docs/compatibility.md).

## How learning works

| Checkpoint | What it does |
| --- | --- |
| Build | You explain your approach; VibeWise asks about meaningful gaps. |
| Design | Confirm a design and continue planning. |
| Implementation | Agree to a concrete coding step and its checks. |

When you're ready to code, one Implementation checkpoint can confirm both design
and scope. Afterward, VibeWise explains the change and actual verification results.
Existing explicit implementation authorization is respected.

Beginners get smaller questions and concept explanations. Experienced developers
explore constraints and tradeoffs. Checkpoint frequency is independent of experience.
Change preferences in plain language:

- “Use fewer checkpoints.”
- “Focus on backend architecture.”
- “Use multiple-choice questions.”
- “Just implement this step.”
- “Pause learning.” / “Resume learning.”
- “Reset my learning for this project.”

## Local notes and backups

Local mode stores `profile.md`, `progress.md`, and `project-map.md` in `.vibe-wise/`.
Existing `.sensible-vibes/` notes are supported in place. Lookup stays inside the
nearest Git repository/worktree; without Git, it stays in the current directory.
Add the notes directory to your project's `.gitignore` if you want it private.
VibeWise does not silently edit other projects' ignore files.

Use the helper directly if needed, replacing the sample path with your actual project:

```sh
python3 skills/vibewise/scripts/state.py status --cwd /path/to/project
python3 skills/vibewise/scripts/state.py init --cwd /path/to/project
python3 skills/vibewise/scripts/state.py pause --cwd /path/to/project
python3 skills/vibewise/scripts/state.py resume --cwd /path/to/project
python3 skills/vibewise/scripts/state.py export --cwd /path/to/project
python3 skills/vibewise/scripts/state.py reset --cwd /path/to/project
```

Reset without `--confirm` previews the target and returns a content-bound token.
After reviewing it, repeat with `--confirm TOKEN`. Changed notes invalidate the
token. Original bytes are saved in `backups/` before fresh onboarding templates
replace the three managed files. Unrelated files and source code are preserved.

No telemetry, hosted account, or external state service. Notes included in a model
conversation follow your normal ChatGPT/Codex data settings; don't save secrets.

## Develop and verify

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build.py
python3 scripts/build.py --check
```

The build writes an OpenAI plugin ZIP, a ChatGPT-only ZIP, and a clean GitHub source
ZIP to `dist/`. Generated archives are excluded from Git; download CI artifacts
from successful GitHub Actions runs or attach packages to a GitHub release.
It also updates `chatgpt/instructions.md` from shared guides. CI checks state isolation,
safe resets, hook output, generated instructions, and bundle contents. Behavioral
model checks are listed in [docs/behavior-checks.md](docs/behavior-checks.md).

## Contributing and publishing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development and pull requests,
[CHANGELOG.md](CHANGELOG.md) for release history, and
[the GitHub publishing guide](docs/github.md) to create your repository.

## License

Released under the [MIT License](LICENSE). You can use, modify, and distribute
this project, including commercially, while retaining the license and copyright
notice. Original project attribution is preserved in [NOTICE.md](NOTICE.md).
