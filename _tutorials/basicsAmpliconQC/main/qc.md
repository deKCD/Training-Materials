---
title: "Quality Treatment of Illumina Paired-End Reads"
questions:
  - How do I assess and improve the quality of Illumina paired-end reads?
  - How can I trim low quality bases, poly-G tails, and adapters?
objectives:
  - Inspect the quality of real sequencing data
  - Perform quality trimming with `fastp`
  - Remove poly-G tails
  - Trim adapters with `cutadapt`
time_estimation: "1h"
level: Intermediate
key_points:
  - Quality control is essential for NGS data
  - Multiple tools can be combined for optimal results
  - It is important to inspect quality both before and after processing
---

# Introduction

In this exercise, you will learn how to quality trim Illumina paired-end reads. Illumina paired-end sequencing is still the most common NGS approach for metagenomics. Here, you will work with real sequencing data that shows some quality issues, and proceed through a series of quality control and trimming steps.

---

## 1. Inspecting the Data

Let's start by downloading some example sequencing data and running an initial quality check with **FastQC**.

> ### {% icon hands_on %} Hands-on: Inspect raw data
>
> 1. Open a terminal and create a directory for this tutorial.
> 2. Download the dataset and unpack it.
> 3. Run FastQC on the raw FASTQ files.
>
> ```
> mkdir -p /mnt/qc
> cd /mnt/qc
> wget https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/mgcourse_data/qc.tgz
> tar -xvzf qc.tgz
> fastqc *.fastq
> ```
>
> Open the FastQC reports to inspect the quality metrics.
{: .hands_on}

---

## 2. Quality Trimming with Fastp

For quality trimming, we use the software `fastp`, which trims reads from the 5' to 3' end using a sliding window. If the mean quality within a window drops below a specific threshold, the remaining sequence will be trimmed. Reads that become too short are discarded.

> ### {% icon hands_on %} Hands-on: Run fastp for quality trimming
>
> 1. Review the help documentation for fastp and its parameters.
> 2. Run fastp for quality trimming:
>
> ```
> fastp \
>   -i forward.fastq \
>   -I reverse.fastq \
>   -o forward_qc1.fastq \
>   -O reverse_qc1.fastq \
>   --cut_tail -Q -A -G -w 16
> ```
>
> Now, run FastQC again to inspect the trimmed reads and compare with the untrimmed data:
>
> ```
> fastqc forward_qc1.fastq reverse_qc1.fastq
> ```
{: .hands_on}

---

## 3. Removing Poly-G Tails

Reads may still have issues at the 3' end, particularly poly-G tails, which are common with some sequencers. Let's try to remove poly-G tails with fastp.

> ### {% icon hands_on %} Hands-on: Remove poly-G tails
>
> ```
> fastp \
>   -i forward.fastq \
>   -I reverse.fastq \
>   -o forward_qc2.fastq \
>   -O reverse_qc2.fastq \
>   --cut_tail -A -g --poly_g_min_len 5 -w 16
> ```
>
> Again, inspect the results using FastQC:
>
> ```
> fastqc forward_qc2.fastq reverse_qc2.fastq
> ```
{: .hands_on}

---

## 4. Trimming Adapter Sequences

The FastQC report may still show some adapter contamination. While Fastp can also trim adapters, tools like `cutadapt` often perform better for this task.

> ### {% icon tip %} Tip: Know your adapters!
> You should know the adapter and primer sequences used for your library. Typically, this information is provided by your sequencing facility.
>
> For Illumina libraries, common adapter sequences can be found [here](https://dnatech.genomecenter.ucdavis.edu/wp-content/uploads/2019/03/illumina-adapter-sequences-2019-1000000002694-10.pdf) and [here](https://teichlab.github.io/scg_lib_structs/methods_html/Illumina.html).
{: .tip}

For this dataset, the sequences to trim are:
- Forward: `CTGTCTCTTATACACATCT`
- Reverse: `CTGTCTCTTATACACATCT`

> ### {% icon hands_on %} Hands-on: Trim adapters with cutadapt
>
> ```
> cutadapt -e 0.15 -O 10 -m 25 \
>   -a CTGTCTCTTATACACATCT \
>   -A CTGTCTCTTATACACATCT \
>   -o forward_qc3.fastq -p reverse_qc3.fastq \
>   forward_qc2.fastq reverse_qc2.fastq
> ```
>
> Finally, assess the quality of the trimmed files one last time:
>
> ```
> fastqc forward_qc3.fastq reverse_qc3.fastq
> ```
{: .hands_on}

---

## Conclusion

You have now performed:
- An initial quality check on raw data
- Quality and poly-G tail trimming with fastp
- Adapter trimming with cutadapt
- Iterative inspection of sequence quality

Regular quality checks and iterative trimming can greatly improve the quality of your downstream bioinformatics analyses.

---

## References

- [FastQC Documentation](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- [fastp: A tool designed to provide fast all-in-one preprocessing for FastQ files](https://github.com/OpenGene/fastp)
- [cutadapt documentation](https://cutadapt.readthedocs.io/)
