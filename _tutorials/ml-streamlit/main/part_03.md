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