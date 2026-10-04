# Reset learning

Reset current learning notes, never source or Git history. Preference changes need
no reset. With shell access, run:

```sh
python3 /absolute/skill/path/scripts/state.py reset --cwd /absolute/project/path
```

This is a read-only preview. Show project, notes path, files, and backup location.
If no notes exist, stop. Unless the user already authorized this exact target and
scope, ask for Reset learning / Cancel and wait for an explicit answer. Explain
that target review prevents resetting another project's notes. Don't ask twice
when the existing request already authorizes this exact target and scope.

Use the same command with `--confirm` and the exact preview token. Quote actual
paths and tokens. Changed notes or target invalidate the preview; show a new preview
before acting. On failure, report the error and any backup path; don't improvise
deletion commands. On success, show backup path and use only post-reset onboarding
answers. Backups remain historical unless the user asks to recover them.

Without filesystem tools, summarize the session and reset effect. On an authorized
reset, offer the prior state as a handoff backup and begin fresh conversation state.
Say no local/uploaded file changed. Don't claim deletion of ChatGPT memory or history.
