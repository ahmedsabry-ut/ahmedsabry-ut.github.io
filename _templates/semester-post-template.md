---
title: "Semester Title"
date: YYYY-MM-DD
semester: 0
description: One casual line about the semester vibe — no course names or codes.
tags: [msds, semester-recap]
---

Set `semester` from the schedule in the promote skill (term dates live in `_data/semesters.yml`).
Set `date` to that semester's `semester_end` and use the same date in the filename: `_posts/YYYY-MM-DD-<slug>.md`.
Add optional `meme: /assets/images/memes/<file>` when the post has a meme (used for the semester card thumbnail and social preview; falls back to the grade report from `_data/semesters.yml`).
Add or update `credential_url` for each taken course in `_data/courses.yml` (omit the field when the credential is unavailable).

Write the semester story here.

## Transcript

{% include transcript-credentials.html %}
