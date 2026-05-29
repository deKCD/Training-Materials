## The Tutorial Data Set  

The first thing you need to do is to connect to your virtual machine with the **X2Go Client**.  
If you are working with your laptop and haven’t installed it yet, you can get it here:  

<https://wiki.x2go.org/doku.php/download:start>

1. Enter the IP of your virtual machine, the port, the username **`ubuntu`**, and select your SSH key.  
2. When you have successfully connected to your machine, open a terminal.

><code-in-title>Give the attached volume to the `ubuntu` user</code-in-title>
>```bash
>sudo chown ubuntu:ubuntu /mnt/volume/
>```
{: .code-in}

><code-in-title>Create a link to the mounted volume in your home directory</code-in-title>
>```bash
>ln -s /mnt/volume/ workdir
>```
{: .code-in}

><code-in-title>Download the tutorial dataset (and pre‑computed results)</code-in-title>  
>```bash
>cd ~/workdir
>wget https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/mgcourse_data/16S-data.tgz
>```
{: .code-in}

><code-in-title>Unpack the archive</code-in-title>   
>```bash
>tar -xzvf 16S-data.tgz
>ln -s 16S-data/raw/ 16Sdata
>```
{: .code-in}

><code-in-title>Clean up</code-in-title>    
>```bash
>rm 16S-data.tgz
>```
{: .code-in}

><code-in-title>Inspect the data directory</code-in-title>    
>```text
>(mgcourse) ubuntu@sebmain-939e0:~/workdir$ ls -la 16Sdata/
>total 179704
>drwxrwxr-x 2 ubuntu ubuntu     4096 Oct  8 12:12 .
>drwxr-xr-x 4 ubuntu ubuntu     4096 Nov 20  2015 ..
>-rw-rw-r-- 1 ubuntu ubuntu  5712157 Nov 20  2015 BGA1_1_R1.fastq
>-rw-rw-r-- 1 ubuntu ubuntu  5712157 Nov 20  2015 BGA1_1_R2.fastq
>-rw-rw-r-- 1 ubuntu ubuntu 21370972 Nov 20  2015 BGA1_2_R1.fastq
>-rw-rw-r-- 1 ubuntu ubuntu 21370972 Nov 20  2015 BGA1_2_R2.fastq
>-rw-rw-r-- 1 ubuntu ubuntu  8910118 Nov 20  2015 BGA2_1_R1.fastq
>-rw-rw-r-- 1 ubuntu ubuntu  8910118 Nov 20  2015 BGA2_1_R2.fastq
>-rw-rw-r-- 1 ubuntu ubuntu 11004978 Nov 20  2015 BGA2_2_R1.fastq
>-rw-rw-r-- 1 ubuntu ubuntu 11004978 Nov 20  2015 BGA2_2_R2.fastq
>-rw-rw-r-- 1 ubuntu ubuntu 19342508 Nov 20  2015 BGA3_1_R1.fastq
>-rw-rw-r-- 1 ubuntu ubuntu 19342508 Nov 20  2015 BGA3_1_R2.fastq
>-rw-rw-r-- 1 ubuntu ubuntu 12128141 Nov 20  2015 BGA3_2_R1.fastq
>-rw-rw-r-- 1 ubuntu ubuntu 12128141 Nov 20  2015 BGA3_2_R2.fastq
>-rw-rw-r-- 1 ubuntu ubuntu  9294674 Nov 20  2015 BGA4_1_R1.fastq
>-rw-rw-r-- 1 ubuntu ubuntu  9294674 Nov 20  2015 BGA4_1_R2.fastq
>-rw-rw-r-- 1 ubuntu ubuntu  4222729 Nov 20  2015 BGA4_2_R1.fastq
>-rw-rw-r-- 1 ubuntu ubuntu  4222729 Nov 20  2015 BGA4_2_R2.fastq
>-rw-r--r-- 1 ubuntu ubuntu     1240 Nov 23  2015 Pipe.tsv
>-rw-rw-r-- 1 ubuntu ubuntu       55 Nov 20  2015 Primers.txt
>(mgcourse) ubuntu@sebmain-939e0:~/workdir$
>```
{: .code-in}

><code-in-title>Inspect the data directory</code-in-title>    
>```bash
>ls -la 16Sdata/
>```
>><code-out-title>Code-out</code-out-title>
>>```text
>>total 179704
>>drwxrwxr-x 2 ubuntu ubuntu     4096 Oct  8 12:12 .
>>drwxr-xr-x 4 ubuntu ubuntu     4096 Nov 20  2015 ..
>>-rw-rw-r-- 1 ubuntu ubuntu  5712157 Nov 20  2015 BGA1_1_R1.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu  5712157 Nov 20  2015 BGA1_1_R2.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu 21370972 Nov 20  2015 BGA1_2_R1.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu 21370972 Nov 20  2015 BGA1_2_R2.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu  8910118 Nov 20  2015 BGA2_1_R1.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu  8910118 Nov 20  2015 BGA2_1_R2.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu 11004978 Nov 20  2015 BGA2_2_R1.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu 11004978 Nov 20  2015 BGA2_2_R2.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu 19342508 Nov 20  2015 BGA3_1_R1.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu 19342508 Nov 20  2015 BGA3_1_R2.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu 12128141 Nov 20  2015 BGA3_2_R1.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu 12128141 Nov 20  2015 BGA3_2_R2.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu  9294674 Nov 20  2015 BGA4_1_R1.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu  9294674 Nov 20  2015 BGA4_1_R2.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu  4222729 Nov 20  2015 BGA4_2_R1.fastq
>>-rw-rw-r-- 1 ubuntu ubuntu  4222729 Nov 20  2015 BGA4_2_R2.fastq
>>-rw-r--r-- 1 ubuntu ubuntu     1240 Nov 23  2015 Pipe.tsv
>>-rw-rw-r-- 1 ubuntu ubuntu       55 Nov 20  2015 Primers.txt
>>(mgcourse) ubuntu@sebmain-939e0:~/workdir$
>>```
>{: .code-out}
>
{: .code-in}

><code-in-title>(Optional) Disable system beep sounds</code-in-title>      
>```bash
>xset -b
>```
{: .code-in}

><hands-on-title>Activate Conda Environment</hands-on-title>
>
>In order to follow the hands‑on session you need to activate a special Conda environment where all tools and software have been installed and are available:
>
>```bash
>conda activate mgcourse
>```
> **Note:** You need to run the command above in **every** new terminal you open.
>
{: .hands_on}



