---
title: Tags
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
    <ul>
      {% for post in site.posts %}
        {% if post.tags contains tag %}
        <li><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></li>
        {% endif %}
      {% endfor %}
    </ul>
  </li>
  {% endif %}
{% endfor %}
</ul>
<!-- vale on -->
