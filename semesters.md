---
title: By Semester
permalink: /semesters/
---

Semester-by-semester write-ups from my MSDS program. [Back to home](/).

<!-- vale off -->
{% assign semester_posts = site.posts | where_exp: "item", "item.semester_post" | sort: "semester" %}

<div class="post-list-sortable" data-sort-default="asc" data-sort-default-key="semester" data-sort-storage-key="/semesters/">
  {% include post-list-sort-controls.html mode=semester %}
  <ul class="post-list journey-list">
  {% for post in semester_posts %}
    {% include post-list-item.html post=post %}
  {% endfor %}
  </ul>
</div>
<!-- vale on -->
