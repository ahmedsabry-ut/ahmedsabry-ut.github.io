# ahmedsabry-ut.github.io

UT Austin Blog

## Site features

- **[Journey](/semesters/)** — semester-by-semester archive with prev/next navigation on each recap post.
- **Course schedule** — driven by [`_data/courses.yml`](_data/courses.yml); edit that file to update the table on the home page.
- **SEO** — `jekyll-seo-tag`, `jekyll-sitemap`, and optional per-post `image:` for social previews (grade report images).
- **Future posts** — `future: true` in `_config.yml` so dated drafts in `_posts/` build before their publish date.
- **Navigation** — breadcrumbs, reading time, optional TOC (`toc: true`), tags, related posts, and a [tags index](/tags/).
- **Plugins** — `jekyll-redirect-from`, `jekyll-include-cache`, `jekyll-relative-links`, `jekyll-gist`, `jekyll-avatar` (see `_config.yml`).

### Local preview (optional)

GitHub Pages builds the site on push. To preview locally, install the [github-pages gem](https://pages.github.com/versions/) and run `bundle exec jekyll serve` from the repository root.

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
