---
layout: tutorial_hands_on
title: Metagenomic Assembly
description: "This tutorial will guide you through the typical steps of metagenome assembly. "
slug: mgworkshop_assembly
time_estimation: 6H
questions:
  - "How do I run a metagenome assembly?"
  - "How do I compare metagenome assemblies?"
version:
  - main
life_cycle: "alpha"
contributions:
  authorship:
  - Nils Kleinbölting
  - Alexander Sczyrba
  - Sebastian Jünemann
  editing: 
  funding:
---

## Prerequisites

Please do the linux introduction before this tutorial. We assume you have successfully connected to an instance in the de.NBI cloud with the software pre-installed. Otherwise you will need to install the required tools on your own and make sure you have sufficient resources available. 

TODO: Add data download!!!

## Table of Contents
* [Quick introduction to (meta)-genome assembly](#metagenome-assembly)
* [Tutorial](#tutorial)
    * [Data download](#data-download)
    * [Velvet](#velvet)
    * [Megahit](#megahit)
    * [metaspades](#metaspades)
    * [idba_ud](#idba_ud)
    * [ray](#ray)

## Metagenome Assembly

Describe Metagenome Assembly here, include images from the slides.

## **Tutorial**

We are going to use different assemblers and compare the results.

### **Data download**

We have prepared a small toy data set for this tutorial. It's simulated data, so there is actually no need for quality control.


> ## Download data
> Please use the following commands to download the data to your VM:
> ```bash
> sudo chown ubuntu:ubuntu /mnt
> cd /mnt
> wget https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/denbi-mg-course/WGS-data.tar
> tar xvf WGS-data.tar
> ```
> 
{: .hands_on}

The `/mnt/WGS-data` directory has the following content:

| File          | Content                                    |
|---------------|--------------------------------------------|
| genomes/      | Directory containing the reference genomes |
| gold_std/     | Gold Standard assemblies                   |
| read1.fq      | Read 1 of paired reads (FASTQ)             |
| read2.fq      | Read 2 of paired reads (FASTQ)             |
| reads.fas     | Shuffled reads (FASTA)                     |


### **Velvet**

Velvet was one of the first de novo genomic assemblers specially
designed for short read sequencing technologies. It was developed by
Daniel Zerbino and Ewan Birney at the European Bioinformatics
Institute (EMBL-EBI). Velvet currently takes in short read sequences,
removes errors then produces high quality unique contigs. It then uses
paired-end read and long read information, when available, to retrieve
the repeated areas between contigs. See the `Velvet GitHub page
<https://github.com/dzerbino/velvet>`_ for more info.

> ## Step 1: velveth
> `velveth` takes in a number of sequence files, produces a hashtable, then
> outputs two files in an output directory (creating it if necessary), Sequences
> and Roadmaps, which are necessary for running `velvetg` in the next step.
> 
> Let's create multiple hashtables using kmer-lengths of 31 and 51. We
are going to run two jobs::
> ```bash
> cd /mnt/WGS-data  
> velveth velvet_31 31 -shortPaired -fastq -separate read1.fq read2.fq  
> velveth velvet_51 51 -shortPaired -fastq -separate read1.fq read2.fq
> ```
> 
>  Once the two jobs are finished (use `top` to monitor your jobs), you 
> should have two output directories for the two different kmer-lengths: 
> `velvet_31` and `velvet_51`.
> 
{: .hands_on}

Now we have to start the actual assembly using `velvetg`. 

> ## Step 2: velvetg
> `velvetg` is the core of Velvet where the de Bruijn
> graph is built then manipulated. Let's run assemblies for both
> kmer-lengths. See the `Velvet manual
> <https://github.com/dzerbino/velvet/blob/master/Manual.pdf>`_ for more
> info about parameter settings. Run:

> ```bash
> cd /mnt/WGS-data
> velvetg velvet_31 -cov_cutoff auto -ins_length 270 -min_contig_lgth 500 -exp_cov auto &
> velvetg velvet_51 -cov_cutoff auto -ins_length 270 -min_contig_lgth 500 -exp_cov auto &
> ```
> 
{: .hands_on}

The contig sequences are located in the `velvet_31` and `velvet_51`
directories in file `contigs.fa`. Let's get some very basic statistics
on the contigs.

> ## Step 3: getN50
> The script ``getN50.pl`` reads the contig file and
> computes the total length of the assembly, number of contigs, N50 and
> largest contig size. In our example we will exclude contigs shorter
> than 500bp (option `-s 500`)::
> ```bash
> cd /mnt/WGS-data
> getN50.pl -s 500 -f velvet_31/contigs.fa
> getN50.pl -s 500 -f velvet_51/contigs.fa
> ```
> 
{: .hands_on}

### **Megahit**


### **metaspades**
### **idba_ud**
### **ray**