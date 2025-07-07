---
layout: tutorial_hands_on
title: SimpleVM Workshop
description: "FIXME"
slug: simplevmworkshop
time_estimation: "FIXME"
questions:
  - "FIXME"
  - "FIXME"
objectives:
  - "FIXME"
  - "FIXME"
key_points:
  - "FIXME"
  - "FIXME"
version:
  - main
contributions:
  authorship:
  - Peter Belmann
  - Nils Hoffmann
  - dweinholz
  editing: 
  funding:
---

## Table of Contents
* [Section 1: Big things start small](#section-1-big-things-start-small)
    * [1.1 Create a de.NBI Cloud Account](#11-create-a-denbi-cloud-account)
    * [1.2 Select the SimpleVMIntro23 project](#12-select-the-simplevmintro23-project)
    * [1.3 Start a VM](#13-start-a-vm)
* [Section 2: Verify your VM properties and tools](#section-2-verify-your-vm-properties-and-tools)
* [Section 3: Scale up your analysis ](#section-3-scale-up-your-analysis)
    * [3.1 Create a new VM based on your snapshot](#31-create-a-new-vm-based-on-your-snapshot)
    * [3.2 Interact with the SRA Mirror and search for more datasets to analyse](#32-interact-with-the-sra-mirror-and-search-for-more-datasets-to-analyse)
    * [3.3 Run commands with more cores and plot your result](#33-run-commands-with-more-cores-and-plot-your-results)
* [Section 4: Inspect your generated data via a research environment](#section-4-inspect-your-generated-data-via-a-research-environment)
    * [4.1 Create a VM based on a Research Environment](#41-create-a-vm-based-on-a-research-environment)
    * [4.2 RStudio](#42-rstudio)
    * [4.3 Provide your research data to a reviewer](#43-provide-your-research-data-to-a-reviewer)
* [Section 5: ](#)
    * [5.1 Create a Cluster](#51-create-a-cluster)
    * [5.2 Investigate your cluster setup](#52-investigate-your-cluster-setup)
    * [5.3 Scan the SRA for genomes](#53-scan-the-sra-for-genomes)


This workshop demonstrates a typical workflow of a SimpleVM user.
In this workshop your goal will be to identify pathogenic bacteria
that were classified as "greatest threat to human health" by the 
[World Health Organisation (WHO) in 2017](https://www.who.int/news/item/27-02-2017-who-publishes-list-of-bacteria-for-which-new-antibiotics-are-urgently-needed)

You will search for those microbes
in publicly available metagenomic datasets that are stored in the 
Sequence Read Archive ([SRA](https://www.ncbi.nlm.nih.gov/sra)). 
In metagenomics, microbial genetic material 
is extracted from environmental samples like human gut, soil, 
freshwater or biogas plants in order to investigate the functions and
interactions of the microbial community.

In order to find those microbes, you will have to interact with 
the de.NBI Cloud via SimpleVM. This workshop is divided into three
parts.

## **Section 1: Big things start small**

In the first part you will learn the basic concept of virtual machines
and how to configure them.

Since you are new to SimpleVM, it is resource-saving to start with a VM that
has a few cores and a small amount of RAM.

You start this tutorial from your [profile page](https://cloud.denbi.de/portal/).

### **1.1 Create a de.NBI Cloud Account**

If you do not have a de.NBI Cloud account, please register for one
via this [link](https://cloud.denbi.de/register).
You can read more about the registration process in our 
[de.NBI Cloud wiki](https://cloud.denbi.de/wiki/registration/).
Please make sure to to click on “continue” if this button shows up.

If you successfully registered for a de.NBI Cloud account,
you should be able to log in to the [de.NBI Cloud Portal](https://cloud.denbi.de/portal/).

### **1.2 Select the SimpleVMIntro23 project**

> ## Hands On: Select the SimpleVMIntro23 project
> 1. Click on the `New Instance` tab.
> 
> 2. If you are already member of a SimpleVM project then you are offered a drop down menu to select
> a project. In this case please select the **SimpleVMIntro23** project. If this is
> your first SimpleVM project, you are now able to select/generate a key (next point) or directly start a VM.
> 
> 3. If you have no SSH key set so far, just click on generate key and save the
> private key. During this workshop you will not need this file because 
> you will access all VMs via the browser. However, for your future work using
> SimpleVM, we highly recommend to read our de.NBI Cloud wiki regarding
> [SSH keys](https://cloud.denbi.de/wiki/portal/user_information/#ssh-key)
>
{: .hands_on}

### **1.3 Start a VM**

> ## Hands On: Start a VM
> 1. Choose a name for your VM.
> 2. Select **de.NBI default**.
> 3. In the image section, please click on the *Research Environments* tab 
>    and select the **TheiaIDE-ubuntu22.04** image.
>    ![](/tutorials/simpleVMWorkshop/figures/theiaImage.png){: .responsive-img }
> 4. Select the Conda tab and choose the following tools with their version numbers given below for installation via Conda:
>    * ncbi-genome-download (0.3.3)
>    * mash (2.2)
>    * csvtk (0.28.0)
>    * entrez-direct (16.2)
>    * jq (1.6)
>    * parallel (20230922)
>    ![](/tutorials/simpleVMWorkshop/figures/bioconda.png){: .responsive-img }
>    
>    The filter in the name column can be used to search for the packages.
>    You will learn in the next sections how to apply these tools.
> 
> 5. Select a URL path for Theia. You will access Theia via this URL.
>    ![](/tutorials/simpleVMWorkshop/figures/researchenvironment_url.png){: .responsive-img }
> 6. Grant access to all project members with a `Cloud-portal-support` tag.
>    This way these members get ssh access to your VM and can help you in case
>    something does not work as expected.
>    ![](/tutorials/simpleVMWorkshop/figures/grantAccess.png){: .responsive-img }
> 7. Confirm the checkboxes and click on Start.
>
{: .hands_on}

## **Section 2: Verify your VM properties and tools**

In the second section you will test whether SimpleVM correctly
provisioned your VM with all your tools installed on it.

After the start of the machine has been triggered, some time may pass before the machine is available.
As soon as this is the case, this becomes visible via a green icon.

Once the VM is available, you can use it for testing the tools and inspecting the data before
you scale up your analysis in the next section.

Log in to the VM and verify that SimpleVM provisioned the VM correctly.

> ## Hands On: Verify VM properties and tools
> 1. Click on the Instances tab (Overview -> Instances). After you have initiated the start-up of the machine, you should have been automatically redirected there.
>    Now > open the "How to connect"
>    dropdown of your machine. Click on the Theia ide URL which opens a new browser tab.
>    ![](/tutorials/simpleVMWorkshop/figures/howtoconnect.png){: .responsive-img }
> 2. Click on `Terminal` in the upper menu and select `New Terminal`.
>    ![](/tutorials/simpleVMWorkshop/figure/terminal.png){: .responsive-img }
> 3. Inspect the VM before starting to work with it. Let's check whether the VM
>    has the properties that SimpleVM promised you by typing the following commands
>    in your newly opened terminal window.
>    `nproc` tells you the number of processing units.
> 
>    ```bash
>    nproc
>    ```
>    
>    Does that correspond to the actual number of cores of the flavor you selected?
>    `free -h` tells you the amount of RAM that is available to your VM. You will see
>    that the sum of the total amount of Mem (`total` column, `Mem` row) corresponds 
>    roughly to the RAM size of your selected flavor.
>    
>    ```bash
>    free -h
>    ```
>    
>    You can also check what kind of processes are running on your VM by executing `top`
>    or `htop`.
>    
>    ```bash
>    htop
>    ```
>    
>    Exit `htop` by typing `q` or `F10`.
> 
> 4. You can use the tools you selected in the previous part by running `conda activate denbi`.
> 
> 5. Test if the needed commands are installed by running all of them with `-h` parameter.
>    You will get an explanation of their usage in the next chapter.
> 
>    * `ncbi-genome-download -h`
>    * `mash -h`
>    * `csvtk -h`
>    * `jq -h`
>    
>    If there is an error reported, then something went wrong, and we have to either
>    repeat the conda installation manually or install it a different way.
> 
> 6. Remember that you have root permissions on the VM. You can install any
>    tool that you need for your research.
>    Let's test this statement by first fetching the latest information about available packages and installing the following commands (`fortune-mod`, `cowsay`) via > > `sudo`.
> 
>    Update:
>    ```bash
>    sudo apt update
>    ```
>    Install the commands:
>    
>    ```bash
>    sudo apt install -y fortune-mod cowsay
>    ```
>    
>    You can run both commands via
>    ```bash
>    /usr/games/fortune | /usr/games/cowsay 
>    ```
>
{: .hands_on}

## **Section 3: Scale up your analysis**

In the first part you have tested the SimpleVM environment. 
Now it is time for using a VM with more cores to scale up the analysis. 
For this reason you have either saved your installed tools by creating a snapshot or, 
if you are starting with this section, a snapshot has been prepared for you. 
You will now reuse one of these snapshots with a larger flavor.
Further, we will alos search for more metagenomic datasets via object storage
and scale up our analysis by providing more cores to mash.

### **3.1 Create a new VM based on your snapshot**

> ## Hands On: Create a new VM based on snapshot
> 1. Click on `Overviews` -> `Snapshots` in left menu and check which status
>    your snapshot has. You can also filter of the name in the top menu. 
>    If it has the status `active`, you can 
>    navigate to the `New Instance` tab (and select the SimpleVMIntro23 project).
> 
> 2. Provide again a name for your instance.
> 3. In the flavors sections please choose the **de.NBI large** flavor which has 28 cores available.
>    ![](/tutorials/simpleVMWorkshop/figures/large_flavor.PNG){: .responsive-img }
> 
>    Click on the Snapshot tab to select the snapshot **SimpleVMIntro23**.
>    ![](/tutorials/simpleVMWorkshop/figures/startsnap.png){: .responsive-img }
> 
> 5. Please create a volume for your VM and enter your name without whitespace 
>    (Example: Max Mustermann -> MaxMusterman) as the volume name. 
>    Enter `data` (`/vol/data`) as mountpath and provide 1 GB as the storage size.
>    ![](/tutorials/simpleVMWorkshop/figures/createVolume.png){: .responsive-img }
> 
> 6. Grant again access to all project members with a `Cloud-portal-support` tag.
>    This way these members get ssh access to your VM and can help you in case
>    something does not work as expected.
>    ![](/tutorials/simpleVMWorkshop/figures/grantAccess.png){: .responsive-img }
> 
> 7. Confirm the checkboxes and click on Start.
>    While the VM is starting please fill out our [user survey](https://cloud.denbi.de/survey/index.php/638945?lang=en).
>
{: .hands_on}

### **3.2 Interact with the SRA Mirror and search for more datasets to analyse**

> ## Hands On
> 1. You are now on the `Instance Overview` page. You can delete your old VM which
>    we used to create your snapshot. To do this, open the action selection of the old machine again
>    by clicking on 'Show Actions' and select 'Delete VM'. Confirm the deletion of the machine.
>    
> 2. On your new VM, please click on `how to connect`.
>    You should see again a link. Please click on the link to open Theia-IDE on a new
>    browser tab.
>    ![](/tutorials/simpleVMWorkshop/figures/howtoconnect.png){: .responsive-img }
> 
> 3. Click on `Terminal` in the upper menu and select `New Terminal`.
>    ![](/tutorials/simpleVMWorkshop/figures/terminal.png){: .responsive-img }
> 
> 4. Activate the conda environment by running:
>    ```bash
>    conda activate denbi
>    ```
>    
> 5. Unfortunately, conda does not offer a minio cli binary,
>    which means that we would have to install it manually.
>    Download the binary:
>    ```bash
>    wget https://dl.min.io/client/mc/release/linux-amd64/mc
>    ```
>    Move it to a folder where other binaries usually are stored:
>    ```bash
>    sudo mv mc /usr/local/bin/
>    ```
>    Change file permissions:
>    ```bash
>    chmod a+x /usr/local/bin/mc
>    ```
> 
> 6. Add S3 config for our public SRA mirror on our Bielefeld Cloud site:
>    ```bash
>    mc config host add sra https://openstack.cebitec.uni-bielefeld.de:8080 "" ""
>    ```
> 
> 7. List which files are available for SRA number `SRR3984908`:
>    ```bash
>    mc ls sra/ftp.era.ebi.ac.uk/vol1/fastq/SRR398/008/SRR3984908
>    ```
> 
> 8. Check the size of these files
>    ```bash
>    mc du sra/ftp.era.ebi.ac.uk/vol1/fastq/SRR398/008/SRR3984908
>    ```
> 
> 9. You can read the first lines of these files by using `mc cat`.
>    ```bash
>    mc cat sra/ftp.era.ebi.ac.uk/vol1/fastq/SRR398/008/SRR3984908/SRR3984908_1.fastq.gz | zcat | head
>    ```
> 
> 10. Search for SRA run accessions we want to analyse and check the sum of their size
>    (this may take a while to complete):
>    ```bash
>    mc find --regex "SRR6439511.*|SRR6439513.*|ERR3277263.*|ERR929737.*|ERR929724.*"  sra/ftp.era.ebi.ac.uk/vol1/fastq  -exec "  mc ls -r --json  {} " \
>       |  jq -s 'map(.size) | add'  \
>       | numfmt --to=iec-i --suffix=B --padding=7
>    ```
>
{: .hands_on}

> ## Explanation
>    * `mc find` reports all files that have one of the following prefixes in their file name: `SRR6439511.`, `SRR6439513.`, `ERR3277263.`, `ERR929737.`, `ERR929724.`.
>    *  `jq` uses the json that is produced by `mc find` and sums up the size of all files (`.size` field).
>    * `numfmt` transforms the sum to a human-readable string.
>   
{: .details}


### **3.3 Run commands with more cores and plot your result**

1. We created a mash index out of selected genomes that were classified as  
   "greatest threat to human health" by the [World Health Organisation (WHO)
   in 2017](https://www.who.int/news/item/27-02-2017-who-publishes-list-of-bacteria-for-which-new-antibiotics-are-urgently-needed)
   Please download the index:
   ```bash
   wget https://openstack.cebitec.uni-bielefeld.de:8080/simplevm-workshop/genomes.msh
   ```

2. We created a file that points to the datasets that you have found in the previous chapter.
   Download the input file via:
   ```bash
   wget https://openstack.cebitec.uni-bielefeld.de:8080/simplevm-workshop/reads.tsv
   ```
   You can inspect the file by using `cat`:
   ```bash
   cat reads.tsv
   ```
3. We will create a directory for the output for the following command. We will place an output
   file for every SRA ID.
   ```bash
   mkdir -p output
   ```

4. You can now run the commands from the first part with found datasets as input (this may take a while to complete):
   Create a function that we will run in prallel:
   ```bash
   search(){ 
      left_read=$(echo $1 | cut -d ' '  -f 1);  
      right_read=$(echo $1 | cut -d ' ' -f 2); 
      sra_id=$(echo ${left_read} | rev | cut -d '/' -f 1 | rev | cut -d '_' -f 1 | cut -d '.' -f 1);
      mc cat $left_read $right_read | mash screen -p 3 genomes.msh - \
          | sed "s/^/${sra_id}\t/g"  \
          | sed 's/\//\t/' > output/${sra_id}.txt ;
   }
   ```
   
> ## Explanation
>   In order to understand what this function does let's take the following datasets as an example:
> 
> >```bash
> > sra/ftp.era.ebi.ac.uk/vol1/fastq/SRR643/001/SRR6439511/SRR6439511_1.fastq.gz
> > sra/ftp.era.ebi.ac.uk/vol1/fastq/SRR643/001/SRR6439511/SRR6439511_2.fastq.gz
> > ```
>   where  
>    * `left_read` is left file (`sra/ftp.era.ebi.ac.uk/vol1/fastq/SRR643/001/SRR6439511/SRR6439511_1.fastq.gz`)
>    * `right_read` is the right file (`sra/ftp.era.ebi.ac.uk/vol1/fastq/SRR643/001/SRR6439511/SRR6439511_2.fastq.gz`)
>    * `sra_id` is the prefix of the file name (`SRR6439511`)
>    * `mc cat` streams the files into `mash screen` which is using the sketched genomes `genomes.msh`
>       to filter the datasets.
>    * Both `sed`s are just post-processing the output and place every match in the `output` folder.
>      
{: .details}  

   Export this function, so that we can use it in the next command.
   ```bash
   export -f search
   ```
   Run your analysis in parallel.
   ```bash
   parallel -a reads.tsv search
   ```
   where
     * `reads.tsv` is a list of datasets that we want to scan.
     * `search` is the function that we want to call.
   
   
5. Optional: This command will run a few minutes. You could open a second terminal
   and inspect the cpu utilization with `htop`.
   ![](/tutorials/simpleVMWorkshop/figures/htop.png){: .responsive-img }

6. Concatenate all results into one file via 
   ```bash
   cat output/*.txt > output.tsv
   ```

7. Let's plot how many genomes we have found against the number of their matched k-mer hashes:
   ```bash
   csvtk -t plot hist -H -f 3 output.tsv -o output.pdf
   ```
   You can open this file by a click on the Explorer View and selecting the pdf. 
   ![](/tutorials/simpleVMWorkshop/figures/openpdf.png){: .responsive-img }

8. Get the title and the environment name about the found datasets by using Entrez tools
   ```bash
   for sraid in $(ls -1 output/ | cut -f 1 -d '.'); do  
     esearch -db sra -query ${sraid} \
       | esummary \
       | xtract -pattern DocumentSummary -element @ScientificName,Title \
       | sort | uniq  \
       | sed "s/^/${sraid}\t/g"; 
   done > publications.tsv
   ```
    
> ## Explanation
>    * `for sraid in $(ls -1 output/ | cut -f 1 -d '.');` iterates over all datasets found in the output
>      directory.
>    * `esearch` just looks up the scientific name and title of the SRA study.
>    * 'sed' adds the SRA ID to the output table. The first column is the SRA ID, the second column is 
>       the scientific name and the third column is the study title.
>    * All results are stored the `publications.tsv` file.
>
{: .details}

9. Set correct permissions on your volume:
   ```bash
   sudo chown ubuntu:ubuntu /vol/data/
   ```

10. Copy your results to the volume for later use:
    ```bash
    cp publications.tsv output.tsv /vol/data
    ```

11. Go to the Instance Overview page. Click on actions and detach the volume.
    ![](/tutorials/simpleVMWorkshop/figures/detachvolume.png){: .responsive-img }

12. Finally, since you saved your output data you can safely delete the VM.


## **Section 4: Inspect your generated data via a research environment**

We now want to start a new VM. This time we would like to use RStudio 
in order to inspect and visualize our results.

### **4.1 Create a VM based on a Research Environment**

1. Start a new VM. This time select again the de.NBI default flavor since
   we do not need that much resources anymore.

2. In the image tab please select Rstudio (`RStudio-ubuntu22.04`).
   
3. In the volume tab please choose the volume you created
   in the previous part of the workshop.
   Please use again `/vol/data` as mountpath. Click on `Add +` to add the volume.
   ![](/tutorials/simpleVMWorkshop/figures/reuseVolume.png){: .responsive-img }

4. Grant again access to all project members with a `Cloud-portal-support` tag.
   This way these members get ssh access to your VM and can help you in case
   something does not work as expected.
   ![](/tutorials/simpleVMWorkshop/figures/grantAccess.png){: .responsive-img }

5. Confirm all checkboxes and click on start.
   Since it takes some time until the VM is started, please complete the last part of the
   [unix tutorial](https://github.com/deNBI/unix-course#part-3-advanced-concepts) in the meantime.

6. Again it will take some while to start the machine. On the instance overview, select `How to connect` of the newly started VM 
   and click on the URL. A tab should be opened up in your browser.

### **4.2 RStudio**

1. Login credentials for the RStudio user login are.
   ```
   Username: ubuntu  
   Password: simplevm
   ```

2. In RStudio please open a Terminal first by either selecting the `Terminal` tab, or by clicking on
   `Tools` -> `Terminal` -> `New Terminal`.

3. Download the Script by running wget:
   ```bash
   wget https://openstack.cebitec.uni-bielefeld.de:8080/simplevm-workshop/analyse.Rmd
   ```   
   
4. Further you have to install necessary R libraries. Please switch back
   to the R console:
   ![](/tutorials/simpleVMWorkshop/figures/rconsole.png){: .responsive-img }
   
   Install the following libraries: 
   ```R
   install.packages(c("ggplot2","RColorBrewer","rmarkdown"))
   ```
5. You can now open the `analyse.Rmd` R notebook via `File` -> `Open File`.

6. You can now start the script by clicking on `Run` -> `Restart R and run all chunks`.
  ![](/tutorials/simpleVMWorkshop/figures/runRScript.png){: .responsive-img }

### **4.3 Provide your research data to a reviewer**

Finally, you may want to publish your results once you are done with your research project.
You could provide your data and tools via your snapshot and volumes to a reviewer,
who could reproduce your results. Alternatively, you can also provide the Rmarkdown document 
together with the input data to reproduce the last part of the analysis and the visualization.

You can share your research results via [Zenodo](https://zenodo.org/), [Figshare](https://figshare.com/)
and other providers who will generate a citable, stable Digital Object Identifier (DOI) for your results.
[re3data](https://www.re3data.org/) provides an overview of research data repositories that are suitable 
for your domain-specific research results.


## **Section 5: Use a cluster setup to further scale up your analysis**

In this part of the tutorial you will scale up your cluster horizontally by using a SimpleVM Cluster.
A SimpleVM Cluster consists of a master and multiple worker nodes. On all nodes a SLURM workload manager
will be installed. SLURM allows you to submit scripts, so-called jobs, that are queued up and once there
are free resources (CPUs, RAM) available on one of the worker nodes the script will be executed on that node.
This way you don't have to look up which nodes are free in order to run your jobs.
In the following you will configure a cluster and submit your tools to a SLURM job scheduler. 

### **5.1 Create a Cluster**

1. Click on "New Cluster" on the left menu.
   If you can not see the "New Cluster" item then reload the page.

2. Since your master node is just used for submitting jobs, please select *de.NBI mini* as flavor and
   the snapshot **SimpleVMIntro23** as image.
   ![](/tutorials/simpleVMWorkshop/figures/clusterMasterImage.png){: .responsive-img }
   The same snapshot will also be used for all worker nodes.
3. The worker nodes will run the actual tools, so we need a flavor wir more cores then the one
   that the master node is using. Therefore, please select *de.NBI large* as flavor and start
   two worker nodes by providing `2` as the worker count.
      ![](/tutorials/simpleVMWorkshop/figures/batch_worker.png){: .responsive-img }


5. Now click on Start! That's it! Just with a few clicks you started your own cluster.


### **5.2 Investigate your cluster setup**

1. Click on the Clusters tab (Overview -> Clusters). After you have initiated the start-up of the cluster,
   you should have been automatically redirected there. Now open the "How to connect"
   dropdown of your machine. Click on the Theia ide URL which opens a new browser tab.

2. Click on `Terminal` in the upper menu and select `New Terminal`.
   ![](/tutorials/simpleVMWorkshop/figures/terminal.png)

3. Check how many nodes are part of your cluster by using `sinfo`

```bash
sinfo
```
which will produce the following example output

> ## Code Out
> ```
> PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
> debug*       up   infinite      2   idle bibigrid-worker-1-1-us6t5hdtlklq7h9,bibigrid-worker-1-2-us6t5hdtlklq7h9
> ```
{: .code-out}

The important columns here are `STATE` which tells you if the worker nodes are processing jobs
or are just in `idle` state and the column `NODELIST` which is just a list of nodes.

4. You could now submit a job and test if your cluster is working as expected.
   `/vol/spool` is the folder which is shared between all nodes. You should always submit jobs
   from that directory.
   ```bash
   cd /vol/spool
   ```

5. Please fetch the script that we want to execute
   ```bash
   wget https://openstack.cebitec.uni-bielefeld.de:8080/simplevm-workshop/basic.sh
   ```
   The script contains the following content:
   ```bash
   #!/bin/bash
   
   #Do not do anything for 30 seconds 
   sleep 30
   #Print out the name of the machine where the job was executed
   hostname
   ```
   where
    * `sleep 30` will delay the process for 30 seconds.
    * `hostname` reports the name of the worker node.

6. You could now submit the job to the SLURM scheduler by using `sbatch` and directly after that
   check if SLURM is executing your script with `squeue`.

   sbatch:
   ```bash
   sbatch basic.sh
   ```
   
   squeue:
   ```bash
   squeue
   ```
   which will produce the following example output:


> ## Code Out
> ```
>    JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
>    212     debug basic.sh   ubuntu  R       0:03      1 bibigrid-worker-1-1-us6t5hdtlklq7h9
> ```
{: .code-out}

   Squeue tells you the state of your jobs and which nodes are actually executing them.
   In this example you should see that `bibigrid-worker-1-1-us6t5hdtlklq7h9` is running (`ST` column) your job
   with the name `basic.sh`.

8. Once the job has finished you should see a slurm output file in your directory (Example: `slurm-212.out`)
   which will contain the name of the worker node which executed your script.
   Open the file with the following command:
   ```bash
   cat slurm-*.out
   ```
   
> ## Code Out: Example output
>    ```
>    bibigrid-worker-1-1-us6t5hdtlklq7h9
>    ```
{: .code-out}

9. One way to distribute jobs is to use so-called array jobs. With array jobs you specify how many times
   your script should be executed. Every time the script is executed, a number between 1 and the number of times
   you want the script to be executed is assigned to the script execution. The specific number is saved in a
   variable (`SLURM_ARRAY_TASK_ID`). If you specify `--array=1-100` then your script is 100 times executed and
   the `SLURM_ARRAY_TASK_ID` variable will get a value between 1 and 100. SLURM will distribute the
   jobs on your cluster.

   Please fetch the modified script
   ```bash
   wget https://openstack.cebitec.uni-bielefeld.de:8080/simplevm-workshop/basic_array.sh
   ```

   Which is simply reading out the `SLURM_ARRAY_TASK_ID` variable and placing them in a file in an
   output directory:

> ## Code In
>    ```bash
>    #!/bin/bash
>    
>    # Create output directory in case it was not created so far
>    mkdir -p output_array
>    
>    #Do not do anything for 10 seconds 
>    sleep 10
>    
>    #Create a file with the name of SLURM_ARRAY_TASK_ID content. 
>    touch output_array/${SLURM_ARRAY_TASK_ID}
>    ```
{: .code-in}

   You can execute this script a 100 times with the following command 
   ```bash
   sbatch --array=1-100 basic_array.sh
   ```
   
   If you now check the `output_array` folder, you should see numbers from 0 to 100.
   ```bash
   ls output_array
   ```

### **5.3 Scan the SRA for genomes**

1. We can now reuse the `search` function of the third part of this tutorial and
submit an array job with the number of datasets we want to scan. Remember the search function
searches a list of genomes in a list of metagenomic datasets. 

Please download the updated script by using wget:

```bash
wget https://openstack.cebitec.uni-bielefeld.de:8080/simplevm-workshop/search.sh
```

> ## This is the content of the script
> > ```bash
> > #!/bin/bash
> >
> > #Create an output directory
> > mkdir output_final
> >
> > #Use the conda environment you installed in your snapshot and activate it
> > eval "$(conda shell.bash hook)"
> > conda activate denbi
> > 
> > #Add S3 SRA OpenStack Config
> > /vol/spool/mc config host add sra https://openstack.cebitec.uni-bielefeld.de:8080 "" ""
> > 
> > #Define search function you have already used in part 3
> > search(){
> >    left_read=$(echo $1 | cut -d ' '  -f 1);  
> >    right_read=$(echo $1 | cut -d ' ' -f 2);
> >    sra_id=$(echo ${left_read} | rev | cut -d '/' -f 1 | rev | cut -d '_' -f 1 | cut -d '.' -f 1);
> >    /vol/spool/mc cat $left_read $right_read | mash screen -p 3 genomes.msh - \
> >         | sed "s/^/${sra_id}\t/g"  \
> >         | sed 's/\//\t/' > output_final/${sra_id}.txt ;
> > }
> > 
> > #Create a variable for the array task id
> > LINE_NUMBER=${SLURM_ARRAY_TASK_ID}
> > LINE=$(sed "${LINE_NUMBER}q;d" reads2.tsv)
> > 
> > #Search for the datasets
> > search ${LINE} 
> > ```
>
{: .keypoints}

2. The input for the script is a file containing fastq datasets (`reads.tsv`) and
a file containing a sketch of the genomes.

Fastq datasets:
```bash
wget https://openstack.cebitec.uni-bielefeld.de:8080/simplevm-workshop/reads2.tsv
```

Sketch:
```bash
wget https://openstack.cebitec.uni-bielefeld.de:8080/simplevm-workshop/genomes.msh
```

3. We also need to download `mc` again since it was not saved as part of the snapshot.

```bash
wget https://dl.min.io/client/mc/release/linux-amd64/mc
```

Please set executable rights:

```bash
chmod a+x mc
```

4. You can execute the array job by using the following command:

```bash
sbatch --array=1-386 search.sh
```

5. You could now check the state of your jobs by using `squeue`.
   Please note that the job execution might take a few hours. The VM will be available even after the workshop.
   If you are interested in the results, you could plot them later.

6. Concatenate all results into one file via `cat output_final/*.txt > output_final.tsv`

7. Let's plot how many genomes we have found against the number of their matched k-mer hashes:
   Activate the denbi conda environment:
   ```bash
   conda activate denbi
   ```
   Run `csvtk` on the output

   
   ```bash
   csvtk -t plot hist -H -f 3 output_final.tsv -o output_final.pdf
   ```
   You can open this file by a click on the Explorer View and selecting the pdf.
   ![](/tutorials/simpleVMWorkshop/figures/spoolPDF.png)
    
   Since there are many matches with a low number of k-mer hashes, you could filter the table first and plot
   the filtered results.
   ```bash
   sort -rnk 3,3 output_final.tsv | head -n 50 > output_final_top50.tsv
   ```   

   ```bash
   csvtk -t plot hist -H -f 3 output_final_top50.tsv -o output_final_top50.pdf
   ```

9. Finally, you could view the top matches via `less` and check their description on the 
   [SRA website](https://www.ncbi.nlm.nih.gov/sra) by providing the SRA run accession
   (Example `ERR4181696`) for further investigation.
   ```bash
   less output_final_top50.tsv
   ```