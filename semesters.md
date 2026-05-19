---
title: Journey
permalink: /semesters/
---

Semester-by-semester write-ups from my MSDS program. [Back to home](/).

<!-- vale off -->
{% assign semester_posts = site.posts | where_exp: "item", "item.semester_post" | sort: "semester" %}

<ul class="post-list journey-list">
{% for post in semester_posts %}
  <li class="post-item semester-card">
    <p class="badge">Semester {{ post.semester }} · {% include semester-dates.html post=post %}</p>
    <h3>
      <a class="post-link" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
    </h3>
    {% if post.image %}
    <a href="{{ post.url | relative_url }}"><img class="semester-card-thumb" src="{{ post.image | relative_url }}" alt="" width="120" loading="lazy"></a>
    {% endif %}
    <div class="post-excerpt">{{ post.excerpt }}</div>
  </li>
{% endfor %}
</ul>
<!-- vale on -->
