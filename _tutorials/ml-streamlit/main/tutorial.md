---
layout: tutorial_hands_on
title: Setting up ML project in the cloud infrastructure
description: Transform a trained model into an online service with a UI using Streamlit.
time_estimation: 5H
level: intermediate
questions:
  - How does TabICL simplify the training process compared to traditional machine learning models?
objectives:
  - Learn how to create, configure, and access a VM instance in the de.NBI Cloud using SimpleVM.
  - Learn basics of Streamlit syntax and deploy a trained ML model as an interactive web application.
key_points:
  - Streamlit allows rapid creation of user-friendly web apps for deploying models and sharing results.
version:
  - main
life_cycle: under development
contributions:
  authorship:
  - Dilfuza Djamalova
  editing: 
  funding: 
  - deKCD
---

## Introduction
Machine learning projects often demand far more computational power and storage than what is typically available on local machines. Training models on large-scale datasets can quickly exceed the capabilities of personal hardware. Cloud infrastructure solves this problem by providing scalable, on-demand computing resources, making it easier to train models faster, manage larger datasets, and run reproducible workflows. Understanding how to create, configure, and access virtual machines (VMs) in the cloud is a foundational skill for scaling machine learning workflows whether for research experiments or production deployments. 

In this hands-on tutorial, you will learn how to (1) create a VM instance on the de.NBI Cloud using SimpleVM; (2) preprocess and embed protein sequence dataset for training TabICL - a tabular foundation model for in-context learning on large datasets; (3) transform your trained model  into an online app/service with a user interface using Streamlit.

><comment-title>Note</comment-title>
> This tutorial focuses on scaling machine learning workflows in the cloud, not on the theoretical aspects of how machine learning models learn. We assume you already have basic to intermediate knowledge of model training and libraries like **scikit-learn**. 
> 
{: .comment}

><details-title>Prerequisites</details-title>
>Before you start, ensure you meet the following requirements:
>
> - LifeScience AAI account to access the de.NBI Cloud
>    - You can find instructions for registration and setup in the [de.NBI Cloud Wiki](https://cloud.denbi.de/get-started/)
> - Familiarity with the Unix commands and the SimpleVM
>    - Review the [previous tutorial on Unix commands](/tutorials/unix-course/main/tutorial.md) or check the [SimpleVM Wiki](https://simplevm.denbi.de/wiki/)
> - Basic to intermediate experience with machine learning model training and using `scikit-learn` library.
{: .details}
  
## **Preparation**

### **Access SimpleVM instance**

If you are already a member of a SimpleVM project, you can proceed to create a VM instance. If you are unfamiliar with this process, we recommend reviewing our [SimpleVM tutorial](/tutorials/simpleVMWorkshop/main/tutorial/) and the [SimpleVM Wiki](https://simplevm.denbi.de/wiki/) for step-by-step guidance.

><tip-title>Instance Flavor</tip-title>
> Ensure to select a flavor with the enough RAM and GPU, *e.g.* FIXME 
> 
{: .tip}

### **Install the required packages**

For this hands-on tutorial, we need to install the following packages:
- [torch](https://pytorch.org/)
- [huggingface datasets](https://huggingface.co/docs/datasets/en/installation#pip)
- [tabicl](https://github.com/soda-inria/tabicl/tree/main?tab=readme-ov-file#from-pypi)
- [sklearn](https://scikit-learn.org/stable/install.html)
- [pandas](https://pandas.pydata.org/) 
- [biopython](https://pypi.org/project/biopython/)
- [Streamlit](https://docs.streamlit.io/)
- *(Optional)* [jupyterlab](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html)

Once you have logged in your instance, install the `pip` following [this instructions](https://pip.pypa.io/en/stable/installation/)

><code-in-title>Install `venv` and `pip3`</code-in-title>
> ```bash
> sudo apt update
> sudo apt install python3-venv python3-pip -y
> pip3 --version
> ``` 
{: .code-in}

><code-in-title>Activate virtual environment and upgrade `pip`</code-in-title>
> ```bash
> python3 -m venv ~/mlenv
> source ~/mlenv/bin/activate
> ```
{: .code-in}

To install torch, please check the [PyTorch site](https://pytorch.org/get-started/locally/). Depending on your compute platform, select CPU or CUDA version and run the suggested command, *e.g.*: 

![torch installation]({{ "/tutorials/ml-streamlit/img/torch_installation.png" | relative_url }}){: .responsive-img }

><code-in-title>Install the remaining packages:</code-in-title>
> ```bash
> pip install pandas
> pip3 install -U scikit-learn
> pip install tabicl # TabICL model
> pip install datasets # Huggingface Datasets 
> pip install streamlit # for model deployment
> pip install biopython
> ```
{: .code-in}

---
{% include _tutorials/ml-streamlit/main/part_01.md %}

---

---

---

><details-title>What to learn next?</details-title>
> Explore alternative approaches to deploy your trained model on the cloud:
> * [Deploy the model on cloud with FastAPI](/tutorials/ml-fastapi/main/tutorial/)
{: .details}