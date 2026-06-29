---
layout: tutorial_hands_on
title: "Introduction to Long-Read Metagenomics using the Metagenomics-Toolkit"
description: "This tutorial will guide you through the first steps to run the Metagenmoics-Toolkit on ONT data"
time_estimation: 1H
level: beginner
keywords: ONT, Nanopore, Metagenomics, Assembly, Classification, Binning, Annotation, Workflow, Nextflow
questions:
- "How do I configure and execute a long-read metagenomics workflow using the Metagenomics-Toolkit with nextflow?"
- "What does the entrypoint and output architecture of the Metagenomics-Toolkit look like for ONT data?"
- "How do I prepare a long-read sample sheet for the automated per-sample pipeline?"
objectives:
- "Understand the execution syntax and command-line parameters of Nextflow-based workflows."
- "Configure a YAML parameter file for long-read metagenomic quality control and assembly steps."
- "Navigate the hierarchical per-sample and aggregation output structures of the Metagenomics-Toolkit."
key_points:
- "Nextflow profiles allow seamless transitions between running on a single machine (`standard`) or a cluster environment (`slurm`)."
- "Long-read sample sheets utilize a simplified flat schema, tracking single FASTQ pathways instead of paired-end forward/reverse channels."
- "The Metagenomics-Toolkit organizes results into a standardized, deterministic folder structure separating logs, tools, and specific module versions."
version:
  - main
life_cycle: under development
contributions:
  authorship:
  - Nils Kleinbölting
  editing: 
  funding:
---

This tutorial is a very short introduction to the Metagenomics-Toolkit which shows the main steps in analysing Nanopore long-read metagenomics data using the Metagenomics-Toolkit.
A more detailed introduction and Tutorials can be found [here](https://metagenomics.github.io/metagenomics-tk/latest/). 
In this part you will learn how to configure and run the Toolkit and what the output of a Toolkit run looks like.

## Tutorial Scope and Requirements

The Metagenomics-Toolkit allows you to run either the full pipeline of assembly, binning, and many other downstream analysis tasks or the individual analyses separately. 
In this tutorial you will only use the *full pipeline* mode. The *full pipeline* mode itself is structured into two parts. The first part runs the Toolkit on each
sample separately (*per-sample*), and the second part runs a combined downstream analysis on the output of the *per-sample* runs; this step is called *aggregation*. We will only run a few tools of the *per sample* part of the pipeline.
While there are several optimizations for running the Toolkit on a cloud-based setup, 
during this workshop you will run the Toolkit on a single machine.

### Requirements

* Basic Linux command-line usage

* This tutorial has been tested on a machine with 28 CPUs and 64 GB of RAM with Ubuntu installed on it.

* Docker: Install Docker by following the official Docker installation [instructions](https://docs.docker.com/engine/install/ubuntu/).

* Java: In order to run Nextflow, you need to install Java on your machine, which can be achieved via `sudo apt install default-jre`.

* Nextflow should be installed. Please check the official Nextflow [instructions](https://www.nextflow.io/docs/latest/install.html#install-nextflow).

* Throughout the course we assume you are working on data downloaded to a volume under `/vol/longread/`, we create a link `~/workdir/` to that  folder, if you are working somewhere else, adjust the `~/workdir` link to that location and all commands should work as outlined in the course.

* We also assume that you have a machine with **28 cores** and **64GB of RAM** available, if not - adjust the configuration that specifies a certain number of cores/memory accordingly.

### **Download the data and preparations**

First **(if not already done)**, create a link to `/vol/longread` (or the folder in which you want to work during the course) and switch to that directory:

```bash
ln -s /vol/longread/ ~/workdir
cd ~/workdir
```
You might need to change the permissions of `/vol/longread`, for example (in the cloud setup we use for the on-site course) with:

```bash
sudo chown ubuntu:ubuntu /vol/longread/
```
(Adjust accordingly to your setup)

---

Next, we download our tutorial dataset (into a data folder):

```bash
cd ~/workdir
mkdir mgtk_data
cd ~/workdir/mgtk_data/
wget https://s3.bi.denbi.de/cmg/mgcourses/mgtk_short/sample0_5p.fastq.gz
cd ~/workdir
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
Please note that computational resources are also global parameters and will be handled in the third part of this configuration section. 
{: .tip}
    

##### Input Field

The input field (line 3, snippet 1) specifies the type of input data to process (Nanopore, Illumina, data hosted on SRA or a mirror)
and you can find a dedicated wiki section [here](https://metagenomics.github.io/metagenomics-tk/latest/pipeline_input/). Regardless of which input type
is used, the user must provide a file containing a list of datasets to be processed.
The list can be a list of remote or local files and in the case of SRA, a list of SRA run IDs.

Since you will work with Nanopore long-read data in this tutorial, your input sample sheet is flat and looks like this:

```bash
SAMPLE    READS
sample1   /path/to/sample1_ont.fastq.gz
sample2   /path/to/sample2_ont.fastq.gz
```

The first column (SAMPLE) specifies the unique name of the dataset. The second column (READS) specifies the single file pathway containing the long-read sequence strings.

#### Part 2: Toolkit Analyses Steps 

Analyses (also called modules) that the Toolkit executes are placed directly under the **steps** attribute in the configuration file.
In the example below, the modules **qc** and **assembly** are placed directly under the **steps** attribute. Any tools or methods
that are used as part of the module can be considered a property of the module. For example, long-read assemblers like **Flye** (or metaFlye) are executed as part of the assembly module instead of short-read graph builders.
The level below the tool names is for configuring the tools and methods. Each analysis is listed on the [modules page](../../modules/introduction.md). 

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

* **RUN_ID:** The run ID will be part of the output path and allows to distinguish between different pipeline configurations that were used for the same dataset.

* **MODULE** is the analysis that is executed by the Toolkit (e.g. qc, assembly, etc.). 

* **MODULE_VERSION** is the version number of the module.

* **TOOL** is the tool or method that is executed by the Toolkit.

Below you can see an example output structure configured for long-read data.
Every output folder includes four log files:

* **.command.err:** Contains the standard error.

* **.command.out:** Contains the standard output. 

* **.command.log:** Contains the combined standard error and standard output.

* **.command.sh:** Contains the command that was executed. 

```bash
output/
└── sample0_5
    └── 1
        ├── assemblyONT
        │   └── 0.2.0
        │       └── metaflye
        │           ├── sample0_5_assembly_graph.gfa -> /volume/helgoland/metagenomics-tk/work_camitest5/be/79804d7d54f074279ed4a6881ba1ae/sample0_5_assembly_graph.gfa
        │           ├── sample0_5_assembly_info.txt -> /volume/helgoland/metagenomics-tk/work_camitest5/be/79804d7d54f074279ed4a6881ba1ae/sample0_5_assembly_info.txt
        │           ├── sample0_5_contigs.fa.gz -> /volume/helgoland/metagenomics-tk/work_camitest5/be/79804d7d54f074279ed4a6881ba1ae/sample0_5_contigs.fa.gz
        │           ├── sample0_5_contigs_header_mapping.tsv -> /volume/helgoland/metagenomics-tk/work_camitest5/be/79804d7d54f074279ed4a6881ba1ae/sample0_5_contigs_header_mapping.tsv
        │           └── sample0_5_contigs_stats.tsv -> /volume/helgoland/metagenomics-tk/work_camitest5/be/79804d7d54f074279ed4a6881ba1ae/sample0_5_contigs_stats.tsv
        └── qcONT
            └── 0.1.1
                ├── nanoplot
                │   ├── LengthvsQualityScatterPlot_dot.html -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/LengthvsQualityScatterPlot_dot.html
                │   ├── LengthvsQualityScatterPlot_dot.png -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/LengthvsQualityScatterPlot_dot.png
                │   ├── LengthvsQualityScatterPlot_kde.html -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/LengthvsQualityScatterPlot_kde.html
                │   ├── LengthvsQualityScatterPlot_kde.png -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/LengthvsQualityScatterPlot_kde.png
                │   ├── NanoPlot-report.html -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/NanoPlot-report.html
                │   ├── NanoStats.tsv -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/NanoStats.tsv
                │   ├── Non_weightedHistogramReadlength.html -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/Non_weightedHistogramReadlength.html
                │   ├── Non_weightedHistogramReadlength.png -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/Non_weightedHistogramReadlength.png
                │   ├── Non_weightedLogTransformed_HistogramReadlength.html -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/Non_weightedLogTransformed_HistogramReadlength.html
                │   ├── Non_weightedLogTransformed_HistogramReadlength.png -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/Non_weightedLogTransformed_HistogramReadlength.png
                │   ├── WeightedHistogramReadlength.html -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/WeightedHistogramReadlength.html
                │   ├── WeightedHistogramReadlength.png -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/WeightedHistogramReadlength.png
                │   ├── WeightedLogTransformed_HistogramReadlength.html -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/WeightedLogTransformed_HistogramReadlength.html
                │   ├── WeightedLogTransformed_HistogramReadlength.png -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/WeightedLogTransformed_HistogramReadlength.png
                │   ├── Yield_By_Length.html -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/Yield_By_Length.html
                │   └── Yield_By_Length.png -> /volume/helgoland/metagenomics-tk/work_camitest5/10/0903bbde0e86a1618f758a4fc2696e/Yield_By_Length.png
                └── porechop
                    └── sample0_5_qc.fq.gz -> /volume/helgoland/metagenomics-tk/work_camitest5/7a/e331f1f6b4399859763044c994ff58/sample0_5_qc.fq.gz

```

### Metagenomics-Toolkit Execution 

We will now proceed with actually running the QC, assembly, binning and annotation part of the toolkit. The dataset we use is quite small, so don't expect too much.

#### Create the samplesheet

First, we define a samplesheet:

```bash
cd ~/workdir
gedit samples.tsv
```

Then add the following content to the file:
**Important:** Make sure there are actually tabs in between the columns! And adjust the path if your is not `/vol/longread/`.


```bash
SAMPLE  READS
test    /vol/longread/mgtk_data/sample0_5p.fastq.gz
```

#### Create the configuration

Next we define a configuration yaml file with the above mentioned steps and proper resource definitions:
**Important:** Adjust the path if your is not `/vol/longread/`.

```bash
cd ~/workdir
gedit config.yml
```

Paste the following code into the file:


```bash
tempdir: "tmp"
s3SignIn: true
input:
  ont:
    sheet: "/vol/longread/samples.tsv"
    watch: false
output: output
logDir: log
runid: 1
databases: "/vol/longread/databases"
publishDirMode: "symlink"
logLevel: 1
scratch: "/vol/scratch"
steps:
  qcONT:
    porechop:
       additionalParams:
         chunkSize: 450000
         porechop: ""
         filtlong: " --min_length 1000  --keep_percent 90 "
    nanoplot:
      additionalParams: ""
  assemblyONT:
    metaflye:
      additionalParams: " -i 1 "
      quality: "AUTO"
  binningONT:
    minimap:
      additionalParams: 
        minimap: " "
        samtoolsView: " " 
    contigsCoverage:
      additionalParams: ""
    genomeCoverage:
      additionalParams: " --min-covered-fraction 0 "
    semibin2:
      additionalParams: " --environment global --sequencing-type long_read  "
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
git clone https://github.com/metagenomics/metagenomics-tk/
cd metagenomics-tk
```

Execute this command:

```bash
cd ~/workdir/
NXF_VER=25.10.4 nextflow run main.nf \
	  -profile standard \
	  -params-file ~/workdir/config.yml
	  -entry wFullPipeline \
```

Then check the results in the `output` folder. Check the tutorials in the Metagenomics-Toolkit documentation for further information.

---
### APPENDIX: Reference Links for Metagenomics-Toolkit Tools

* **Nextflow (Workflow Orchestration Engine):**
  * **GitHub:** [https://github.com/nextflow-io/nextflow](https://github.com/nextflow-io/nextflow)
  * **Publication:** *Di Tommaso, P. et al. (2017). Nextflow enables reproducible computational workflows. Nature Biotechnology.*
* **Metagenomics-Toolkit:**
  * **GitHub:** [https://github.com/metagenomics/metagenomics-tk/](https://github.com/metagenomics/metagenomics-tk/)