# Publish on GitHub

Suggested repository name: **vibewise-openai**.

Suggested description: **Learn software design as ChatGPT and Codex help you build.**

Suggested topics: `chatgpt`, `codex`, `agent-skills`, `learning`, `software-design`.

The source includes an MIT `LICENSE`, upstream attribution, contribution guidelines,
issue and pull request templates, and CI for Python 3.10 and 3.14 on Linux and macOS.
The CI builds downloadable ZIP artifacts after validation. GitHub-hosted CI results
are only available after you push; local checks are documented in the README.

## Create the repository

Run these commands in your own terminal from the project folder. This preparation
session could not initialize `.git` because the workspace makes that path read-only.

```sh
cd /Users/faronbleed/Desktop/vibewise
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v
git init -b main
git add .
git status --short
git commit -m "Initial release: VibeWise for ChatGPT and Codex"
```

If Git requests a name or email, configure your own commit identity before committing.
The MIT license already exists; do not add a second generated license or remove
the original copyright notice.

Choose one publishing option:

### GitHub CLI

With GitHub CLI installed and authenticated:

```sh
gh auth login
gh repo create vibewise-openai --public --source=. --remote=origin --push
```

Use `--private` instead of `--public` if you want a private repository.
[GitHub CLI documents these repository creation options](https://cli.github.com/manual/gh_repo_create).

### GitHub website

Create an empty repository named `vibewise-openai` in your GitHub account. Leave
the automatic README, `.gitignore`, and license options unchecked because those
files are included here. Replace `YOUR_USERNAME` below with your account name:

```sh
git remote add origin https://github.com/YOUR_USERNAME/vibewise-openai.git
git push -u origin main
```

If `origin` already exists, inspect it with `git remote -v` before changing it.

## Downloads and the first release

Run `python3 scripts/build.py` to generate:

- `dist/vibewise-openai.zip`: installable local OpenAI plugin with its marketplace catalog.
- `dist/vibewise-chatgpt.zip`: ChatGPT instructions, setup guide, and handoff template.
- `dist/vibewise-github-source.zip`: clean source files, tests, documentation, and GitHub templates.

The source archive omits Git metadata, local learner notes, caches, environments,
and generated archives. Extract its contents before uploading source files; uploading
the ZIP itself doesn't make its contents a browsable GitHub repository.

After your first push and a passing CI run, create a GitHub release named `v1.0.0`
through the repository's Releases page and attach the OpenAI and ChatGPT ZIPs.
The version matches `plugin.json`. Publishing a release is a separate action;
this preparation does not create a remote repository or publish any files.
