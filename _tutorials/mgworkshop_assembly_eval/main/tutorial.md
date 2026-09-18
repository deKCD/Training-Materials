---
layout: tutorial_hands_on
title: Assembly Evaluation
description: "This tutorial introduces the workflow for evaluating metagenomic assemblies by mapping reads back to contigs and computing assembly metrics using MetaQUAST."
time_estimation: 1H
level: intermediate
keywords: metagenomics, assembly evaluation, BBMap, MetaQUAST, QUAST, read mapping, contigs
questions:
  - "How do I map sequencing reads back to assembled contigs for quality assessment?"
  - "How can I evaluate assembly quality using reference genomes with MetaQUAST?"
  - "What metrics does QUAST provide to compare different assemblers?"
objectives:
  - "Index and map Illumina reads to assembled contigs using BBMap."
  - "Process BAM files with samtools for downstream analysis and visualization."
  - "Visualize read assemblies in the IGV genome browser."
  - "Evaluate and compare multiple assemblies using MetaQUAST with reference genomes."
  - "Interpret QUAST metrics to assess assembly completeness and accuracy."
key_points:
  - "Read mapping quality provides a direct measure of assembly accuracy and completeness."
  - "BBMap efficiently handles large metagenomic assemblies with millions of scaffolds."
  - "MetaQUAST computes comprehensive assembly metrics by aligning contigs to reference genomes."
  - "QUAST reports include contig/N50 statistics, misassemblies, and coverage profiles."
version:
  - main
life_cycle: under development
contributions:
  authorship:
  - Nils Kleinbölting
  - Sebastian Jünemann
  - Alexander Sczyrba
  editing: 
  funding:
---

><details-title>Prerequisites</details-title>
> - Completion of the [Metagenomic Assembly tutorial]({{ site.url }}{{ site.baseurl }}/tutorials/mgworkshop_assembly/main/tutorial/) or equivalent assembly experience.
> - Basic knowledge of Unix/Linux command line operations.
> - Familiarity with NGS data formats (FASTA, FASTQ, BAM, SAM).
> - An assembly of metagenomic reads (e.g., from MEGAHIT, metaSPAdes).
> - We assume you are working in a computational environment with sufficient CPU cores (e.g., 28). All commands specifying thread counts can be adjusted (`-t` or `--threads`) to match your available resources.
{: .details}

## **Download the data and preparations**

*You can skip this section if you already did the [Metagenomic Assembly tutorial]({{ site.url }}{{ site.baseurl }}/tutorials/mgworkshop_assembly/main/tutorial/*

First, create a link to `/vol/mgcourse` (or the folder in which you want to work during the course) and switch to that directory:

```bash
ln -s /vol/mgcourse/ ~/workdir
cd ~/workdir
```
You might need to change the permissions of `/vol/mgcourse`, for example (in the cloud setup we use for the on-site course) with:

```bash
sudo chown ubuntu:ubuntu /vol/mgcourse/
```
(Adjust accordingly to your setup)

><details-title>IMPORTANT</details-title>
>Some software is installed within a python virtual environment, you need to activate it with:
>
>```bash
>source ~/mgcourse/bin/activate
>```
>If some tool cannot be executed during this tutorial - make sure the environment is active! Indicated byt `(longread)` in your commandline.
{: .details}

Next, we download our tutorial dataset and extract it:

```bash
cd ~/workdir
wget https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/denbi-mg-course/WGS-data.tar
tar xvf WGS-data.tar
```

---

## Read Mapping: Validating Assemblies Against Raw Data

After assembling metagenomic sequencing reads into contigs, **read mapping** allows us to validate the assembly quality by mapping the original reads back to the assembled contigs. High mapping rates indicate that the assembly successfully captured the underlying sequence information, while poor mapping rates may suggest assembly errors or fragmentation.

### Mapping Reads with BBMap

**BBMap** is a ultrafast shotgun aligner capable of handling arbitrarily large genomes with millions of scaffolds. It supports Illumina, PacBio, 454, and other read types with very high sensitivity and tolerance for errors and large indels.

#### Building the Index

BBMap needs to build an index for the contig sequences before it can map reads onto them. Navigate to your assembly directory and run:

```bash
cd ~/workdir/WGS-data/megahit_out

bbmap.sh ref=final.contigs.fa
```

> <tip-title>Indexing Time</tip-title>
> Building the BBMap index for large metagenomic assemblies can take several minutes depending on the total assembly size. The terminal will show progress during index construction.
{: .tip}

#### Mapping the Reads

Once the index is built, map your paired-end reads to the assembled contigs:

```bash
bbmap.sh in=../read1.fq in2=../read2.fq out=megahit.bam threads=28
```

BBMap produces output in BAM format (the binary version of the [SAM format](http://samtools.github.io/hts-specs/SAMv1.pdf)).

### Processing BAM Files with samtools

Before visualization or downstream analysis, we need to process the BAM file.

#### Index the FASTA Reference

First, build a sequence index for the FASTA file:

```bash
samtools faidx final.contigs.fa
```

#### Sort and Index the BAM File

Sort the BAM file by starting position of the alignments, then index it:

```bash
samtools sort -o megahit_sorted.bam -@ 28 megahit.bam
samtools index megahit_sorted.bam
```

> <tip-title>Indexing Time</tip-title>
> Sorted BAM files enable efficient random access to alignments, which is required for most downstream tools and for visualization in genome browsers. Indexing creates a `.bai` file that allows genome browsers to jump to specific genomic regions without scanning the entire file.
> Without sorting, alignments are in arbitrary order, making it impossible to efficiently view reads at a specific locus. Without indexing, visualizers would need to read through the entire BAM file sequentially, which is prohibitively slow for large datasets.
{: .title}

#### Inspecting Mapped Reads

Quickly inspect the mapped reads on the command line:

```bash
samtools view megahit_sorted.bam | head -n 10
```

### Visualizing in IGV

The **Integrative Genomics Viewer (IGV)** provides an interactive graphical interface for exploring read alignments, coverage depth, and potential assembly artifacts.

Launch IGV

```bash
igv
```

and load the following tracks:

1. **Load the contig sequences:** Use the menu `Genomes → Load Genome from File...` to load `final.contigs.fa`.
2. **Load the BAM file:** Use the menu `File → Load from File...` to load `megahit_sorted.bam`.
3. **Load predicted genes (optional):** Use `File → Load from File...` to load the corresponding GFF file if available.

> <tip-title>What to Look For in IGV</tip-title>
> - **Coverage depth:** Uniform coverage suggests a good assembly; sudden drops may indicate misassemblies.
> - **Read orientation:** Properly paired reads should map in expected orientations (forward-reverse).
> - **Split alignments:** Reads that align to non-contiguous regions may indicate repeats or assembly breaks.
{: .tip}

---

## Assembly Evaluation with MetaQUAST

**QUAST** (QUality ASsessment Tool) evaluates genome assemblies by computing various metrics, including N50, the number of contigs, misassemblies, and coverage. **MetaQUAST** extends this functionality for metagenomic assemblies, incorporating gene finding, taxonomic classification, and comparison against multiple reference genomes simultaneously.

### Preparing Assembly Results

If you didn't compute all the assemblies in the previous part (or skipped some) you can copy the finished assemblies with this command:

```bash
cd ~/workdir/WGS-data/
cp -r --update=none assembly_results/* .
```

### Running MetaQUAST

Execute MetaQUAST to evaluate all assemblies against the provided reference genomes:

> <comment-title>Reference Genomes in Metagenomics</comment-title>
> In real-world metagenomics, reference genomes are typically not available. However, for this workshop we use them to demonstrate how to objectively compare assembly quality. In practice, reference-free metrics (e.g., N50, BUSCO scores) are used instead.
{: .comment}

```bash
cd ~/workdir/WGS-data

metaquast.py --threads 28 --gene-finding \
  -R genomes/Aquifex_aeolicus_VF5.fna,\
genomes/Bdellovibrio_bacteriovorus_HD100.fna,\
genomes/Chlamydia_psittaci_MN.fna,\
genomes/Chlamydophila_pneumoniae_CWL029.fna,\
genomes/Chlamydophila_pneumoniae_J138.fna,\
genomes/Chlamydophila_pneumoniae_LPCoLN.fna,\
genomes/Chlamydophila_pneumoniae_TW_183.fna,\
genomes/Chlamydophila_psittaci_C19_98.fna,\
genomes/Finegoldia_magna_ATCC_29328.fna,\
genomes/Fusobacterium_nucleatum_ATCC_25586.fna,\
genomes/Helicobacter_pylori_26695.fna,\
genomes/Lawsonia_intracellularis_PHE_MN1_00.fna,\
genomes/Mycobacterium_leprae_TN.fna,\
genomes/Porphyromonas_gingivalis_W83.fna,\
genomes/Wigglesworthia_glossinidia.fna \
  -o quast \
  -l MegaHit,metaSPAdes,Ray_31,Ray_51,velvet_31,velvet_51,velvet_71,idba_ud \
  megahit_out/final.contigs.fa \
  metaspades_out/contigs.fasta \
  ray_31/Contigs.fasta \
  ray_51/Contigs.fasta \
  velvet_31/contigs.fa \
  velvet_51/contigs.fa \
  velvet_71/contigs.fa \
  idba_ud_out/contig.fa
```

> <tip-title>Understanding MetaQUAST Options</tip-title>
> - `--gene-finding`: Activates gene prediction within assembled contigs for functional comparison.
> - `-R`: Comma-separated list of reference genomes used to gauge assembly accuracy.
> - `-l`: Labels assigned to each assembly for clear identification in reports.
> - `-o`: Output directory for all QUAST reports and statistics.
{: .tip}

### Interpreting QUAST Reports

QUAST generates HTML reports including interactive graphics and comprehensive statistics. Access the reports in your web browser:

```bash
firefox quast/report.html
```

Key metrics to examine:
- **N50 and L50:** Measure assembly contiguity. Higher N50 and lower L50 indicate better continuity.
- **Number of contigs:** Fewer contigs generally suggest a more complete assembly (for single genomes; for metagenomes, this is less informative).
- **Misassemblies:** Incorrect joins between non-contiguous regions — fewer is better.
- **Genome fraction:** Percentage of reference genomes covered by the assembly.
- **Duplication ratio:** Values >1 indicate possible over-assembly or strain variation.

> <question-title>Comparing Assemblers</question-title>
> Given that different assemblers (MEGAHIT, metaSPAdes, Ray, Velvet, IDBA-UD) have different strengths, which metrics would you prioritize when choosing an assembler for your metagenomic project?
> 
> > <solution-title>Solution</solution-title>
> > For single-species genomes, N50 and genome fraction are often most important. For complex metagenomes, consider the balance between contiguity and accuracy — a very high N50 with many misassemblies is less useful than a moderate N50 with high accuracy. Gene completeness (BUSCO/CheckM) should also factor into the decision.
> {: .solution}
{: .question}

---

## APPENDIX: References & Tools

* **BBMap:**
  * **Publication:** Bushnell, B. (2014). BBMap: A fast, accurate, splice-aware aligner. *Proceedings of the RECOMB 2014 Annual Meeting*.
  * **Documentation:** [https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/](https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/)
* **samtools:**
  * **Publication:** Li, H., et al. (2009). The Sequence Alignment/Map format and SAMtools. *Bioinformatics*, 25(16), 2078–2079.
  * **Documentation:** [http://www.htslib.org/](http://www.htslib.org/)
* **IGV (Integrative Genomics Viewer):**
  * **Publication:** Robinson, J. T., et al. (2011). Integrative Genomics Viewer. *Nature Biotechnology*, 29(1), 24–26.
  * **Homepage:** [https://igv.org/](https://igv.org/)
* **MetaQUAST:**
  * **Publication:** Mikheenko, A., et al. (2018). An accurate and fast metagenome assembly evaluation tool. *Bioinformatics*, 34(10), 1796–1802.
  * **Documentation:** [http://quast.sourceforge.net/metaquast](http://quast.sourceforge.net/metaquast)
* **QUAST:**
  * **Publication:** Gurevich, A., et al. (2013). QUAST: quality assessment tool for genome assemblies. *Bioinformatics*, 29(8), 1072–1075.
  * **Documentation:** [http://quast.sourceforge.net/quast](http://quast.sourceforge.net/quast)