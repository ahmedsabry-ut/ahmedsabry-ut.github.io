---
title: By Tag
permalink: /tags/
---

Posts grouped by topic.

<!-- vale off -->
{% assign all_tags = site.posts | map: "tags" | flatten | uniq | sort %}
<ul class="tag-list">
{% for tag in all_tags %}
  {% if tag %}
  <li id="tag-{{ tag | slugify }}">
    <h2>{{ tag }}</h2>
    {% assign posts_by_date = site.posts | sort: 'date' | reverse %}
    <ul class="post-list tag-post-list">
    {% for post in posts_by_date %}
      {% if post.tags contains tag %}
      {% include post-list-item.html post=post %}
      {% endif %}
    {% endfor %}
    </ul>
  </li>
  {% endif %}
{% endfor %}
</ul>
<!-- vale on -->
