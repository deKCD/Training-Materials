---
layout: base
title: Collection of Tutorials
description: List of de.KCD/de.NBI Cloud training materials
permalink: /tutorials/
---

<table>
  <thead>
    <tr>
      <th>Tutorial Title</th>
      <th>Description</th>
      <th>Contributors</th>
      <th>Estimated Time</th>
    </tr>
  </thead>
  <tbody>
    {% for tutorial in site.tutorials %}
      <tr>
        <td><a href="{{ tutorial.url }}">{{ tutorial.title }}</a></td>
          <td>{{ tutorial.description }}</td>
          <td>{{ tutorial.contributors | join: ", "}}</td>
          <td>{{ tutorial.time_estimation }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>