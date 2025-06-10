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
      <th>Description</th>
      <th>Contributors</th>
      <th>Estimated Time</th>
    </tr>
  </thead>
  <tbody>
    {% assign tutorials = site.tutorials | where: "layout", "hands_on_tutorial" %}
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
        <td>{{ first.description }}</td>
        <td>
            <ul>
                {% for contributor in first.contributors %}
                    {% if contributor.orcid %}
                    <a href="https://orcid.org/{{ contributor.orcid }}" target="_blank">{{ contributor.name }}</a>
                    {% else %}
                    {{ contributor.name }}
                    {% endif %}
                {% endfor %}
            </ul>
        </td>
        <td>{{ first.time_estimation }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
