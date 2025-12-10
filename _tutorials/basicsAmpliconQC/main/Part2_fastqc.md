# FastQC

[FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) provides an easy way to perform quality control checks on raw high-throughput sequencing data. Its modular set of analyses allows you to quickly determine if your data have problematic features that could affect downstream analysis.

**Main functions of FastQC:**
- Import data from BAM, SAM, or FASTQ files (any variant)
- Provide a quick overview to identify potential problems
- Summarize data with graphs and tables
- Export results into permanent HTML reports
- Allow offline/automated report generation (including CLI)

You can run FastQC interactively or via the command-line interface (CLI).

---

## Running FastQC

To see all FastQC options, use:

```bash
fastqc --help
```

**Common usage:**

```bash
fastqc seqfile1 seqfile2 .. seqfileN
fastqc [-o output_dir] [--(no)extract] [-f fastq|bam|sam] [-c contaminant file] seqfile1 .. seqfileN
```

**Frequently used options:**

| Option                 | Description |
|------------------------|-------------|
| `-o, --outdir`         | Output directory (must exist) |
| `--casava`             | Treat files as raw Casava output (groups samples) |
| `--nano`               | Special support for Nanopore fast5 directories |
| `--nofilter`           | With --casava, do not remove poor quality reads |
| `--nogroup`            | Disable base grouping for long reads (be careful!) |
| `-f, --format`         | Force a specific file format (fastq, bam, sam, etc) |
| `-t, --threads`        | Number of threads/files processed in parallel |
| `-c, --contaminants`   | File with named contaminants to check for |
| `-a, --adapters`       | File with named adapter sequences to check for |
| `-l, --limits`         | Custom file with module warn/error thresholds |
| `-k, --kmers`          | Kmer length for kmer content module (default 7) |
| `-q, --quiet`          | Suppress progress messages |
| `-d, --dir`            | Temporary file directory for images |

For more detailed information, see the [FastQC documentation](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/).

---

## {% icon hands_on %} Hands-on: Evaluating Quality with FastQC

Let's evaluate a set of FASTQ files using FastQC from the command line.

> 1. Create a results directory and run FastQC on your files.
>
>    ```bash
>    cd ~/workdir
>    mkdir -p ~/workdir/fastqc  
>    fastqc -t 14 -o ~/workdir/fastqc/ ~/workdir/16Sdata/*.fastq
>    ```
>
> 2. View the reports in your web browser (replace `*.html` with your actual report name if needed):
>
>    ```bash
>    cd ~/workdir/fastqc
>    firefox *.html
>    ```
>
> 3. Browse through the FastQC HTML report. Together, we will inspect which modules flag your data as poor, warning, or pass.

---

> ### {% icon tip %} FastQC Example Reports
>
> See the [FastQC homepage](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) for example reports—some with notably bad quality!
{: .tip}

---

# References

- [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)

