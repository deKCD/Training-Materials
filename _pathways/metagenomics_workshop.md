---
layout: pathway
title: "Metagenomics Workshop: From Raw Reads to MAGs"
description: "This learning path introduces the complete metagenomic analysis workflow, from raw read quality control through assembly, evaluation, binning, and classification. You will learn how to process Illumina short-read data, assemble complex microbial communities, evaluate assembly quality, recover metagenome-assembled genomes (MAGs), and assign taxonomic labels using standardized, phylogeny-aware frameworks."
keywords: [metagenomics, QC, FastQC, fastp, Cutadapt, assembly, MEGAHIT, metaSPAdes, MetaQUAST, binning, MaxBin, MetaBAT, GTDB-Tk, CheckM2, MAGs]
level: intermediate
life_cycle: under development

pathway:
  - section: "Module 1: Quality Control & Preprocessing"
    description: "This module introduces the essential first step of any metagenomic workflow: assessing and improving the quality of raw sequencing reads. You will learn how to evaluate data with FastQC, trim adapters and low-quality bases using fastp, and perform precise adapter removal with Cutadapt."
    tutorials:
      - name: mgworkshop_qc
        version: main

  - section: "Module 2: Metagenome Assembly"
    description: "This module covers the principles and hands-on application of metagenome assembly. You will learn about de Bruijn graph approaches, k-mer selection strategies, and metagenome-specific challenges such as uneven coverage and strain diversity. Several assemblers (MEGAHIT, metaSPAdes, Velvet, Ray, IDBA-UD) will be applied and compared."
    tutorials:
      - name: mgworkshop_assembly
        version: main

  - section: "Module 3: Assembly Evaluation"
    description: "This module introduces methods for evaluating assembly quality by mapping reads back to contigs, visualizing alignments in IGV, and computing comprehensive assembly metrics using MetaQUAST against reference genomes."
    tutorials:
      - name: mgworkshop_assembly_eval
        version: main

  - section: "Module 4: Binning and Classification"
    description: "This module covers the recovery of individual genomes from metagenomic assemblies through binning, the application of standardized taxonomic classification using GTDB-Tk, and the quality assessment of metagenome-assembled genomes (MAGs) with CheckM2."
    tutorials:
      - name: mgworkshop_binning_classification
        version: main

  - section: "Module 5: Metagenomics Toolkit (Jupyter)"
    description: "This module introduces the Metagenomics Toolkit, a comprehensive workflow for metagenomics analysis. You will learn how to prepare sequencing data, run the initial analysis workflow, and explore first steps of metagenomic data processing and interpretation."
    tutorials:
      - name: mgworkshop_toolkit_jupyter
        version: main

contributions:
  authorship:
  - Nils Kleinbölting
  - Sebastian Jünemann
  - Alexander Sczyrba
  editing:
  funding:
---