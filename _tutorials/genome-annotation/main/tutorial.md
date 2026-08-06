---
layout: tutorial_hands_on
title: Prokaryotic Genome Annotation (hands-on)
description: "Learn the steps of prokaryotic genome annotation by generating and comparing annotations with Prokka and Bakta. The tutorial also introduces EDGAR for comparative genome analysis, including core-genome, pan-genome and ortholog identification."
time_estimation: 2H
level: beginner
keywords: prokka, bakta, EDGAR
questions:
  - "How do I functionally annotate a bacterial genome using Prokka and Bakta, and what role does EDGAR play in comparative genomics?"
objectives:
  - "Generate comprehensive genome annotations with Prokka and Bakta, and interpret differences in functional naming and hypothetical protein rates."
  - "Explain how comparative genomics frameworks like EDGAR identify core genomes, pan-genomes, and unique singleton genes."
key_points:
  - "Modern annotation systems like Bakta significantly reduce the rate of uncharacterized 'hypothetical proteins' by integrating curated, up-to-date RefSeq and UniProt cross-references."
  - "Comparative workflows like EDGAR utilize BLAST Score Ratios (BSR) across multiple annotated genomes to instantly segregate the core genome from unique singleton genes."
version: main
life_cycle: under development
contributions:
  authorship:
  - Nils Kleinbölting
  editing: 
  - Dilfuza Djamalova
  funding:
---

This tutorial demonstrates how to annotate a polished prokaryotic genome assembly using Prokka and Bakta, compare their annotation outputs, and briefly explore comparative genomics with EDGAR. It uses the genome assembly generated in the previous tutorial [Assembly and assembly evaluation (hands-on)]({{ site.url }}{{ site.baseurl }}/tutorials/genome-assembly/main/tutorial/) as the input for all analyses.

><details-title>Prerequisites</details-title>
> - Please complete the [Unix/Linux introduction tutorial]({{ site.url }}{{ site.baseurl }}/tutorials/unix-course/main/tutorial/) before this tutorial. 
> - We assume you have successfully connected to an instance in the de.NBI cloud with the software pre-installed. Otherwise you will need to install the required tools on your own and make sure you have sufficient resources available. 
> - Throughout the course we assume you are working on data downloaded to a volume under `/vol/longread/`, we create a link `~/workdir/` to that  folder, if you are working somewhere else, adjust the `~/workdir` link to that location and all commands should work as outlined in the course.
> - We also assume that you have a machine with **28 cores** available, if not - adjust the commands that specify a certain number of threads / cores accordingly.
{: .details}

## Introduction to Prokaryotic Genome Annotation

Once you have successfully assembled and polished a bacterial chromosome, it consists simply of a long, uncharacterized string of nucleotides (A, C, G, T). To make this data useful for biological research, you must perform **genome annotation**. This process involves identifying the structural features of the genome—such as protein-coding sequences (CDS), transfer RNAs (tRNAs), and ribosomal RNAs (rRNAs)—and assigning functional biological identities to them based on sequence similarity to known databases.

In this module, we will compare two popular tools used for this task:

* **Prokka:** For nearly a decade, Prokka has been the legacy workhorse tool for rapid prokaryotic genome annotation. It coordinates an ensemble of open-source tools (like Prodigal for CDS finding and Aragorn for tRNAs) to generate comprehensive annotation suites in minutes. However, because its internal reference databases are no longer actively maintained, it often over-assigns generic functional names or labels proteins as "hypothetical protein".

> <tip-title>Optional: How to install Prokka</tip-title>
It's quite complicated to install without conda/docker/singularity. Check out the [github repository](https://github.com/tseemann/prokka) and use one of those methods.
{: .tip}

* **Bakta:** A modern, next-generation annotation platform designed specifically for microbial genomes. Bakta addresses Prokka's database stagnation by utilizing a thoroughly curated, regularly updated SQLite database synchronized with NCBI RefSeq, UniProt, and specialized feature resources. It provides highly accurate protein names, precise cross-reference tags (DBXrefs), and native tracking of non-coding RNAs (ncRNAs), pseudogenes, and antimicrobial resistance (AMR) gene identifiers.

> <tip-title>Optional: How to install Bakta</tip-title>
It's quite complicated to install without conda/docker/singularity. Check out the [github repository](https://github.com/oschwenders/bakta) and use one of those methods.
{: .tip}
---

## Hands-on: Annotating Your Assembly

We will run both annotators on our polished long-read assembly (`flye_polished.fasta`) and evaluate how their structural findings and functional naming conventions differ.

><hands-on-title>Step 1: Running Prokka</hands-on-title>
> Execute Prokka by specifying an output directory and a custom file prefix:
>
>```bash
>prokka --cpus 28 --outdir ~/workdir/prokka_output --prefix prokka_ont ~/workdir/polypolish/flye_polished.fasta
>```
{: .hands-on}

Don't worry about the `Could not run command: tbl2asn` message if it appears. We don't need the `asn` file.

><hands-on-title>Step 2: Running Bakta</hands-on-title>
>
> Unlike Prokka, Bakta relies on a separate, heavy database containing millions of curated proteins. For this workshop, this database has been pre-staged for you. Run Bakta using the following command:
>
>```bash
>conda activate bakta
>bakta --threads 28 --db ~/bakta_db/db-light --output ~/workdir/bakta_output ~/workdir/polypolish/flye_polished.fasta 
>conda deactivate
>source ~/longread/bin/activate
>```
{: .hands-on}

---

## Hands-on: Comparing Annotation Profiles

Both tools generate various standardized outputs, including GFF3, GenBank, and FASTA files. To quickly benchmark their structural predictions, we can review the text-based summary logs (`.txt`) produced by each pipeline.

><hands-on-title>Step 3: Inspecting Summary Outputs</hands-on-title>
>
>Use `cat` to print out both overview profiles in your terminal:
>
>```bash
># View the Prokka summary report
>cat ~/workdir/prokka_output/prokka_ont.txt
>
># View the Bakta summary report
>cat ~/workdir/bakta_output/bakta_ont.txt
>```
{: .hands-on}

> <question-title>Analyzing Annotation Discrepancies</question-title>
> Look closely at the total counts of Coding Sequences (CDS), tRNAs, and rRNAs in both outputs. Are the numbers identical? If they differ, what could cause one tool to predict more genes than the other?
> 
> > <solution-title>Solution</solution-title>
> > Even though they use the same underlying software for core gene finding (Prodigal), the total counts often differ slightly. Bakta uses stricter structural filters and a much larger database, allowing it to accurately split overlapping reading frames, filter out false positive predictions, and identify specialized elements like pseudogenes or small non-coding RNAs that Prokka completely misses.
> {: .solution}
{: .question}

><hands-on-title>Step 4: Comparing Functional Descriptions</hands-on-title>
>
>A major difference lies in how specifically proteins are named. Let's use `grep` to check how many genes were left uncharacterized as "hypothetical protein" in both annotation suites:
>
>```bash
># Count hypothetical proteins in Prokka's GFF output
>grep -c "hypothetical protein" ~/workdir/prokka_output/prokka_ont.gff
>
># Count hypothetical proteins in Bakta's GFF output
>grep -c "hypothetical protein" ~/workdir/bakta_output/bakta_ont.gff
>```
{: .hands-on}

> <comment-title>Interpreting Naming Quality</comment-title>
> You will notice that Bakta significantly reduces the fraction of `hypothetical protein` labels compared to Prokka. Thanks to its modern reference integration with UniProt and RefSeq, Bakta can assign definitive, functional gene names to sequences where Prokka could only find vague, outdated family matches.
{: .comment}

---

## Comparative Genomics with EDGAR

Once individual genomes are annotated, the next logical milestone is to explore how multiple strains or species relate to one another. For this downstream phase, we shift from localized command-line annotation to web-based comparative genomics using **EDGAR** (Efficient Database framework for comparative Genome Analyses).

* **Official Server Link:** [http://edgar3.computational.bio](http://edgar3.computational.bio)

### How EDGAR Works:
EDGAR is a fully automated high-throughput platform tailored for the deep comparative analysis of prokaryotic genomes. Users upload their fully annotated genome files (such as the `.gff` or GenBank files generated by Bakta) into public or password-protected private projects. 

The underlying pipeline performs intensive all-versus-all sequence alignments across all selected strains. By evaluating **BLAST Score Ratios (BSR)**, EDGAR accurately determines orthology relational paths to delineate specific genomic subsets:
1. **The Core Genome:** The conserved set of genes shared identically across *all* analyzed organisms, often used to build highly precise core-genome phylogenetic trees.
2. **The Pan-Genome:** The complete global pool of all unique genes present across the entire group.
3. **Singleton Genes:** Unique genes present in only *one* specific strain, which are crucial for identifying specific downstream traits like pathogenicity islands or unique metabolic capabilities.

Furthermore, EDGAR calculates average nucleotide identity (ANI) metrics and renders publication-ready  visualizations, including Venn diagrams, UpSet plots, and synteny maps mapping gene order conservation across syntenic chromosomal layouts.

---

## APPENDIX: References for tools used within the tutorial
* **Prokka (Rapid Prokaryotic Genome Annotation):**
  * **GitHub:** [https://github.com/tseemann/prokka](https://github.com/tseemann/prokka)
  * **Publication:** *Seemann, T. (2014). Prokka: rapid prokaryotic genome annotation. Bioinformatics.*
* **Bakta (Next-generation Microbial Genome Annotation):**
  * **GitHub:** [https://github.com/oschwenders/bakta](https://github.com/oschwenders/bakta)
  * **Publication:** *Schwengers, O. et al. (2021). Bakta: rapid and standardized annotation of bacterial genomes and plasmids. Microbial Genomics.*
* **EDGAR (Comparative Genomics Framework):**
  * **Webserver Platform:** [http://edgar3.computational.bio](http://edgar3.computational.bio)
  * **Publication:** *Dieckmann, M. A. et al. (2021). EDGAR 3.0: comparative genomics and phylogenomics on a scalable infrastructure. Nucleic Acids Research.*