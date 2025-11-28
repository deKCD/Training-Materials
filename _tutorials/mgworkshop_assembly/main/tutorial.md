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
are going to run two jobs:
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
> kmer-lengths. See the [Velvet manual](https://github.com/dzerbino/velvet/blob/master/Manual.pdf)
> for more info about parameter settings. Run:
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

### **MEGAHIT**

MEGAHIT is a single node assembler for large and complex metagenomics
NGS reads, such as soil. It makes use of succinct de Bruijn graph
(SdBG) to achieve low memory assembly. MEGAHIT can optionally utilize
a CUDA-enabled GPU to accelerate its SdBG contstruction. See the
[MEGAHIT home page](https://github.com/voutcn/megahit/) for more
info.

> ## Step 1: Run MEGAHIT
> MEGAHIT can be run by the following command. As our compute instance
> has multiple cores, we use the option `-t 14` to tell MEGAHIT it
> should use 14 parallel threads. The output will be redirected to file
> ```bash
> cd /mnt/WGS-data
> megahit -1 read1.fq -2 read2.fq -t 28 -o megahit_out
> ```
> 
{: .hands_on}

The contig sequences are located in the `megahit_out` directory in
file `final.contigs.fa`. 

> ## Step 2: getN50
> Again, let's get some basic statistics on the contigs:
> ```bash
> commandgetN50.pl -s 500 -f megahit_out/final.contigs.fa
> ```
> 
{: .hands_on}

### **metaSPAdes**

SPAdes – St. Petersburg genome assembler – is an assembly toolkit
containing various assembly pipelines. See the 
[SPAdes home page](http://cab.spbu.ru/software/spades/) for more info.

> ## Step 1: Run metaSPAdes
> metaSPAdes can be run by the following command:
> ```bash
> cd /mnt/WGS-data
> metaspades.py -o metaspades_out --pe1-1 read1.fq --pe1-2 read2.fq
> ```
> 
{: .hands_on}

The contig sequences are located in the `metaspades_out` directory in file `contigs.fasta`.

> ## Step 2: getN50
> Again, let's get some basic statistics on the contigs:
> ```bash
> getN50.pl -s 500 -f metaspades_out/contigs.fasta
> ```
> 
{: .hands_on}

### **IDBA-UD**

IDBA is the basic iterative de Bruijn graph assembler for
second-generation sequencing reads. IDBA-UD, an extension of IDBA, is
designed to utilize paired-end reads to assemble low-depth regions and
use progressive depth on contigs to reduce errors in high-depth
regions. It is a generic purpose assembler and epspacially good for
single-cell and metagenomic sequencing data. See the [IDBA home page](https://github.com/loneknightpy/idba) for more info.

IDBA-UD requires paired-end reads stored in single FastA file and a
pair of reads is in consecutive two lines. You can use `fq2fa` (part
of the IDBA repository) to merge two FastQ read files to a single
file. 

> ## Step 1: Create fasta file
> The following command will generate a FASTA formatted file
> called `reads12.fas` by "shuffling" the reads from FASTQ files
> `read1.fq` and `read2.fq`::
> ```bash
> cd /mnt/WGS-data
> fq2fa --merge read1.fq read2.fq reads12.fas
> ```
> 
{: .hands_on}

> ## Step 2: Run IDBA_UD
> IDBA-UD can be run by the following command. As our compute instances
> have multiple cores, we use the option `--num_threads 28` to tell
> IDBA-UD it should use 28 parallel threads.
> ```bash
> cd /mnt/WGS-data
> idba_ud -r reads12.fas --num_threads 28 -o idba_ud_out
> ```
> 
{: .hands_on}

The contig sequences are located in the `idba_ud_out` directory in file `contig.fa`. 

> ## Step 3: getN50
> Again, let's get some basic statistics on the contigs:
> ```bash
> getN50.pl -s 500 -f idba_ud_out/contig.fa
> ```
> 
{: .hands_on}


### **Ray**

Ray is a parallel software that computes de novo genome assemblies
with next-generation sequencing data.  Ray is written in C++ and can
run in parallel on numerous interconnected computers using the
message-passing interface (MPI) standard. See the [Ray home page](http://denovoassembler.sourceforge.net/) for more info.

> ## Step 1: Run Ray
> Ray can be run by the following command using a kmer-length of 51 and
> 31, repectively. As our compute instance have multiple cores, we
> specify this in the `mpiexec -n 28 ` command to let Ray know it should
> use 28 parallel MPI processes:
> ```bash
> cd /mnt/WGS-data
> mpiexec -n 28 /usr/local/bin/Ray -k 51 -p read1.fq read2.fq -o ray_51
> ```
> 
{: .hands_on}

> ## Step 2: Run another assembly
>If there is enough time, you can run another Ray assembly using a smaller kmer size.
> ```bash
> mpiexec -n 28 /usr/local/bin/Ray -k 31 -p read1.fq read2.fq -o ray_31
> ```
> 
{: .hands_on}

This will create the output directory `ray_51` (and `ray_31`), the final
contigs are located in `ray_51/Contigs.fasta` (and
`ray_31/Contigs.fasta`).  

> ## Step 3: getN50
> Again, let's get some basic statistics on the contigs:
> ```bash
> getN50.pl -s 500 -f ray_51/Contigs.fasta
> getN50.pl -s 500 -f ray_31/Contigs.fasta
> ```
> 
{: .hands_on}

> ## Step 4: getN50
> Now that you have run assemblies using Velvet, MEGAHIT, metaSPAdes, IDBA-UD and Ray, let's have a > quick look at the assembly statistics of all of them::
> ```bash
> cd /mnt/WGS-data
> sh ./get_assembly_stats.sh
> ```
> 
{: .hands_on}
