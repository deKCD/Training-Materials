---
layout: base_paths
permalink: /pathways/
---

<div class="justify-text">

<p>Learning pathways are sets of tutorials curated for you by community experts to form a coherent set of lessons around a topic, building up knowledge as you go.</p>
    
<p>We always recommend following the tutorials in the order they are listed in the pathway.</p>

</div>

<div class="pathway-grid">
  {% assign pathways = site.pathways %}
  {% for pathway in pathways %}
    {% assign life_cycle = pathway.life_cycle | default: "under development" %}
    <div class="pathway-card" pathway-{{ life_cycle }}>
      <div class="pathway-status">
        {% if life_cycle == "under development" %} 
          <span class="status-dots status-development" aria-label="under development">
            <i></i><i></i><i></i>
          </span>
        {% else %} 
          <span class="status-dots status-active" aria-label="active">
            <i></i><i></i><i></i>
          </span>
        {% endif %}
      </div>

      <h3>
        <a href="{{ pathway.url | relative_url }}">
          {{ pathway.title }}
        </a>
      </h3>

      <p class="pathway-description">
        {{ pathway.description }}
      </p>

      {% if pathway.keywords %}
        <div class="tags">
          {% for keyword in pathway.keywords %}
            <span>{{ keyword }}</span>
          {% endfor %}
        </div>
      {% endif %}

    </div>
  {% endfor %}
</div>