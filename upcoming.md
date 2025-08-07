---
layout: base
title: "Upcoming Tutorials"
description: List of upcoming tutorials and learning pathways 
permalink: /upcoming/
---

<p>Here is a list of the training materials that will be available soon.</p>
<div class="pathway-grid">
  {% assign materials = site.upcoming %}
  {% for material in materials %}
    <div class="pathway-card">
      <p style="text-align:left;color:lightgrey;font-size:1em;">
        {{ material.type }}
      </p>
      <h3><a href="{{ material.url }}">{{ material.title }}</a></h3>
      <p>{{ material.description }}</p>
      {% if material.tags %}
        <div class="tags">
          {% for tag in material.tags %}
            <span>{{ tag }}</span>
          {% endfor %}
        </div>
      {% endif %}
    </div>
  {% endfor %}
</div>
