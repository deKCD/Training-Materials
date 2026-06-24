---
layout: tutorial_hands_on
title: Nanopore Workshop
description: "This tutorial will guide you through the typical steps of analyzing read data from an isolate genome using ONT sequencing data and Illumina. "
time_estimation: 6H
level: beginner
keywords: ONT, Nanopore, Assembly, Polishing, Genomics, Annotation
questions:
  - "How do I basecall ONT data?"
  - "What is the difference between FAST5 and POD5 files?"
  - "How can we inspect and convert raw Nanopore data formats?"
  - "How do I assemble ONT data"
  - "How do I map ONT data?"
  - "How do I polish my ONT assembly using Illumina data?"
  - "How do run a hybrid assembly?"
  - "How do I compare assemblies?"
  - "How do I annotate my genome?"
objectives:
  - "Understand the physical and electrical principles of Nanopore sequencing."
  - "Explain the transition from early HMM-based basecallers to modern Transformer-based models."
  - "Interpret Phred quality scores and differentiate between Fast, HAC, and SUP models."
  - "Compare the structural differences between HDF5-based FAST5 and Arrow-based POD5."
  - "Use command-line tools to inspect legacy raw data."
  - "Convert legacy FAST5 files into the modern POD5 standard."
key_points:
  - "Basecalling translates raw ionic current disruptions ('squiggles') into nucleotide sequences."
  - "The evolution from Albacore to Guppy and Dorado represents a major shift from CPUs to GPU-accelerated deep learning."
  - "Modern R10.4.1 chemistry paired with Dorado pushes accuracies past Q20 (>99%), matching or exceeding short-read standards."
  - "FAST5 uses a hierarchical structure that causes I/O bottlenecks during high-throughput basecalling."
  - "POD5 uses a flat, columnar format (Apache Arrow) that offers faster multi-threaded access and smaller file sizes."
version:
  - main
life_cycle: under development
contributions:
  authorship:
  - Nils Kleinbölting
  editing: 
  funding:
---

><details-title>Prerequisites</details-title>
>
> - Please do the linux introduction before this tutorial. 
> - Basic understanding of the ONT and Illumina sequencing technology.
> - We assume you have successfully connected to an instance in the de.NBI cloud with the software pre-installed. Otherwise you will need to install the required tools on your own and make sure you have sufficient resources available. 
> - Throughout the course we assume you are working on data downloaded to a volume under `/vol/longread/`, we create a link `~/workdir/` to that  folder, if you are working somewhere else, adjust the `~/workdir` link to that location and all commands should work as outlined in the course.
> - We also assume that you have a machine with **28 cores** available, if not - adjust the commands that specify a certain number of threads / cores accordingly.
{: .details}

## **Download the data and preparations**

First, create a link to `/vol/longread` (or the folder in which you want to work during the course) and switch to that directory:

```bash
ln -s /vol/longread/ ~/workdir
cd ~/workdir
```
You might need to change the permissions of `/vol/longread`, for example (in the cloud setup we use for the on-site course) with:

```bash
sudo chown ubuntu:ubuntu /vol/longread/
```
(Adjust accordingly to your setup)

**IMPORTANT**: Some software is installed within a python virtual environment, you need to activate it with:

```bash
source ~/longread/bin/activate
```
If some tool cannot be executed during this tutorial - make sure the environment is active! Indicated byt `(longread)` in your commandline.


Next, we download our tutorial dataset and extract it:

```bash
cd ~/workdir
wget https://s3.bi.denbi.de/cmg/mgcourses/longread2026/coursedata.tar.gz
tar -xzvf coursedata.tar.gz
```

Have a quick look at the content of the `coursedata` folder:

```bash
ls -l ~/workdir/coursedata/
```
It contains the following components:
1. **illumina/** A folder containing fastq files with Illumina reads
2. **ont/** A folder containing fastq files with Nanopore reads
3. **raw/** A folder containing a file with raw Nanopore data which we will inspect in the next section
4. **reference.fasta** A reference fasta for the strain we are going to analyze

## Basecalling ONT data

Unlike traditional sequencing-by-synthesis methods, Oxford Nanopore Technologies (ONT) sequences native DNA or RNA molecules directly. This allows for the observation of full, unbroken fragments of genomic material, providing unprecedented insights into structural variations, repetitive regions, and base modifications.

### From Current Signals to Genetic Code: How It Works

The journey from a biological molecule to a digital sequence file relies on a highly sophisticated combination of nanoscale biophysics and deep learning algorithms.

1. **The Pore and the Current:** A microscopic protein pore (nanopore) is embedded in an electrically resistant synthetic membrane. A constant voltage is applied across this membrane, driving a steady flow of ions through the pore opening and creating a baseline ionic current.
2. **The Disruption (The Raw Signal):** As a single-stranded nucleic acid molecule is pulled through the pore by a motor protein, the nucleotides physically block the constriction. Because different combinations of bases have distinct chemical shapes, volumes, and electrical properties, they disrupt the ionic current in unique patterns.
3. **The Raw Data:** The sequencer records these rapid fluctuations in ionic current over time, measured in picoamperes (pA). This raw, continuous time-series data is known as a **"squiggle plot"** and is stored in binary raw data files (historically `.fast5`, nowadays `.pod5`).

> <tip-title>What's in a Squiggle?</tip-title>
> Multiple nucleotides (usually 4 to 6) occupy the narrowest part of the pore constriction at any given 
> millisecond. This means the electrical signal does not correspond to a single base at a time, but rather a 
> moving k-mer context. Translating these overlapping signals requires powerful machine learning models.
{: .tip}

**Basecalling** is the computational process of translating this noisy, continuous electrical current into a discrete sequence of characters (A, C, G, T/U).

### The Evolution of ONT Basecallers

The software responsible for basecalling has undergone a massive paradigm shift over the last decade, moving from simple statistical frameworks to cutting-edge deep learning architectures optimized for modern graphics processors (GPUs).

#### 1. Early Days (2014–2018): Albacore & Metrichor
Early basecalling algorithms relied on **Hidden Markov Models (HMMs)** and simple, shallow neural networks. 
* **Architecture:** Compute-heavy processes heavily reliant on CPU architectures.
* **Data Format:** Raw data was saved in the highly complex and heavy `.fast5` format (based on the HDF5 standard).
* **Performance:** Due to limitations in early algorithms and R7/R9 pore chemistries, raw read accuracy hovered around 85% to 90%, requiring complex downstream bioinformatics pipelines to build a consensus and correct errors.

#### 2. The Production Workhorse (2018–2023): Guppy
Guppy revolutionized long-read bioinformatics by transitioning to **GPU acceleration** and deep learning frameworks.
* **Architecture:** Utilized **Recurrent Neural Networks (RNNs)** and later **Conditional Random Fields (CRF)** to analyze time-series data dynamically.
* **Performance:** Enabled real-time basecalling during live sequencing runs. It pushed raw read accuracy past the 95% threshold, eventually peaking at 97-98% when combined with improved R10.3 and R10.4 pore chemistries.

#### 3. The Modern Era (2023–Present): Dorado
Dorado is ONT's current state-of-the-art production basecaller. Written in optimized C++ for peak hardware performance, it replaces Guppy entirely.
* **Architecture:** Powered by advanced **Transformer-based neural networks** (similar to modern large language models), which are exceptionally well-suited for capturing long-range contextual dependencies in data.
* **Data Format:** Operates natively with the highly efficient `.pod5` file format, significantly speeding up file input/output (I/O).
* **Key Features:** Natively supports **Duplex basecalling** (sequencing both the template and complement strands of a single DNA molecule consecutively) and real-time **modified base calling** (e.g., epigenetic changes like 5mC and 5hmC methylation) without requiring separate workflows.

### The Evolution of Quality Scores (Q-Scores)

To indicate the reliability of each called base, basecallers output a quality score using the standard Phred scale. The Phred quality score ($$Q$$) is logarithmically linked to the base-calling error probability ($$P$$) by the formula:

$$
Q = -10 \log_{10}(P)
$$

> <question-title>What does Q20 mean?</question-title>
> If a base is called with a quality score of 20 (Q20), what is the probability that this base call is an error?
>  
> > <solution-title>Solution</solution-title>
> > Rearranging the formula:
> > $$P = 10^{-\frac{Q}{10}} = 10^{-\frac{20}{10}} = 10^{-2} = 0.01$$
> > A score of Q20 indicates a **1% error probability**, meaning the base call has a **99.0% accuracy**.
> > 
> {: .solution}
>
{: .question}

As algorithms shifted from HMMs to advanced Transformers, and chemistry moved from the R9.4.1 pore to the refined geometry of the R10.4.1 pore, accuracy underwent a dramatic transformation. This shift is often described as entering the **"Q20 Era."**

| Era / Pore & Software Combination | Typical Raw Q-Score | Base Call Accuracy | Significance |
| :--- | :--- | :--- | :--- |
| **Early R9 + Albacore** | Q7 – Q10 | ~80.0% – 90.0% | High error rates; required heavy consensus bioinformatics to fix systematic mistakes. |
| **Late R9.4.1 + Guppy (HAC)** | Q13 – Q15 | ~95.0% – 96.8% | The standard for several years; highly capable for structural variants but struggled with homopolymers. |
| **Modern R10.4.1 + Dorado (HAC)** | Q20+ | **≥ 99.0%** | **The Q20 Milestone:** Raw reads match traditional sequencing accuracy, enabling reliable single-nucleotide variant (SNV) calling. |
| **Modern R10.4.1 + Dorado (Duplex)** | Q30+ | **≥ 99.9%** | High-fidelity long reads, ideal for ultra-accurate rare variant detection and *de novo* assembly. |

> <tip-title>Choosing the Right Dorado Model</tip-title>
> Dorado offers three different model types depending on your computational budget and laboratory goals:
> 1. **Fast:** Lightweight models optimized for real-time quality control checks during a run.
> 2. **High Accuracy (HAC):** The balanced standard baseline for most biological applications.
> 3. **Super Accuracy (SUP):** Compute-intensive models that require heavy GPU power but yield the highest possible raw Q-scores and the most accurate homopolymer resolution.
{: .tip}


### Raw Signal Data Formats – FAST5 vs. POD5

Before raw electrical signals ("squiggles") can be basecalled into sequence characters, they must be stored on disk. Oxford Nanopore Technologies (ONT) has utilized two primary formats for this purpose: **FAST5** and **POD5**. 

* **FAST5 (.fast5):** The legacy container format based on the **HDF5** (Hierarchical Data Format v5) standard. It organizes data hierarchically, much like a filesystem within a single file. While highly flexible, it suffers from significant metadata duplication, massive file size overhead, and poor multi-threaded I/O performance. This architectural layout creates massive bottlenecks for high-throughput sequencers and modern GPU-accelerated basecallers.
* **POD5 (.pod5):** The modern production standard format. Built on top of **Apache Arrow**, POD5 replaces legacy FAST5 files by employing a flat, columnar memory architecture. It natively supports streaming writes from the sequencing software (MinKNOW) and provides exceptionally fast multi-threaded random-access reads during basecalling. This transition yields significantly compressed file footprints, prevents disk fragmentation, and drastically speeds up processing times in Dorado.


#### Hands-on: Inspecting and Converting Raw Signal Data

In this practical exercise, you will peek inside a legacy `.fast5` file using standard system tools, convert it to the optimized `.pod5` format, and view its tabular metadata on the command line.

##### Prerequisites
Ensure you have `hdf5-tools` (supplying `h5ls`) and the official `pod5` Python package ready in your environment:

```bash
# Install the hdf5-tools command line tools if needed
sudo apt install hdf5-tools
# Install the pod5 command line utility if needed
pip install pod5
```

##### Peeking inside a FAST5 file

Because `.fast5` files are binary HDF5 containers, standard text-processing commands like `cat`, `head`, or `less` will output unreadable machine code. Instead, we use specialized HDF5 system utilities like `h5ls` to explore their internal directories.

Run the following command to recursively view the internal structure of a sample file:

```bash
cd ~/workdir/
h5ls -r coursedata/raw/rawdata.fast5
```

> <comment-title>Understanding HDF5 Structure</comment-title>
> Running this reveals a deeply nested tree layout. Each individual sequencing read gets its own path containing specific arrays like `/Raw/Signal` (the continuous stream of picoampere measurements) and `/channel_id` (the metadata tracking the specific pore block). Extracting files out of this nested design in parallel strains compute resources.
{: .comment}

##### Converting FAST5 to POD5

Because modern basecallers like Dorado are heavily optimized for Apache Arrow layouts, converting older data assets to `.pod5` is a crucial initial preprocessing step.

Execute the format conversion using the command line toolkit:

```bash
pod5 convert fast5 coursedata/raw/rawdata.fast5 --output coursedata/raw/rawdata.pod5
```

> <tip-title> Converting multiple files </tip-title>
> If you are dealing with an entire run directory containing hundreds of legacy files, you can point the tool to a folder instead:
> ```bash
> pod5 convert fast5 ./legacy_fast5_dir/ --output ./modern_pod5_dir/
> ```
{: .tip}

> <tip-title>Speeding up processing via Multi-threading</tip-title>
> The `pod5 convert` tool splits workloads efficiently. On multi-core systems, you can append the `--threads` or `-t` flag (e.g., `--threads 4`) to execute concurrent data writing routines.
{: .tip}

##### Viewing and Inspecting the POD5 file

Once converted, you can examine the file contents without extracting the heavy signal traces. The `pod5 view` tool acts as a rapid extraction program, rendering raw file attributes into a clean, human-readable tabular output.

Run the standard view command:

```bash
pod5 view coursedata/raw/rawdata.pod5
```

To slice the data or quickly check specific fields across your run, you can instruct the program to isolate target metrics and pipe them directly into a tab-separated (`.tsv`) file:

```bash
pod5 view coursedata/raw/rawdata.pod5 --include "read_id,channel,num_samples,end_reason" --output summary.tsv
```

> <question-title>Checking Data Footprints</question-title>
> Execute a file size check on your local disk using `ls -lh coursedata/raw/rawdata.*`. What differences do you notice between the two formats?
> 
> > <solution-title>Solution</solution-title>
> > You will instantly see that the `.pod5` variant is smaller than its `.fast5` source file. Columnar storage models compress highly repetitive data streams far more tightly while preserving identical raw electrical signal arrays.
> {: .solution}
{: .question}


### Basecalling with dorado

Now that we understand the raw data formats and have our datasets ready, we will perform the actual basecalling using **Dorado**, Oxford Nanopore's official state-of-the-art basecaller.

> <tip-title>Optional: How to install Dorado manually</tip-title>
> If Dorado is not pre-installed on your workshop instance, you can download, extract, and add the executable to your environment's `PATH` with these commands:
> ```bash
> # Download the Linux x64 binary
> wget https://cdn.oxfordnanoportal.com/software/analysis/dorado-0.9.6-linux-x64.tar.gz
> 
> # Extract the archive
> tar -xzvf dorado-0.9.6-linux-x64.tar.gz
> 
> # Append the bin folder to your PATH environment variable
> export PATH=$PATH:$(pwd)/dorado-0.9.6-linux-x64/bin
> ```
{: .tip}

> <tip-title>Which dorado version to use?</tip-title>
>  We are using an older version (0.9.6) of dorado that fits to our data. It is the latest version that still supports 4kHz sample rate. Newer versions of dorado (>1.0.0) don't support 4kHz models/data anymore. 
> For newer data, watch out for the latest version of dorado and make sure to use the latest model since every generation of models improves the basecall accuracy.
{: .tip}


#### Exploring Available Models

Dorado relies on deep-learning neural network models specifically trained on different pore types, sequencing speeds, and accuracy requirements. You can view all officially available models directly via the command line:

```bash
dorado download --list
```
The models are grouped into distinct categories based on their design and use case:
* **Simplex Models:** The standard sequencing baseline. These models are trained to read a single strand of DNA or RNA passing through the pore. The naming convention follows a structured pattern: `[molecule]_[pore]_[speed]_[accuracy]@[version]`. For example, `dna_r10.4.1_e8.2_400bps_fast@v4.1.0` tells us it is for DNA, using R10.4.1 pores, running at a translocation speed of 400 bases per second, utilizing the Fast neural network architecture.
* **Modification Models:** These models are trained to simultaneously call standard bases and detect epigenetic modifications (e.g., methylation) from the raw signal in real-time. They contain an extra suffix indicating the targeted modification type (e.g., `_5mCG_5hmCG` or `_6mA`).
* **Polish & Correction Models:** Advanced models (such as `herro-v1` or models containing `_polish`) optimized for post-processing steps or consensus correction. They are used to maximize final sequence accuracy by refining draft assemblies or correction arrays.
* **Stereo Models:** Take the complementary read pairs identified by duplex analysis and re-basecall them into a single, high-fidelity duplex read.

In addition, dorado models are categorized into three main performance tiers:
1. **Fast:** Minimal neural network layers. It is highly optimized for speed and real-time quality control but has the lowest consensus accuracy and struggles with homopolymer regions.
2. **High Accuracy (HAC):** The balanced standard production baseline for most biological studies, offering a strong trade-off between execution speed and reliable accuracy.
3. **Super Accuracy (SUP):** A highly complex, compute-heavy model structure. It requires extensive GPU power but yields the highest possible raw read accuracy and optimal homopolymer resolution.

Let's download both the **Fast simplex** model (which we will run completely) and the **SUP simplex** model (to test its performance impact):

```bash
# Download the Fast model specified for our R10.4.1 chemistry
dorado download --model dna_r10.4.1_e8.2_400bps_fast@v4.1.0

# Download the corresponding Super Accuracy (SUP) model
dorado download --model dna_r10.4.1_e8.2_400bps_sup@v4.1.0
```

---

#### Hands-on: Running Basecalling

We will now perform basecalling on our raw sample data using the lightweight `fast` model. By default, Dorado outputs alignments in SAM/BAM format. To force a traditional text-based output, we will pass the `--emit-fastq` flag.

Run the basecaller on our raw POD5 file/directory:

```bash
dorado basecaller dna_r10.4.1_e8.2_400bps_fast@v4.1.0 ~/workdir/coursedata/raw/rawdata.pod5 --emit-fastq > ~/workdir/fast_reads.fastq
```

Once completed, let's inspect the first few lines of your freshly generated FASTQ sequence file:

```bash
head -n 4 ~/workdir/fast_reads.fastq
```

> <question-title>Analyzing the FASTQ structure</question-title>
> Can you identify the four core lines making up a standard FASTQ record? What do the characters in the fourth line represent?
> 
> > <solution-title>Solution</solution-title>
> > A standard FASTQ block contains:
> > 1. `@` followed by the unique read identifier metadata.
> > 2. The actual base sequence characters (A, C, G, T).
> > 3. A `+` separator line.
> > 4. The ASCII-encoded Phred quality scores ($$Q$$) mapping directly to the error probability of each called base.
> {: .solution}
{: .question}

Now, let's observe the massive computational difference when running the high-complexity **SUP** model. Launch the following command:

```bash
dorado basecaller dna_r10.4.1_e8.2_400bps_sup@v4.1.0 ~/workdir/coursedata/raw/rawdata.pod5 --emit-fastq > ~/workdir/sup_reads.fastq
```

> <comment-title>Observing Performance Profiles</comment-title>
> Notice how the processing speed drops dramatically compared to the Fast run. Without a high-end dedicated graphics processor (GPU), running the Super Accuracy model on large datasets can take a massive amount of time. 
>
> Once you have observed this behavior for a few moments, **terminate the running process manually by pressing `Ctrl + C`** in your terminal window.
{: .comment}

---

#### Preparing the Full Dataset

For the downstream analysis sections of this course, we want to work with a complete dataset. We have already basecalled several raw data files (located in `coursedata/ont/`). To make processing streamlined (since many tools only take a single input file), we will concatenate all our prepared Nanopore FASTQ files into a single file using `cat`.

Execute the following command to merge your ONT reads:

```bash
cat ~/workdir/coursedata/ont/*.fastq.gz > ~/workdir/coursedata/ont.fastq.gz
```

> <tip-title>Verifying file concatenation</tip-title>
> You can verify the success of your merge step by listing the files and evaluating their sizes:
> ```bash
> ls -lh ~/workdir/coursedata/ont.fastq.gz  ~/workdir/coursedata/ont/*.fastq.gz
> ```
{: .tip}

## QC of ONT data

### Quality Trimming and Filtering in Dorado (Reference)

While we will use the full pre-prepared datasets for our hands-on exercises, it is important to know how to manage adapter trimming and quality filtering directly during the basecalling stage using Dorado. 

Unlike other tools where you must explicitly turn trimming on, **Dorado enables trimming of adapters, primers, and barcodes by default for DNA sequencing**. You can modify or disable this behavior using specific flags:

* `--no-trim` (or `--trim none`): Skips all trimming entirely, keeping raw adapter/barcode sequences in your reads.
* `--trim adapters`: Restricts trimming to *only* sequencing adapters, leaving barcodes or primers intact.
* `--min-qscore [value]`: Discards any read whose mean Phred quality score falls below your specified threshold (default is 0, meaning no filtering).

```bash
# Example reference command (Do not run during this workshop):
# This skips default barcode/primer trimming and filters out reads with a mean Q-score below 10:
# dorado basecaller dna_r10.4.1_e8.2_400bps_hac@v5.0.0 input_pod5/ --emit-fastq --trim adapters --min-qscore 10 > filtered_reads.fastq
```

---

### Hands-on: Quality Control of Sequencing Reads

To evaluate the success of our sequencing run, we must look at quality metrics such as read length distributions and Phred score frequencies. We will use **FastQC** and **NanoPlot** to analyze our long-read ONT data, and compare the profile to short-read Illumina data.

#### Step 1: Evaluating ONT Data with FastQC and NanoPlot

First, let's run FastQC on our combined Nanopore reads:

> <tip-title>Optional: How to install fastqc</tip-title>
Run this (or follow instructions on the github linked in the Appendix)
> ```bash
> sudo apt install fastqc
> ```
{: .tip}

```bash
mkdir ~/workdir/fastqc
fastqc -t 8 ~/workdir/coursedata/ont.fastq.gz -o ~/workdir/fastqc/
```

To view the generated interactive HTML quality report, open it in a web browser using `firefox`:

```bash
firefox ~/workdir/fastqc/ont_fastqc.html
```

Since FastQC was originally designed for short reads, it can struggle with the highly variable read lengths of Nanopore data. Therefore, we use **NanoPlot**, a tool specifically tailored for long-read technologies.

Run NanoPlot to generate a comprehensive quality report:

> <tip-title>Optional: How to install NanoPlot</tip-title>
Run this (or follow instructions on the github linked in the Appendix)
> ```bash
> pip install nanoplot
> ```
{: .tip}
```bash
NanoPlot --fastq ~/workdir/coursedata/ont.fastq.gz -o ~/workdir/nanoplot_ont
```

NanoPlot creates a dedicated output folder filled with various diagnostic plots (PNG/PDF formats) and a master HTML report summary. Let's open the main report:

```bash
firefox ~/workdir/nanoplot_ont/NanoPlot-report.html
```

> <question-title>Comparing FastQC and NanoPlot</question-title>
> Look at both browser tabs. What key metrics does NanoPlot show that are missing or misrepresented in FastQC?
> 
> > <solution-title>Solution</solution-title>
> > NanoPlot provides explicit long-read metrics such as N50 read length, active pore counters over time, and read length vs. read quality scatter plots. FastQC often flags long reads as "failed" due to length variations because it expects uniform short-read lengths.
> {: .solution}
{: .question}

#### Step 2: Filtering and Trimming with fastplong

**fastplong** is an ultra-fast, all-in-one quality control and preprocessing tool explicitly designed for long-read sequencing datasets (Nanopore and PacBio). It serves as the long-read counterpart to the widely used short-read tool `fastp`.

In a single multi-threaded execution pass, `fastplong` can perform:
* **Adapter Removal:** Auto-detects and clips residual sequencing adapters at both read starts and read ends.
* **Length Filtering:** Automatically drops fragments below a specified length threshold.
* **Quality Filtering:** Discards low-quality reads or performs sliding-window trimming on noisy terminal regions.

> <tip-title>Optional: How to install fastplong</tip-title>
Run this (or follow instructions on the github linked in the Appendix)
> ```bash
> wget http://opengene.org/fastplong/fastplong
> chmod a+x ./fastplong
> sudo mv fastplong /usr/local/bin/
> ```
{: .tip}

Let's run `fastplong` to enforce a minimum length requirement of 1,000 bp (`-l 1000`) and generate a localized performance dashboard:

```bash
fastplong -i ~/workdir/coursedata/ont.fastq.gz \
          -o ~/workdir/coursedata/ont_trimmed.fastq.gz \
          -l 1000 \
          -h ~/workdir/fastplong_report.html
```

Open the interactive HTML summary generated natively by `fastplong`:

```bash
firefox ~/workdir/fastplong_report.html
```

---

#### Step 3: Re-evaluating Processed ONT Data

To visualize the direct impact of our preprocessing step, let's run FastQC and NanoPlot a second time, pointing them to our freshly filtered output file:

```bash
# Re-run FastQC on trimmed data
fastqc -t 8 ~/workdir/coursedata/ont_trimmed.fastq.gz -o ~/workdir/fastqc/
firefox ~/workdir/fastqc/ont_trimmed_fastqc.html  ~/workdir/fastqc/ont_fastqc.html

# Re-run NanoPlot on trimmed data
NanoPlot --fastq ~/workdir/coursedata/ont_trimmed.fastq.gz -o ~/workdir/nanoplot_ont_trimmed/
firefox ~/workdir/nanoplot_ont_trimmed/NanoPlot-report.html  ~/workdir/nanoplot_ont/NanoPlot-report.html
```

> <question-title>Analyzing Post-Filtering Changes</question-title>
> Compare the browser tabs for the raw NanoPlot report (`nanoplot_ont`) vs. the filtered report (`nanoplot_ont_trimmed`). What happened to the total read count, the mean read length, and the N50 metric?
> 
> > <solution-title>Solution</solution-title>
> > Because we enforced a minimum length filter of 1,000 bp, all short fragments were eliminated. This causes the total read count to decrease, while both the *mean read length* and the *N50 value* increase. The overall mean Phred quality profile also shifts upwards, as short, degraded molecules are successfully purged from the dataset.
> {: .solution}
{: .question}

---

#### Step 4: Evaluating Illumina Data for Comparison

Now, let's run FastQC on our paired-end Illumina data to see the differences in throughput and quality distributions:

```bash
fastqc ~/workdir/coursedata/illumina/Barcode11_TSLF_S10_L001_R1_001.fastq.gz \
       ~/workdir/coursedata/illumina/Barcode11_TSLF_S10_L001_R2_001.fastq.gz \
       -t 8 \
       -o ~/workdir/fastqc/
```

Open both resulting reports to inspect the short-read profiles:

```bash
firefox ~/workdir/fastqc/Barcode11_TSLF_S10_L001_R1_001_fastqc.html ~/workdir/fastqc/Barcode11_TSLF_S10_L001_R2_001_fastqc.html
```

---

### Mapping Reads to the Reference Genome

To identify variants or verify the structure of our sequenced strain, we need to align our reads to the provided reference genome (`reference.fasta`). Long reads and short reads require completely different alignment algorithms.

#### Step 1: Aligning ONT Long Reads with minimap2

Create a folder to store our mappings first:
```bash
mkdir ~/workdir/mappings/
```

> <tip-title>Optional: How to install minimap2</tip-title>
Run this (or follow instructions on the github linked in the Appendix)
> ```bash
> curl -L https://github.com/lh3/minimap2/releases/download/v2.31/minimap2-2.31_x64-linux.tar.bz2 | tar -jxvf -
> export PATH=$PATH:$(pwd)/minimap2-2.31_x64-linux/
> chmod a+x ./fastplong
> sudo mv fastplong /usr/local/bin/
> ```
{: .tip}

**Minimap2** is the standard for aligning long, error-prone reads. We will use the `-ax map-ont` preset optimized for Oxford Nanopore data.

```bash
minimap2 -t 28 -ax map-ont ~/workdir/coursedata/reference.fasta ~/workdir/coursedata/ont_trimmed.fastq.gz > ~/workdir/mappings/ont_mapped.sam
```

#### Step 2: Aligning Illumina Short Reads with BWA

For short reads, we use **BWA (Burrows-Wheeler Aligner)**. Before aligning, BWA requires building an index of the reference genome.

> <tip-title>Optional: How to install bwa</tip-title>
Run this (or follow instructions on the github linked in the Appendix)
> ```bash
> sudo apt install bwa
> ```
{: .tip}

```bash
# Index the reference genome
bwa index ~/workdir/coursedata/reference.fasta

# Align the paired-end short reads using BWA-MEM
bwa mem -t 28 ~/workdir/coursedata/reference.fasta \
        ~/workdir/coursedata/illumina/Barcode11_TSLF_S10_L001_R1_001.fastq.gz \
        ~/workdir/coursedata/illumina/Barcode11_TSLF_S10_L001_R2_001.fastq.gz \
        > ~/workdir/mappings/illumina_mapped.sam
```

---

### Post-processing Alignments with samtools

Our alignment outputs are currently in **SAM** (Sequence Alignment Map) format, which is human-readable text but highly inefficient for visualization tools. We need to convert them to binary **BAM** format, sort them by genomic coordinates, and build a coordinate index (`.bai`) for quick random-access loading in **IGV** (Integrative Genomics Viewer).

> <tip-title>Optional: How to install samtools</tip-title>
Run this (or follow instructions on the github linked in the Appendix)
> ```bash
> sudo apt install samtools
> ```
{: .tip}


#### Step 3: Processing the ONT Mapping

```bash
# Convert SAM to BAM
samtools view -S -b ~/workdir/mappings/ont_mapped.sam > ~/workdir/mappings/ont_mapped.bam

# Sort the BAM file by coordinate position
samtools sort ~/workdir/mappings/ont_mapped.bam -o ~/workdir/mappings/ont_sorted.bam

# Index the sorted BAM file
samtools index ~/workdir/mappings/ont_sorted.bam
```

#### Step 4: Processing the Illumina Mapping

```bash
# Convert SAM to BAM
samtools view -S -b ~/workdir/mappings/illumina_mapped.sam > ~/workdir/mappings/illumina_mapped.bam

# Sort the BAM file by coordinate position
samtools sort ~/workdir/mappings/illumina_mapped.bam -o ~/workdir/mappings/illumina_sorted.bam

# Index the sorted BAM file
samtools index ~/workdir/mappings/illumina_sorted.bam
```

---

### Hands-on: Visualizing Alignments in IGV

Now that both datasets are fully optimized and indexed, we will visually inspect and compare our mapping data to explore how long reads perform against short reads across trickier genomic features.

> <tip-title>Optional: How to install IGV</tip-title>
Run this: and start IGV via `igv.sh`.
> ```bash
> wget https://data.broadinstitute.org/igv/projects/downloads/2.19/IGV_Linux_2.19.8_WithJava.zip
> unzip IGV_Linux_2.19.8_WithJava.zip
> #start IGV_Linux_2.19.8/igv.sh
> ```
{: .tip}

#### Execution Steps:
1. Open the **IGV** (Integrative Genomics Viewer) application on your system.
```bash
IGV
```
2. In the top menu, navigate to **Genomes** -> **Load Genome from File...** and select the reference genome file located at `~/workdir/coursedata/reference.fasta`.
3. Load the alignment files by navigating to **File** -> **Load from File...** and select your sorted BAM files:
   * `~/workdir/ont_sorted.bam`
   * `~/workdir/illumina_sorted.bam`
4. Zoom into an active genomic region or search for a specific gene coordinate to observe the read distribution.

> <question-title>Investigating Structural Differences</question-title>
> Browse through the alignment tracks. What is the main difference in terms of sequencing errors? What specific problem is caused by the ONT errors?
> 
> > <solution-title>Solution</solution-title>
> > Illumina has less errors and they are usullay substitutions, ONT has a high amount of insertions. Which causes a problem for gene prediction and annotation due to frameshifts.
> {: .solution}
{: .question}

## Assembly and assembly evaluation

### Introduction to De Novo Genome Assembly

Genome assembly is the process of piecing together massive amounts of short or long DNA fragments (reads) to reconstruct the original underlying chromosome. Because we do not use a reference genome during *de novo* assembly, the algorithms rely strictly on sequence overlaps. Two main algorithmic paradigms dominate the field:

* **De Bruijn Graph (DBG):** Primarily used for short reads (e.g., Illumina). Reads are broken down into smaller fixed-length strings called **$$k$$-mers**. Overlaps are tracked by constructing a network where nodes or edges represent shared $$k$$-mers. DBG is computationally efficient for processing hundreds of millions of short reads and highly accurate, but it struggles enormously with genomic repeats because the short $$k$$-mer contexts cannot resolve long duplicate regions.
* **Overlap-Layout-Consensus (OLC):** Primarily used for long reads (e.g., ONT, PacBio). The algorithm calculates all-versus-all alignments between full reads (**Overlap**), constructs an alignment graph to simplify paths and resolve structures (**Layout**), and finally determines the most accurate sequence across overlapping reads (**Consensus**). Long reads easily span across genomic repeats, allowing OLC-based pipelines to assemble completely closed chromosomes. This approach is usually not feasible for short reads due to the massive amount of alignments that have to be computed.

---

### Understanding the Assembly and Assembly Evaluation Tools

#### 1. Flye
Flye is a specialized *de novo* assembler designed for long, error-prone reads. Instead of building a classic OLC overlap graph (which scales poorly with high read depths), Flye constructs an unpolished **repeat graph**. It collapses complex genomic repeats into single edges, and then utilizes the long span of individual read paths to accurately untangle and separate those repeat copies.

> <tip-title>Optional: How to install Flye</tip-title>
Run this (or follow instructions in github):
> ```bash
> pip install setuptools
> git clone https://github.com/fenderglass/Flye
> cd Flye
> python setup.py install
> ```
{: .tip}

#### 2. SPAdes
SPAdes (St. Petersburg Genome Assembler) is the gold standard for bacterial short-read assemblies. It relies on multi-sized De Bruijn Graphs (combining multiple $k$-mer lengths) to simultaneously optimize specificity and sensitivity, providing robust performance across single-isolate cultures and single-cell sequencing.

> <tip-title>Optional: How to install Flye</tip-title>
Run this (or follow instructions in github):
> ```bash
> wget https://github.com/ablab/spades/releases/download/v4.3.0/SPAdes-4.3.0-Linux.tar.gz
> tar -xzvf SPAdes-4.3.0-Linux.tar.gz
> export PATH=PATH:$(pwd)/SPAdes-4.3.0-Linux/bin/
> ```
{: .tip}

#### 3. QUAST
QUAST (Quality Assessment Tool) is an evaluation utility that calculates structural metrics (like contig counts, N50 value, and total length) and identifies misassemblies by aligning your assembled contigs back against a trusted reference genome.

> <tip-title>Optional: How to install Quast</tip-title>
Run this (or follow instructions in github):
> ```bash
> wget https://github.com/ablab/quast/releases/download/quast_5.3.0/quast-5.3.0.tar.gz
> tar -xzvf quast-5.3.0.tar.gz
> cd quast-5.3.0
> ./setup.py install
> ```
{: .tip}

#### 4. Bandage
Bandage (Bioinformatics Application for Navigating De Novo Assembly Graphs Easily) is a graphical interface utility that reads Graphical Assembly Graph (`.gfa`) files. It allows you to see how contigs connect to one another, helping you determine whether your bacterial genome successfully assembled into a single closed circular chromosome.

> <tip-title>Optional: How to install Bandage</tip-title>
Run this (or follow instructions in github):
> ```bash
> wget https://github.com/rrwick/Bandage/releases/download/v0.8.1/Bandage_Ubuntu_dynamic_v0_8_1.zip
> unzip Bandage_Ubuntu_dynamic_v0_8_1.zip
> sudo mv Bandage /usr/local/bin/
> #might be necessary:
> sudo apt install libqt5svg5
> ```
{: .tip}

---

### Hands-on: Building and Evaluating Assemblies

In this section, we will run separate long-read and short-read assembly pipelines, statistically benchmark their outputs against our reference, inspect their connectivity graphs, and align the draft contigs visually.

#### Step 1: Long-Read Assembly with Flye

Because modern Dorado basecalled data achieves exceptional accuracy (entering the Q20 standard), we use Flye's high-fidelity option (`--nano-hq`) to generate our draft genome:

```bash
flye --nano-hq ~/workdir/coursedata/ont.fastq.gz --out-dir ~/workdir/flye_output --threads 28
```

#### Step 2: Short-Read Assembly with SPAdes

Next, we generate a corresponding short-read assembly utilizing our paired-end Illumina datasets:

```bash
spades.py -1 ~/workdir/coursedata/illumina/Barcode11_TSLF_S10_L001_R1_001.fastq.gz \
          -2 ~/workdir/coursedata/illumina/Barcode11_TSLF_S10_L001_R2_001.fastq.gz \
          -o ~/workdir/spades_output --threads 28
```

#### Step 3: Benchmarking Assemblies with QUAST

We can now run a direct comparative evaluation between both assembly results using our known genome sequence as a reference:

```bash
quast.py ~/workdir/flye_output/assembly.fasta \
         ~/workdir/spades_output/contigs.fasta \
         -r ~/workdir/coursedata/reference.fasta \
         -o ~/workdir/quast_output
```

Open the interactive QUAST HTML summary document in your browser to view the benchmark comparison:

```bash
firefox ~/workdir/quast_output/report.html
```

> <question-title>Analyzing Assembly Metrics</question-title>
> Look at the metric comparisons in the QUAST report. Which assembly contains fewer total contigs? Which possesses a higher N50 score? What does this tell you about the power of long reads?
> 
> > <solution-title>Solution</solution-title>
> > Typically, the Flye long-read assembly will result in significantly fewer contigs (often a single continuous contig for a closed bacterial chromosome) and a drastically higher N50 score approaching the true size of the genome. The SPAdes short-read assembly is usually split across multiple fragments because short fragments cannot resolve genomic repeats.
> {: .solution}
{: .question}

---

#### Step 4: Visualizing Graphs in Bandage

Statistical metrics only tell half the story. We need to look at the assembly graphs to see the structure of our contigs.

1. Launch the **Bandage** GUI application via your terminal:
```bash
   Bandage
   ```
2. In the Bandage menu, navigate to **File** -> **Load graph**.
3. First, load the Flye assembly graph file located at `~/workdir/flye_output/assembly_graph.gfa` and click **Draw graph**.
4. Next, clear the screen and load the SPAdes assembly graph file found at `~/workdir/spades_output/assembly_graph_with_scaffolds.gfa` and click **Draw graph**.

> <comment-title>Interpreting Graph Topologies</comment-title>
> In the Flye window, you should see a single, beautiful, interconnected closed loop representing the intact circular bacterial chromosome. In contrast, the SPAdes graph will likely display a highly fragmented web of disjointed paths and isolated nodes, highlighting where the short-read assembly broke down at repeat boundaries.
{: .comment}

---

#### Step 5: Aligning Contigs to Reference for IGV

Finally, we want to align our assembled fasta contigs back against the reference genome to visually spot missing structural parts or mismatches in IGV. We use `minimap2` with the `-ax asm5` preset, which is optimized for aligning highly accurate genome assemblies.

```bash
# Map the Flye assembly contigs
minimap2 -t 28 -ax asm5 ~/workdir/coursedata/reference.fasta ~/workdir/flye_output/assembly.fasta > ~/workdir/mappings/flye_vs_ref.sam
samtools view -S -b ~/workdir/mappings/flye_vs_ref.sam | samtools sort -o ~/workdir/mappings/flye_vs_ref_sorted.bam
samtools index ~/workdir/mappings/flye_vs_ref_sorted.bam

# Map the SPAdes assembly contigs
minimap2 -t 28 -ax asm5 ~/workdir/coursedata/reference.fasta ~/workdir/spades_output/scaffolds.fasta > ~/workdir/mappings/spades_vs_ref.sam
samtools view -S -b ~/workdir/mappings/spades_vs_ref.sam | samtools sort -o ~/workdir/mappings/spades_vs_ref_sorted.bam
samtools index ~/workdir/mappings/spades_vs_ref_sorted.bam
```

#### Verification in IGV:
1. Open **IGV**, and make sure your reference genome (`~/workdir/coursedata/reference.fasta`) is actively loaded.
2. Load both new alignment files via **File** -> **Load from File...**:
   * `~/workdir/mappings/flye_vs_ref_sorted.bam`
   * `~/workdir/mappings/spades_vs_ref_sorted.bam`
3. Inspect the alignment tracks to identify gaps or fragmentation points where the short-read assembly failed to recover structural elements.

---

## Improving the flye assembly and trying a hybrid assembly approach

### Short-Read Polishing with Polypolish

Even though modern ONT R10.4.1 chemistry combined with Dorado pushes raw read accuracy into the Q20 (>99%) range, long-read assemblies can still retain minor systematic errors. These errors are most frequently found in homopolymer runs (e.g., long stretches of AAAA), manifesting as small insertions or deletions (indels). To fix these remaining micro-errors, we can perform a process called **polishing** using highly accurate Illumina short reads.

We will use **Polypolish**, a short-read polishing tool designed specifically for long-read assemblies. 

> <comment-title>How Polypolish Avoids False Corrections</comment-title>
> Traditional polishers take all short-read alignments and use a consensus to alter the assembly. However, in repetitive genomic regions, short reads frequently misalign to the wrong repeat copy, leading the polisher to introduce errors rather than fix them. 
> 
> Polypolish solves this by examining the alternative alignments for each short read. If a read can map to multiple places in the assembly, Polypolish will only propose a correction if *all* possible target sites agree on the mismatch. If the mapping is ambiguous, it leaves the sequence untouched, preventing false corrections in repeat boundaries.
{: .comment}

To ensure Polypolish operates effectively, we must execute a specific multi-step pipeline:
1. Map short reads **separately** (R1 and R2 independently) using `bwa mem` with the `-a` option. This option forces the aligner to output *all* possible alignment locations for a read, not just the single best hit.
2. Run `polypolish filter` to calculate the expected insert size of read pairs and filter out low-confidence alignments.
3. Run `polypolish polish` to correct the assembly using the filtered pileups.

> <tip-title>Optional: How to install Polypolish</tip-title>
Run this (or follow instructions in github):
> ```bash
> wget https://github.com/rrwick/Polypolish/releases/download/v0.6.1/polypolish-linux-x86_64-musl-v0.6.1.tar.gz
> tar -xzvf polypolish-linux-x86_64-musl-v0.6.1.tar.gz
> sudo mv polypolish /usr/local/bin/
> ```
{: .tip}

---

### Hands-on: Polishing the Long-Read Assembly

#### Step 1: Mapping Short Reads with All Alignments Enabled

First, let's build the BWA index of our long-read genome assembly and map both Illumina forward and reverse files completely independently using the required `-a` flag:

```bash
# Index the Flye draft genome
bwa index ~/workdir/flye_output/assembly.fasta

# Create directory for polypolish files
mkdir polypolish
# Map R1 and R2 forward/reverse reads completely independently with the -a flag
bwa mem -t 28 -a ~/workdir/flye_output/assembly.fasta ~/workdir/coursedata/illumina/Barcode11_TSLF_S10_L001_R1_001.fastq.gz > ~/workdir/polypolish/polypolish_r1.sam
bwa mem -t 28 -a ~/workdir/flye_output/assembly.fasta ~/workdir/coursedata/illumina/Barcode11_TSLF_S10_L001_R2_001.fastq.gz > ~/workdir/polypolish/polypolish_r2.sam
```

#### Step 2: Filtering Alignments by Insert Size

Next, we pass our independent raw SAM files into Polypolish's filtering subcommand. This evaluates read pairing distances to clear away non-specific background mappings:

```bash
polypolish filter --in1 ~/workdir/polypolish/polypolish_r1.sam --in2 ~/workdir/polypolish/polypolish_r2.sam --out1 ~/workdir/polypolish/filtered_r1.sam --out2 ~/workdir/polypolish/filtered_r2.sam
```

#### Step 3: Executing the Final Consensus Polish

Now, we provide the original unpolished Flye assembly along with both freshly filtered alignment tracks to create our refined fasta file:

```bash
polypolish polish ~/workdir/flye_output/assembly.fasta ~/workdir/polypolish/filtered_r1.sam ~/workdir/polypolish/filtered_r2.sam > ~/workdir/polypolish/flye_polished.fasta
```

---

### Hybrid Assembly with SPAdes

Instead of assembling long reads first and polishing them later, a **hybrid assembly** combines both data types simultaneously into a single algorithmic workflow. 

We will use the hybrid mode of **SPAdes**. The SPAdes hybrid approach works as follows:
1. It builds a high-accuracy, highly-resolved **De Bruijn Graph** using only the pristine Illumina short reads.
2. It then maps the ONT long reads onto this graph. The long reads act as structural templates or "scaffolds" to bridge across repeat-induced gaps and resolve complex branches within the graph structure.

This approach combines the single-nucleotide accuracy of short reads with the structural spanning power of long reads seamlessly.

#### Step 4: Running Hybrid SPAdes

Execute the hybrid SPAdes pipeline by supplying both your paired-end short reads and your combined long-read datasets:

```bash
spades.py -1 ~/workdir/coursedata/illumina/Barcode11_TSLF_S10_L001_R1_001.fastq.gz \
          -2 ~/workdir/coursedata/illumina/Barcode11_TSLF_S10_L001_R2_001.fastq.gz \
          --nanopore ~/workdir/coursedata/ont.fastq.gz \
          -o ~/workdir/spades_hybrid_output --threads 28
```

---

### Hands-on: Comprehensive Assembly Evaluation

We now have four distinct assembly variants tracking our target genome. Let's run a final comparative evaluation with QUAST to see how polishing and hybrid strategies alter genome completeness and accuracy metrics.

The 4 assembly variants to evaluate are:
1. `flye_output/assembly.fasta` (ONT Long-Reads Only)
2. `spades_output/scaffolds.fasta` (Illumina Short-Reads Only)
3. `flye_polished.fasta` (ONT Long-Reads Polished with Short-Reads)
4. `spades_hybrid_output/contigs.fasta` (Hybrid Co-Assembly)

#### Step 5: Comparing all Four Frameworks in QUAST

Run QUAST with all four assembly files against the true reference genome:

```bash
quast.py ~/workdir/flye_output/assembly.fasta \
         ~/workdir/spades_output/contigs.fasta \
         ~/workdir/polypolish/flye_polished.fasta \
         ~/workdir/spades_hybrid_output/contigs.fasta \
         -l "flye,spades,polypolish,hybrid_spades" \
         -r ~/workdir/coursedata/reference.fasta \
         -t 28 \
         -o ~/workdir/quast_final_output
```

Open the resulting dashboard summary report in your browser:

```bash
firefox ~/workdir/quast_final_output/report.html
```

> <question-title>Evaluating the Impact of Polishing and Hybridization</question-title>
> Compare the column profiles of the unpolished Flye assembly vs. the polished Flye assembly. Look at metrics like "mismatches per 100 kbp" or "indels per 100 kbp". What changes do you observe? How does the Hybrid assembly compare in contig count?
> 
> > <solution-title>Solution</solution-title>
> > Polishing with Polypolish typically causes a significant drop in the number of indels per 100 kbp compared to raw Flye contigs, which often restores disrupted open reading frames and increases the total number of fully recovered genes. The Hybrid SPAdes assembly often improves in contiguity, but depending on repeat complexity, it may still contain a few more contig fragments than Flye's completely closed loop structure.
> {: .solution}
{: .question}

---

## Genome Annotation

### Introduction to Prokaryotic Genome Annotation

Once you have successfully assembled and polished a bacterial chromosome, it consists simply of a long, uncharacterized string of nucleotides (A, C, G, T). To make this data useful for biological research, you must perform **genome annotation**. This process involves identifying the structural features of the genome—such as protein-coding sequences (CDS), transfer RNAs (tRNAs), and ribosomal RNAs (rRNAs)—and assigning functional biological identities to them based on sequence similarity to known databases.

In this module, we will compare two popular tools used for this task:

* **Prokka:** For nearly a decade, Prokka has been the legacy workhorse tool for rapid prokaryotic genome annotation. It coordinates an ensemble of open-source tools (like Prodigal for CDS finding and Aragorn for tRNAs) to generate comprehensive annotation suites in minutes. However, because its internal reference databases are no longer actively maintained, it often over-assigns generic functional names or labels proteins as "hypothetical protein".

> <tip-title>Optional: How to install Prokka</tip-title>
It's quite complicated to install without conda/docker/singularity. Check out the github and use one of those methods.
{: .tip}

* **Bakta:** A modern, next-generation annotation platform designed specifically for microbial genomes. Bakta addresses Prokka's database stagnation by utilizing a thoroughly curated, regularly updated SQLite database synchronized with NCBI RefSeq, UniProt, and specialized feature resources. It provides highly accurate protein names, precise cross-reference tags (DBXrefs), and native tracking of non-coding RNAs (ncRNAs), pseudogenes, and antimicrobial resistance (AMR) gene identifiers.

> <tip-title>Optional: How to install Bakta</tip-title>
It's quite complicated to install without conda/docker/singularity. Check out the github and use one of those methods.
{: .tip}
---

### Hands-on: Annotating Your Assembly

We will run both annotators on our polished long-read assembly (`flye_polished.fasta`) and evaluate how their structural findings and functional naming conventions differ.

#### Step 1: Running Prokka

Execute Prokka by specifying an output directory and a custom file prefix:

```bash
prokka --cpus 28 --outdir ~/workdir/prokka_output --prefix prokka_ont ~/workdir/polypolish/flye_polished.fasta
```

Don;t worry about the `Could not run command: tbl2asn` message if it appears. We don't need the `asn` file.

#### Step 2: Running Bakta

Unlike Prokka, Bakta relies on a separate, heavy database containing millions of curated proteins. For this workshop, this database has been pre-staged for you. Run Bakta using the following command:

```bash
conda activate bakta
bakta --threads 28 --db ~/bakta_db/db-light --output ~/workdir/bakta_output ~/workdir/polypolish/flye_polished.fasta 
conda deactivate
source ~/longread/bin/activate
```

---

### Hands-on: Comparing Annotation Profiles

Both tools generate various standardized outputs, including GFF3, GenBank, and FASTA files. To quickly benchmark their structural predictions, we can review the text-based summary logs (`.txt`) produced by each pipeline.

#### Step 3: Inspecting Summary Outputs

Use `cat` to print out both overview profiles in your terminal:

```bash
# View the Prokka summary report
cat ~/workdir/prokka_output/prokka_ont.txt

# View the Bakta summary report
cat ~/workdir/bakta_output/bakta_ont.txt
```

> <question-title>Analyzing Annotation Discrepancies</question-title>
> Look closely at the total counts of Coding Sequences (CDS), tRNAs, and rRNAs in both outputs. Are the numbers identical? If they differ, what could cause one tool to predict more genes than the other?
> 
> > <solution-title>Solution</solution-title>
> > Even though they use the same underlying software for core gene finding (Prodigal), the total counts often differ slightly. Bakta uses stricter structural filters and a much larger database, allowing it to accurately split overlapping reading frames, filter out false positive predictions, and identify specialized elements like pseudogenes or small non-coding RNAs that Prokka completely misses.
> {: .solution}
{: .question}

#### Step 4: Comparing Functional Descriptions

A major difference lies in how specifically proteins are named. Let's use `grep` to check how many genes were left uncharacterized as "hypothetical protein" in both annotation suites:

```bash
# Count hypothetical proteins in Prokka's GFF output
grep -c "hypothetical protein" ~/workdir/prokka_output/prokka_ont.gff

# Count hypothetical proteins in Bakta's GFF output
grep -c "hypothetical protein" ~/workdir/bakta_output/bakta_ont.gff
```

> <comment-title>Interpreting Naming Quality</comment-title>
> You will notice that Bakta significantly reduces the fraction of "hypothetical protein" labels compared to Prokka. Thanks to its modern reference integration with UniProt and RefSeq, Bakta can assign definitive, functional gene names to sequences where Prokka could only find vague, outdated family matches.
{: .comment}

---

### Comparative Genomics with EDGAR

Once individual genomes are annotated, the next logical milestone is to explore how multiple strains or species relate to one another. For this downstream phase, we shift from localized command-line annotation to web-based comparative genomics using **EDGAR** (Efficient Database framework for comparative Genome Analyses).

* **Official Server Link:** [http://edgar3.computational.bio](http://edgar3.computational.bio)

#### How EDGAR Works:
EDGAR is a fully automated high-throughput platform tailored for the deep comparative analysis of prokaryotic genomes. Users upload their fully annotated genome files (such as the `.gff` or GenBank files generated by Bakta) into public or password-protected private projects. 

The underlying pipeline performs intensive all-versus-all sequence alignments across all selected strains. By evaluating **BLAST Score Ratios (BSR)**, EDGAR accurately determines orthology relational paths to delineate specific genomic subsets:
1. **The Core Genome:** The conserved set of genes shared identically across *all* analyzed organisms, often used to build highly precise core-genome phylogenetic trees.
2. **The Pan-Genome:** The complete global pool of all unique genes present across the entire group.
3. **Singleton Genes:** Unique genes present in only *one* specific strain, which are crucial for identifying specific downstream traits like pathogenicity islands or unique metabolic capabilities.

Furthermore, EDGAR calculates average nucleotide identity (ANI) metrics and renders publication-ready  visualizations, including Venn diagrams, UpSet plots, and synteny maps mapping gene order conservation across syntenic chromosomal layouts.

---

## APPENDIX: References for tools used within the tutorial

* **Dorado (Basecalling Platform):**
  * **GitHub:** [https://github.com/nanoporetech/dorado](https://github.com/nanoporetech/dorado)
* **POD5-Tools (File Manipulation Toolkit):**
  * **GitHub:** [https://github.com/nanoporetech/pod5-file-format](https://github.com/nanoporetech/pod5-file-format)
* **FastQC (Quality Control Analysis):**
  * **Homepage:** [https://www.bioinformatics.babraham.ac.uk/projects/fastqc/](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
* **fastplong (Ultrafast Long-Read Preprocessor & Filtering toolkit):**
  * **GitHub:** [https://github.com/OpenGene/fastplong](https://github.com/OpenGene/fastplong)
  * **Publication:** *Chen, S. (2023). fastplong: An ultra-fast all-in-one tool for long-read sequencing data quality control and preprocessing. iMeta.*
* **NanoPlot (Long-read Quality Plotting):**
  * **GitHub:** [https://github.com/wdecoster/NanoPlot](https://github.com/wdecoster/NanoPlot)
  * **Publication:** *De Coster, W. et al. (2018). NanoPack: visualizing and processing long-read sequencing data. Bioinformatics.*
* **Minimap2 (Versatile Sequence Aligner):**
  * **GitHub:** [https://github.com/lh3/minimap2](https://github.com/lh3/minimap2)
  * **Publication:** *Li, H. (2018). Minimap2: pairwise alignment for nucleotide sequences. Bioinformatics.*
* **BWA (Burrows-Wheeler Aligner for Short Reads):**
  * **GitHub:** [https://github.com/lh3/bwa](https://github.com/lh3/bwa)
  * **Publication:** *Li, H. & Durbin, R. (2009). Fast and accurate short read alignment with Burrows-Wheeler transform. Bioinformatics.*
* **Samtools (Alignment File Processing utilities):**
  * **Homepage:** [https://www.htslib.org/](https://www.htslib.org/)
  * **Publication:** *Danecek, P. et al. (2021). Twelve years of SAMtools and BCFtools. GigaScience.*
* **IGV (Integrative Genomics Viewer):**
  * **Homepage:** [https://software.broadinstitute.org/software/igv/](https://software.broadinstitute.org/software/igv/)
  * **Publication:** *Robinson, J. T. et al. (2011). Integrative Genomics Viewer. Nature Biotechnology.*
* **Flye**
  * **GitHub:** [https://github.com/fenderglass/Flye](https://github.com/fenderglass/Flye)
  * **Publication:** *Kolmogorov, M. et al. (2019). Assembly of long, error-prone reads using repeat graphs. Nature Biotechnology.*
* **SPAdes**
  * **GitHub:** [https://github.com/ablab/spades](https://github.com/ablab/spades)
  * **Publication:** *Bankevich, A. et al. (2012). SPAdes: a new genome assembly algorithm and its applications to single-cell sequencing. Journal of Computational Biology.*
* **QUAST**
  * **GitHub:** [https://github.com/ablab/quast](https://github.com/ablab/quast)
  * **Publication:** *Gurevich, A. et al. (2013). QUAST: quality assessment tool for genome assemblies. Bioinformatics.*
* **Bandage**
  * **GitHub:** [https://github.com/rrwick/Bandage](https://github.com/rrwick/Bandage)
  * **Publication:** *Wick, R. R. et al. (2015). Bandage: interactive visualization of de novo genome assembly graphs. Bioinformatics.*
* **Polypolish (Short-read Polisher for Long-read Assemblies):**
  * **GitHub:** [https://github.com/rrwick/Polypolish](https://github.com/rrwick/Polypolish)
  * **Publication:** *Wick, R. R. & Holt, K. E. (2022). Polypolish: Short-read polishing of long-read bacterial genome assemblies. PLoS Computational Biology.*
* **SPAdes (Hybrid Assembly Mode Support):**
  * **GitHub:** [https://github.com/ablab/spades](https://github.com/ablab/spades)
  * **Publication:** *Antipov, D. et al. (2016). hybridSPAdes: an algorithm for genome assembly from microbial long and short reads. Bioinformatics.*
* **Prokka (Rapid Prokaryotic Genome Annotation):**
  * **GitHub:** [https://github.com/tseemann/prokka](https://github.com/tseemann/prokka)
  * **Publication:** *Seemann, T. (2014). Prokka: rapid prokaryotic genome annotation. Bioinformatics.*
* **Bakta (Next-generation Microbial Genome Annotation):**
  * **GitHub:** [https://github.com/oschwenders/bakta](https://github.com/oschwenders/bakta)
  * **Publication:** *Schwengers, O. et al. (2021). Bakta: rapid and standardized annotation of bacterial genomes and plasmids. Microbial Genomics.*
* **EDGAR (Comparative Genomics Framework):**
  * **Webserver Platform:** [http://edgar3.computational.bio](http://edgar3.computational.bio)
  * **Publication:** *Dieckmann, M. A. et al. (2021). EDGAR 3.0: comparative genomics and phylogenomics on a scalable infrastructure. Nucleic Acids Research.*
