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

><details-title>IMPORTANT</details-title>
>Some software is installed within a python virtual environment, you need to activate it with:
>
>```bash
>source ~/longread/bin/activate
>```
>If some tool cannot be executed during this tutorial - make sure the environment is active! Indicated byt `(longread)` in your commandline.
{: .details}

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
