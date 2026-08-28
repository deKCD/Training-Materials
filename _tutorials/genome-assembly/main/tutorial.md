---
layout: tutorial_hands_on
title: Assembly and assembly evaluation (hands-on)
description: "This tutorial demonstrates how to assemble a prokaryotic genome using Oxford Nanopore and Illumina sequencing data, evaluate assembly quality, improve assemblies through polishing and hybrid assembly approaches, and assess the final results."
time_estimation: 2H
level: beginner
keywords: flye, SPAdes, QUAST, polypolish, hybrid assembly
questions:
  - "What are the core differences between De Bruijn Graph (DBG) and Overlap-Layout-Consensus (OLC) assembly approaches?"
  - "How do I perform a long-read assembly with Flye and a short-read assembly with SPAdes?"
  - "How can we improve a long-read assembly via short-read polishing with Polypolish?"
  - "What is a hybrid assembly approach, and how does SPAdes execute it?"
  - "How do I evaluate and compare multiple assemblies using QUAST and Bandage?"
objectives:
  - "Reconstruct a bacterial genome using Flye and SPAdes, and visually evaluate assembly graph topologies in Bandage."
  - "Execute the multi-step Polypolish workflow (all-mapping, filtering by insert size, and polishing) to correct homopolymer indels."
key_points:
  - "Long reads effortlessly resolve repetitive genomic structures via the OLC paradigm, allowing Flye to assemble fully closed circular bacterial chromosomes."
  - "Polypolish guards against false corrections in repeat regions by only proposing sequence fixes if all alternative short-read alignments agree on the mismatch."
  - "Hybrid co-assembly leverages highly accurate short-read graphs while using long reads as structural scaffolds to resolve complex repeat branches."
version: main
life_cycle: under development
contributions:
  authorship:
  - Nils Kleinbölting
  editing: 
  - Dilfuza Djamalova
  funding:
---

This tutorial demonstrates how to assemble a prokaryotic genome using Oxford Nanopore and Illumina sequencing data, evaluate assembly quality, improve assemblies through polishing and hybrid assembly approaches, and assess the final results. The sequencing reads generated in the previous tutorial, [Basecalling and QC of ONT data]({{ site.url }}{{ site.baseurl }}/tutorials/nanopore/main/tutorial/), will be used as input for all analyses. The resulting polished genome assembly will serve as the starting point for the subsequent [Prokaryotic Genome Annotation (hands-on)]({{ site.url }}{{ site.baseurl }}/tutorials/genome-annotation/main/tutorial/) tutorial.

><details-title>Prerequisites</details-title>
> - Please complete the [Unix/Linux introduction tutorial]({{ site.url }}{{ site.baseurl }}/tutorials/unix-course/main/tutorial/) before this tutorial. 
> - We assume you have successfully connected to an instance in the de.NBI cloud with the software pre-installed. Otherwise you will need to install the required tools on your own and make sure you have sufficient resources available. 
> - Throughout the course we assume you are working on data downloaded to a volume under `/vol/longread/`, we create a link `~/workdir/` to that  folder, if you are working somewhere else, adjust the `~/workdir` link to that location and all commands should work as outlined in the course.
> - We also assume that you have a machine with **28 cores** available, if not - adjust the commands that specify a certain number of threads / cores accordingly.
{: .details}


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

## APPENDIX: References for tools used within the tutorial
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