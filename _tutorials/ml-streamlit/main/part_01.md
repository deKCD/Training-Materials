## **Get the dataset**

In this tutorial, we will use `tattabio/mibig_classification_prot` dataset from the [Hugging Face](https://huggingface.co/datasets/tattabio/mibig_classification_prot) as an example for our classification task. 

The [MIBiG](https://mibig.secondarymetabolites.org/) — *Minimum Information about a Biosynthetic Gene Cluster* — is a community-driven standard for annotating biosynthetic gene clusters (BGCs) and their associated molecular products.

BGCs are physically linked sets of genes on a genome that collectively encode a biosynthetic pathway for producing specific metabolites, including antibiotics and antifungals, which are of great interest to the agricultural and pharmaceutical industries.

MIBiG standard provides a structured way to categorize BGCs by product type (*e.g.*, nonribosomal peptides (NRPs), terpenes, saccharides) and enable standardized data sharing and reproducible research.
  
In our case, we will use this dataset to train a protein sequence classifier that predicts the class of each BGC based on sequence information.

### **Load and inspect the dataset**
Hugging Face Datasets provides several easy ways to load the data. Navigate to `Use this dataset` in the dataset page and select one of the libraries:
![Load the dataset]({{ "/tutorials/ml-streamlit/img/get_data.png" | relative_url }}){: .responsive-img }

For this tutorial, we will use the `datasets` library from Hugging Face:

><code-in-title>Load dataset</code-in-title>
> ```python
> from datasets import load_dataset
> 
> ds = load_dataset("tattabio/mibig_classification_prot")
> print(ds)
> ```
{: .code-in}

This returns the following dataset structure:

><code-out-title>Dataset structure</code-out-title>
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
  

><code-in-title>Convert the Hugging Face Dataset objects to Pandas DataFrames for easier manipulation using `.to_pandas()`:</code-in-title>
>```python
>train = ds["train"].to_pandas()
>test = ds["test"].to_pandas()
>```
{: .code-in}

><hands-on-title>Explore the dataset to better understand its structure before training our model</hands-on-title>
> 1. Handle duplicates in the `Entry` column for both train and test splits. Keep the same number of samples as before, but assign unique indices by creating a new column `Entry_id`.
> 2. Count how many unique classes exist in both `simple_class` and `class`. Identify which classes are most common in the dataset.
> 
>><solution-title>Solution</solution-title>
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

><tip-title>Pitfall #1: Class imbalance</tip-title>
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
 
><details-title>gLM papers and platforms</details-title>
> For more information regarding the model, please read the following papers:
> * [Gaia: A Context-Aware Sequence Search and Discovery Tool for Microbial Proteins](https://doi.org/10.1101/2024.11.19.624387)
> * [The OMG dataset: An Open MetaGenomic corpus for mixed-modality genomic language modeling](https://doi.org/10.1101/2024.08.14.607850)
> * [Genomic language model predicts protein co-regulation and function](https://doi.org/10.1038/s41467-024-46947-9)
> 
> Also, if you are interested in functional annotation of the protein sequences, check the [Gaia annotator](https://gaia.tatta.bio/) and [SeqHub](https://seqhub.org/) from the [Tattabio](https://www.tatta.bio/). 
> 
{: .details}


><hands-on-title>Step 1: Import the required packages</hands-on-title>
>><code-in-title>Code-in</code-in-title>
>>```python
>>import torch
>>from torch.utils.data import DataLoader, Dataset
>>from transformers import AutoModel, AutoTokenizer
>>import pandas as pd
>>```
>{: .code-in}
>
>><details-title>Packages description</details-title>
>> - `torch` and `torch.utils.data`: for tensor operations and data batching.
>> - `transformers`: for loading the gLM2 model and tokenizer.
>> - `pandas`: for handling dataframes.
>>
>{: .details}
>
>><code-in-title>Check if GPU is available:</code-in-title>
>>```python
>>import torch
>>print(torch.cuda.is_available())  # should return True on GPU-enabled instances
>>```
>{: .code-in}
{: .hands_on}


Embedding thousands of sequences is computationally intensive. While CPUs are versatile, they process data sequentially and can be orders of magnitude slower. 

GPUs, on the other hand, are optimized for parallel computation. They enable processing many sequences at once, significantly speeding up the embedding step and making large-scale workflows practical.

><hands-on-title>Step 2: Load the model and tokenizer</hands-on-title>
>><code-in-title>Code-in</code-in-title>
>>```python
>>model_name = 'tattabio/gLM2_650M_embed' # path of the pre-trained model hosted on Hugging Face Hub
>>device = "cuda" if torch.cuda.is_available() else "cpu" # check if a GPU is available for faster computation; otherwise, run on CPU
>>
>>model = AutoModel.from_pretrained(model_name, torch_dtype=torch.bfloat16, trust_remote_code=True).cuda()
>>tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
>>```
>{: .code-in}
>
>><details-title>Description</details-title>
>>    - `torch_dtype=torch.bfloat16` – specifies the data type for model weights. Using `bfloat16` reduces memory usage and speeds up computation on GPUs without significantly sacrificing precision.  
>>    - `trust_remote_code=True` – allows execution of custom code provided by the model repository (required when models have custom architectures or tokenizers). Only use this flag with trusted sources.  
>>    - `.cuda()` – moves the model to the GPU, enabling faster computation for embedding generation.  
>>    - `AutoTokenizer.from_pretrained(...)` – loads the tokenizer associated with the model, ensuring proper tokenization of sequences for embedding generation.  
>{: .details}
{: .hands_on}

><hands-on-title>Step 3: Build a custom `Dataset`</hands-on-title>
>We define a small `ProteinDataset` class to store sequences and their IDs. This will let the `DataLoader` efficiently iterate through the dataset in batches:
>><code-in-title>Code-in</code-in-title>
>>```python
>>class ProteinDataset(Dataset):
>>    def __init__(self, seq_dict):
>>        self.keys = list(seq_dict.keys())
>>        self.sequences = list(seq_dict.values())
>>
>>    def __len__(self):
>>        return len(self.keys)
>>
>>    def __getitem__(self, idx):
>>        return self.keys[idx], str(self.sequences[idx])
>>```
>{: .code-in}
{: .hands_on}

><hands-on-title>Step 4: Collate function for tokenization</hands-on-title>
>The collate function batches sequences together and tokenizes them dynamically. By **padding** (*i.e.*, adding special tokens to shorter sequences so all sequences in a batch have the same length) and **truncating** (*i.e.*, shortening sequences that exceed the maximum length) sequences to the same length within each batch, the model can process them efficiently. 
>
>><details-title>Padding and Truncation</details-title>
>> For a comprehensive explanation of **padding** and **truncation** strategies, refer to the [Hugging Face documentation](https://huggingface.co/docs/transformers/en/pad_truncation).
>> 
>{: .details}
>
>><code-in-title>Code-in</code-in-title>
>>```python
>>def collate_fn(batch):
>>    keys, sequences = zip(*batch)
>>    tokens = tokenizer(
>>        list(sequences),
>>        padding=True,
>>        truncation=True,
>>        return_tensors='pt'
>>    )
>>    return keys, tokens
>>```
>{: .code-in}
>
{: .hands_on}

><hands-on-title>Step 5: Create a `DataLoader`</hands-on-title>
>The `DataLoader` handles batching, shuffling (if needed), and efficient data loading. Here, we use a `batch_size` of 32 — a good starting point for GPUs with moderate memory. Adjust the size depending on your GPU capacity:
>
>><code-in-title>Code-in</code-in-title>
>>```python
>>train_dc = train.set_index("Entry_id")["Sequence"].to_dict()
>>train_dataset = ProteinDataset(train_dc)
>>
>>train_loader = DataLoader(
>>    train_dataset,
>>    batch_size=32,  # adjust based on GPU memory
>>    shuffle=False,
>>    collate_fn=collate_fn
>>)
>>```
>{: .code-in}
{: .hands_on}


><hands-on-title>Step 6: Generate embeddings</hands-on-title>
>
>Iterate over the `DataLoader`, move each batch to the GPU, and extract embeddings from the model.
>><code-in-title>Code-in</code-in-title>
>>```python
>>embeddings = {}
>>
>>model.eval()
>>with torch.no_grad():
>>    for keys, tokens in tqdm(train_loader, desc="Embedding Sequences"):
>>        tokens = {k: v.to(device) for k, v in tokens.items()}
>>        outputs = model(tokens["input_ids"]).pooler_output.cpu()
>>        for k, emb in zip(keys, outputs):
>>            embeddings[k] = emb.to(torch.float32)
>>
>>torch.save(embeddings, "train.pt")          
>>```
>{: .code-in}
>
>><details-title>Description</details-title>
>>Here, 
>>- `model.eval()` ensures we are in inference mode (no gradients computed, faster processing).
>>- `torch.no_grad()` disables gradient tracking, reducing memory usage.
>{: .details}
>
> Repeat the last step for the test split and save the embeddings.
> 
{: .hands_on}