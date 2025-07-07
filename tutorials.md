---
layout: base
title: Collection of Tutorials
description: List of de.KCD/de.NBI Cloud training materials
permalink: /tutorials/
---

<div class="justify-text">
<p>
    Explore our curated collection of training materials covering a wide range of topics in cloud computing, bioinformatics, and data science. 
    These tutorials are designed for hands-on learning and support both beginners and advanced users. 
</p>
<p>   
    Lesson materials are all available online, under a <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">CC BY license</a>, for self-directed study or for adaptation and re-use in your own training sessions.
</p>
</div>

{% assign groups = site.data.tutorial_groups %}

{% for group in groups %}
<section class="tutorial-group">
  <h2>{{ group.title }}</h2>
  <p>{{ group.description }}</p>

  <table>
      <colgroup>
          <col style="width: 40%;">
          <col style="width: 5%;">
          <col style="width: 5%;">
          <col style="width: 40%;">
          <col style="width: 10%;">
          <col style="width: 5%;">
      </colgroup>
    <thead>
      <tr>
        <th>Tutorial</th>
        <th>Versions</th>
        <th>Slides</th>
        <th>Description</th>
        <th>Contributors</th>
        <th>Estimated Time</th>
      </tr>
    </thead>
    <tbody>
      {% for tutorial_id in group.tutorials %}
        {% assign group_items = site.tutorials | where: "layout", "tutorial_hands_on" | where: "slug", tutorial_id %%}
        {% assign sorted_versions = group_items | sort: "version" %}
        {% assign first = sorted_versions[0] %}
        {% if first %}
        <tr>
          <td><strong>{{ first.title }}</strong></td>
          <td>
            {% for version in sorted_versions %}
              <a href="{{ version.url }}">{{ version.version }}</a>{% unless forloop.last %}, {% endunless %}
            {% endfor %}
          </td>
          <td>
            {% capture slide_links %}{% endcapture %}
            {% assign first_slide = true %}
            {% for v in sorted_versions %}
              {% if v.has_slides %}
                {% capture link %}
                  <a href="{{ v.slides_url }}">{{ v.version }}</a>
                {% endcapture %}
                {% if first_slide %}
                  {% capture slide_links %}{{ link | strip }}{% endcapture %}
                  {% assign first_slide = false %}
                {% else %}
                  {% capture slide_links %}{{ slide_links }}, {{ link | strip }}{% endcapture %}
                {% endif %}
              {% endif %}
            {% endfor %}
            {{ slide_links }}
          </td>
          <td>{{ first.description }}</td>
          <td>
            {% for contributor in first.contributions.authorship %}
              <a href="https://orcid.org/{{ contributor.orcid }}" target="_blank">{{ contributor }}</a>{% unless forloop.last %}, {% endunless %}
            {% endfor %}
          </td>
          <td>{{ first.time_estimation }}</td>
        </tr>
        {% endif %}
      {% endfor %}
    </tbody>
  </table>
</section>
{% endfor %}
