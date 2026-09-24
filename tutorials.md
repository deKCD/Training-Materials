---
layout: base_tutorial
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
  <p style="font-weight:600;">{{ group.title }}</p>
  <p>{{ group.description }}</p>

  <table>
      <colgroup>
          <col style="width: 30%;">
          <col style="width: 7%;">
          <col style="width: 5%;">
          <col style="width: 40%;">
          <col style="width: 40%;">
          <col style="width: 7%;">
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
        {% assign group_items = site.tutorials | where: "layout", "tutorial_hands_on" | where_exp: "item", "item.path contains tutorial_id" %}
        {% assign sorted_versions = group_items | sort: "version" %}
        {% assign first = sorted_versions[0] %}
        {% if first %}
        <tr>
          <td>{{ first.title }}</td>
          <td>
            {% for version in sorted_versions %}
              <a href="{{ version.url | relative_url }}">{{ version.version }}</a>{% unless forloop.last %}<br>{% endunless %}    {% endfor %}
          </td>
          <td>
            <!-- Capture tutorial slides -->
            <!-- Possible files: Quarto markdown and PDF -->
            {% capture slide_links %}{% endcapture %}
            {% assign first_slide = true %}

            {% for v in sorted_versions %}
              {% assign base_dir = v.path | split: '/tutorial.md' | first %}

              {% assign quarto_slides_path = base_dir | append: '/slides.html' %}
              {% assign quarto_slides_url = v.url | replace: '/tutorial/', '/' | append: 'slides.html' %}

              {% assign pdf_slides_path = base_dir | append: '/slides.pdf' %}
              {% assign pdf_slides_url = v.url | replace: '/tutorial/', '/' | append: 'slides.pdf' %}

              {% assign has_quarto_slides = site.static_files | where: "path", quarto_slides_path | size %}
              {% assign has_pdf_slides = site.static_files | where: "path", pdf_slides_path | size %}

              {% if has_quarto_slides > 0 %}
                {% capture link %}
                  <a href="{{ quarto_slides_url | relative_url }}" target="_blank">{{ v.version }} (Quarto)</a>
                {% endcapture %}

                {% if first_slide %}
                  {% capture slide_links %}{{ link | strip }}{% endcapture %}
                  {% assign first_slide = false %}
                {% else %}
                  {% capture slide_links %}{{ slide_links }}, {{ link | strip }}{% endcapture %}
                {% endif %}
              {% endif %}

              {% if has_pdf_slides > 0 %}
                {% capture link %}
                  <a href="{{ pdf_slides_url | relative_url }}" target="_blank">{{ v.version }} (PDF)</a>
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
              {% assign author_data = site.data.contributors | where: "name", contributor | first %}
              {% assign author_url = author_data.ORCID %}
              {% if author_data and author_url == nil or author_url == "" %}
                {% assign author_url = author_data.Github %}
              {% endif %}

              <div>
                {% if author_data and author_url %}
                  <a href="{{ author_url }}" target="_blank">{{ contributor }}</a>
                {% elsif author_data %}
                  {{ contributor }}
                {% else %}
                  {{ contributor }}
                {% endif %}
              </div>
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
