---
layout: tutorial_hands_on
title: Metagenomic Binning and Classification
description: "This tutorial introduces the workflow for clustering assembled metagenomic contigs into genomes (binning), evaluating their quality, and assigning taxonomic labels using modern bioinformatics tools."
time_estimation: 1H
level: intermediate
keywords: metagenomics, binning, MaxBin, MetaBAT, GTDB-Tk, CheckM2, MAGs, taxonomy
questions:
  - "How do I bin metagenomic contigs into Metagenome-Assembled Genomes (MAGs)?"
  - "What are the algorithmic differences and use-cases for MaxBin and MetaBAT?"
  - "How can I objectively classify MAGs using the Genome Taxonomy Database?"
  - "How do I assess and filter MAG quality using CheckM2?"
objectives:
  - "Prepare coverage profiles from mapped sequencing reads for binning algorithms."
  - "Execute MaxBin and MetaBAT to cluster contigs into putative genomes."
  - "Classify recovered bins using GTDB-Tk for standardized, phylogeny-aware taxonomy."
  - "Evaluate bin quality (completeness, contamination, strain heterogeneity) with CheckM2."
  - "Apply MIMAG quality standards to select high-quality MAGs for downstream analysis."
key_points:
  - "Binning relies on sequence composition (e.g., tetranucleotide frequency) and coverage depth profiles across samples."
  - "MaxBin uses an Expectation-Maximization approach with marker genes, while MetaBAT integrates probabilistic distances of coverage and composition."
  - "GTDB-Tk provides a unified, phylogeny-aware taxonomic framework based on whole-genome relationships."
  - "CheckM2 employs machine learning to estimate completeness and contamination more accurately than traditional marker gene sets."
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
> - Basic knowledge of Unix/Linux command line operations.
> - Completion of the [Metagenomic Assembly tutorial]({{ site.url }}{{ site.baseurl }}/tutorials/mgworkshop_assembly/main/tutorial/) or equivalent assembly experience.
> - Familiarity with NGS data formats (FASTA, BAM, FASTQ).
> - We assume you are working in a computational environment with sufficient CPU cores (e.g., 28). All commands specifying thread counts can be adjusted (`-thread` or `--cpus`) to match your available resources.
{: .details}

## Metagenomic Binning: Recovering Individual Genomes

After assembling metagenomic sequencing reads into contigs, **binning** algorithms attempt to cluster these contigs into discrete groups, each representing a single microbial genome. This process resolves complex community mixtures into individual organisms, enabling the study of uncultivated microbes directly from environmental samples.

Modern binning tools typically leverage two complementary signals:
1. **Sequence Composition:** Nucleotide frequency patterns (e.g., tetranucleotide usage) are often species-specific and stable across a genome.
2. **Coverage/Abundance Profiles:** Contigs originating from the same genome exhibit highly similar abundance patterns across multiple samples, time points, or environmental gradients.

> <tip-title>Why Binning Matters</tip-title>
> Binning transforms heterogeneous metagenomic data into isolated, high-quality **Metagenome-Assembled Genomes (MAGs)**. This enables functional annotation, comparative genomics, and ecological modeling of previously inaccessible microorganisms.
{: .tip}

---

### Preparing Coverage Profiles

Most binning algorithms require a coverage file that indicates how many sequencing reads map to each contig. We will extract this information from your mapped reads (`megahit_sorted.bam`).

```bash
cd ~/workdir/WGS-data/megahit_out
mkdir maxbin metabat
cd maxbin

# Calculate per-contig coverage from the sorted BAM file
pileup.sh in=../megahit_sorted.bam out=cov.txt

# Extract contig headers and their corresponding depth values
awk '{print $1"\t"$5}' cov.txt | grep -v '^#' > abundance.txt
```

## Bin Maximization with MaxBin

**MaxBin** is a widely used binning software that clusters metagenomic contigs into species-level bins using an Expectation-Maximization (EM) algorithm. It integrates tetranucleotide frequency and coverage information, iteratively enriching potential bins by identifying single-copy marker genes.

### Running MaxBin

Execute the binning process using your assembly and the generated coverage file:

```bash
cd ~/workdir/WGS-data/megahit_out/maxbin
run_MaxBin.pl -thread 28 -contig ../final.contigs.fa -out maxbin -abund abundance.txt
```

> <comment-title>Environment Setup</comment-title>
> If `run_MaxBin.pl` returns a "command not found" error, source the environment module or the .bashrc first:
> ```bash
> source /etc/environment
> source ~/.bashrc
> run_MaxBin.pl -thread 28 -contig ../final.contigs.fa -out maxbin -abund abundance.txt
> ```
{: .comment}

### Understanding MaxBin Output

Assuming your output prefix is `maxbin`, the tool generates several key files:

| File Name | Description |
| :--- | :--- |
| `maxbin.0XX.fasta` | Individual bin files (`XX` is a bin number, e.g., `maxbin.001.fasta`) |
| `maxbin.summary` | Classification table detailing contig-to-bin assignments |
| `maxbin.log` | Execution log recording algorithm steps and convergence status |
| `maxbin.marker` | Marker gene presence counts per bin (ready for R/Python visualization) |
| `maxbin.noclass` | Contigs passing the minimum length threshold but failing classification |
| `maxbin.tooshort` | Contigs filtered out for being below the minimum length requirement |

> <question-title>Validating Your Bins</question-title>
> Now that you have bins, how would you verify their taxonomic identity or assess if the community structure matches expectations?
> 
> > <solution-title>Solution</solution-title>
> > You can run gene prediction on each bin using `prodigal`, followed by a BLAST search against reference databases. Additionally, compare predicted 16S rRNA abundances in your bins against your original 16S amplicon sequencing profile to check for consistency.
> {: .solution}
{: .question}

## Bin Reconstruction with MetaBAT

**MetaBAT** (Metagenome Binning Algorithm Toolkit) is an automated binning tool that integrates empirical probabilistic distances of genome abundance and tetranucleotide frequency. It is optimized for high precision and often recovers a larger number of bins compared to composition-only methods.

### Running MetaBAT

Navigate to your output directory and execute the binner:

```bash
cd ~/workdir/WGS-data/megahit_out/metabat

# Run MetaBAT using the assembler and sorted BAM file
runMetaBat.sh ../final.contigs.fa ../megahit_sorted.bam
```

MetaBAT will automatically distribute contigs into multiple bins based on coverage and compositional signatures. You can inspect the generated bins with:

```bash
ls -l final.contigs.fa.metabat-bins*
```

> <tip-title>Bin Quality Considerations</tip-title>
> MetaBAT often produces a larger number of bins, which increases total genome recovery but may also yield more fragmented or chimeric assemblies. Downstream validation, dereplication, and quality filtering are crucial steps before downstream analysis.
{: .tip}

---

## Taxonomic Classification with GTDB-Tk

Once bins are recovered, assigning objective, standardized taxonomic labels is essential. **GTDB-Tk** is a tool that classifies bacterial and archaeal genomes based on the Genome Taxonomy Database (GTDB). It replaces traditional 16S-based taxonomy with a fixed, phylogeny-aware framework, making it the current standard for MAG classification.

### Step 1: Download the GTDB Database

The reference database is substantial (~64 GB). We will download it from local storage and extract it:

```bash
cd ~/workdir
wget -qO- https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/denbi-mg-course/gtdbtk_v2_data.tar.gz | tar xvz
```

> <comment-title>Extraction Time</comment-title>
> Extracting large tar archives can take several minutes depending on disk I/O. The terminal may appear to hang; allow the process to complete fully.
{: .comment}

We need to download the mash database, since it takes some time to create:

```bash
cd /mnt/release207_v2
wget https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/mg_databases/mash.msh
```

### Step 2: Configure Environment Variables

Set paths for GTDB-Tk to locate the database and executables:

```bash
# Point to the extracted database directory
export GTDBTK_DATA_PATH=~/workdir/release207_v2
# Activate GTDB-tk environment:
source ~/gtdb_env/bin/activate
```

### Step 3: Classify MaxBin Results

Run the classification pipeline on your MaxBin output folder:

```bash
cd ~/workdir/WGS-data/megahit_out/maxbin

gtdbtk classify_wf \
    --extension fasta \
    --cpus 28 \
    --genome_dir . \
    --out_dir gtdbtk_out \
    --mash_db ~/workdir/release207_v2/mash.msh
```

> <tip-title>Running GTDB-tk without mash db</tip-title>
> You can run GTDB-tk without a mash db which takes substantially more time, but will give you tree files to inspect:
> ```bash
> gtdbtk classify_wf \
>    --extension fasta \
>    --cpus 28 \
>    --genome_dir . \
>    --out_dir gtdbtk_out \
>    --skip_ani_screen
> ```
{: .tip}


### Step 4: Classify MetaBAT Results

Similarly, classify the MetaBAT bins for downstream comparison. Navigate to the MetaBAT bin directory (adjust the folder name as generated by the binner) and run:

```bash
cd ~/workdir/WGS-data/megahit_out/metabat/final.contigs.fa.metabat-bins.*YOUR_FOLDERNAME*
# Run classification on the bin directory
gtdbtk classify_wf \
    --extension fa \
    --cpus 28 \
    --genome_dir . \
    --out_dir gtdbtk_out \
    --mash_db ~/workdir/release207_v2/mash.msh
```

> <question-title>Comparing Binning Classifications</question-title>
> After both runs finish, how would you compare the taxonomic resolution and bin completeness between MaxBin and MetaBAT outputs?
> 
> > <solution-title>Solution</solution-title>
> > You can cross-reference GTDB-Tk lineage assignments with quality metrics from tools like CheckM or BUSCO. GTDB-Tk provides consistent, phylogeny-based ranks, allowing direct comparison of community composition, dominant phyla, and bin recovery rates across both binning approaches.
> {: .solution}
{: .question}

## Genomic Quality Assessment with CheckM2

After binning and taxonomy classification, it is essential to evaluate the quality of each recovered genome. **CheckM2** improves upon traditional marker gene methods by utilizing deep learning to predict genome quality metrics. It estimates completeness, contamination, and strain heterogeneity, which are critical for downstream ecological and functional analyses.

First, we activate the conda environmnt for checkm2:
```bash
conda activate checkm2
```

### Step 1: Database Setup

CheckM2 relies on a reference database to perform its predictions. Since this database is substantial, we will explicitly download it to a dedicated location:

```bash
checkm2 database --download --path ~/workdir/checkm2_db
```

> <tip-title>Why CheckM2 over traditional CheckM?</tip-title>
> Unlike traditional CheckM, which relies on a fixed set of 120 single-copy marker genes and linear regression models, CheckM2 uses a deep neural network trained on thousands of high-quality reference genomes. This allows it to achieve significantly higher accuracy, especially for draft-quality MAGs and underrepresented phyla.
> CheckM2's machine learning approach captures complex genomic signatures beyond simple marker gene presence/absence, providing more robust completeness and contamination estimates for diverse and fragmented metagenomic assemblies.
{: .tip}

### Step 2: Assessing MaxBin Results

Navigate to the MaxBin output directory containing your bins and run CheckM2:

```bash
cd ~/workdir/WGS-data/megahit_out/maxbin

checkm2 predict \
    --input . \
    -x fasta \
    --output-directory checkm2 \
    --threads 28 \
    --database_path ~/workdir/checkm2_db/CheckM2_database/uniref100.KO.1.dmnd
```

### Step 3: Assessing MetaBAT Results

Similarly, run CheckM2 on the MetaBAT bins:

```bash
cd ~/workdir/WGS-data/megahit_out/metabat/YOUR_BINFOLDER_NAME

checkm2 predict \
    --input . \
    -x fa \
    --output-directory checkm2 \
    --threads 28 \
    --database_path ~/workdir/checkm2_db/CheckM2_database/uniref100.KO.1.dmnd
```

### Interpreting CheckM2 Output

CheckM2 generates a `summary_table.txt` file containing global quality metrics for each bin:

| Metric | Description |
| :--- | :--- |
| `Completeness` | Predicted percentage of conserved single-copy genes present. |
| `Contamination` | Predicted percentage of redundant or multi-origin contigs in the bin. |
| `Strain Heterogeneity` | Indicates potential contamination from closely related strains. |
| `CheckM2 Score` | A composite quality metric combining the above factors. |

> <question-title>Evaluating Genome Quality</question-title>
> The MIMAG standards define "High-quality" MAGs as having ≥90% completeness and ≤5% contamination, while "Medium-quality" requires ≥50% completeness and ≤10% contamination. How would you use the CheckM2 summary table to filter your bins for downstream analysis?
> 
> > <solution-title>Solution</solution-title>
> > You can parse the `summary_table.txt` to filter bins meeting the MIMAG thresholds (e.g., using `awk` or a script). Typically, you would select bins with high completeness (>70-90%) and low contamination (<5-10%). Lower quality bins might still be useful for specific functional or phylogenetic analyses but should be excluded from comparative genomic studies unless appropriately weighted.
> {: .solution}
{: .question}

## APPENDIX: References & Tools

* **MaxBin:**
  * **Publication:** Wu, Y. W., et al. (2014). MaxBin: an automated binning method that recovers individual genomes from metagenomes using an expectation maximization algorithm. *Microbiome*.
  * **Homepage:** [https://downloads.jbei.org/data/microbial_communities/MaxBin/](https://downloads.jbei.org/data/microbial_communities/MaxBin/)
* **MetaBAT:**
  * **Publication:** Kang, D. D., et al. (2015). MetaBAT, an efficient tool for accurately reconstructing single genomes from complex microbial communities. *PeerJ*.
  * **Documentation:** [https://bitbucket.org/berkeleylab/metabat](https://bitbucket.org/berkeleylab/metabat)
* **GTDB-Tk:**
  * **Publication:** Chaumeil, P. A., et al. (2022). GTDB-Tk v2: memory-friendly classification with the genome taxonomy database. *Bioinformatics*.
  * **Documentation:** [https://ecogenomics.github.io/GTDBTk/](https://ecogenomics.github.io/GTDBTk/)
* **CheckM2:**
  * **Publication:** Manni, M., et al. (2021). CheckM2: a fast, flexible and accurate framework for estimating completeness and contamination in draft metagenome assemblies by artificial intelligence. *Nature Biotechnology*.
  * **Documentation:** [https://github.com/chenghanfong/checkm2](https://github.com/chenghanfong/checkm2)
* **Prodigal (Gene Prediction):**
  * **Publication:** Hyatt, D., et al. (2010). Prodigal: prokaryotic gene recognition and translation initiation site identification. *BMC Bioinformatics*.
  * **Homepage:** [https://github.com/hyattpd/Prodigal](https://github.com/hyattpd/Prodigal)