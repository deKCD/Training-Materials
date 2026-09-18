---
layout: tutorial_hands_on
title: Metagenomic Quality Control & Preprocessing
description: "This tutorial introduces the workflow for assessing sequencing quality with FastQC, trimming adapters, and removing low-quality bases using fastp and Cutadapt."
time_estimation: 1H
level: intermediate
keywords: metagenomics, FastQC, fastp, Cutadapt, QC, quality trimming, adapters
questions:
  - "How do I assess the quality of raw sequencing reads?"
  - "How do I trim adapters and low-quality bases using fastp?"
  - "How can I remove residual adapter contamination with Cutadapt?"
objectives:
  - "Generate and interpret FastQC reports for raw data."
  - "Apply sliding window quality trimming and poly-G removal using fastp."
  - "Trim remaining adapter sequences using Cutadapt."
  - "Validate preprocessing results to ensure high-quality input for downstream assembly."
key_points:
  - "FastQC provides immediate visual feedback on sequencing quality, adapter contamination, and base composition."
  - "fastp performs efficient quality trimming, sliding window analysis, and adapter/poly-G removal in parallel."
  - "Cutadapt offers precise adapter trimming when fastp's built-in detection is insufficient."
  - "Always verify preprocessing results with FastQC before proceeding to assembly."
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
> - Familiarity with NGS data formats (FASTA, FASTQ, BAM, SAM).
> - Raw paired-end sequencing reads (e.g., `read1.fq`, `read2.fq`).
> - We assume you are working in a computational environment with sufficient CPU cores (e.g., 28). All commands specifying thread counts can be adjusted to match your available resources.
{: .details}

## FastQC: Assessing Raw Sequence Quality

**FastQC** aims to provide a simple way to perform quality control checks on raw sequence data coming from high-throughput sequencing pipelines. It offers a modular set of analyses to give a quick impression of whether your data has any problems that should be addressed before downstream processing.

### Running FastQC

To launch the quality assessment on your raw reads, simply navigate to your data directory and run:

```bash
cd ~/workdir/WGS-data
fastqc read1.fq read2.fq
```

After `FastQC` finishes, it generates HTML-based reports for each file. You can review them in the host's default browser:

```bash
firefox *.html
```

> <tip-title>Key Metrics in FastQC</tip-title>
> Pay close attention to the following plots:
> - **Per Base Sequence Quality:** Identify positions with significant quality drops.
> - **Per Sequence Quality Scores:** Spot outlier reads with uniformly low quality.
> - **Adapter Content:** Detect residual adapter or primer contamination.
> - **Per Base N Content:** Flag regions with excessive unknown bases.
{: .tip}

Check the [FastQC home page](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/) for detailed examples of reports, including those containing problematic data.

---

## Quality Treatment & Preprocessing

In this exercise, you will learn how to effectively quality-trim paired-end Illumina reads. While Illumina PE reads remain the standard for metagenomics, raw outputs often contain technical artifacts that must be removed.

### Step 1: Initial Quality Assessment

First, let's download a representative dataset and inspect it with FastQC:

```bash
mkdir -p ~/workdir/qc
cd ~/workdir/qc
wget https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/mgcourse_data/qc.tgz
tar -xvzf qc.tgz
fastqc *.fastq
```

Review the generated reports to identify the specific quality issues present in the raw data.

### Step 2: Sliding Window Trimming with fastp

**fastp** is a fast, all-in-one tool for FASTQ file processing. It trims reads from the 5' to 3' end using a sliding window approach. If the mean quality of bases inside the window drops below a specific threshold (q-score), the remaining portion of the read is trimmed. Reads that become too short are discarded.

Inspect the help page first (`fastp -h`) to understand all parameters, then run the initial quality trim:

```bash
fastp \
  -i forward.fastq \
  -I reverse.fastq \
  -o forward_qc1.fastq \
  -O reverse_qc1.fastq \
  --cut_tail -Q -A -G -w 16
```

> <comment-title>Parameter Breakdown</comment-title>
> - `--cut_tail`: Aggressively trim if the tail is too short.
> - `-Q`: Skip reads where base quality is too low.
> - `-A`: Automatically detect and trim adapters.
> - `-G`: Trim the first 5 bases (common adapter artifact).
> - `-w 16`: Sliding window size (16 bases).
{: .comment}

Validate the effect by re-running FastQC on the trimmed output:

```bash
fastqc forward_qc1.fastq reverse_qc1.fastq
```

### Step 3: Removing Poly-G Tails

Poly-G tails often appear in Illumina reads due to phasing issues or incomplete cluster generation. fastp handles this efficiently:

```bash
fastp \
  -i forward.fastq \
  -I reverse.fastq \
  -o forward_qc2.fastq \
  -O reverse_qc2.fastq \
  --cut_tail -A -g --poly_g_min_len 5 -w 16
```

Re-evaluate the quality with FastQC:

```bash
fastqc forward_qc2.fastq reverse_qc2.fastq
```

> <question-title>Why do poly-G tails occur in Illumina sequencing?</question-title>
> Poly-G tails are typically artifacts caused by incomplete cluster generation or phasing/pre-phasing errors during the sequencing run, particularly in later cycles. They do not represent biological sequence and must be removed to avoid assembly fragmentation.
> 
> > <solution-title>Solution</solution-title>
> > fastp's `--poly_g_min_len 5` flag detects and trims consecutive G bases that exceed the specified length threshold, effectively cleaning the 3' ends without discarding valid biological content.
> {: .solution}
{: .question}

### Step 4: Precise Adapter Trimming with Cutadapt

Fastp's automatic adapter detection (`-A`) is excellent, but residual contamination sometimes persists. For highly precise adapter trimming, **Cutadapt** is often preferred due to its rigorous alignment algorithms.

First, identify the exact primers/adapters used. Sequencing facilities usually provide this information, but standard Illumina adapters can also be verified via:
* [Illumina Adapter Sequences (UCD Davis)](https://dnatech.genomecenter.ucdavis.edu/wp-content/uploads/2019/03/illumina-adapter-sequences-2019-1000000002694-10.pdf)
* [SCG Library Structure (Teichlab)](https://teichlab.github.io/scg_lib_structs/methods_html/Illumina.html)

The adapter sequence to be trimmed from our reads is:
- Forward: `CTGTCTCTTATACACATCT`
- Reverse: `CTGTCTCTTATACACATCT`

Feed these directly into Cutadapt, targeting the 3' ends:

```bash
cutadapt -f fastq \
  -e 0.15 -O 10 -m 25 \
  -a CTGTCTCTTATACACATCT \
  -A CTGTCTCTTATACACATCT \
  -o forward_qc3.fastq \
  -p reverse_qc3.fastq \
  forward_qc2.fastq reverse_qc2.fastq
```

> <comment-title>Cutadapt Parameters</comment-title>
> - `-e 0.15`: Maximum allowed error rate (15%).
> - `-O 10`: Minimum overlap length to initiate trimming.
> - `-m 25`: Minimum read length (reads shorter than 25bp are discarded).
> - `-a` / `-A`: Target adapters for the forward and reverse reads, respectively.
{: .comment}

Finally, run FastQC one last time to confirm that all technical artifacts have been successfully removed:

```bash
fastqc forward_qc3.fastq reverse_qc3.fastq
```

### Interpreting Preprocessing Results

Compare the initial and final FastQC reports. You should observe:
- **Baseline shift** in per-base quality scores to higher Phred values.
- **Adapter content plots** dropping to zero across all cycle positions.
- **Cleaner GC content distributions** matching expected metagenomic profiles.

> <question-title>When is quality control complete?</question-title>
> Quality control is considered complete when all known adapter sequences are removed, base quality scores meet the minimum threshold (typically Q20 or Q30), and no systematic biases (e.g., extreme GC bias or poly-G tails) remain in the FastQC reports. Only then should data proceed to assembly.
> 
> > <solution-title>Solution</solution-title>
> > Cross-reference FastQC metrics with downstream assembly success. A high-quality assembly typically yields long N50 contigs with minimal contamination, confirming that the preprocessing pipeline was effective.
> {: .solution}
{: .question}

## APPENDIX: References & Tools

* **FastQC:**
  * **Publication:** Andrews, S. (2010). FastQC: A Quality Control Tool for High Throughput Sequence Data.
  * **Home Page:** [http://www.bioinformatics.babraham.ac.uk/projects/fastqc/](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
* **fastp:**
  * **Publication:** Chen, S., et al. (2018). fastp: an ultra-fast all-in-one FASTQ preprocessor. *Bioinformatics*, 34(17), i884–i890.
  * **Documentation:** [https://github.com/OpenGene/fastp](https://github.com/OpenGene/fastp)
* **Cutadapt:**
  * **Publication:** Martin, M. (2011). Cutadapt removes adapter sequences from high-throughput sequencing reads. *EMBnet.journal*, 17(1), 10–12.
  * **Documentation:** [https://cutadapt.readthedocs.io/](https://cutadapt.readthedocs.io/)
* **Illumina Adapter Sequences:**
  * **Reference:** [https://teichlab.github.io/scg_lib_structs/methods_html/Illumina.html](https://teichlab.github.io/scg_lib_structs/methods_html/Illumina.html)