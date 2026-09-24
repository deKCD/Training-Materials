---
layout: tutorial_hands_on
title: "Introduction to the Metagenomics-Toolkit"
description: "This tutorial will guide you through the first steps to run the Metagenomics-Toolkit on paired-end metagenomic sequencing data. It covers pipeline configuration, execution, result inspection, and interactive analysis with Jupyter notebooks."
time_estimation: 1H
level: beginner
keywords: Metagenomics, Metagenomics-Toolkit, Nextflow, QC, Assembly, Binning, Annotation, Short-read, Illumina
questions:
- "How do I configure and execute the Metagenomics-Toolkit pipeline for paired-end metagenomic data?"
- "What does the entrypoint and output architecture of the Metagenomics-Toolkit look like?"
- "How do I prepare a short-read sample sheet for the automated per-sample pipeline?"
objectives:
- "Configure YAML parameter files for a multi-module metagenomics pipeline including QC, assembly, binning and annotation."
- "Execute the full pipeline with Nextflow and understand the role of entry points."
- "Navigate the hierarchical output structure of the Toolkit and locate key analysis results."
- "Explore and visualize binning results, MAG quality metrics, and taxonomy with a Jupyter Notebook."
key_points:
- "Nextflow profiles allow seamless transitions between running on a single machine (`standard`) or a cluster environment (`slurm`)."
- "Short-read sample sheets use a paired-end schema with separate columns for forward (READS1) and reverse (READS2) fastq files."
- "The Metagenomics-Toolkit organizes results into a standardized, deterministic folder structure separating logs, tools, and specific module versions."
- "The full pipeline integrates QC, assembly, binning, and annotation modules across per-sample and aggregation stages."
- "The notebook exports MAG fastas and produces overview plots for bin quality, taxonomy, and abundance."
version:
  - main
life_cycle: under development
contributions:
  authorship:
  - Nils Kleinbölting
  editing: 
  - Dilfuza Djamalova
  funding:
---

This tutorial is a very short introduction to the Metagenomics-Toolkit which shows the main steps in analysing Illumina short-read metagenomics data using the Metagenomics-Toolkit.
A more detailed introduction and tutorials can be found [here](https://metagenomics.github.io/metagenomics-tk/latest/). 
In this part you will learn how to configure and run the Toolkit and what the output of a Toolkit run looks like.

## Tutorial Scope and Requirements

The Metagenomics-Toolkit allows you to run either the full pipeline of assembly, binning, and many other downstream analysis tasks or the individual analyses separately. 
In this tutorial you will only use the *full pipeline* mode. The *full pipeline* mode itself is structured into two parts. The first part runs the Toolkit on each
sample separately (*per-sample*), and the second part runs a combined downstream analysis on the output of the *per-sample* runs; this step is called *aggregation*. We will only run a few tools of the *per sample* part of the pipeline.
While there are several optimizations for running the Toolkit on a cloud-based setup, 
during this workshop you will run the Toolkit on a single machine.

><details-title>Requirements</details-title>
>* Please complete the [Unix/Linux introduction tutorial]({{ site.url }}{{ site.baseurl }}/tutorials/unix-course/main/tutorial/) before this tutorial.
>* This tutorial has been tested on a machine with 28 CPUs and 64 GB of RAM with Ubuntu installed on it.
>* Docker: Install Docker by following the official Docker installation [instructions](https://docs.docker.com/engine/install/ubuntu/).
>* Java: In order to run Nextflow, you need to install Java on your machine, which can be achieved via `sudo apt install default-jre`.
>* Nextflow should be installed. Please check the official Nextflow [instructions](https://www.nextflow.io/docs/latest/install.html#install-nextflow).
>* Throughout the course we assume you are working on data downloaded to a volume under `/vol/mgcourse/`, we create a link `~/workdir/` to that  folder, if you are working somewhere else, adjust the `~/workdir` link to that location and all commands should work as outlined in the course.
>* We also assume that you have a machine with **28 cores** and **64GB of RAM** available, if not - adjust the configuration that specifies a certain number of cores/memory accordingly.
{: .details}

### **Download the data and preparations**

First **(if not already done)**, create a link to `/vol/mgcourse` (or the folder in which you want to work during the course) and switch to that directory:

```bash
ln -s /vol/mgcourse/ ~/workdir
cd ~/workdir
```

You might need to change the permissions of `/vol/mgcourse`, for example (in the cloud setup we use for the on-site course) with:

```bash
# Adjust accordingly to your setup
sudo chown ubuntu:ubuntu /vol/mgcourse/
```

Next, we create a folder for our Metagenomics Toolkit tutorial:

```bash
cd ~/workdir
mkdir mgtk
cd ~/workdir/mgtk/
```

Then we download and extract ONE of the datasets below - pick one!
```bash
cd ~/workdir/mgtk/

wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/data/DMC_BGA22_4_N_75MB.tar.gz
tar -xzvf DMC_BGA22_4_N_75MB.tar.gz

wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/data/DMC_BGA52_4_N_75MB.tar.gz
tar -xzvf DMC_BGA52_4_N_75MB.tar.gz

wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/data/LF_Silphie_R1_75MB.tar.gz
tar -xzvf LF_Silphie_R1_75MB.tar.gz

wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/data/P2_F1_R1_75MB.tar.gz
tar -xzvf P2_F1_R1_75MB.tar.gz

wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/data/P7-F1_R1_75MB.tar.gz
tar -xzvf P7-F1_R1_75MB.tar.gz

wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/data/PB22_180226_F1_R1_75MB.tar.gz
tar -xzvf PB22_180226_F1_R1_75MB.tar.gz

wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/data/PB37_180322_F_R1_75MB.tar.gz
tar -xzvf PB37_180322_F_R1_75MB.tar.gz

wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/data/P9_F1_T1_R1_75MB.tar.gz
tar -xzvf P9_F1_T1_R1_75MB.tar.gz
```


## Metagenomics-Toolkit Introduction

### Execution

The Toolkit is based on Nextflow and can be executed with the following command-line pattern:

```bash
NXF_VER=NEXTFLOW_VERSION nextflow run metagenomics/metagenomics-tk NEXTFLOW_OPTIONS TOOLKIT_OPTIONS 
```

* `NEXTFLOW_VERSION` is the Nextflow version supported (or required) by the Toolkit. Every code snippet in this tutorial has a hard-coded version number. 
  If you ever choose the wrong version, then the Toolkit will print out the versions that are supported.

* `NEXTFLOW_OPTIONS` are options that are implemented by Nextflow:

    * `-profile` determines the technology which is used to execute the Toolkit. Here we support **standard** for running the workflow on a single machine and
                 **slurm** for running the Toolkit on a cluster which uses [SLURM](https://slurm.schedmd.com/documentation.html) to distribute jobs. 

	* `-params-file` points to a configuration file that tells the Toolkit which analyses to run and which resources it should use. An example configuration file will be explained in the next section.

    * `-resume` In some cases, you may want to resume the workflow execution, such as when you add an analysis.
                  Resuming the workflow forces Nextflow to reuse the results of the previous analyses that the new analysis depends on, rather than starting from scratch. 

	* `-ansi-log` accepts a boolean (default: **true**) that, when set to **true**, tells Nextflow to print every update as a new line on the terminal. If **false** then Nextflow
                  prints a line for every process and updates the specific line on an update. We recommend setting **-ansi-log** to **false** because it is not possible to
                  print all possible processes on a terminal at once when running the Toolkit.

	* `-entry` specifies which entrypoint Nextflow should use to run the workflow. To run the *full pipeline* that you will use in this workshop, use the **wFullPipeline** entrypoint. 
               If you ever want to run separate modules, you can check on the modules-specific page (e.g. [assembly](https://metagenomics.github.io/metagenomics-tk/latest/modules/assembly/)).

* `TOOLKIT_OPTIONS` are options that are provided by the Toolkit. All Toolkit options are either in a configuration file or can be provided on the command line which will be explained in the following section. 


> <question-title>Find entrypoint</question-title>
> Open the Metagenomics-Toolkit wiki in a second browser tab by clicking this
> [link](https://metagenomics.github.io/metagenomics-tk/latest/){:target="_blank"}.
> Imagine you need to run the quality-control part separately for this dataset. Can you tell the name of the **entrypoint**? 
> Use the wiki page you have opened on another tab to answer the question.
> > <solution-title>Solution</solution-title>
> > If you navigate to the [quality control](https://metagenomics.github.io/metagenomics-tk/latest/modules/qualityControl/) section, you will find the **wOntQualityControl** entrypoint designated for Oxford Nanopore long reads (while **wShortReadQualityControl** is kept for short-read data).
> > 
> {: .solution}
>
{: .question}

### Configuration

The Toolkit uses a YAML configuration file that specifies global parameters, the analyses that will be executed and the computational resources that can be used. 

The configuration file is divided into three parts:

#### Part 1: Global Workflow Parameters

The following snippet shows parameters that affect the whole execution of the 
workflow. All parameters are explained in a dedicated Toolkit wiki [section](https://metagenomics.github.io/metagenomics-tk/latest/configuration/). 

```bash
tempdir: "tmp"
summary: false
s3SignIn: false 
input:
  paired:
    sheet: "test_data/tutorials/tutorial1/reads.tsv"
    watch: false
output: output
logDir: log
runid: 1
databases: "/vol/scratch/databases"
publishDirMode: "symlink"
logLevel: 1
scratch: false 
```

> <tip-title>Computational Resources</tip-title>
> Please note that computational resources are also global parameters and will be handled in the third part of this configuration section. 
{: .tip}
    

##### Input Field

The input field specifies the type of input data to process (Nanopore, Illumina, data hosted on SRA or a mirror)
and you can find a dedicated wiki section [here](https://metagenomics.github.io/metagenomics-tk/latest/pipeline_input/). Regardless of which input type
is used, the user must provide a file containing a list of datasets to be processed.
The list can be a list of remote or local files and in the case of SRA, a list of SRA run IDs.

Since you will work with Illumina read data in this tutorial, your input sample sheet contains forward and reverse reads and looks like this: 

```bash
SAMPLE    READS1  READS2
sample1   /path/to/sample1_R1.fastq.gz  /path/to/sample1_R2.fastq.gz
sample2   /path/to/sample2_R2.fastq.gz  /path/to/sample1_R2.fastq.gz
```

The first column (SAMPLE) specifies the unique name of the dataset. The second and third column (READS1/READS2) specifies the forward and reverse reads.
When working with Nanopore long-read data, your input sample sheet would look like this:

```bash
SAMPLE    READS
sample1   /path/to/sample1_ont.fastq.gz
sample2   /path/to/sample2_ont.fastq.gz
```

The first column (SAMPLE) specifies the unique name of the dataset. The second column (READS) specifies the single file pathway containing the long-read sequence strings.

#### Part 2: Toolkit Analyses Steps 

Analyses (also called modules) that the Toolkit executes are placed directly under the **steps** attribute in the configuration file.
In the example below, the modules **qc** and **assembly** are placed directly under the **steps** attribute. Any tools or methods
that are used as part of the module can be considered a property of the module. For example, assemblers like **Flye** (or metaFlye), MEGAHIT etc. are executed as part of the assembly module.
The level below the tool names is for configuring the tools and methods. Each analysis is listed on the [modules page](https://metagenomics.github.io/metagenomics-tk/latest/modules/introduction/).

```bash
steps:
  qc:
    fastp:
       # For PE data, the adapter sequence auto-detection is disabled by default since the adapters can be trimmed by overlap analysis. However, you can specify --detect_adapter_for_pe to enable it.
       # For PE data, fastp will run a little slower if you specify the sequence adapters or enable adapter auto-detection, but usually result in a slightly cleaner output, since the overlap analysis may fail due to sequencing errors or adapter dimers.
       # -q, --qualified_quality_phred       the quality value that a base is qualified. Default 15 means phred quality >=Q15 is qualified.
       # --cut_front move a sliding window from front (5') to tail, drop the bases in the window if its mean quality is below cut_mean_quality, stop otherwise.
       # --length_required  reads shorter than length_required will be discarded, default is 15. (int [=15])
       # PE data, the front/tail trimming settings are given with -f, --trim_front1 and -t, --trim_tail1
       additionalParams:
         fastp: " --detect_adapter_for_pe -q 20 --cut_front --trim_front1 3 --cut_tail --trim_tail1 3 --cut_mean_quality 10 --length_required 50 "
         reportOnly: false
       timeLimit: "AUTO"
    nonpareil:
      additionalParams: " -v 10 -r 1234 "
    filterHuman:
      additionalParams: "  "
      database:
        download:
          source: https://openstack.cebitec.uni-bielefeld.de:8080/databases/human_filter.db.20231218v2.gz
          md5sum: cc92c0f926656565b1156d66a0db5a3c
  assembly:
    megahit:
      # --mem-flag 0 to use minimum memory, --mem-flag 1 (default) moderate memory and --mem-flag 2 all memory.
      # meta-sensitive: '--min-count 1 --k-list 21,29,39,49,...,129,141' 
      # meta-large:  '--k-min  27  --k-max 127 --k-step 10' (large & complex metagenomes, like soil)
      additionalParams: " --min-contig-len 500 --presets meta-sensitive "
      fastg: true
      resources:
        RAM:
          mode: 'PREDICT'
          predictMinLabel: 'highmemLarge'
```

#### Part 3: Computational Resources

The third part of a Toolkit configuration file is the **resources** attribute.
The **resources** attribute lists computational resource configurations, where each configuration has a label and consists of the number of CPUs and amount of RAM assigned to it.
Predefined labels are listed in the following example snippet. These labels are assigned to the processes that run the workflow-specific tools.
You can read more about resource parameters [here](../../configuration.md/#configuration-of-computational-resources-used-for-pipeline-runs).

```bash
resources:
  highmemLarge:
    cpus: 28
    memory: 60
  highmemMedium:
    cpus: 14
    memory: 30
  large:
    cpus: 28
    memory: 58
  medium:
    cpus: 14
    memory: 29
  small:
    cpus: 7
    memory: 14
  tiny:
    cpus: 1
    memory: 1
```

#### Configuration File vs. Command-line Parameters

All parameters defined in the YAML configuration file can also be supplied as command-line arguments. To do this, prefix each parameter with a double dash (--). 
If a parameter is nested within the hierarchy of the YAML file, represent it as a command-line argument by connecting each level of the hierarchy using a dot (.).

For example, consider the CPU count of the *highmemLarge* resource label in the previous snippet.
The corresponding command-line argument would be `--resources.highmemLarge.cpus`.

Command-line arguments supersede the configuration file. This is a quick way to change variables without touching files. 


### Output

The Toolkit output fulfills the following schema:

```bash
SAMPLE_NAME/RUN_ID/MODULE/MODULE_VERSION/TOOL
```

* `RUN_ID`: The run ID will be part of the output path and allows to distinguish between different pipeline configurations that were used for the same dataset.

* `MODULE` is the analysis that is executed by the Toolkit (e.g., qc, assembly, etc.). 

* `MODULE_VERSION` is the version number of the module.

* `TOOL` is the tool or method that is executed by the Toolkit.

Below you can see an example output structure configured for short-read data.
Every output folder includes four log files:

* `.command.err`: Contains the standard error.

* `.command.out`: Contains the standard output. 

* `.command.log`: Contains the combined standard error and standard output.

* `.command.sh`: Contains the command that was executed. 

```bash
output/
├── P7
│   └── 1
│       ├── qc
│       │   └── 0.4.1
│       │       └── fastp
│       │           ├── P7_fastp.json 
│       │           ├── P7_fastp_summary_after.tsv 
│       │           ├── P7_fastp_summary_before.tsv
│       │           ├── P7_interleaved.qc.fq.gz
│       │           ├── P7_report.html 
│       │           ├── P7_unpaired.qc.fq.gz
│       │           └── P7_unpaired_summary.tsv 
│       ├── assembly
│       │   └── 1.2.3
│       │       └── megahit
│       │           ├── P7_contigs.fa.gz 
│       │           ├── P7_contigs.fastg 
│       │           └── P7_contigs_stats.tsv 
│      ...
```

### Metagenomics-Toolkit Execution 

We will now proceed with actually running the QC, assembly, binning and annotation part of the toolkit. The dataset we use is quite small, so don't expect too much.

#### Create the samplesheet

First, we define a samplesheet in your working directory. Switch to the `mgtk` directory:

```bash
cd ~/workdir/mgtk
```

Then create the samplesheet file `samples.tsv` according to the dataset you downloaded above. Choose exactly **one** of the following samplesheets:

---

**Option 1: DMC_BGA22_4_N**

```bash
cat > samples.tsv << EOF
SAMPLE	READS1	READS2
DMC_BGA22_4_N	/vol/mgcourse/mgtk/WGS/DMC_BGA22_4_N_75MB_R1.fastq.gz	/vol/mgcourse/mgtk/WGS/DMC_BGA22_4_N_75MB_R2.fastq.gz
EOF
```

**Option 2: DMC_BGA52_4_N**

```bash
cat > samples.tsv << EOF
SAMPLE	READS1	READS2
DMC_BGA52_4_N	/vol/mgcourse/mgtk/WGS/DMC_BGA52_4_N_75MB_R1.fastq.gz	/vol/mgcourse/mgtk/WGS/DMC_BGA52_4_N_75MB_R2.fastq.gz
EOF
```

**Option 3: LF_Silphie_R1**

```bash
cat > samples.tsv << EOF
SAMPLE	READS1	READS2
LF_Silphie_R1	/vol/mgcourse/mgtk/WGS/LF_Silphie_R1_75MB_R1.fastq.gz	/vol/mgcourse/mgtk/WGS/LF_Silphie_R1_75MB_R2.fastq.gz
EOF
```

**Option 4: P2_F1_R1**

```bash
cat > samples.tsv << EOF
SAMPLE	READS1	READS2
P2_F1_R1	/vol/mgcourse/mgtk/WGS/P2_F1_R1_75MB_R1.fastq.gz	/vol/mgcourse/mgtk/WGS/P2_F1_R1_75MB_R2.fastq.gz
EOF
```

**Option 5: P7-F1_R1**

```bash
cat > samples.tsv << EOF
SAMPLE	READS1	READS2
P7_F1_R1	/vol/mgcourse/mgtk/WGS/P7-F1_R1_75MB_R1.fastq.gz	/vol/mgcourse/mgtk/WGS/P7-F1_R1_75MB_75MB_R2.fastq.gz
EOF
```

**Option 6: PB22_180226_F1_R1**

```bash
cat > samples.tsv << EOF
SAMPLE	READS1	READS2
PB22_180226	/vol/mgcourse/mgtk/WGS/PB22_180226_F1_R1_75MB_R1.fastq.gz	/vol/mgcourse/mgtk/WGS/PB22_180226_F1_R1_75MB_R2.fastq.gz
EOF
```

**Option 7: PB37_180322_F_R1**

```bash
cat > samples.tsv << EOF
SAMPLE	READS1	READS2
PB37_180322	/vol/mgcourse/mgtk/WGS/PB37_180322_F_R1_75MB_R1.fastq.gz	/vol/mgcourse/mgtk/WGS/PB37_180322_F_R1_75MB_R2.fastq.gz
EOF
```

**Option 8: P9_F1_T1_R1**

```bash
cat > samples.tsv << EOF
SAMPLE	READS1	READS2
P9_F1_T1	/vol/mgcourse/mgtk/WGS/P9_F1_T1_R1_75MB_R1.fastq.gz	/vol/mgcourse/mgtk/WGS/P9_F1_T1_R1_75MB_R2.fastq.gz
EOF
```
P9_F1_T1_R1
---

> <tip-title>Verify your samplesheet</tip-title>
> After creating your `samples.tsv`, verify the file contains tab-separated columns and that the file paths point to existing files:
> ```bash
> cat samples.tsv
> ls -lh /vol/mgcourse/mgtk/WGS/*_R1.fastq.gz
> ls -lh /vol/mgcourse/mgtk/WGS/*_R2.fastq.gz
> ```
> Make sure the files actually exist before proceeding. Adjust the paths in the samplesheet if your directory structure differs.
> {: .tip}

#### Create the configuration

Next we define a configuration yaml file with the above mentioned steps and proper resource definitions:
**Important:** Adjust the path if your is not `/vol/mgcourse/`.

```bash
cd ~/workdir/mgtk/
gedit config.yml
```

Paste the following code into the file:

```bash
tempdir: "tmp"
s3SignIn: true
input:
  paired:
    sheet: "/vol/mgcourse/mgtk/samples.tsv"
    watch: false
output: output_test
logDir: log
runid: 1
databases: "/vol/mgcourse/databases"
publishDirMode: "symlink"
logLevel: 1
scratch: "/vol/mgcourse/scratch/"
steps:
  qc:
    fastp:
       additionalParams:
         fastp: " --detect_adapter_for_pe -q 20 --cut_front --trim_front1 3 --cut_tail --trim_tail1 3 --cut_mean_quality 10 --length_required 50 "
         reportOnly: false
       timeLimit: "AUTO"
  assembly:
    megahit:
      additionalParams: " --min-contig-len 1000 --presets meta-sensitive "
      fastg: true
      resources:
        RAM:
          mode: 'DEFAULT'
          predictMinLabel: 'highmemLarge'
  binning:
    bwa2:
      additionalParams:
        bwa2: " "
        # samtools flags are used to filter resulting bam file
        samtoolsView: " -F 3584 "
    contigsCoverage:
      additionalParams: " --min-covered-fraction 0 --min-read-percent-identity 100 --min-read-aligned-percent 100 "
    genomeCoverage:
      additionalParams: " --min-covered-fraction 0 --min-read-percent-identity 100 --min-read-aligned-percent 100 "
    # Primary binning tool
    metabat:
      # Set --seed positive numbers to reproduce the result exactly. Otherwise, random seed will be set each time.
      additionalParams: " --seed 234234  "
  annotation:
    prokka:
      defaultKingdom: false
      additionalParams: " --mincontiglen 500 "
resources:
  highmemLarge:
    cpus: 28
    memory: 60
  highmemMedium:
    cpus: 14
    memory: 30
  large:
    cpus: 28
    memory: 58
  medium:
    cpus: 16
    memory: 29
  small:
    cpus: 7
    memory: 14
  tiny:
    cpus: 1
    memory: 1
```

#### Run the pipeline

First, we clone the Metagenomics-Toolkit Repository:
```bash
cd ~/workdir/mgtk/
git clone https://github.com/metagenomics/metagenomics-tk/
cd metagenomics-tk
```

Execute this command:

```bash
cd ~/workdir/mgtk/
NXF_VER=25.10.4 nextflow run main.nf \
	  -profile standard \
	  -params-file ~/workdir/mgtk/config.yml \
	  -entry wFullPipeline 
```

Then check the results in the `output_test` folder. Check the tutorials in the Metagenomics-Toolkit documentation for further information.

#### Explore the pipeline output

Before downloading pre-computed results, take some time to explore the toolkit output that was generated from your run. The results are stored in the `output_test` directory. In this short tutorial run, only the **binning** and **annotation** modules completed successfully. The directory structure looks like this:

```bash
cd ~/workdir/mgtk/output_test
ls -la
```

Browse through the directory hierarchy — each sample has its own subfolder (e.g., `DMC_BGA22_4_N_1GB/1/`), and within each are subdirectories for `binning/`, `assembly/`, and `annotation/`.

Try to find the Assembly, binning and annotation results:

1. **Assembly:** Look inside the `assembly` directory for individual bin files
3. **Binning:** Look inside the `binning` directory for individual bin files
4. **Annotation:** Look inside the `annotation` directory for gene predictions and functional annotations from Prokka.

> <question-title>What files should you be looking for?</question-title>
> - **Assembly output:** FASTA contig file from MEGAHIT (e.g., `*_contigs.fa.gz`).
> - **Binning output:** Individual bin FASTA files from MetaBAT (e.g., `*_bin.1.fa`, `*_bin.2.fa`).
> - **Annotation output:** Predicted gene annotations (GFF/GBK files), protein FASTA files, and summary tables.
> 
> > <solution-title>Solution</solution-title>
> > In the `binning/0.7.1/metabat/` output directory you will find individual `.fa` bin files. The annotation results can be found under `assembly/1.2.3/megahit/`. And annotation from prokka in `annotation/2.0.1/prokka/`
> {: .solution}
>
{: .question}

Next have a look on some specific features of your run.

> <question-title>How successful was your assembly and binning?</question-title>
> How many BINs got generated in this very small subsample? How is the assembly quality (length and N50?)?
> 
> > <solution-title>Solution</solution-title>
> > You can just count the number of BINs in the BIN directory the assembly quality can be found in: `assembly/1.2.3/megahit/contigs_stats.tsv`.
> {: .solution}
>
{: .question}


#### Copy full results:

> <tip-title>Why download pre-computed results?</tip-title>
> Running the full Toolkit pipeline on complete datasets can take hours and requires tens of gigabytes of RAM and substantial disk space due to large databases. For this workshop, we provide pre-computed results as compressed tar archives (each ~3–5 GiB) that contain a representative subset of the output — enough to explore and visualize meaningful results without waiting for a full pipeline run. You can download **1–3 of the 8 available result sets** to compare different samples and their binning outcomes.
> {: .tip}

Select **1–3 result sets** corresponding to the datasets you used (or are interested in) and download them:

---

**Result set 1: DMC_BGA22_4_N**

```bash
cd ~/workdir/mgtk/
wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/results/DMC_BGA22_4_N_1GB.tar.gz
tar -xvzf DMC_BGA22_4_N_1GB.tar.gz
```

**Result set 2: DMC_BGA52_4_N**

```bash
cd ~/workdir/mgtk/
wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/results/DMC_BGA52_4_N_1GB.tar.gz
tar -xvzf DMC_BGA52_4_N_1GB.tar.gz
```

**Result set 3: LF_Silphie_R1**

```bash
cd ~/workdir/mgtk/
wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/results/LF_Silphie_R1_1GB.tar.gz
tar -xvzf LF_Silphie_R1_1GB.tar.gz
```

**Result set 4: P2_F1_R1**

```bash
cd ~/workdir/mgtk/
wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/results/P2_F1_R1_1GB.tar.gz
tar -xvzf P2_F1_R1_1GB.tar.gz
```

**Result set 5: P7-F1_R1**

```bash
cd ~/workdir/mgtk/
wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/results/P7-F1_R1_1GB.tar.gz
tar -xvzf P7-F1_R1_1GB.tar.gz
```

**Result set 6: PB22_180226_F1_R1**

```bash
cd ~/workdir/mgtk/
wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/results/PB22_180226_F1_R1_1GB.tar.gz
tar -xvzf PB22_180226_F1_R1_1GB.tar.gz
```

**Result set 7: PB37_180322_F_R1**

```bash
cd ~/workdir/mgtk/
wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/results/PB37_180322_F_R1_1GB.tar.gz
tar -xvzf PB37_180322_F_R1_1GB.tar.gz
```

**Result set 8: P9_F1_T1_R1**

```bash
cd ~/workdir/mgtk/
wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/results/P9_F1_T1_R1_1GB.tar.gz
tar -xvzf P9_F1_T1_R1_1GB.tar.gz
```

---

After extracting your chosen result set(s), the pre-computed outputs will be within  the `output` directory, so you can proceed to the Jupyter Notebook section below.

#### Explore the downloaded results

The downloaded result archives contain the complete full-pipeline output for each sample, including all modules: `qc/`, `assembly/`, `binning/`, `annotation/`, and the `magAttributes/` step.

Browse the extracted directory and try to locate the following:

1. **GTDB-Tk classifications:** Find the taxonomic lineage files for each MAG.
2. **CheckM2 quality metrics:** Locate the summary tables with completeness and contamination scores.

> <question-title>Where to find GTDB-Tk and CheckM2 output?</question-title>
> 
> > <solution-title>Solution</solution-title>
> > The GTDB-Tk classification results can be found under `magAttributes/4.0.0/gtdb/` in the respective folders for CheckM2 and GTDBtk — look for files named like `*combined.tsv`, which contain the taxonomic lineages for each bin. The CheckM2 results can be found in `magAttributes/4.0.0/checkm2/` the file named like `*generated.tsv`, which lists completeness, contamination, and strain heterogeneity for every MAG.
> {: .solution}
>
{: .question}

## Inspect the results using a Jupyter Notebook

To explore the Metagenomics-Toolkit results interactively, we will use Jupyter Notebook. This section walks you through setting up a Python virtual environment, installing Jupyter, launching the Jupyter server, and running a notebook that inspects binning and MAG statistics from the Toolkit output.

### Step 1: Set up the Jupyter Environment

#### Install Jupyter and create a virtual environment

Python provides `venv` as the standard way to create isolated environments:

```bash
cd ~/workdir/mgtk/
python3 -m venv mgtk_venv
source mgtk_venv/bin/activate
```

With the virtual environment activated, install Jupyter Notebook:

```bash
pip install jupyterlab ipykernel
```

### Step 2: Download and Extract the Example Notebook

The example notebook demonstrates how to visualize and analyze the binning and MAG statistics produced by the Metagenomics-Toolkit. Download it:

```bash
cd ~/workdir/mgtk/
wget https://s3.bi.denbi.de/cmg/mgcourses/mg2026/mgtk_jupyter.tar
tar -xvf mgtk_jupyter.tar
```

Also create a folder for plots to be stored:

```bash
cd ~/workdir/mgtk/
mkdir mgtk_plots
```


This extracts a notebook called `mgtk_binning_mag_statistics.ipynb` and a python file `utils.py` into your working directory.

### Step 3: Register the Virtual Environment as a Jupyter Kernel

Jupyter Notebook needs to know about the Python environments available on your system. Register the virtual environment we just created:

```bash
python -m ipykernel install --user --name mgtk_venv --display-name "Python (mgtk_venv)"
```

This registers the kernel so you can select **Python (mgtk_venv)** as the notebook kernel.

### Step 4: Start the Jupyter Server

Launch the Jupyter server in your working directory:

```bash
cd ~/workdir/mgtk/
jupyter lab --port=8889 --no-browser
```

After the server starts, it prints a URL with a token to the terminal, similar to:

```
    http://localhost:8889/lab?token=abc123...
```

Copy this URL. Open it in your web browser:

```bash
$BROWSER http://localhost:8889/lab?token=abc123...
```

> <tip-title>Jupyter vs. JupyterLab</tip-title>
> This tutorial uses **JupyterLab** (`jupyter lab`) instead of the classic Jupyter Notebook interface. JupyterLab provides a more modern, flexible environment with a file browser, integrated terminal, and notebook support. Both `jupyter lab` and `jupyter notebook` are installed with the `jupyterlab` package.
{: .tip}

### Step 5: Open and Run the Notebook

In the JupyterLab interface:

1. Navigate to your working directory (`~/workdir`) using the file browser on the left.
2. Double-click `mgtk_binning_mag_statistics.ipynb` to open the notebook.
3. In the top menu, select **Kernel → Change Kernel → Python (mgtk_venv)** to ensure you are using the virtual environment where the required Python packages will be installed.
4. Run all cells by selecting **Kernel → Run All Cells** from the top menu, or by pressing **Shift + Enter** in each cell individually.

> <tip-title>Automatic Package Installation</tip-title>
> The notebook is designed to install any missing Python dependencies automatically at the beginning. If packages need to be installed, you may be prompted to confirm — click **Restart and Run Entire** to proceed. After installation, the notebook will execute all cells from start to finish.
{: .tip}

### What the Notebook Does

The `mgtk_binning_mag_statistics` notebook:

1. **Loads the Toolkit output directory** — parses the hierarchical per-sample and combined output structure produced by the *full pipeline* run.
2. **Reads binning statistics** — extracts information about the number of bins, bin sizes, and quality metrics (completeness, contamination) from CheckM2 and GTDB-Tk outputs.
3. **Visualizes MAG quality distributions** — generates summary plots showing the completeness/contamination distribution of recovered genomes.
4. **Displays taxonomic assignments** — summarizes the taxonomic classification results from the GTDB-Tk module.
5. **Export fastas for MAGs** — Export fasta files for specific MAGs for use in other tools

By running the notebook, you gain an interactive overview of the key results from the Metagenomics-Toolkit pipeline, making it easy to assess data quality and downstream analysis outcomes.

> <question-title>Exploring your own results</question-title>
> If you ran the Metagenomics-Toolkit on your own dataset, how would you adapt the notebook to inspect results from a different run?
> 
> > <solution-title>Solution</solution-title>
> > The notebook expects output in the standard `output/SAMPLE/RUN_ID` directory structure. Simply update the input path to point to your own sample's output folder (e.g., `your_output/`), and the notebook will parse the same module outputs. You can also extend the visualization code to include additional statistics from the Toolkit's modules like annotation.
> {: .solution}
{: .question}

### Stopping the Jupyter Server

When you are finished, stop the Jupyter server by pressing **Ctrl + C** in the terminal where it is running. Confirm the shutdown when prompted:

```
Shutdown this server (y/[n])? y
```

You can deactivate the Python virtual environment afterward:

```bash
deactivate
```

### APPENDIX: Reference Links for Metagenomics-Toolkit Tools

* **Nextflow (Workflow Orchestration Engine):**
  * **GitHub:** [https://github.com/nextflow-io/nextflow](https://github.com/nextflow-io/nextflow)
  * **Publication:** *Di Tommaso, P. et al. (2017). Nextflow enables reproducible computational workflows. Nature Biotechnology.*
* **Metagenomics-Toolkit:**
  * **GitHub:** [https://github.com/metagenomics/metagenomics-tk/](https://github.com/metagenomics/metagenomics-tk/)
  * **Publication:** *Belmann, P.et al. (2025). Metagenomics-Toolkit: the flexible and efficient cloud-based metagenomics workflow featuring machine learning-enabled resource allocation. NAR Genomics and Bioinformatics*, 7(3), lqaf093. [https://doi.org/10.1093/nargab/lqaf093](https://doi.org/10.1093/nargab/lqaf093)