---
layout: tutorial_hands_on
title: "Complete Example Tutorial with All GTN Elements"
level: Introductory
zenodo_link: "https://zenodo.org/record/1234567"
questions:
  - "What are the different markdown elements available in Galaxy Training Network?"
  - "How can I structure a comprehensive tutorial using GTN formatting?"
objectives:
  - "Learn to use all available box types in GTN tutorials"
  - "Understand the metadata structure for GTN tutorials"
  - "Practice writing effective hands-on sections with proper formatting"
time_estimation: "2H"
key_points:
  - "GTN tutorials use specialized markdown boxes for different types of content"
  - "Metadata at the top of the file controls tutorial appearance and behavior"
  - "Hands-on boxes guide learners through practical steps"
  - "Question and solution boxes help with self-assessment"
contributions:
  authorship:
    - contributor1
    - contributor2
  editing:
    - editor1
  testing:
    - tester1
  funding:
    - funding-org
tags:
  - example
  - documentation
  - getting-started
subtopic: basics
abbreviations:
  GTN: Galaxy Training Network
  QC: Quality Control
  RNA-Seq: RNA Sequencing
---

# Introduction

This tutorial demonstrates all the markdown elements available in the Galaxy Training Network. It serves as a comprehensive reference for creating training materials.

The GTN uses specialized markdown syntax to create engaging, interactive tutorials. This document showcases all available box types, formatting options, and interactive elements.

> <agenda-title></agenda-title>
>
> In this tutorial, we will cover:
>
> 1. TOC
> {:toc}
>
{: .agenda}

# Basic Text Formatting

You can use standard markdown for **bold**, *italic*, and ***bold italic*** text. You can also create [links](https://training.galaxyproject.org) and add inline code like `this`.

## Lists

Numbered lists:
1. First item
2. Second item
3. Third item

Bulleted lists:
- First bullet
- Second bullet
  - Nested bullet
  - Another nested item

# Special Boxes

## Hands-on Box

The hands-on box is the most important element in GTN tutorials. It contains step-by-step instructions for learners.

> <hands-on-title>Data Upload and Quality Control</hands-on-title>
>
> 1. Create a new history for this tutorial
>
> 2. {% tool [Import](upload1) %} the following files from Zenodo:
>    - Copy the Zenodo link
>    - Open the Galaxy Upload Manager
>    - Select **Paste/Fetch Data**
>    - Paste the link
>    - Press **Start**
>
> 3. **FastQC** {% icon tool %}: Run quality control on the uploaded data
>    - {% icon param-files %} *"Short read data from your current history"*: Select the uploaded FASTQ files
>    - {% icon param-select %} *"Output format"*: `Webpage`
>    - {% icon param-check %} *"Create a report"*: `Yes`
>
>    > <comment-title>Output format</comment-title>
>    > The webpage format is easier to interpret for beginners
>    {: .comment}
>
> 4. {% tool [MultiQC](toolshed.g2.bx.psu.edu/repos/iuc/multiqc/multiqc/1.11+galaxy0) %}: Aggregate QC reports
>    - {% icon param-repeat %} **"Results"**
>      - *"Which tool was used generate logs?"*: `FastQC`
>      - {% icon param-files %} *"FastQC output"*: Select all FastQC raw data outputs
>
{: .hands_on}

## Question and Solution Boxes

Questions help learners check their understanding. Always provide clear solutions.

> <question-title>Understanding Quality Scores</question-title>
>
> 1. What does a Phred quality score of 30 represent?
> 2. Why might adapter sequences appear in your data?
> 3. What is an acceptable percentage of duplicated sequences?
>
> > <solution-title>Answers</solution-title>
> >
> > 1. A Phred score of 30 means there is a 1 in 1000 chance of an incorrect base call (99.9% accuracy)
> > 2. Adapter sequences can appear when the insert size is shorter than the read length, causing the sequencer to read into the adapter
> > 3. This depends on the experiment type. For RNA-Seq, 20-40% duplication is normal due to highly expressed genes. For genomic DNA, lower duplication (5-20%) is expected
> >
> {: .solution}
>
{: .question}

## Tip Box

Tips provide helpful hints about Galaxy operations or best practices.

> <tip-title>Renaming Datasets</tip-title>
>
> You can rename datasets to make them easier to identify:
> - Click on the {% icon galaxy-pencil %} pencil icon for the dataset
> - Change the name in the **Name** field
> - Click **Save**
>
> Using descriptive names makes it easier to track your analysis!
>
{: .tip}

## Comment Box

Comments provide additional context or explanations.

> <comment-title>About Reference Genomes</comment-title>
>
> - The reference genome version matters for reproducibility
> - Different versions (e.g., hg19 vs hg38) have different coordinates
> - Always document which version you used
> - Make sure all your data uses the same genome build
>
{: .comment}

## Warning Box

Warnings alert users to potential problems or important considerations.

> <warning-title>Data Loss Risk</warning-title>
>
> Permanently deleting datasets cannot be undone! Always make sure you have backups or have exported important results before permanently deleting data.
>
> Use the "Delete Permanently" option only when you're absolutely sure you no longer need the data.
>
{: .warning}

## Details Box

Details boxes provide expandable background information that users can choose to read.

> <details-title>Background: The Phred Quality Score</details-title>
>
> The Phred quality score is a measure of the quality of the identification of the nucleobases generated by automated DNA sequencing.
>
> The Phred quality score Q is logarithmically related to the base-calling error probability P:
>
> $$ Q = -10 \log_{10} P $$
>
> For example:
> - Q10 = 90% accuracy (1 in 10 error rate)
> - Q20 = 99% accuracy (1 in 100 error rate)  
> - Q30 = 99.9% accuracy (1 in 1000 error rate)
> - Q40 = 99.99% accuracy (1 in 10,000 error rate)
>
{: .details}

## Code In/Out Boxes

Use these to show command-line examples and their outputs.

> <code-in-title>Bash</code-in-title>
> ```bash
> ls -lh data/*.fastq.gz
> wc -l data/sample1.fastq
> ```
{: .code-in}

> <code-out-title>Output</code-out-title>
> ```
> -rw-r--r-- 1 user group 2.3G Mar 15 10:30 data/sample1.fastq.gz
> -rw-r--r-- 1 user group 2.1G Mar 15 10:35 data/sample2.fastq.gz
> 40000000 data/sample1.fastq
> ```
{: .code-out}

# Images and Figures

Images can be added with descriptive alt text and captions:

![Diagram showing the RNA-Seq workflow from raw reads to gene expression counts](../../images/rnaseq-workflow.png "Overview of the RNA-Seq analysis pipeline")

You can reference figures in text like this: See [Figure 1](#figure-1) for the complete workflow.

# Mathematical Expressions

You can include mathematical formulas using LaTeX:

Inline math: The p-value threshold is typically $$ \alpha = 0.05 $$

Block equations:

$$ 
\text{TPM}_i = \frac{X_i}{L_i} \times \frac{1}{\sum_j \frac{X_j}{L_j}} \times 10^6 
$$

Where \\(X_i\\) is the number of reads mapped to gene \\(i\\) and \\(L_i\\) is the length of gene \\(i\\).

# Tables

| Tool | Purpose | Time Required |
|------|---------|---------------|
| FastQC | Quality control of raw reads | ~5 minutes |
| Trimmomatic | Adapter trimming and quality filtering | ~15 minutes |
| HISAT2 | Alignment to reference genome | ~30 minutes |
| FeatureCounts | Quantification of gene expression | ~10 minutes |

# Interactive Elements

## Choose Your Own Adventure

Sometimes you want to offer different paths through a tutorial:

{% include _includes/cyoa-choices.html option1="I have paired-end data" option2="I have single-end data" default="I have paired-end data" text="The analysis differs based on your sequencing type. Select your data type to see the appropriate steps." %}

<div class="I-have-paired-end-data" markdown="1">

> <hands-on-title>Paired-End Analysis</hands-on-title>
>
> 1. **HISAT2** {% icon tool %}: Align paired-end reads
>    - *"Source for the reference genome"*: `Use a built-in genome`
>    - *"Select a reference genome"*: `Human (Homo sapiens): hg38`
>    - *"Is this a single or paired library"*: `Paired-end`
>    - {% icon param-files %} *"FASTA/Q file #1"*: Forward reads (R1)
>    - {% icon param-files %} *"FASTA/Q file #2"*: Reverse reads (R2)
>
{: .hands_on}

</div>

<div class="I-have-single-end-data" markdown="1">

> <hands-on-title>Single-End Analysis</hands-on-title>
>
> 1. **HISAT2** {% icon tool %}: Align single-end reads
>    - *"Source for the reference genome"*: `Use a built-in genome`
>    - *"Select a reference genome"*: `Human (Homo sapiens): hg38`
>    - *"Is this a single or paired library"*: `Single-end`
>    - {% icon param-files %} *"FASTA/Q file"*: Your reads
>
{: .hands_on}

</div>

## Workflow Execution Buttons

You can include buttons to run workflows directly:

{% snippet faqs/galaxy/workflows_run_trs.md path="topics/sequence-analysis/tutorials/quality-control/workflows/main-workflow.ga" title="Quality Control Workflow" %}

# Snippets (FAQs)

Common questions can be included as reusable snippets:

{% snippet faqs/galaxy/histories_create_new.md %}

{% snippet faqs/galaxy/datasets_import_via_link.md %}

# Nested Boxes

Boxes can be nested for complex instructions:

> <hands-on-title>Advanced Parameter Selection</hands-on-title>
>
> 1. **RNA STAR** {% icon tool %}: Run the aligner
>    - *"Single-end or paired-end reads"*: `Paired-end`
>    - *"Select reference genome"*: `hg38`
>    
>    > <question-title>Which settings should I use?</question-title>
>    >
>    > Should I adjust the default alignment parameters?
>    >
>    > > <solution-title></solution-title>
>    > >
>    > > For most RNA-Seq experiments, the default parameters work well. However:
>    > > - For very short reads (<50bp), consider adjusting minimum intron length
>    > > - For non-model organisms, you may need to adjust splice junction parameters
>    > >
>    > > > <tip-title>Advanced users</tip-title>
>    > > >
>    > > > You can fine-tune parameters based on your specific research question. See the STAR manual for details on all available options.
>    > > >
>    > > {: .tip}
>    > >
>    > {: .solution}
>    >
>    {: .question}
>
{: .hands_on}

# Icons

GTN provides many icons you can use:

- {% icon tool %} Tool icon
- {% icon galaxy-pencil %} Edit
- {% icon galaxy-eye %} View
- {% icon galaxy-delete %} Delete
- {% icon hands_on %} Hands-on
- {% icon question %} Question
- {% icon solution %} Solution
- {% icon tip %} Tip
- {% icon comment %} Comment
- {% icon warning %} Warning
- {% icon details %} Details
- {% icon galaxy-upload %} Upload
- {% icon galaxy-gear %} Settings
- {% icon galaxy-history %} History
- {% icon galaxy-barchart %} Visualization

# Abbreviations

Using abbreviations makes text more readable. The GTN will automatically expand them on hover. For example: 

Working with RNA-Seq data requires careful QC. The GTN provides comprehensive tutorials for learning bioinformatics.

# Citations

You can cite papers using BibTeX references. For example: Recent work by {% cite bebatut2018community %} describes the community-driven approach to training.

Citations will be automatically formatted and listed at the end of the tutorial.

# Quotes

You can include inspirational or relevant quotes:

> The best way to learn is by doing.
{: .quote cite="https://example.com/learning-theory" author="Educational Researcher"}

# Multiple Choice Questions

> <question-title>Check Your Understanding</question-title>
>
> Which quality score represents 99.9% accuracy?
>
> - [ ] Q20
> - [x] Q30
> - [ ] Q40
> - [ ] Q50
>
> > <solution-title></solution-title>
> >
> > Q30 represents 99.9% accuracy. This corresponds to a 1 in 1000 error rate, which is generally considered the minimum threshold for high-quality sequencing data.
> >
> {: .solution}
>
{: .question}

# Footnotes

You can add footnotes to provide additional information[^1]. Footnotes can be referenced multiple times[^1] throughout the text.

# Section with No TOC Entry

Sometimes you want a section that doesn't appear in the table of contents:

### Minor Technical Note
{: .no_toc}

This subsection won't appear in the agenda because of the `{: .no_toc}` tag.

# Conclusion

This tutorial has demonstrated all the major elements available for creating Galaxy Training Network materials. Key features include:

- Rich metadata for tutorial organization
- Multiple box types for different content types (hands-on, questions, tips, warnings, details)
- Support for images, math, tables, and code blocks
- Interactive elements like Choose Your Own Adventure paths
- Snippet system for reusable FAQ content
- Citation management
- Icon library for visual cues

Using these elements effectively will help create engaging, accessible, and professional training materials.

# Additional Resources

For more information on creating GTN tutorials, see:
- [GTN Tutorial Development Guide](https://training.galaxyproject.org/training-material/topics/contributing/)
- [GTN Style Guide](https://training.galaxyproject.org/training-material/topics/contributing/tutorials/create-new-tutorial-content/tutorial.html)
- [Galaxy Training GitHub Repository](https://github.com/galaxyproject/training-material)

[^1]: Footnotes appear at the bottom of the page and can provide supplementary information without disrupting the main text flow.
