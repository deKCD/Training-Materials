---
layout: page
title: "Learning Pathways"
description: List of structured learning pathways 
---

{% assign pathways_science = site.pages | where: "layout", "pathway" | where: "type", "use" | sort: "priority", "last" %}

{% assign pathways_other = site.pages | where: "layout", "pathway" | where_exp: "item", "item.type != 'use'" | sort: "priority", "last" %}

Learning pathways are sets of tutorials curated for you by community experts to form a coherent set of lessons around a topic, building up knowledge as you go. We always recommend to follow the tutorials in the order they are listed in the pathway.

<!-- list all available pathways as cards  -->
<div class="pathwaylist row">

{% include pathway-card.html %}

</div>