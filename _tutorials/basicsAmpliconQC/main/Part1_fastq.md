# FASTQ Format

Let's first have a look at what a FASTQ file looks like and how its format is defined:

![Example of a FASTQ file](https://github.com/jueneman/16S-workshop-denbi/raw/master/docs/qc/pics/fastq.png)

A FASTQ file contains four lines per sequence:

1. **Sequence identifier**, starting with `@`
2. **Raw sequence letters**
3. **A separator line**, beginning with `+` (can optionally be followed by the identifier)
4. **Quality string**, encoding per-base quality scores

---

## Sequence Quality Scores

Sequence quality scores were first introduced by the phred base caller used for Sanger sequencing.

![Sanger chromatogram and base calls](https://github.com/jueneman/16S-workshop-denbi/raw/master/docs/qc/pics/chromatogram.png)

Quality scores (Q-scores) are a log transformation of the error probability for each base:

| Quality value | Error probability |
|:-------------:|:----------------:|
| 20            | 1/100            |
| 30            | 1/1000           |
| 40            | 1/10,000         |
| 50            | 1/100,000        |

- Quality score = log-transformed error probability

The higher the quality score, the lower the probability that the base call is incorrect.

---

# References

**Images**: [CUNY OpenLab, Next-gen sequencing](https://openlab.citytech.cuny.edu/bio-oer/analyzing-dna/next-gen-sequencing/2/)
