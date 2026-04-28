---
name: promote-semester-post-draft
description: Derives Jekyll title, date, and `_posts/YYYY-MM-DD-slug.md` from a semester draft, validates structure, shows a preview of planned git/PR actions, then—only after explicit human approval—creates a branch, commits, pushes, and opens the PR. Use when finalizing semester drafts or asking to publish, branch, commit, push, or open a PR for a new semester post.
---

# Promote semester post draft

## When this applies

The user has a **working copy** of the semester template (for example `_posts/semester-post-template.md`) with real narrative in the body but placeholder front matter (`title: "Semester Title"`, `date: YYYY-MM-DD`). Turn it into a real Jekyll post: correct **title**, **date**, and **filename**.

Canonical empty template: `_templates/semester-post-template.md`.

## Steps

1. **Read the draft** (path from the user, or default `_posts/semester-post-template.md`). Parse YAML front matter and body.

2. **Infer title from context** — use the body (and any headings), not the placeholder:
   - Prefer a short, specific title matching the tone of existing posts (see `_posts/*.md` for examples such as `First Semester`).
   - Reflect the semester story: milestone, course focus, or narrative hook (e.g. final courses, a named semester theme).
   - Set `title:` in front matter to that string (quoted if needed for YAML).

3. **Set the post date** — use **today’s calendar date** in `YYYY-MM-DD` form:
   - When working in Cursor, prefer the **Today's date** value from user/session context if provided.
   - Otherwise use the system date (e.g. `date +%Y-%m-%d` in the repository).

4. **Choose the filename** — Jekyll convention: `_posts/YYYY-MM-DD-<slug>.md`
   - Use the **same** `YYYY-MM-DD` as front matter `date:`.
   - **Slug**: lowercase ASCII, words separated by hyphens, no spaces or punctuation noise; keep it readable and specific to this post (compare `_posts/2025-08-25-first-semester.md`).
   - Avoid generic slugs like `semester-post` when the content implies something more specific.

5. **Apply edits**
   - Update front matter: `title`, `date`; keep `enforce_structure: true` unless the user explicitly opts out (expect `## Certificates` and `## Transcript` in the body when structure is enforced).
   - **Rename** the file from the draft name to `_posts/YYYY-MM-DD-<slug>.md` (move/rename in the filesystem or editor; do not leave two copies unless the user asks).

6. **Validate**
   - Run **pre-commit** using the project **virtual environment** (this repository uses `.venv`; see `README.md`). From the repository root: `source .venv/bin/activate` then `pre-commit run --all-files`, or invoke `.venv/bin/pre-commit run --all-files` without activating. Fix any failures before continuing.

7. **Preview and human gate** (required before git)
   - **Do not** create a branch, commit, push, or open a PR until the human approves.
   - Present a clear **preview** of what will happen next, including:
     - Final `title` and `date`, and resolved path `_posts/YYYY-MM-DD-<slug>.md` (plus source path removed if renaming from a draft file).
     - Planned **branch name** (e.g. `post/<slug>` or `posts/<YYYY-MM-DD>-<slug>`).
     - Planned **commit message** (exact or near-final text).
     - Planned **PR title** and **PR body** (draft text they can skim).
     - Brief **git commands** overview (checkout base branch, branch name, push, `gh pr create`) so nothing is ambiguous.
   - **Stop** and wait for explicit approval (e.g. “yes”, “go ahead”, “looks good”, “approve”). Adjust the plan if they request changes—then show an updated preview if the plan materially changes before running git.
   - **Only after** that approval: proceed to **Git: branch, commit, push, PR** below.

## Git: branch, commit, push, PR

Run this **only** after the preview (step 7) has been approved—post file finalized, pre-commit (via `.venv`) passing, human go-ahead given.

1. **Working tree** — If there are unrelated local changes, either stop and tell the user, or commit **only** the new/renamed post (never bundle unrelated edits without explicit approval).

2. **Branch** — From up-to-date `main` (this repository’s default):
   - `git fetch origin` and `git checkout main` then `git pull origin main` when safe; otherwise branch from the user’s current base if they are mid-workflow.
   - Create a descriptive branch, e.g. `post/<slug>` or `posts/<YYYY-MM-DD>-<slug>` (lowercase, hyphens; align with the post slug).

3. **Commit** — Stage **only** post changes under `_posts/`: if the draft was renamed, include both the deleted draft path and the new `_posts/YYYY-MM-DD-slug.md` (e.g. `git add -u _posts/semester-post-template.md` and `git add _posts/YYYY-MM-DD-slug.md`, or equivalent so Git can detect a rename). Use a **clear, human commit message** (imperative mood, what changed). Follow repository rules: no boilerplate AI attribution in commit messages.

4. **Push** — `git push -u origin <branch-name>`.

5. **Open a PR** — Prefer GitHub CLI when available:
   - `gh pr create --base main --title "..." --body "..."`
   - **Title**: concise and specific (e.g. mirror or shorten the post `title:`), not generic (“Update post”).
   - **Body**: 2–4 short paragraphs or bullets: what semester/milestone the post covers, notable courses or themes from the draft, any placeholders still in the post (e.g. certificate images TBD), and how `enforce_structure` / section requirements were satisfied. No filler and no tool attribution (see `.cursor/rules/no-ai-attribution-boilerplate.mdc`).
   - If `gh` is missing or unauthenticated, give exact commands and tell the user to open the PR from the pushed branch on GitHub, pasting the same title and body.

## Edge cases

- If the body is still mostly placeholders (`## Context` only, or template bullets unchanged), summarize what is missing and ask whether to proceed or wait for more content — still set date/title/slug if the user wants a stub file.
- If the user wants a **historical** post date (not today), follow their explicit date for both front matter and filename prefix.

## Quick checklist

- [ ] `title` reflects body context, not `"Semester Title"`.
- [ ] `date` is today (or user-specified) and matches the filename date prefix.
- [ ] File lives at `_posts/YYYY-MM-DD-<slug>.md` with matching slug.
- [ ] Pre-commit run via `.venv` and passing (with `enforce_structure: true` as applicable).
- [ ] Preview shown; explicit human approval received before any branch/commit/push/PR.
- [ ] Branch created from `main`, only the post (re)named file committed, pushed, PR opened with substantive title and description.
