---
layout: tutorial_hands_on
title: Setting up ML project in the cloud infrastructure
description: "FIXME"
slug: ml-streamlit
time_estimation: 2H
questions:
  - "How does TabICL simplify the training process compared to traditional machine learning models?"
objectives:
  - "Learn how to create, configure, and access a VM instance in the de.NBI Cloud using SimpleVM."
  - "Learn basics of Streamlit syntax and deploy a trained ML model as an interactive web application."
key_points:
  - "Streamlit allows rapid creation of user-friendly web apps for deploying models and sharing results."
version:
  - main
life_cycle: "alpha"
contributions:
  authorship:
  - Dilfuza Djamalova
  editing: 
  funding: 
  - deKCD
---

Machine learning projects often demand far more computational power and storage than what is typically available on local machines. Training models on large-scale datasets can quickly exceed the capabilities of personal hardware. Cloud infrastructure solves this problem by providing scalable, on-demand computing resources, making it easier to train models faster, manage larger datasets, and run reproducible workflows. Understanding how to create, configure, and access virtual machines (VMs) in the cloud is a foundational skill for scaling machine learning workflows whether for research experiments or production deployments. 

In this hands-on tutorial, you will learn how to (1) create a VM instance on the de.NBI Cloud using SimpleVM; (2) preprocess and embed protein sequence dataset for training TabICL - a tabular foundation model for in-context learning on large datasets; (3) transform your trained model  into an online app/service with a user interface using Streamlit.

> ## Note
> This tutorial focuses on scaling machine learning workflows in the cloud, not on the theoretical aspects of how machine learning models learn. We assume you already have basic to intermediate knowledge of model training and libraries like **scikit-learn**. 
> 
{: .warning}

## **Prerequisites**
Before you start, ensure you meet the following requirements:

- LifeScience AAI account to access the de.NBI Cloud
    - You can find instructions for registration and setup in the [de.NBI Cloud Wiki](https://cloud.denbi.de/get-started/)
- Familiarity with the Unix commands and the SimpleVM
    - Review the [previous tutorial on Unix commands](/tutorials/unix-course/main/tutorial.md) or check the [SimpleVM Wiki](https://simplevm.denbi.de/wiki/)
- Basic to intermediate experience with machine learning model training and using `scikit-learn` library.

## **Table of Content**
* [Preparation](#preparation)
    * [Access SimpleVM instance](#access-simplevm-instance)
    * [Install the required packages](#install-the-required-packages)
* [Get the dataset](#get-the-dataset)
    * [Load and inspect the dataset](#load-and-inspect-the-dataset)
    * [Extract protein embeddings using gLM2](#extract-protein-embeddings-using-glm2)
* [Train TabICL model](#train-tabicl-model)
* [Model deployment on cloud with UI](#model-deployment-on-cloud-with-ui)
    * [Basic Streamlit commands](#basic-streamlit-commands)
    * [Deploy trained model on Streamlit](#deploy-trained-model-on-streamlit)
* [What to learn next?](#what-to-learn-next)
  
## **Preparation**

### **Access SimpleVM instance**

If you are already a member of a SimpleVM project, you can proceed to create a VM instance. If you are unfamiliar with this process, we recommend reviewing our [SimpleVM tutorial](/tutorials/simpleVMWorkshop/main/tutorial/) and the [SimpleVM Wiki](https://simplevm.denbi.de/wiki/) for step-by-step guidance.

> ## Instance Flavor
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

> ## Install `venv` and `pip3`
> ```bash
> sudo apt update
> sudo apt install python3-venv python3-pip -y
> pip3 --version
> ``` 
{: .code-in}

> ## Activate virtual environment and upgrade `pip`
> ```bash
> python3 -m venv ~/mlenv
> source ~/mlenv/bin/activate
> ```
>
{: .code-in}

To install torch, please check the [PyTorch site](https://pytorch.org/get-started/locally/). Depending on your compute platform, select CPU or CUDA version and run the suggested command, *e.g.*: 

![torch installation](/tutorials/ml-streamlit/img/torch_installation.png){: .responsive-img }


> ## Install the remaining packages:
> ```bash
> pip install pandas
> pip3 install -U scikit-learn
> pip install tabicl # TabICL model
> pip install datasets # Huggingface Datasets 
> pip install streamlit # for model deployment
> pip install biopython
> ```
{: .code-in}

## **Get the dataset**

In this tutorial, we will use `tattabio/mibig_classification_prot` dataset from the [Hugging Face](https://huggingface.co/datasets/tattabio/mibig_classification_prot) as an example for our classification task. 

The [MIBiG](https://mibig.secondarymetabolites.org/) — *Minimum Information about a Biosynthetic Gene Cluster* — is a community-driven standard for annotating biosynthetic gene clusters (BGCs) and their associated molecular products.

BGCs are physically linked sets of genes on a genome that collectively encode a biosynthetic pathway for producing specific metabolites, including antibiotics and antifungals, which are of great interest to the agricultural and pharmaceutical industries.

MIBiG standard provides a structured way to categorize BGCs by product type (*e.g.*, nonribosomal peptides (NRPs), terpenes, saccharides) and enable standardized data sharing and reproducible research.
  
In our case, we will use this dataset to train a protein sequence classifier that predicts the class of each BGC based on sequence information.

### **Load and inspect the dataset**
Hugging Face Datasets provides several easy ways to load the data. Navigate to `Use this dataset` in the dataset page and select one of the libraries:
![Load the dataset](/tutorials/ml-streamlit/img/get_data.png){: .responsive-img }

For this tutorial, we will use the `datasets` library from Hugging Face:

> ## Load dataset
> ```python
> from datasets import load_dataset
> 
> ds = load_dataset("tattabio/mibig_classification_prot")
> print(ds)
> ```
{: .code-in}

This returns the following dataset structure:

> ## Dataset structure
> ```
DatasetDict({
    train: Dataset({
        features: ['Entry', 'Sequence', 'bgc', 'class', 'simple_class'],
        num_rows: 29992
    })
    test: Dataset({
        features: ['Entry', 'Sequence', 'bgc', 'class', 'simple_class'],
        num_rows: 7213
    })
})
> ```
{: .code-out}

The dataset comes with:
- pre-defined train/test splits for reproducible training.
- five attributes for each sample:
      - `Entry`: protein identifier
      - `Sequence`: protein sequence
      - `bgc`: biosynthetic gene cluster ID
      - `class`: detailed BGC class
      - `simple_class`: simplified, broader class categories
  
Convert the Hugging Face Dataset objects to Pandas DataFrames for easier manipulation using `.to_pandas()`:

```python
train = ds["train"].to_pandas()
test = ds["test"].to_pandas()
```

Now, let’s explore the dataset to better understand its structure before training our model.

> ## Tasks
> 1. Handle duplicates in the `Entry` column for both train and test splits. Keep the same number of samples as before, but assign unique indices by creating a new column `Entry_id`.
> 2. Count how many unique classes exist in both `simple_class` and `class`. Identify which classes are most common in the dataset.
> 
>> ## Solution
>> 1. One way to ensure unique `Entry_id` values is:
>> ```python
>> train.sort_values(by="Entry", inplace=True)
>> train["Entry_id"] = train.groupby("Entry").cumcount().astype(str)
>> train['Entry_id'] = train['Entry'] + '_' + train['Entry_id']
>> ```
>> 2. Use `.value_counts()` to inspect the distribution. This will reveal which classes dominate the dataset, which is critical for handling class imbalance during model training.
>> 
> {: .solution}
>
{: .hands_on}

> ## Pitfall #1: Class imbalance
>
> In many biological datasets, some classes contain significantly more samples than others — known as **class imbalance**. This can lead to biased models that perform well on majority classes but poorly on minority ones.  
>
> Common strategies to handle class imbalance include:
> - **Resampling techniques**  
>   - *Oversampling* minority classes (*e.g.*, using [SMOTE](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html) or random duplication).  
>   - *Undersampling* majority classes to create a more balanced dataset.  
> - **Class weighting**  
>   - Assigning higher weights to minority classes during training so the model pays more attention to underrepresented categories.  
> - **Data augmentation**  
>   - Generating synthetic samples for minority classes when biologically valid approaches are available.  
> - **Evaluation with balanced metrics**  
>   - Using metrics like F1-score, balanced accuracy, or Matthews Correlation Coefficient (MCC) to better assess model performance across all classes.  
>
{: .tip}

For this tutorial, we will use `simple_class` as the label because:
- it has fewer, well-distributed classes, simplifying the classification task.
- it reduces computational requirements while still demonstrating how to train and evaluate the workflow.

However, when working with more complex datasets, applying one or more of these techniques is recommended to improve model robustness.

### **Extract protein embeddings using gLM2**

To train our classifier, we first need to convert protein sequences into numerical representations, *i.e* embeddings. Embeddings capture biological and contextual information from sequences, enabling the machine learning model to learn patterns effectively. For this, we use the `tattabio/gLM2_650M_embed`, a genomic language model fine-tuned specifically for functional annotation task.
 
> ## gLM papers and platforms! 
> For more information regarding the model, please read the following papers:
> * [Gaia: A Context-Aware Sequence Search and Discovery Tool for Microbial Proteins](https://doi.org/10.1101/2024.11.19.624387)
> * [The OMG dataset: An Open MetaGenomic corpus for mixed-modality genomic language modeling](https://doi.org/10.1101/2024.08.14.607850)
> * [Genomic language model predicts protein co-regulation and function](https://doi.org/10.1038/s41467-024-46947-9)
> 
> Also, if you are interested in functional annotation of the protein sequences, check the [Gaia annotator](https://gaia.tatta.bio/) and [SeqHub](https://seqhub.org/) from the [Tattabio](https://www.tatta.bio/). 
> 
{: .details}


**Step 1: Import the required packages**

```python
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModel, AutoTokenizer
import pandas as pd
```

> ## Packages description
> - `torch` and `torch.utils.data`: for tensor operations and data batching.
> - `transformers`: for loading the gLM2 model and tokenizer.
> - `pandas`: for handling dataframes.
>
{: .details}

Check if GPU is available:

```python
import torch
print(torch.cuda.is_available())  # should return True on GPU-enabled instances
```

Embedding thousands of sequences is computationally intensive. While CPUs are versatile, they process data sequentially and can be orders of magnitude slower. 

GPUs, on the other hand, are optimized for parallel computation. They enable processing many sequences at once, significantly speeding up the embedding step and making large-scale workflows practical.

**Step 2: Load the model and tokenizer**

```python
model_name = 'tattabio/gLM2_650M_embed' # path of the pre-trained model hosted on Hugging Face Hub
device = "cuda" if torch.cuda.is_available() else "cpu" # check if a GPU is available for faster computation; otherwise, run on CPU

model = AutoModel.from_pretrained(model_name, torch_dtype=torch.bfloat16, trust_remote_code=True).cuda()
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
```
Here,  
    - `torch_dtype=torch.bfloat16` – specifies the data type for model weights. Using `bfloat16` reduces memory usage and speeds up computation on GPUs without significantly sacrificing precision.  
    - `trust_remote_code=True` – allows execution of custom code provided by the model repository (required when models have custom architectures or tokenizers). Only use this flag with trusted sources.  
    - `.cuda()` – moves the model to the GPU, enabling faster computation for embedding generation.  
    - `AutoTokenizer.from_pretrained(...)` – loads the tokenizer associated with the model, ensuring proper tokenization of sequences for embedding generation.  


**Step 3: Build a custom `Dataset`**

We define a small `ProteinDataset` class to store sequences and their IDs. This will let the `DataLoader` efficiently iterate through the dataset in batches:

```python
class ProteinDataset(Dataset):
    def __init__(self, seq_dict):
        self.keys = list(seq_dict.keys())
        self.sequences = list(seq_dict.values())

    def __len__(self):
        return len(self.keys)

    def __getitem__(self, idx):
        return self.keys[idx], str(self.sequences[idx])
```

**Step 4: Collate function for tokenization**
The collate function batches sequences together and tokenizes them dynamically. By **padding** (*i.e.*, adding special tokens to shorter sequences so all sequences in a batch have the same length) and **truncating** (*i.e.*, shortening sequences that exceed the maximum length) sequences to the same length within each batch, the model can process them efficiently. 

> ## Padding and Truncation
> For a comprehensive explanation of **padding** and **truncation** strategies, refer to the [Hugging Face documentation](https://huggingface.co/docs/transformers/en/pad_truncation).
> 
{: .details}

```python
def collate_fn(batch):
    keys, sequences = zip(*batch)
    tokens = tokenizer(
        list(sequences),
        padding=True,
        truncation=True,
        return_tensors='pt'
    )
    return keys, tokens
```

**Step 5: Create a `DataLoader`**
The `DataLoader` handles batching, shuffling (if needed), and efficient data loading. Here, we use a `batch_size` of 32 — a good starting point for GPUs with moderate memory. Adjust the size depending on your GPU capacity:

```python
train_dc = train.set_index("Entry_id")["Sequence"].to_dict()
train_dataset = ProteinDataset(train_dc)

train_loader = DataLoader(
    train_dataset,
    batch_size=32,  # adjust based on GPU memory
    shuffle=False,
    collate_fn=collate_fn
)
```

**Step 6: Generate embeddings**

Iterate over the `DataLoader`, move each batch to the GPU, and extract embeddings from the model.
  
```python
embeddings = {}

model.eval()
with torch.no_grad():
    for keys, tokens in tqdm(train_loader, desc="Embedding Sequences"):
        tokens = {k: v.to(device) for k, v in tokens.items()}
        outputs = model(tokens["input_ids"]).pooler_output.cpu()
        for k, emb in zip(keys, outputs):
            embeddings[k] = emb.to(torch.float32)

torch.save(embeddings, "train.pt")          
```

Here, 
- `model.eval()` ensures we are in inference mode (no gradients computed, faster processing).
- `torch.no_grad()` disables gradient tracking, reducing memory usage.

> ## Task
> Repeat the last step for the test split and save the embeddings.
> 
{: .hands_on}

## **Train TabICL model**

Import required packages and additionally split train into `train` and `validation` splits. You will be using `validation` split later for hyperparameter tuning. 

```python
import torch
import pandas as pd
from tabicl import TabICLClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# load train embeddings
train_emb = torch.load("train.pt")
X_train_val = pd.DataFrame({k: v.numpy() for k, v in train_emb.items()}).T

# load test embeddings
test_emb = torch.load("test.pt")
X_test = pd.DataFrame({k: v.numpy() for k, v in test_emb.items()}).T
```

> ## Prepare train and validation splits
> 1. Split the train into **training** and **validation** subsets:  
>    - Use `sklearn.model_selection.train_test_split` for a random split.  
>    - Alternatively, use `sklearn.model_selection.GroupShuffleSplit` with the `groups` parameter set to `X_train_val["bgc"]` to ensure that entries from the same biosynthetic gene cluster (BGC) are kept in the same split, maintaining a balanced class distribution.  
> 2. Extract the corresponding labels for each split to create `y_train` and `y_val` sets.  
> 3. Verify that the number of samples in `X_train`, `X_val`, `y_train`, and `y_val` are consistent.
>
{: .hands_on}

> ## Pitfall #2: Data Leakage
> **Data leakage** occurs when information (samples) from the validation or test set present in the training process. In our case, leakage could happen if protein sequences from the same **BGC class** are present in both the training and validation splits. This leads to overly optimistic results, as the model indirectly "sees" validation data during training.  
> 
> **How to avoid it:**  
> - Use `GroupShuffleSplit` with the `bgc` column as the grouping variable to ensure that all sequences from the same BGC remain in a single split.  
> - Always double-check splits to confirm no overlap of BGC identifiers between training and validation datasets.  
>
> For more information about pitfalls in machine learning applications in genomics, please read this [article](https://www.nature.com/articles/s41576-021-00434-9)
> 
{: .tip}

The code below will automatically download the pre-trained checkpoint from the Hugging Face Hub on first use and choose a GPU if available:

```python
clf = TabICLClassifier(device="cuda:0")
# clf = TabICLClassifier() # to train on CPU
```

TabICL offers a set of hyperparameters to tune which can be checked using `.get_params` method.

```python
clf.get_params()

{'allow_auto_download': True,
 'average_logits': True,
 'batch_size': 8,
 'checkpoint_version': 'tabicl-classifier-v1.1-0506.ckpt',
 'class_shift': True,
 'device': 'cuda:0',
 'feat_shuffle_method': 'latin',
 'inference_config': None,
 'model_path': None,
 'n_estimators': 32,
 'n_jobs': None,
 'norm_methods': None,
 'outlier_threshold': 4.0,
 'random_state': 42,
 'softmax_temperature': 0.9,
 'use_amp': True,
 'use_hierarchical': True,
 'verbose': False}
```

However, TabICL can produce good predictions without hyperparameter tuning, unlike classical methods that require extensive tuning for optimal performance. 

> ## Train TabICL with the default hyperparameters
> 1. Train the classifier with the default parameters.
> 2. Make predictions on the validation set.
> 3. Generate the classification report using `sklearn.metrics.classification_report` or compute any additional metrics from `sklearn.metrics`. You can also save the report for later inspection. 
> 
>> ## Solution
>> ```python
>> clf.fit(X_train, y_train)
>> val_pred = clf.predict(X_val)
>> 
>> report = classification_report(y_val, val_pred, output_dict=True)
>> report = pd.DataFrame(report).transpose()
>> report.reset_index(inplace=True)
>> ```
> {: .solution}
>
{: .hands_on}

> ## Train TabICL with hyperparameter tuning
> 1. Experiment with different values for `n_estimators` (*e.g.*, [50, 100, 150]) and observe their effect on the classifier’s performance.  
> 2. Use `GridSearchCV` with `cv=10` to identify the optimal number of `n_estimators`.  
> 3. Evaluate the tuned model and generate performance reports for both the validation and test sets.  
> 4. *(Optional)* Visualize the results to compare model performance across different hyperparameter settings.  
>
{: .hands_on}

> ## Train TabICL with additional classes
> 1. Retrain the classifier using the more granular labels from the `class` column.  
> 2. Compare the model’s average performance when trained on `simple_class` vs. `class` to evaluate the impact of increased class granularity.  
> 3. *(Optional)* Tune hyperparameters to determine whether the overall performance improves.  
>
{: .hands_on}

Save the trained model using `joblib` library. You may choose other techniques of storing model, *e.g.* `pickle`.

```python
import joblib

joblib.dump(clf, "model.joblib")
```

Congratulations! You have learned how to set up the simple ML project. 

---
## **Model deployment on cloud with UI**

You have trained the classifier to predict BGC — now it is time to share it with others using a simple and interactive web interface using [Streamlit](https://streamlit.io/). 

Streamlit is an open-source framework that lets you turn your machine learning models, data pipelines, or any python script into a web app — with just a few lines of code. 

Installing Streamlit is pretty easy and you can follow the [official documentation](https://docs.streamlit.io/get-started/installation).

> ## Install Streamlit
> ```bash
> pip install streamlit
> ```
> 
{: .code-in}

To check whether streamlit was successfully installed, run the command `streamlit hello` in your terminal and click on local URLs. You will be redirected to the Welcome Page:

![Streamlit Welcome Page](/tutorials/ml-streamlit/img/streamlit_welcome.png){: .responsive-image}

After installation, you would be able to launch your app as follows:

```bash
streamlit run my_app.py
```

Streamlit runs the script from top to bottom each time a user interaction occurs, such as pressing a button or uploading a file. This ensures that the user interface always reflects the current state of your data.

While editing your script, Streamlit automatically detects changes and prompts you to rerun the app. For continuous updates during development, you can enable the "Always rerun" option from the top-right dropdown, allowing the app to refresh automatically whenever you save your code.

### **Basic Streamlit commands**

Here are some commands to help you get started.

> ## Tasks
> Create `my_app.py` and edit it as follows to learn some basics:
> 
> **Titles and text**
> ```python
> import streamlit as st
> 
> st.title("TabICL classifier to predict BGC")
> st.header("Input dataset")
> st.subheader("Upload your protein sequences in FASTA format")
> st.text("This app uses a pre-trained model to make predictions.")
> ```
> 
> **Display data**
> ```python
> import streamlit as st
> import pandas as pd
> 
> # load your data
> df = pd.read_csv("custom_dataset.csv") # provide example dataset here
> # or create a new one
> df = pd.DataFrame(
>     {
>         "samples": ["A", "B", "C"],
>         "feature_1": [0.3, 0.1, 0.7],
>         "class": [0, 1, 0]
>     }
> )
> st.dataframe(df)  # interactive table
> st.table(df.head())  # static table
> st.write(df.describe())  # flexible writer: handles text, tables, plots, etc.
> ```
> 
> **Display charts**
> ```python
> import matplotlib.pyplot as plt
> import seaborn as sns
> 
> fig, ax = plt.subplots()
> sns.histplot(df["feature_1"], ax=ax)
> st.pyplot(fig)
> ```
> 
> ```python
> st.line_chart(df)
> st.bar_chart(df)
> st.area_chart(df)
> ```
> 
> **Images**
> ```python
> from PIL import Image
> img = Image.open("example.jpg") # provide example image here
> st.image(img, caption="Sample image", use_column_width=True)
> ```
> 
{: .hands_on}

For further information, please check the [Streamlit documentation](https://docs.streamlit.io/get-started/fundamentals/main-concepts). 

### **Deploy trained model on Streamlit**

Let's deploy our classifier on Streamlit, with the ability to upload a new protein sequence for model inference and download predictions as a table. Also, provide some details about dataset requirements and model. 

First, create a new folder to store your trained model, python code, and requirements. Create `app.py` file within a folder and import the required packages:

```python
import streamlit as st
import pandas as pd
import joblib
import numpy as np
from tabicl import TabICLClassifier # here import model you used for training
import torch
```

To launch the Streamlit app, run the following command in your terminal:

```bash
streamlit run app.py
```

To access the app via localhost, open a new terminal and establish an SSH tunnel with:

```bash
ssh -N -L localhost:XXXX:localhost:XXXX -i PRIVATE_SSH_KEY INSTANCE@FLOATING_IP
```

Here,
* replace `XXXX` in with the localhost, *e.g.* `localhost:8000:localhost:8000`.
* `-i PRIVATE_SSH_KEY` specifies the SSH key to authenticate with your instance.
* `INSTANCE` corresponds to your username on the remote VM (you can verify it by running `whoami` in your previous terminal session).


To set up the title and description for your app, you may use the functions `st.title`, `st.subheader`, `st.write`, and `st.caption`:

> ## Add title and description
> ```python
> st.title("Biosynthetic Gene Cluster Inference")
> st.subheader("Upload your protein sequences for prediction")
> ```
> 
{: .code-in}

To be able to see the updated page, save the changes and rerun the page via `Rerun` button. 

Let’s create a sidebar which contains some descriptions of data, its format requirements and model information. 

> ## Add sidebar
> ```python
> with st.sidebar:
>     st.header("Input Data Requirements")
>     st.caption("Upload your data for inference.")
>     with st.expander("Supported Formats"):
>         st.markdown("- FASTA")
>     st.divider()
>     
>     st.header("Model Information")
>     st.caption("This model predicts BGC class using protein embeddings")
>     st.markdown("The model is a TabICL classifier trained on protein embeddings generated by `tattabio/gLM2_650M_embed`")
>     st.markdown("- Input feature dimension: 512")
> ```
>
{: .code-in}

You might also specify who trained the model by adding the caption inside the sidebar code snippet. Link your name to your github page:

```python
st.divider()
st.caption("<p style = 'text-align:center'>Developed by <a href='https://github.com/USERNAME'>YOUR_NAME</a></p>", unsafe_allow_html=True)
```
In this example, we use an HTML snippet to format the caption:  

- `<p style='text-align:center'>` centers the paragraph horizontally.  
- `<a href='https://github.com/USERNAME'>YOUR NAME</a>` creates a hyperlink to the developer’s GitHub profile (replace `USERNAME` with your actual GitHub username).  
- `unsafe_allow_html=True` enables Streamlit to render the HTML content as-is. By default, Streamlit sanitizes HTML to prevent security risks; setting this parameter explicitly acknowledges the potential risks and allows custom HTML rendering.

> ## Upload a dataset
> Create a button to upload a dataset. Use `st.button` and `st.file_uploader` functions. Also specify the input data type. 
>
>> ## Solution
>> ```python
>> if st.button("Upload FASTA"):
>>     input_file = st.file_uploader("Choose FASTA file", type="fasta")
>> ```
> {: .solution}
>
{: .hands_on}

Click on button and upload your FASTA file. 

> ## File Uploader
> In Streamlit, the script runs from top to bottom every time the user interacts with the app (*e.g.*, clicking a button). This behavior can cause the file uploader to reset or disappear after an interaction. To keep the file uploader visible after a button click, you need to store the button’s state in `st.session_state`, allowing the app to “remember” that the button was pressed.
> 
> ```python
> # initialize
> if "upload_clicked" not in st.session_state:
>     st.session_state.upload_clicked = {1: False}
> 
> # callback function to update click state
> def mark_upload_clicked(button):
>     st.session_state.upload_clicked[button] = True
> 
> # render button
> st.button("Upload FASTA", on_click=mark_upload_clicked, args=[1])
> 
> if st.session_state.upload_clicked[1]:
>     st.file_uploader("Choose a FASTA file", type=["fasta", "fa"])
> ```
>
{: .tip}

Click on `Upload FASTA` button and upload your file. 

> ## *(Optional Task)* Enter a single protein sequence
> Use `st.text_area` to past a single protein sequence directly 
> 
>> ## Solution
>> ```python
>> if st.session_state.upload_clicked[1]:
>>     st.file_uploader("Choose a FASTA file", type=["fasta", "fa"])
>>     
>>     # paste a single protein sequence
>>     st.markdown("---")
>>     st.markdown("Or paste a single protein sequence")
>>     protein_sequence = st.text_area(
>>         "Enter a protein sequence",    )
>> ```
> {: .solution}
>  
{: .hands_on}

> ## Add model inference button
> 1. Create a new python file in the `src` folder (*e.g.*, `utils.py`) to store reusable functions for protein embeddings extraction and prediction. Move your trained model (`model.joblib`) into the same folder for easy access.
> `utils.py` should include functions to:
> * **parse a FASTA file** – read sequences and their identifiers.
> * **generate embeddings** – compute embeddings for sequences in a FASTA file using your chosen model or embedding method.
> * **make predictions** – load the trained model (`model.joblib`) and predict classes from the generated embeddings.
> 
>> ## Solution
>> ```python
>> import io
>> import joblib
>> from Bio import SeqIO
>> import pandas as pd
>> import torch
>> from transformers import AutoModel, AutoTokenizer
>> from tabicl import TabICLClassifier
>> 
>> # global variables to load models once
>> _embedding_model = None
>> _tokenizer = None
>> _prediction_model = None
>> 
>> def parse_fasta(uploaded_file) -> dict:
>>     """
>>     Parse FASTA file.
>>     """
>>     sequences = {}
>>     fasta_io = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
>>     for rec in SeqIO.parse(fasta_io, "fasta"):
>>         sequences[rec.id] = str(rec.seq)
>>     return sequences
>> 
>> def _load_embedding_model():
>>     """
>>     Load and cache the embedding model and tokenizer.
>>     """
>>     global _embedding_model, _tokenizer
>>     if _embedding_model is None or _tokenizer is None:
>>         _embedding_model = AutoModel.from_pretrained(
>>             "tattabio/gLM2_650M_embed",
>>             torch_dtype=torch.bfloat16,
>>             trust_remote_code=True
>>         ).cuda()
>>         _tokenizer = AutoTokenizer.from_pretrained(
>>             "tattabio/gLM2_650M_embed",
>>             trust_remote_code=True
>>         )
>>     return _embedding_model, _tokenizer
>> 
>> def generate_embeddings(sequences: dict) -> dict:
>>     """
>>     Generate embeddings for one or more protein sequences.
>>     """
>>     model, tokenizer = _load_embedding_model()
>>     query_embeddings = {}
>> 
>>     for seq_id, seq in sequences.items():
>>         tokens = tokenizer([seq], return_tensors="pt")
>>         with torch.no_grad():
>>             embedding = model(tokens.input_ids.cuda()).pooler_output.cpu().squeeze(0)
>>         query_embeddings[seq_id] = embedding.to(torch.float32)
>> 
>>     return query_embeddings
>> 
>> def _load_prediction_model():
>>     """
>>     Load and cache the TabICL pre-trained classifier.
>>     """
>>     global _prediction_model
>>     if _prediction_model is None:
>>         _prediction_model = joblib.load("model.joblib")
>>     return _prediction_model
>> 
>> def make_prediction(query_embeddings: dict) -> pd.DataFrame:
>>     """
>>    Make predictions.
>>     """
>>     model = _load_prediction_model()
>>     emb_df = pd.DataFrame({k: v.numpy() for k, v in query_embeddings.items()}).T
>>     predictions = model.predict(emb_df)
>>     return pd.DataFrame({"prediction": predictions}, index=emb.index)
>> ```
> {: .solution}
> 
{: .hands_on}

Then, import the functions from `src/utils.py` into `app.py`:
```python
from src.utils import parse_fasta, generate_embeddings, make_prediction
```

Add logic to process the protein sequences and generate predictions, using `st.spinner` to display a loading spinner while the code executes.

```python
if uploaded_file and st.button("Predict"):
    query_sequences = parse_fasta(uploaded_file)
    with st.spinner("Generating embeddings..."):
        embeddings = generate_embeddings(query_sequences)
    with st.spinner("Making predictions..."):
        results = make_prediction(embeddings)
    st.dataframe(results)
```

You can also access the final [app.py](/tutorials/ml-streamlit/main/src/app.py) and [util.py](/tutorials/ml-streamlit/main/src/utils.py) scripts. Please review your script and test it by making predictions on the protein sequences of interest.

> ## *(Optional Task)* Download predictions
> Add "**Download predictions**" button and obtain your results using `st.download_button`.
>
>> ## Solution
>> ```python
>> csv = results.to_csv().encode("utf-8")
>> st.download_button(
>>     label="Download predictions",
>>     data=csv,
>>     file_name="results.csv",
>>     mime="text/csv"
>> )
>> ```
> {: .solution}
> 
{: .hands_on}

Congratulations! You have successfully deployed your trained model using Streamlit.

> ## **What to learn next?**
> Explore alternative approaches to deploy your trained model on the cloud:
> * [Deploy the model on cloud with FastAPI](/tutorials/ml-fastapi/main/tutorial/)
{: .details}