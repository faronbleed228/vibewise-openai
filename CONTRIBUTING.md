# Contributing

VibeWise supports learning while building in ChatGPT and Codex. Keep changes focused
on that workflow and retain the distinction between design agreement, implementation,
and verified results.

## Local setup

Use Python 3.10 or newer. All runtime and test code uses the standard library, so
there is no dependency installation step.

```sh
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v
```

The canonical coaching guides live in `skills/vibewise/references/`.
`chatgpt/instructions.md` is generated from those guides and `scripts/build.py`;
edit the sources, then run the build and commit the updated instructions.

```sh
python3 scripts/build.py
```

Generated ZIPs in `dist/`, Python caches, local environments, and learner notes
are excluded from Git. Do not commit private handoffs or credentials.

## Changes and pull requests

Describe the problem, observable behavior, and checks you actually ran. Add a
focused regression test for changed state or packaging behavior. For coaching
changes, use `docs/behavior-checks.md` and distinguish manual model checks from
automated Python tests. Documentation-only edits normally need a build check.

State helpers must preserve project boundaries, existing notes, and original
backups. Avoid external dependencies unless the capability clearly needs them.

Contributions are made under this repository's MIT license. Preserve existing
copyright and attribution notices. No separate contributor agreement is required.
