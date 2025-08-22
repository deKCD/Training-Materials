---
layout: tutorial_hands_on
title: Ansible
description: 
slug: ansible
time_estimation: FIXME
questions:
  - How can Ansible automate software installation across a cluster?
  - What steps are required to set up Kraken2 and Krona for metagenomic analysis?
  - How can results be processed, scheduled, and visualized efficiently in a grid environment?
objectives:
  - Build and customize an Ansible role for installing bioinformatics tools.
  - Use Ansible Galaxy to integrate external roles for additional tools like Krona.
  - Run and visualize Kraken2 taxonomic classification results across a cluster environment.
key_points:
  - Ansible simplifies automated deployment and configuration across multiple nodes.
  - Kraken2 enables efficient taxonomic classification; Krona supports interactive visualization.
  - BibiGrid combined with Slurm scheduling allows scalable execution of bioinformatics workloads.
version:
  - main
life_cycle: "alpha"
contributions:
  authorship:
    - Alexander Walender
  editing: 
  funding:
---


This is an Ansible skeleton role as hands-on tutorial for setting up kraken in the bibigrid cluster.
Also we have a [Wiki-Tutorial](https://cloud.denbi.de/wiki/Tutorials/Ansible/) on de.NBI Cloud available, which can help to give an overiew.

In this hands-on, we want you to create an ansible role for installing the bioinformatics tool [Kraken](https://ccb.jhu.edu/software/kraken2/).
We want to install kraken on all machines in our freshly created BibiGrid-Cluster:

![overview]({{ site.baseurl }}/tutorials/ansible/gfx/overview.png){: .responsive-img }
  
We will also install [Krona](https://github.com/marbl/Krona/wiki) in our cluster, a tool for data exploring in the fields of metagenomics.

## Table of Contents
* [Preparation](#preparation)
* [Tasks](#tasks)

## **Preparation**
To get started, download this repository in your BibiGrid-Master node by executing on your master node:

```ssh
cd ~
git clone https://gitlab.ub.uni-bielefeld.de/denbi/ansible-course.git
```

After this, change the directory:
```ssh
cd ansible-course/
```
  
You will see various files listed here. Some of these files have tasks assigned on them. We will walk you through these
tasks. 
  
## **Tasks**

> ## **Task 0:** Create a hosts (inventory) file.
> As you remember, an ansible inventory is mandatory.
> In the project folder you should see a file called ``hosts``. Open this file in your theia environment or manually
> and follow its instructions.
> 
> If you want to check afterwards that your `hosts`-file is correct, you could try to use this file with `ansible` to ping all machines
> listed in this file with:
> 
> ```
> # make sure to execute this inside the ansible-course/ folder
> ansible all -i hosts -m ping
> ```
>
{: .hands_on}

> ## **Task 1:** Edit the site.yml base playbook
> The `./site.yml` file in the base-folder of this project, describes all actions that will be executed
> in our cluster. This file should include all roles needed for this tutorial. Open the file and edit the missing fields.
> 
> ![task1]({{ site.baseurl }}/tutorials/ansible/gfx/task1site.png){: .responsive-img }
>
{: .hands_on}

> ## **Task 2:** Insert the tasks for the kraken role
> In `roles/clum2022.kraken2/tasks/main.yml`, you will see a list of tasks needed to be executed in order to get kraken installed.
> I have set up the basic structure. You will need to fill out the missing fields. Follow the instructions in this file
> and prepare to "google" for some ansible modules 😉
> 
> ![task2]({{ site.baseurl }}/tutorials/ansible/gfx/task2.png){: .responsive-img }
>
{: .hands_on}

> ## **Task 3:** Get familiar with Ansible Galaxy.
> Including the kraken role (which you have finished creating) is sadly not enough. We need an additional role
> for installing **Krona**, our visualisation tool. I have uploaded a role for this tool to Ansible Galaxy.
> You will need to use the ansible-galaxy command-line-tool in order to download this role to your BibiGrid-master node.
> Follow the instructions in the file ``./site.yml``, which you have previously edited in [Task 1](#task-1-edit-the-siteyml-base-playbook). On the lower part
> of the file you should see the instructions for this task.
> 
> > ## **Optional:** Install more roles from Ansible-Galaxy
> > You can also search for roles with ``ansible-galaxy search [TAGS]``. Try installing and adding various roles.
> > ANXS.nodejs and ANXS.build-essential are good starts.
> {: .hands_on}
> 
{: .hands_on}

> ## **Task 4:** Execute everything!
> After every task has been finished, we can finally make the ansible call to setup all of our needed tools.
> For this, make the ansible call (from the root of this project folder): `ansible-playbook -i hosts site.yml`
> If everything is alright, you should see no errors on the result screen.
>
{: .hands_on}
 
> ## **Task 5:** Access public ECBI storage and download a kraken2 database
> You may have noticed, that there is another `.yml` file in the project root folder called `minio_kraken.yml`:
> 
> ![ganesha]({{ site.baseurl }}/tutorials/ansible/gfx/ganesha.png){: .responsive-img }
> 
> I have already prepared an Ansible Playbook which connects to our public ECBI database.
> It will automaticaly download a base kraken2 database. Just execute this playbook with `ansible-playbook -i hosts minio_kraken.yml`.
> You can also take a look inside the file to check out its tasks.
>
{: .hands_on}

> ## **Task 6:** Make some taxonomic classification on our Grid-Cluster
> For a quick overview, we now have the following volumes:
> 
> * `/vol/spool/` <- This is the shared volume via nfs over all nodes in your BibiGrid setup.
> * `/vol/scratch/` <- This is the working directory. Each worker node has its own.
> 
> Also, we have access to a publicly available NCBI-Database via our S3-Storage.
> If you don't know anything about the S3-Protocol, you can find additional info [here](https://cloud.denbi.de/wiki/Tutorials/ObjectStorage/).
> In S3, data is accessible via HTTP and with simple tools like `mc`. Thanks to Ansible, we can browse this public
> database, for example:
> 
> ```bash
> mc ls bielefeld/ftp.era.ebi.ac.uk/vol1/fastq/
> ```
> 
> At this point, you have extended your BibiGrid-Cluster with the following features:
> 
> * Every worker node has `kraken2` installed, which is a taxonomic classification tool.
> * Every worker node has the `kraken2` database ready, which is used for cross-references.
> * The master node has `krona` installed, which can take a `kraken2`-result and visualize them via `HTML`.
> * Each node has `mc` installed and configured.
> 
> > ## How do we make use of this?
> > 
> > We will make use of the `Slurm`-Engine which has been installed via BibiGrid beforehand. `Slurm` is a grid scheduler,
> > which can schedule workloads over the whole cluster. I have prepared 2 types of workload examples, you can find them
> > in this repo at `./slurm_example`.
> > 
> > You can take a look at `./slurm_example/array.sh`. This script has a list of paths from the S3 Storage. The grid-scheduler
> > instructs the worker nodes to download one of these paths and execute `kraken2` on it.
> > 
> > You can schedule this "batch" work with:
> > 
> > ```bash
> > sbatch array.sh
> > ```
> > 
> > ![sbatch]({{ site.baseurl }}/tutorials/ansible/gfx/sbatch.png){: .responsive-img }
> > 
> > You can check the current state of your Slurm-Cluster with `squeue`. After a few minutes, you should see a result 
> > in your shared `/vol/spool/` directory.
> >
> {: .details}
> 
{: .hands_on}


> ## **Task 7:** Visualize your results with krona
> In `/vol/spool/` you should see a new directory named with a timestamp. Inside this folder, you should see some
> result files with the `.krona` file extension:
> 
> ![result]({{ site.baseurl }}/tutorials/ansible/gfx/result.png){: .responsive-img }
> 
> We can now visualize one of these results with `ktImportTaxonomy <resultFile>`.
> After a few minutes, you should find a `.html` file and a html-files directory. You can directly view
> the results by right-clicking on the HTML-File and then "Open with -> Preview"
> 
> ![download]({{ site.baseurl }}/tutorials/ansible/gfx/download.png){: .responsive-img }
> 
> Now you can interactively visualize your work:
> 
> ![krona]({{ site.baseurl }}/tutorials/ansible/gfx/krona.png){: .responsive-img }
>
{: .hands_on}

> ## **Task 8:** Play around and ask questions!
> You now know the basics of Ansible (and Slurm). Play around with your BibiGrid cluster. Extend your ansible playbook
> and try some stuff!
> 
> Maybe you are now considering realising your own projects with Ansible. If you have specific questions regarding that,
> feel free to start a discussion with us. We are happy to help you!
>
{: .hands_on}