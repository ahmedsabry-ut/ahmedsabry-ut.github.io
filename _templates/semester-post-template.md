---
title: "Semester Title"
date: YYYY-MM-DD
layout: semester
semester_post: true
semester: 0
semester_start: YYYY-MM-DD
semester_end: YYYY-MM-DD
description: One casual line about the semester vibe — no course names or codes.
tags: [msds, semester-recap]
---

Set `semester`, `title`, `semester_start`, and `semester_end` from the semester schedule in the promote skill.
Set `date` to `semester_end` and use the same date in the filename: `_posts/YYYY-MM-DD-<slug>.md`.
Add optional `meme: /assets/images/memes/<file>` when the post has a meme (used for the semester card thumbnail and social preview; falls back to the grade report from `_data/semesters.yml`).
Add or update `credential_url` for each taken course in `_data/courses.yml` (omit the field when the credential is unavailable).

Write the semester story here.

## Transcript

{% include transcript-credentials.html %}
