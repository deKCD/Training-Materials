---
layout: pathway
title: "ONT Sequencing: From Reads to Annotation"
description: "This learning path introduces the complete workflow for analyzing isolate genome sequencing data generated with Oxford Nanopore Technologies (ONT) and Illumina platforms. Starting from raw ONT signal data, you will learn how to perform basecalling, quality control, genome assembly, polishing, hybrid assembly, genome annotation, and downstream analysis of long-read metagenomic data."
keywords: [ONT, Nanopore, Basecalling, dorado, flye, SPAdes, QUAST, polypolish, hybrid assembly, binning, prokka, bakta, EDGAR]
level: intermediate
life_cycle: under development

pathway:
  - section: "Module 1: Introduction to basic Unix commands"
    description: "This module introduces essential Unix shell commands and concepts required for working in computational environments. You will learn how to navigate file systems, manipulate files, and execute basic commands commonly used in bioinformatics workflows."
    tutorials:
      - name: unix-course
        version: main

  - section: "Module 2: Basecalling ONT data"
    description: "This module introduces the preprocessing workflow for Oxford Nanopore Technologies (ONT) sequencing data, starting from raw signal files. You will learn how to perform basecalling, assess read quality, and prepare high-quality sequencing reads for downstream genome analysis."
    tutorials:
      - name: nanopore
        version: main

  - section: "Module 3: Metagenomics assembly"
    description: "This module introduces genome assembly approaches for long-read and short-read sequencing data. You will learn how to assemble prokaryotic genomes from ONT and Illumina reads, evaluate assembly quality, improve assemblies through polishing and hybrid assembly strategies, and assess the final assembly results. The module also provides an introduction to metagenome assembly workflows using dedicated bioinformatics tools."
    tutorials:
      - name: mgworkshop_assembly
        version: main

      - name: genome-assembly
        version: main

  - section: "Module 4: Genome annotation"
    description: "This module covers the functional annotation of bacterial genomes. You will learn how to identify genomic features, predict genes, assign functional information, and interpret genome annotations using commonly used annotation tools."
    tutorials:
      - name: genome-annotation
        version: main
        
  - section: "Module 5: Long-Read Metagenomics using the Metagenomics-Toolkit"
    description: "This module introduces long-read metagenomics analysis using the Metagenomics-Toolkit. You will learn how to prepare ONT sequencing data, run the initial analysis workflow, and explore the first steps of metagenomic data processing and interpretation."
    tutorials:
      - name: mgtk_short
        version: main

contributions:
  authorship:
  - Nils Kleinbölting
  editing:
  - Dilfuza Djamalova 
  funding:
---

