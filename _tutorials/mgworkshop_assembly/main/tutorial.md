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


# Metagenome Assembly  
*Based on lecture slides from FZ Jülich :contentReference[oaicite:0]{index=0}*

## Introduction

Metagenome assembly is the computational reconstruction of longer DNA sequences, so-called contigs, from millions to billions of short fragments generated during sequencing of complex microbial communities. It is a central component of metagenomic analysis pipelines because it transforms raw reads into interpretable genomic units. These units enable later steps such as binning, gene prediction, functional annotation, and the identification of community structure.

Metagenomics is often summarized by two overarching questions: *Who is present in the sample?* and *What are they capable of doing?* Assembly occupies a key position among these steps, as illustrated in the workflow diagram from the lecture slides.

**Figure 1.** *Metagenomic analysis strategies, adapted from Sharpton 2014*  
`![Metagenomic analysis strategies]((/tutorials/mgworkshop_assembly/images/strategies.png))`

## A Visual Analogy: Assembly as Puzzle Reconstruction

Metagenome assembly resembles the process of solving a large jigsaw puzzle without the guiding image on the box. Each sequencing read corresponds to a small piece of the puzzle, and assembling them into contigs requires identifying how these pieces fit together based on overlapping sequence information. The analogy from the slides begins with scattered puzzle pieces representing disordered sequencing reads and ends with the completed picture symbolizing a reconstructed genomic sequence.

**Figure 2.** *Puzzle pieces representing short reads*  
`![Puzzle pieces representing short reads]((/tutorials/mgworkshop_assembly/images/puzzle1.png))`

**Figure 3.** *Completed puzzle symbolizing the finished assembly*  
`![Completed puzzle symbolizing the finished assembly]((/tutorials/mgworkshop_assembly/images/puzzle2.png))`

## Classical Genome Sequencing Strategies

Before short-read next-generation sequencing became dominant, genome assembly commonly relied on two main strategies: ordered shotgun sequencing and whole genome shotgun sequencing. In ordered shotgun sequencing, DNA fragments were cloned into vectors such as BACs and arranged into a physical map. This map provided positional information, making it possible to sequence clones individually and then piece them together with high confidence. The physical map served as a scaffold that guaranteed correct global arrangement, though generating it required significant laboratory effort.

**Figure 4.** *Hierarchical (ordered) shotgun sequencing schematic adapted from Venter et al., Nature 2001 *  
`![Hierarchical shotgun sequencing]((/tutorials/mgworkshop_assembly/images/hierarchical_shotgun.png))`

Whole genome shotgun sequencing simplified the experimental workflow by fragmenting the entire genome simultaneously, sequencing all pieces in parallel, and then computationally assembling the resulting reads. While this approach quickly produced large amounts of sequence, it complicated the final assembly step because it lacked positional context. Complex repetitive regions frequently caused ambiguities because reads from different genomic copies appeared identical.

**Figure 5.** *Whole genome shotgun sequencing schematic adapted from Venter et al., Nature 2001 *  
`![Whole genome shotgun sequencing]((/tutorials/mgworkshop_assembly/images/wg_shotgun.png))`

Short-read sequencing intensified this challenge. Technologies such as Illumina produce extremely high coverage but with short reads, typically around 100 base pairs. As a consequence, assembly algorithms require sophisticated data structures to handle both the enormous number of reads and the difficulties imposed by repetitions, sequencing errors, and the shortness of individual fragments.

## Assembly Paradigms

Assembly algorithms fall into three conceptual categories: greedy approaches, the overlap–layout–consensus (OLC) model, and de Bruijn graph assemblers.

Greedy assemblers incrementally merge reads by repeatedly choosing the overlap that appears locally optimal. Because they commit early to decisions based on local criteria, they may fail to recover the globally correct genome structure.

The OLC method attempts to identify all pairwise overlaps between reads, construct an overlap graph, and then determine a layout that visits each read once in an order consistent with these overlaps. The final consensus stage extracts the nucleotide sequence implied by the layout. While conceptually straightforward, the OLC approach suffers from its computational burden. For large datasets, computing all read overlaps scales quadratically with the number of reads. The slides highlight that assembling 27 million Sanger reads would yield approximately one trillion possible overlaps, which would require years of computation if each alignment took even a millisecond.

The memory requirements are likewise severe. Storing such a graph may demand terabytes of memory. Because metagenomes contain far more reads than typical genome projects, OLC approaches have become largely infeasible for short-read metagenomics.

**Figure 6.** *Illustration of overlaps and layouts used in OLC assembly*  
`![Illustration of overlaps and layouts used in OLC assembly]((/tutorials/mgworkshop_assembly/images/olc.png))`

By contrast, de Bruijn graph assemblers break each read into overlapping k-mers, thereby reducing the assembly problem to analysing the connectivity between k-mer prefixes and suffixes. This strategy dramatically increases computational efficiency because nodes of the graph represent k-mers, not entire reads. Instead of finding a Hamiltonian path (visiting each read exactly once), the assembler finds an Eulerian path that visits each edge, corresponding to each k-mer occurrence, exactly once. Eulerian path finding is computationally tractable, making de Bruijn graph methods the standard for short-read metagenome assembly.

**Figure 7.** *Comparison of OLC and de Bruijn graph paradigms*  
`![Comparison of OLC and de Bruijn graph paradigms]((/tutorials/mgworkshop_assembly/images/olc_dbg.png))`

## Repeats and Structural Ambiguities

Repetitive sequences pose difficulties for any assembly strategy. When two genomic regions share identical or nearly identical sequences, the assembler may mistakenly combine reads from distinct regions into a single contig (over-collapsing), or it may produce branching paths representing alternative assemblies that cannot be resolved unambiguously.

The slides include several diagrams showing how repeats create complex graph structures, including branching nodes where multiple contigs are possible. Correct repeat resolution often requires additional information such as paired-end reads, long reads, or coverage differences.

**Figure 8.** *Repeat-induced ambiguities and unitig structure*  
`![Repeat-induced ambiguities and unitig structure]((/tutorials/mgworkshop_assembly/images/repeats1.png))`
**Figure 9.** *Repeat-induced ambiguities and unitig structure*  
`![Repeat-induced ambiguities and unitig structure]((/tutorials/mgworkshop_assembly/images/repeats2.png))`

## Complexity of de Bruijn Graphs

Although de Bruijn graphs avoid the prohibitive OLC overlap computations, they introduce their own challenges. Sequencing errors generate unique or low-frequency k-mers that do not align well within the graph, producing structures known as tips (short dead-end paths) or bubbles (parallel alternative paths). Polymorphisms between closely related organisms in a metagenome create similar structures. Repeats generate converging or diverging paths that require careful handling by the assembler.

**Figure 10.** *Typical complexities within a de Bruijn graph: tips, bubbles, and repeat structures*  
`![Typical complexities within a de Bruijn graph: tips, bubbles, and repeat structures]((/tutorials/mgworkshop_assembly/images/complexities.png))`

## Influence of k-mer Size

Choosing the appropriate k-mer size is a central challenge in constructing de Bruijn graphs. If k is too small, the graph becomes densely connected because short k-mers are insufficient to resolve unique genomic regions. This results in tangled, ambiguous graph structures. If k is too large, the graph becomes fragmented because fewer reads contain each specific k-mer, making it harder to maintain continuous paths.

The lecture slides show a dramatic series of Bandage visualizations illustrating how graph structure changes as k increases from 51 to 91. At small k, the graph is extremely complex, resembling a knot of interwoven paths. As k increases, many ambiguous connections disappear, but the graph becomes more fragmented. Assemblers often work around this by constructing multiple graphs with different k values and combining their information, as done in metaSPAdes.

**Figure 11.** *Examples of de Bruijn graphs at k=51 to k=91*  
`![Examples of de Bruijn graphs at k=51 to k=91]((/tutorials/mgworkshop_assembly/images/bandage.png))`


## Special Challenges in Metagenomic Assembly

...

**Figure 12.** *A metagenome puzzle consisting of two quite distinct genomes*  
`![A metagenome puzzle consisting of two quite distinct genomes]((/tutorials/mgworkshop_assembly/images/mgassembly1.png))`

...

**Figure 13.** *Solved metagenome puzzle consisting of two quite distinct genomes*  
`![Solved metagenome puzzle consisting of two quite distinct genomes]((/tutorials/mgworkshop_assembly/images/mgassembly2.png))`

...

**Figure 14.** *Three very similar genomes*  
`![Three very similar genomes]((/tutorials/mgworkshop_assembly/images/mgassembly3.png))`

...

**Figure 15.** *A real metagenome*  
`![A real metagenome]((/tutorials/mgworkshop_assembly/images/mgassembly4.png))`


Assembly of single genomes is already challenging, but metagenome assembly introduces additional complications. Coverage varies dramatically between species, making it difficult to decide which low-frequency k-mers correspond to rare organisms and which are artifacts. Closely related strains or species may share long genomic regions, producing highly similar k-mers that merge in the graph. Divergent abundance profiles of species introduce asymmetry into the graph that must be addressed by specialized heuristics. Contamination and horizontal gene transfer further blur boundaries between genomic segments.

Assemblers designed for isolated genomes typically assume uniform coverage and do not incorporate metagenome-specific statistical models, which is why specialized tools have been developed.

## Metagenome Assemblers

Several assemblers have been created specifically for metagenomic data.

### MetaVelvet

## K-mer Frequency Distributions

K-mer abundance analysis provides valuable information for filtering erroneous k-mers and identifying genomic signals within mixed communities. True genomic k-mers typically appear at coverage levels reflecting the abundance of their originating organism. Low-frequency k-mers often result from sequencing errors. In metagenomes, the situation is complicated by varying species abundances, producing multiple k-mer coverage peaks rather than a single unicellular distribution. The slides illustrate how frequently particular k-mers occur and how this distribution can be used to distinguish noise from signal.

**Figure 16.** *K-mer frequency distributions demonstrating separation of error-derived and genomic k-mers*  
`![K-mer frequency distributions demonstrating separation of error-derived and genomic k-mers]((/tutorials/mgworkshop_assembly/images/freq1.png))`
**Figure 17.** *K-mer frequency distributions demonstrating separation of error-derived and genomic k-mers*  
`![K-mer frequency distributions demonstrating separation of error-derived and genomic k-mers]((/tutorials/mgworkshop_assembly/images/freq2.png))`
**Figure 18.** *K-mer frequency distributions demonstrating separation of error-derived and genomic k-mers*  
`![K-mer frequency distributions demonstrating separation of error-derived and genomic k-mers]((/tutorials/mgworkshop_assembly/images/freq3.png))`

MetaVelvet extends the Velvet assembler by integrating coverage-based heuristics. It distinguishes high-coverage and low-coverage branches in the graph to separate signals from organisms with different abundances, increasing the likelihood of resolving strain mixtures.

**Figure 19.** *MetaVelvet conceptual diagram (Namiki T et al. Nucl. Acids Res. 2012;40:e155
)*  
`![MetaVelvet conceptual diagram]((/tutorials/mgworkshop_assembly/images/metavelvet.png))`

### IDBA-UD

IDBA-UD (Iterative de Bruijn graph assembler for uneven sequencing depth) adapts dynamically to the depth variability inherent in metagenomic datasets. It eliminates erroneous k-mers using depth-relative thresholds and performs local assemblies that incorporate paired-end information to resolve repeats in low-depth regions. High-depth regions undergo additional error correction to prevent oversaturation of the graph.


### MEGAHIT

MEGAHIT is designed for high efficiency and low memory consumption, making it particularly suitable for large metagenomic datasets. It constructs a compressed de Bruijn graph, iteratively increases k-mer sizes, and simplifies the graph through error removal. Despite its low resource usage, MEGAHIT produces high-quality assemblies.


**Figure 20.** MEGAhit workflow (Li et. al, Bioinformatics, 2015)*  
`![MEGAhit workflow ]((/tutorials/mgworkshop_assembly/images/megahit.png))`

MEGAHIT workflow:

Streaming k-mer decomposition: Splits sequence reads into k-mers but stores them efficiently.
Graph construction: Builds a compressed de Bruijn graph to save memory.
Graph simplification: Removes unnecessary edges and sequencing errors.
Iterative k-mer expansion: Starts with small k-mers and gradually increases their size.
Contig generation: Assembles the best possible long contigs.


### metaSPAdes

metaSPAdes uses a multilayer de Bruijn graph approach in which several k-mer sizes are considered simultaneously. This strategy combines the continuity benefits of small k-mers with the specificity of large k-mers. It includes extensive error correction procedures and explicitly models uneven coverage, making it one of the most accurate assemblers for complex communities.

metaSPAdes workflow:

K-mer analysis: Splits sequence reads into multiple k-mer sizes (e.g., 21, 33, 55, etc.).
Graph construction: Builds a de Bruijn graph to identify sequence connections.
Error correction: Removes sequencing errors from the k-mers for better assembly accuracy.
Multilayer graph: Uses multiple k-mer sizes to resolve complex genome structures.
Metagenome-specific improvements: Takes into account variable coverage depths (since some organisms are more abundant than others).
Final assembly: Merges different graph layers to generate contigs (longer DNA sequences).


### Comparison of MEGAHIT and metaSPAdes

The slides compare MEGAHIT and metaSPAdes, emphasizing that metaSPAdes generally yields higher accuracy but requires much more memory and computation time. MEGAHIT excels when speed or memory constraints are a priority.


**Figure 21.** Comparison of MEGAHIT and metaSPAdes*  
`![Comparison of MEGAHIT and metaSPAdes]((/tutorials/mgworkshop_assembly/images/metaspades_megahit.png))`


## Assessment and Benchmarking

As shown in the slides, the Critical Assessment of Metagenome Interpretation (CAMI) benchmarks evaluate assemblers and analysis pipelines on standardized simulated and real datasets. These benchmarks highlight strengths and weaknesses of individual tools and reveal that no single assembler outperforms all others across all categories. The choice of assembler often depends on dataset complexity, computational resources, and the goals of the analysis.

**Figure 22.** CAMI benchmarking overview (Meyer, F., Fritz, A., Deng, ZL. et al. Critical Assessment of Metagenome Interpretation: the second round of challenges. Nat Methods 19, 429–440 (2022).)*  
`![CAMI benchmarking overview]((/tutorials/mgworkshop_assembly/images/cami.png))`

## Summary

Metagenome assembly reconstructs genomic sequences from mixtures of organisms, relying on computational methods that infer long stretches of DNA from short fragments. Classical OLC methods are computationally infeasible for modern metagenomics, leading to widespread adoption of de Bruijn graph–based assemblers. These assemblers must navigate complexities such as sequencing errors, repeats, uneven coverage, and strain-level diversity. Choices of k-mer size, graph simplification algorithms, and error correction strategies substantially influence assembly quality. Modern assemblers such as MEGAHIT and metaSPAdes incorporate innovative methods to handle these challenges and achieve increasingly accurate reconstructions of microbial communities. Through benchmarks like CAMI, the field continues to refine its methodologies and improve the robustness of metagenome assembly workflows.

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
