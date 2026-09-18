---
layout: tutorial_hands_on
title: "Metagenomics Toolkit"
description: "toolkit description"
time_estimation: 1H
level: beginner
keywords: [metagenomics, genome assembly, OLC, de Bruijn graph, Velvet, MEGAHIT, metaSPAdes, IDBA-UD, Ray]
questions:
  - "What are the main challenges of reconstructing genomes from metagenomic sequencing data?"
  - "How do assembly algorithms differ?"
  - "How do k-mer size, sequencing errors, repeats, and uneven coverage influence assembly quality?"
  - "Which assembly strategies and tools are commonly used for complex metagenomic datasets?"
objectives:
  - "Recognize common sources of assembly ambiguity, such as repeats, sequencing errors, and uneven species abundance."
  - "Run multiple metagenome assemblers on sequencing reads and generate assembly statistics."
key_points:
  - "No single assembler performs best for all datasets; tool selection depends on dataset complexity, accuracy requirements, and available computational resources."
version:
  - main
life_cycle: under development
contributions:
  authorship:
  - Nils Kleinbölting
  - Alexander Sczyrba
  - Sebastian Jünemann
  editing: 
  - Dilfuza Djamalova
  funding:
---

><details-title>Prerequisites</details-title>
> - Please complete the [Unix/Linux introduction tutorial]({{ site.url }}{{ site.baseurl }}/tutorials/unix-course/main/tutorial/) before this tutorial. 
> - We assume you have successfully connected to an instance in the de.NBI cloud with the software pre-installed. Otherwise you will need to install the required tools on your own and make sure you have sufficient resources available. 
{: .details}
