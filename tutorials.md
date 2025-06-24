---
layout: base
title: Collection of Tutorials
description: List of de.KCD/de.NBI Cloud training materials
permalink: /tutorials/
---

<table>
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
    {% assign tutorials = site.tutorials | where: "layout", "tutorial_hands_on" %}
    {% assign tutorials_grouped = tutorials | group_by: "title" %}
    {% for group in tutorials_grouped %}
      {% assign first = group.items[0] %}
      <tr>
        <td>{{ group.name }}</td>
        <td>
          {% assign sorted_versions = group.items | sort: "version" %}
          {% for version in sorted_versions %}
            <a href="{{ version.url }}">{{ version.version }}</a>{% unless forloop.last %}, {% endunless %}
          {% endfor %}
        </td>
        <td>
          {% assign sorted_versions = group.items | sort: "version" %}
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
    {% endfor %}
  </tbody>
</table>

