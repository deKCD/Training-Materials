title: Basics of Amplicon Quality Processing
description: Baic steps to do manually quality processing of 16S data step by step with individual tools instead of using integrated solutions like qiime2 / dada2 / deblur.
slug: BasicAmpliconQC
time_estimation: HM
questions:
  - What is quality processing and why it is important?
  - What are the neccessary steps to do quality processing on 16S amplicon data?
objectives:
  - You will be able to distinguish between different types of errors and bias in amplicon data.
  - You will apply different tools to address the different error types on the data.
  - You will compare the effect of quality processing with unporcessed data.  - 
key_points:
- The take-home messages
- They will appear at the end of the tutorial
version: alpha
life_cycle: tutorial lifecycle
contributions:
  authorship:
  - author jueneman
  editing: 
  funding: 


## Section title

{ % include _tutorials/basicAmpliconQC/main/Part1_fastq.md }



## The Tutorial Data Set  

The first thing you need to do is to connect to your virtual machine with the **X2Go Client**.  
If you are working with your laptop and haven’t installed it yet, you can get it here:  

<https://wiki.x2go.org/doku.php/download:start>

1. Enter the IP of your virtual machine, the port, the username **`ubuntu`**, and select your SSH key.  
2. When you have successfully connected to your machine, open a terminal.

### Give the attached volume to the `ubuntu` user  

```bash
sudo chown ubuntu:ubuntu /mnt/volume/
```

### Create a link to the mounted volume in your home directory  

```bash
ln -s /mnt/volume/ workdir
```

### Download the tutorial dataset (and pre‑computed results)  

```bash
cd ~/workdir
wget https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/mgcourse_data/16S-data.tgz
```

### Unpack the archive  

```bash
tar -xzvf 16S-data.tgz
ln -s 16S-data/raw/ 16Sdata
```

### Clean up  

```bash
rm 16S-data.tgz
```

### Inspect the data directory  

```text
(mgcourse) ubuntu@sebmain-939e0:~/workdir$ ls -la 16Sdata/
total 179704
drwxrwxr-x 2 ubuntu ubuntu     4096 Oct  8 12:12 .
drwxr-xr-x 4 ubuntu ubuntu     4096 Nov 20  2015 ..
-rw-rw-r-- 1 ubuntu ubuntu  5712157 Nov 20  2015 BGA1_1_R1.fastq
-rw-rw-r-- 1 ubuntu ubuntu  5712157 Nov 20  2015 BGA1_1_R2.fastq
-rw-rw-r-- 1 ubuntu ubuntu 21370972 Nov 20  2015 BGA1_2_R1.fastq
-rw-rw-r-- 1 ubuntu ubuntu 21370972 Nov 20  2015 BGA1_2_R2.fastq
-rw-rw-r-- 1 ubuntu ubuntu  8910118 Nov 20  2015 BGA2_1_R1.fastq
-rw-rw-r-- 1 ubuntu ubuntu  8910118 Nov 20  2015 BGA2_1_R2.fastq
-rw-rw-r-- 1 ubuntu ubuntu 11004978 Nov 20  2015 BGA2_2_R1.fastq
-rw-rw-r-- 1 ubuntu ubuntu 11004978 Nov 20  2015 BGA2_2_R2.fastq
-rw-rw-r-- 1 ubuntu ubuntu 19342508 Nov 20  2015 BGA3_1_R1.fastq
-rw-rw-r-- 1 ubuntu ubuntu 19342508 Nov 20  2015 BGA3_1_R2.fastq
-rw-rw-r-- 1 ubuntu ubuntu 12128141 Nov 20  2015 BGA3_2_R1.fastq
-rw-rw-r-- 1 ubuntu ubuntu 12128141 Nov 20  2015 BGA3_2_R2.fastq
-rw-rw-r-- 1 ubuntu ubuntu  9294674 Nov 20  2015 BGA4_1_R1.fastq
-rw-rw-r-- 1 ubuntu ubuntu  9294674 Nov 20  2015 BGA4_1_R2.fastq
-rw-rw-r-- 1 ubuntu ubuntu  4222729 Nov 20  2015 BGA4_2_R1.fastq
-rw-rw-r-- 1 ubuntu ubuntu  4222729 Nov 20  2015 BGA4_2_R2.fastq
-rw-r--r-- 1 ubuntu ubuntu     1240 Nov 23  2015 Pipe.tsv
-rw-rw-r-- 1 ubuntu ubuntu       55 Nov 20  2015 Primers.txt
(mgcourse) ubuntu@sebmain-939e0:~/workdir$
```

### (Optional) Disable system beep sounds  

```bash
xset -b
```

## Activate Conda Environment  

In order to follow the hands‑on session you need to activate a special Conda environment where all tools and software have been installed and are available:

```bash
conda activate mgcourse
```

**Note:** You need to run the command above in **every** new terminal you open.



