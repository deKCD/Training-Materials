---
layout: base
title: "Learning Pathways"
description: List of structured learning pathways 
permalink: /pathways/
---

<p>Learning pathways are sets of tutorials curated for you by community experts to form a coherent set of lessons around a topic, building up knowledge as you go.</p>
    
<p>We always recommend following the tutorials in the order they are listed in the pathway.</p>

<div class="pathway-grid">
  {% assign pathways = site.pathways %}
  {% for pathway in pathways %}
    <div class="pathway-card">
      <h3><a href="{{ pathway.url }}">{{ pathway.title }}</a></h3>
      <p>{{ pathway.description }}</p>
      {% if pathway.tags %}
        <div class="tags">
            {% for tag in pathway.tags %}
            <span>{{ tag }}</span>
            {% endfor %}
        </div>
      {% endif %}
    </div>
  {% endfor %}
</div>
