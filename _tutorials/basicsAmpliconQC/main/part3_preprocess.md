# Quality Treatment

- Reads contain errors (0.1–15%) and contamination
- **Quality matters!**
  - NGS high throughput = lots of data → more data, more (systematic) errors
  - 16S data > WGS read-based > WGS assembly-based (in increasing stringency)
  - Better data = lower computational cost
  - Decreases false positives
  - Always a trade-off (risk of false negatives)
- Quality-based filtering vs. error correction
- Many tools available for this step

---

# Typical Workflow

![Typical QC workflow](https://github.com/jueneman/16S-workshop-denbi/raw/master/docs/qc/pics/workflow.png)

For this exercise, we will use:

- **Only 16S data**
- Merge: FLASh
- Clip primers: cutadapt
- Trim quality: sickle
- Filter by length: ea-utils

---

# Merge Reads

- Assembly of forward and reverse read pairs (if DNA fragment is shorter than twice the read length)
- Ungapped alignment with *min overlap* region (common to Illumina)
- Quality scores at merged positions are recalculated as absolute difference

> ### {% icon hands_on %} Hands-on: Merge first pair of reads
>
> ```bash
> mkdir -p ~/workdir/flash
> cd ~/workdir/flash
> flash -r 300 ~/workdir/16Sdata/BGA1_1_R1.fastq ~/workdir/16Sdata/BGA1_1_R2.fastq -o BGA1_1
> ```
>
> Example output:
>
> ```
> [FLASH] Read combination statistics:
> [FLASH]     Total pairs:      8495
> [FLASH]     Combined pairs:   8388
> [FLASH]     Uncombined pairs: 107
> [FLASH]     Percent combined: 98.74%
> ```
>
> The merged paired-end reads have been written to:
>
> ```
> BGA1_1.extendedFrags.fastq
> ```
{: .hands_on}

> ### {% icon hands_on %} Hands-on: Merge all pairs in batch
>
> ```bash
> parallel "flash -r 300 ~/workdir/16Sdata/{}_R1.fastq ~/workdir/16Sdata/{}_R2.fastq -o {}" ::: {BGA1_2,BGA2_1,BGA2_2,BGA3_1,BGA3_2,BGA4_1,BGA4_2}
> ```
>
> If you have information on the amplified fragment, you can adjust min/max overlap, fragment length, and SD as necessary.
{: .hands_on}

---

# Primer Clipping

First, identify the primer sequences used to amplify your region of interest:

| Domain    | Region | Sequence               |
|-----------|--------|------------------------|
| Bacteria  | V3F    | CTACGGGNGGCWGCAG       |
| Bacteria  | V4R    | GACTACHVGGGTATCTAATCC  |

> ### {% icon hands_on %} Hands-on: Clip forward primer with cutadapt
>
> ```bash
> mkdir ~/workdir/cutadapt
> cd ~/workdir/cutadapt
> cutadapt -g ^CTACGGGNGGCWGCAG ../flash/BGA1_1.extendedFrags.fastq -e 0.2 -O 10 -o BGA1_1.trimmedf.fastq
> ```
>
> - `^` anchors the primer at the 5' end of the read
> - `-e 0.2` sets a max error rate of 20%
> - `-O 10` is a minimum overlap of 10 bases
> - Cutadapt accepts wobble bases and can trim both primers and adapters
> - Adjust stringency parameters as needed; always inspect output for too many/suspiciously trimmed reads!
{: .hands_on}

Example cutadapt output:
```
=== Summary ===
Total reads processed:                   8,388
Reads with adapters:                     8,383 (99.9%)
Reads written (passing filters):         8,388 (100.0%)
Total basepairs processed:     3,808,321 bp
Total written (filtered):      3,665,848 bp (96.3%)
=== Adapter 1 ===
Sequence: CTACGGGNGGCWGCAG; Type: anchored 5'; Length: 16; Trimmed: 8383 times.
No. of allowed errors:
0-4 bp: 0; 5-9 bp: 1; 10-14 bp: 2; 15 bp: 3
...
```

> ### {% icon hands_on %} Hands-on: Clip reverse primer (reverse complement!)
>
> After merging, the reverse primer must be reverse complemented.
>
> 1. Reverse-complement the primer:
>    ```bash
>    cd ~/workdir
>    echo -e ">primer\nGACTACHVGGGTATCTAATCC" > revprimer.fas
>    revseq -sequence revprimer.fas -outseq revprimer_rc.fas
>    cat revprimer_rc.fas
>    ```
>
> 2. Use the reverse-complemented primer sequence with `cutadapt` at the 3' end:
>    ```bash
>    cd ~/workdir/cutadapt
>    cutadapt -a GGATTAGATACCCBDGTAGTC$ BGA1_1.trimmedf.fastq -e 0.2 -O 10 -o BGA1_1.trimmedfr.fastq
>    ```
{: .hands_on}

> ### {% icon hands_on %} Hands-on: Batch primer trimming
>
> ```bash
> cd ~/workdir/cutadapt
> parallel "cutadapt -g ^CTACGGGNGGCWGCAG ../flash/{}.extendedFrags.fastq -e 0.2 -O 10 -o {}.trimmedf.fastq" ::: {BGA1_2,BGA2_1,BGA2_2,BGA3_1,BGA3_2,BGA4_1,BGA4_2}
> parallel "cutadapt -a GGATTAGATACCCBDGTAGTC$ {}.trimmedf.fastq -e 0.2 -O 10 -o {}.trimmedfr.fastq" ::: {BGA1_2,BGA2_1,BGA2_2,BGA3_1,BGA3_2,BGA4_1,BGA4_2}
> ```
{: .hands_on}

---

# Quality Trimming

Reads with very low quality often contain many miscalled bases, which can increase false positives in downstream analyses. Trim low-quality bases from both ends using a sliding window approach with **sickle**.

> ### {% icon hands_on %} Hands-on: Trim low-quality ends
>
> ```bash
> mkdir -p ~/workdir/sickle
> cd ~/workdir/sickle
> sickle se -f ../cutadapt/BGA1_1.trimmedfr.fastq -t sanger -q20 -o BGA1_1.clipped.fastq
> ```
>
> - `-q 20` sets min average quality score to 20
> - `-t sanger` applies Phred+33 scale
> - `-n` truncates at ambiguous bases (N)
{: .hands_on}

> ### {% icon hands_on %} Hands-on: Batch quality trimming
>
> ```bash
> cd ~/workdir/sickle
> parallel "sickle se -f ../cutadapt/{}.trimmedfr.fastq -t sanger -q20 -o {}.clipped.fastq" ::: {BGA1_2,BGA2_1,BGA2_2,BGA3_1,BGA3_2,BGA4_1,BGA4_2}
> ```
{: .hands_on}

---

# Length Filtering

Filter out reads that are too short (or too long) for your expected amplicon size. First, use a Perl script to inspect read lengths:

> ### {% icon hands_on %} Hands-on: Plot and inspect read lengths
>
> ```bash
> cd $CONDA_PREFIX/bin  
> wget https://raw.githubusercontent.com/jueneman/16S-workshop-denbi/master/docs/qc/FastaStats.pl
> chmod u+x FastaStats.pl
>
> mkdir ~/workdir/length
> cd  ~/workdir/length  
> FastaStats.pl -q ../sickle/BGA1_1.clipped.fastq > BGA1_1.fastq.hist
> head -n 10 BGA1_1.fastq.hist
> ```
{: .hands_on}

Now, trim reads to a defined length window (here, using 1.5 × IQR):

> ### {% icon hands_on %} Hands-on: Filter by length with ea-utils (fastq-mcf)
>
> ```bash
> fastq-mcf -0 -l 369 -L 461 n/a ../sickle/BGA1_1.clipped.fastq -o BGA1_1.fastq
> ```
>
> - `-l 369` = lower length threshold
> - `-L 461` = upper length threshold
> - `n/a` = do not provide primer file (no adapter trimming here)
{: .hands_on}

> ### {% icon hands_on %} Hands-on: Batch length filtering
>
> ```bash
> parallel "FastaStats.pl -q ../sickle/{}.clipped.fastq > {}.fastq.hist" ::: {BGA1_2,BGA2_1,BGA2_2,BGA3_1,BGA3_2,BGA4_1,BGA4_2}
> grep IQR *.hist
> fastq-mcf -0 -l 369 -L 461 n/a ../sickle/BGA1_2.clipped.fastq -o BGA1_2.fastq
> parallel "fastq-mcf -0 -l 372 -L 460 n/a ../sickle/{}.clipped.fastq -o {}.fastq" ::: {BGA2_1,BGA2_2}
> parallel "fastq-mcf -0 -l 364 -L 464 n/a ../sickle/{}.clipped.fastq -o {}.fastq" ::: {BGA3_1,BGA3_2}
> parallel "fastq-mcf -0 -l 377 -L 449 n/a ../sickle/{}.clipped.fastq -o {}.fastq" ::: {BGA4_1,BGA4_2}
> ```
{: .hands_on}

---

# FastQC - Revisited

Now inspect how your quality treatment has improved the read quality:

> ### {% icon hands_on %} Hands-on: Run FastQC on filtered files
>
> ```bash
> cd ~/workdir/fastqc
> fastqc -t 14 -o ~/workdir/fastqc/ ~/workdir/length/*.fastq
> ```
{: .hands_on}

As one final step, group all high-quality files together:

> ### {% icon hands_on %} Hands-on: Organize your high-quality reads
>
> ```bash
> cd ~/workdir
> mkdir HQ
> cp length/*.fastq HQ/
> ```
{: .hands_on}

---

# Final Remarks

- **Know your data**: library prep, expected fragment/read length, possible adapters/primers
- Consider the sequencer (Illumina vs. Ion Torrent, etc.)
- Carefully inspect results at each step
- Try different strategies (conservative vs. loose parameters)
- Adapt the QC workflow to your research question (16S vs. read-based shotgun, etc.)
- This is only one workflow; consider other tools or workflow order. Always examine your raw data!

---

# References

- FastQC: [http://www.bioinformatics.babraham.ac.uk/projects/fastqc/](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- Sickle: [https://github.com/najoshi/sickle](https://github.com/najoshi/sickle)
- cutadapt: [https://github.com/marcelm/cutadapt](https://github.com/marcelm/cutadapt)
- FLASh: [http://ccb.jhu.edu/software/FLASH/](http://ccb.jhu.edu/software/FLASH/)
- ea-utils: [https://github.com/ExpressionAnalysis/ea-utils](https://github.com/ExpressionAnalysis/ea-utils)
