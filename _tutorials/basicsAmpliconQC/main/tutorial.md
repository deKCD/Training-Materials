---
layout: tutorial_hands_on
title: Basics of Amplicon Quality Processing
description: Basic steps to do manually quality processing of 16S data step by step with individual tools instead of using integrated solutions like qiime2 / dada2 / deblur.
time_estimation: 2H
level: beginner
keywords: ["16S", "QC", "FastQC"]
questions:
  - What is quality processing and why it is important?
  - What are the neccessary steps to do quality processing on 16S amplicon data?
objectives:
  - You will be able to distinguish between different types of errors and bias in amplicon data.
  - You will apply different tools to address the different error types on the data.
  - You will compare the effect of quality processing with unporcessed data.
key_points:
  - "**Know your data:** library prep, expected fragment/read length, possible adapters/primers."
  - Consider the sequencer (Illumina vs. Ion Torrent, etc.).
  - Carefully inspect results at each step.
  - Try different strategies (conservative vs. loose parameters).
  - Adapt the QC workflow to your research question (16S vs. read-based shotgun, etc.).
  - This is only one workflow; consider other tools or workflow order. Always examine your raw data!
version: 
  - main
life_cycle: under development
contributions:
  authorship:
  - Sebastian Jünemann
  editing: 
  funding: 
---

{% include _tutorials/basicsAmpliconQC/main/Part0_data.md %}
{% include _tutorials/basicsAmpliconQC/main/Part1_fastq.md %}
{% include _tutorials/basicsAmpliconQC/main/Part2_fastqc.md %}
{% include _tutorials/basicsAmpliconQC/main/part3_preprocess.md %}


