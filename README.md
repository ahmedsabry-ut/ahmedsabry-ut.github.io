# ahmedsabry-ut.github.io

UT Austin Blog

## Python tooling setup

This repository uses `pre-commit` for text and Markdown quality checks.

### 1) Create and activate a virtual environment (Python 3.12)

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 2) Install pre-commit

```bash
python -m pip install --upgrade pip
pip install pre-commit
```

### 3) Install git hooks

```bash
pre-commit install
```

### 4) Run checks locally

```bash
pre-commit run --all-files
```

## Vale notes

- Vale is configured via `.vale.ini`.
- Running `pre-commit` does not require a separate Vale installation; the hook manages it.
- Install the standalone `vale` CLI only if you want to run `vale` directly outside `pre-commit`.

## CI

GitHub Actions runs `pre-commit run --all-files` on every `push` and `pull_request`.
