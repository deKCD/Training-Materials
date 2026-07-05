---
layout: tutorial_hands_on
title: Deploying ML workflow using FastAPI
description: "FIXME"
slug: ml-fastapi
time_estimation: 3H
questions:
  - "How to create a synthetic datasets for future inference?"
  - "How to serve model with FastAPI?"
objectives:
  - "Learn best practices to serve model with FastAPI and get predictions as a table."
key_points:
  - "FIXME"
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

Deploying and maintaining machine learning (ML) models can be challenging, especially in academia where .... 

Machine Learning Operations (MLOps) addresses these challenges by streamlining and automating the ML lifecycle - from development to deployment and ongoing management. In this hands-on tutorial, you will learn some basic MLOps practices and tools through an end-to-end project. You will gain practical experience with cloud infrastructure, containerization, orchestration, and model serving—core skills that make ML projects more scalable, reproducible, and production-ready. 

Specifically, you will learn how to (1) deploy a trained model on the cloud; (2) containerize it with [Docker](https://docs.docker.com/) for portability, (3) scale it using [Kubernetes](), and (4) serve the model with [FastAPI](https://fastapi.tiangolo.com/) via an API interface. 

As a proof of concept, we will use the [**Breast Cancer Wisconsin dataset**](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic) from `sklearn.datasets` module. We will focus on deployment and serving rather than preprocessing, so you can gain hands-on experience with moving models into production.

> ## Note
> This tutorial is intended for beginners in MLOps and focuses on the deployment and serving of machine learning workflows in the cloud. It does not cover the theoretical foundations of machine learning or the full range of MLOps tools and best practices. 
> We assume you already have basic to intermediate knowledge of machine learning, including model training and the use of libraries such as [scikit-learn](https://scikit-learn.org/stable/).
> 
{: .warning}

## **Prerequisites**

Before you start, ensure you meet the following requirements:

- LifeScience AAI account to access the de.NBI Cloud
    - You can find instructions for registration and setup in the [de.NBI Cloud Wiki](https://cloud.denbi.de/get-started/)
- Familiarity with the Unix commands, SimpleVM and/or Openstack
    - Review the [previous tutorial on Unix commands](/tutorials/unix-course/main/tutorial.md) or check the [SimpleVM Wiki](https://simplevm.denbi.de/wiki/)
- Basic to intermediate experience with machine learning model training and using [scikit-learn library](https://scikit-learn.org/stable/).
- Familiarity with Docker. 
- Familiarity with Kubernetes.

## **Table of Content**
* [Preparation](#preparation)
  * [Access SimpleVM/Openstack instance](#access-simplevm/openstack-instance)
  * [Install the required packages](#install-the-required-packages)
* [Getting the dataset](#getting-the-dataset)
* [Train a classifier and serve using FastAPI](#train-a-classifier-and-serve-using-fastapi)
  * [Create an API](#create-an-api)
* [Containerize trained model with Docker](#containerize-your-model-with-docker)
* [Scale with kubernetes]
* [What to learn next?](#what-to-learn-next)

## **Preparation**

### **Access SimpleVM/Openstack instance**

If you are already a member of a SimpleVM or Openstack project in de.NBI Cloud, you can proceed to create a VM instance. If you are unfamiliar with this process, we recommend reviewing our [SimpleVM tutorial](/tutorials/simpleVMWorkshop/main/tutorial/) and the [SimpleVM](https://simplevm.denbi.de/wiki/) and [Openstack Wikis](https://cloud.denbi.de/wiki/quickstart/) for step-by-step guidance.

### **Install the required packages**

For this hands-on tutorial, we need to install the following packages:
- [sklearn](https://scikit-learn.org/stable/install.html)
- [sdv](https://github.com/sdv-dev/SDV?tab=readme-ov-file#install)
- [pandas](https://pandas.pydata.org/) 
- [fastapi](https://fastapi.tiangolo.com/#installation)
- [uvicorn](https://uvicorn.dev/installation/)
- *(Optional)* [jupyterlab](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html)

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
{: .code-in}

> ## Install the required packages:
> ```bash
> pip install pandas
> pip3 install -U scikit-learn
> pip install sdv
> pip install "fastapi[standard]"
> pip install uvicorn
> ```
{: .code-in}

## **Getting the datasets**

`sklearn.datasets` has lots of datasets for benchmarking and the utility to generate the one for the task of classifition (`sklearn.dataset.make_classification`) and regression (`sklearn.datasets.make_regression`).

Load the breast cancer Wisconsin dataset and inspect the features and target values which are benign (`0`) and malignant (`1`).

> ## Dataset description
> The dataset consists of 569 samples, 30 features, and 2 classes (benign, malignant).
> Features are extracted from digitized FNA images of breast masses, capturing key characteristics of the cell nuclei.
> 
> 10 features are computed for each cell nucleus:
> - radius (mean of distances from center to points on the perimeter)
> - texture (standard deviation of gray-scale values)
> - perimeter
> - area
> - smoothness (local variation in radius lengths)
> - compactness (perimeter² / area — 1.0)
> - concavity (severity of concave portions of the contour)
> - concave points (number of concave portions of the contour)
> - symmetry
> - fractal dimension (“coastline approximation” — 1)
> 
> The mean, standard error and “worst” or largest (mean of the three largest values) of these features were computed for each image, resulting in 30 features.
{: .details}

> ## Load the dataset
> ```python
> from sklearn.datasets import load_breast_cancer
>
> # returns dictionary with features and target values
> load_breast_cancer() 
> 
> # load dataset into pandas DataFrame and target Series
> X, y = load_breast_cancer(return_X_y=True, as_frame=True)
> ```
{: .code-in}

Here, 
- `return_X_y` function returns a tuple (data, target) instead of a `Bunch` object. Default is `False`.
- `as_frame` function returns the data and target as `pandas.DataFrame` and `pandas.Series`, making it easier to inspect features.


> ## Inspect the dataset
> 1. Check the dataset for missing values.
> 2. Identify features that are highly correlated with one another.
> 3. Identify features with low variance across samples (*i.e.,* uninformative features) using `VarianceThreshold` class from `sklearn.feature_selection` module.
> 4. Is the `target` column balanced in the dataset?
>
>> ## Solution
>> ```python
>> import numpy as np
>> from sklearn.feature_selection import VarianceThreshold
>>
>> # check features with missing values
>> X.isnull().any()
>>
>> # compute the absolute correlation matrix
>> corr_matrix = X.corr().abs()
>> # select the upper or lower triangular part of the correlation matrix
>> upper_triangle = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
>> # select the features with an absolute correlation greater than arbitraty 0.80
>> to_drop = [column for column in upper_triangle.columns if any(upper_triangle[column] > 0.80)]
>> print(len(to_drop))
>>
>> # select features with non-zero variance
>> selector = VarianceThreshold(threshold=0)
>> selector.fit(X)
>> # features with low variance
>> low_variance_features = X.columns[~selector.get_support()]
>> print(low_variance_features.tolist())
>>
>> # check class distribution as percentages/probabilities
>> print(y.value_counts(normalize=True))
>> ```
> {: .solution}
{: .hands_on}

Next, we will generate a synthetic dataset that mimics the statistical properties and correlations of the breast cancer Wisconsin dataset. For this, we will use [**SDV**](https://github.com/sdv-dev/SDV) - **S**ynthetic **D**ata **V**ault - a library specifically designed for generating realistic synthetic data. It supports single-table and multi-table datasets, allowing you to create synthetic data for testing, development, or privacy-sensitive applications. This will allow us to get an inference without relying only on the original dataset. If you would like to dive deeper into how SDV works, you can check out the [official documentation](https://docs.sdv.dev/sdv/tutorials) or read the [research paper](https://ieeexplore.ieee.org/document/7796926).

We will use the Gaussian Copula algorithm because it is both fast and straightforward. The `GaussianCopulaSynthesizer` generates synthetic data by applying classical statistical methods to learn the structure of your dataset. You need to provide a [Metadata](https://docs.sdv.dev/sdv/single-table-data/data-preparation/creating-metadata) object as the first argument to `GaussianCopulaSynthesizer`.

`Metadata` object describes the dataset you want to synthesize. All other parameters are optional and can be used to customize the behavior of the synthesizer. The metadata includes essential information about your dataset, such as:
- table names (for single or multiple tables);
- column names and data types;
- relationship between columns and tables. 

> ## Creating Metadata
> Create metadata for the breast cancer Wisconsin dataset using `Metadata` class from `sdv.metadata` module. 
>> ## Solution
>> ```python
>> # create metadata
>> from sdv.metadata import Metadata
>> metadata = Metadata.detect_from_dataframe(
>>    data=real_data,
>>    table_name='breast_cancer')
>>
>> # inspect metadata
>> metadata.visualize()
>> ```
>>> ## Mark personally-identifiable information
>>> If your dataset contains sensitive information, you can mark personally identifiable information (PII) in the metadata to ensure it is handled appropriately. As a proof of concept, we will generate fake names using the [faker](https://faker.readthedocs.io/en/master/).
>>> ```bash
>>> pip install Faker
>>> ```
>>>
>>> ```python
>>> # generate fake but realistic-looking names
>>> from faker import Faker
>>>
>>> fake = Faker()
>>>
>>> # create fake names for all samples
>>> real_data['Patient'] = [fake.name() for _ in range(len(real_data))]
>>>
>>> # regenerate metadata
>>> metadata.detect_from_dataframe(data=real_data, table_name="breast_cancer")
>>>
>>> # update metadata and mark sensitive information
>>> metadata.update_column(column_name="Patient", sdtype="name", pii=True)
>>> ```
>> {: .tip}
>>> ## Create Metadata for multiple tables
>>> Though it is not the scope of this tutorial, it would be useful for you to also learn how to create a metadata for multiple tables and further generate a synthetic datasets. 
>>>
>> {: .tip}
> {: .solution}
{: .hands_on}


> ## Create synthetic dataset for future inference
> ```python
> from sdv.single_table import GaussianCopulaSynthesizer
> import pandas as pd
> 
> # combine features and targets
> real_data = pd.concat([X, y], axis=1)
>
> # initiate sdv synthesizer with created metadata
> synthesizer = GaussianCopulaSynthesizer(metadata)
>
> # learn patterns from the data
> synthesizer.fit(data=real_data)
>
> # generate 100 samples 
> synthetic_data = synthesizer.sample(num_rows=100)
>
> # visualize the real vs. synthetic data
> from sdv.evaluation.single_table import get_column_plot
> 
> fig = get_column_plot(
>     real_data=real_data,
>     synthetic_data=synthetic_data,
>     column_name='mean radius', # chose any column
> )
> 
> fig.show()
> ```
{: .code-in}

You can also compare the distribution of the `target` values in the real and synthetic datasets to verify that they are similar. Once satisfied, save the synthetic data (without `target` column) as `external_test.tsv` for use in future inference tasks. 

## **Train a classifier and serve using FastAPI**

At this stage, you have explored the dataset and generated synthetic data for future inference. Now, we will train a classifier and prepare it for deployment via an API. Create a python script `train.py` that loads data, trains a model, evaluates performance, and saves the trained model. We will train a Random Forest classifier with the default settings as its robust, easy to use, and work well for structured tabular data.

> ## Train Random Forest with the default parameters
> 1. Divide dataset into into training and test sets. Use [`train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) from `sklearn.model_selection` with a test size of 10% and stratification to preserve the class distribution.
> 2. Train Random Forest with the default parameters. Use [`RandomForestClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) from `sklearn.ensemble` module.
> 3. Generate predictions for the test set and compute a classification report. 
> 4. Save the trained model `joblib`.
>
>> ## Solution
>> ```python
>> from sklearn.model_selection import train_test_split
>> from sklearn.ensemble import RandomForestClassifier
>> from sklearn.metrics import *
>> import joblib 
>> 
>> # split data
>> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, stratify=y, shuffle=True, random_state=42)
>> 
>> # train classifier
>> clf = RandomForestClassifier(random_state=42)
>> clf.fit(X_train, y_train)
>>
>> # evaluate the model
>> test_pred = clf.predict(X_test)
>> 
>> # get classification report
>> report = classification_report(y_test, test_pred, output_dict=True)
>> report = pd.DataFrame(report).transpose()
>> report.reset_index(inplace=True)
>> print(report)
>> 
>> # save the trained model
>> joblib.dump(clf, "model.joblib")
>> ```
> {: .solution}
>
{: .hands_on}

> ## Confusion matrix report
> To further evaluate your model’s performance, you can use [**pycm**](https://github.com/sepandhaghighi/pycm) - **py**thon **c**onfusion **m**atrix - a library that provides detailed statistics and metrics for classification models.
> 
> ```bash
> pip install pycm
> ```
> 
> ```python
> from pycm import *
> 
> # create a confusion matrix
> cm = ConfusionMatrix(actual_vector=y_test.to_numpy(), predict_vector=test_pred)
> 
> # print the matrix
> cm.print_matrix()
> 
> # alternatively save a detailed HTML report
> cm.save_html("breast_cancer_pycm_report", summary=True, color=(0, 64, 64))
> ```
> The detailed HTML report with overall statistics can be opened in your browser.
> 
{: .details}

### **Create an API**

Since the classifier is performing well, we can proceed to the next step: creating an API using FastAPI. For this hands-on tutorial, we will focus only on the essential features of FastAPI needed to serve our trained model, keeping the implementation simple and beginner-friendly. If you would like to learn more, you can refer to the [official documentation](https://fastapi.tiangolo.com/).

Create `app` folder in your working directory and place the trained model in there because this is our server and everything required for this server is inside that folder. Then create a new python file `main.py` whithin `app` folder, import the required libraries, and load the trained model.

> ## `main.py`
> ```python
> from fastapi import FastAPI, UploadFile, File # to handle HTTP requests and file uploads
> from fastapi.responses import StreamingResponse # to send large files (e.g., CSV/TSV) back to the client efficiently
> import pandas as pd
> import joblib # to load pre-trained model
> import io # for in-memory file operations
> 
> # load the trained model
> model = joblib.load("app/model.joblib")
> 
> # define classes
> class_names = {"benign": 0, "malignant": 1} # maps numeric predictions to meaningful class labels
> ```
{: .code-in}

> ## Initialize an app and define root endpoint
> ```python
> app = FastAPI() # creates the main API application object that will handle all routes and endpoints
> 
> # root endpoint
> @app.get("/")
> def read_root():
>     """
>     Root endpoint for checking if the API is running.
>     Returns a simple JSON message.
>     """
>     return {"message": "Breast cancer inference API"}
> ```
{: .code-in}

Next, define prediction endpoint that accepts a tab-separated CVS/TSV file with features and make predictions using our trained model. 

> ## Define prediction endpoint
> ```python
> @app.post("/predict/")
> async def predict_from_csv(file: UploadFile = File(...)):
>     """
>     Endpoint for making predictions from a tab-separated CSV/TSV file.
> 
>     Args:
>         file (UploadFile): Uploaded tab-separated CSV file with feature columns.
> 
>     Returns:
>         StreamingResponse: A downloadable CSV file with an added `prediction` column.
>     """
>     # read uploaded file into pandas DataFrame
>     contents = await file.read()
>     data = pd.read_csv(io.BytesIO(contents), sep="\t")
>     print(data.sample(5)) # optional: inspect sample rows
> 
>     # make predictions using loaded model
>     predictions = model.predict(data)
>     data["prediction"] = class_names[predictions]
> 
>     # save predictions to an in-memory CSV buffer
>     output = io.StringIO()
>     data.to_csv(output, sep="\t", index=False)
>     output.seek(0) # reset buffer pointer to the beginning
> 
>     # return the predictions as downloadable TSV file
>     return StreamingResponse(
>         output,
>         media_type="text/csv",
>         headers={"Content-Disposition": "attachment; filename=predictions.tsv"}
>     )
> ```
{: .code-in}

After creating `main.py`, you can run the FastAPI API and test it with a sample dataset.

To start the server, open a new terminal, run the command, and click the server link to check the root endpoint:
```bash
fastapi dev app/main.py
```

When you are running the API on a remote VM, establish an SSH tunnel to access it from your local browser:

```bash
ssh -N -L localhost:XXXX:localhost:XXXX -i PRIVATE_SSH_KEY INSTANCE@FLOATING_IP
```
Here,
* `XXXX` is the port number, *e.g.,* 8000.
* `-i PRIVATE_SSH_KEY` path to your private SSH key for authentication.
* `INSTANCE` corresponds to your username on the remote VM (you can verify it by running `whoami` in your previous terminal session).
* `FLOATING_IP` is public IP of your remote VM. 

Once the ssh tunnel is established, open your browser at http://127.0.0.1:8000. 
You should see the JSON response:
```json
{"message":"Breast cancer inference API"}
```

FastAPI provides interactive documentation for testing endpoints:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

To test the `/predict/` endpoint, click `Try it out`, upload your features table (*e.g.,* `external_test.tsv`, the synthetic dataset created [earlier](#create-synthetic-dataset-for-future-inference)), click `Execute`, and download the resulting file with predictions.

You can also test the API from the command line:
```bash
curl -X 'POST' 'http://127.0.0.1:8000/predict/' -F "file=@external_test.tsv" --output predictions.tsv
```
Here, 
- `-X POST` sends a POST request.
- `-F "file=@external_test.tsv"` uploads the test file.
- `-o predictions.tsv` saves the API response (predictions) as a local file.

> ## Add data processing endpoint
> Create a FastAPI POST endpoint `/preprocess/normalize/` that does the following:
> 1. accepts a tab-separated CSV/TSV file;
> 2. normalizes all numeric features to the range [0,1] using [`MinMaxScaler`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html) from `sklearn.preprocessing` module;
> 3. returns the processed table.
> 
>> ## Solution
>> ```python
>> from fastapi import FastAPI, UploadFile, File
>> from fastapi.responses import StreamingResponse
>> import pandas as pd
>> import io
>> from sklearn.preprocessing import MinMaxScaler
>> 
>> app = FastAPI()
>> @app.post("/preprocess/normalize/")
>> async def normalize_features(file: UploadFile = File(...)):
>>     # read uploaded file into pandas DataFrame
>>     contents = await file.read()
>>     data = pd.read_csv(io.BytesIO(contents), sep="\t")
>>     print(data.head(5)) # optional: inspect the dataset
>>     
>>     # identify numeric columns
>>     numeric_cols = data.select_dtypes(include='number').columns
>>     
>>     # apply scaling
>>     scaler = MinMaxScaler()
>>     data[numeric_cols] = scaler.fit_transform(data[numeric_cols])
>>     
>>     # save processed data
>>     output = io.StringIO()
>>     data.to_csv(output, sep="\t", index=False)
>>     output.seek(0)
>>     
>>     return StreamingResponse(
>>         output,
>>         media_type="text/csv",
>>         headers={"Content-Disposition": "attachment; filename=normalized.tsv"}
>>     )
>> ```
> {: .solution}
> 
{: .hands_on}

At this point, you have created a basic FastAPI application to serve your trained model. Next, we will wrap the code, dependencies, and API in a Docker container for easy deployment and portability.

## **Containerize trained model with Docker**

To deploy our classifier across different environments (to solve the so-called "It works on my machine" issue 😉), we need to containerize the application. Docker allows us to package the code, dependencies, and runtime environment into a single, portable container.

Create a `requirements.txt` file in the root of your project with the exact versions of libraries used for training your model. This ensures compatibility, especially for scikit-learn, which must match the version used to train the model.
```
scikit-learn==1.6.1
fastapi
pandas
joblib
uvicorn
```

Create `Dockerfile` in your project root. The Dockerfile specifies the operating system, python version, and dependencies your application needs.

```bash
touch Dockerfile
```

 Add the following code:

```Dockerfile
# base image
FROM python:3.12

# set work directory
WORKDIR /app

# copy all files to app in container
COPY . /app

# install dependencies listed in the file
RUN pip install --no-cache-dir -r /app/requirements.txt

# expose port
EXPOSE 8000

# run the FastAPI app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The `Dockerfile` does the following:
- uses python 3.12 base image that will be pulled from the [Docker Hub](https://hub.docker.com/).
- copies all your project files into the container.
- installs dependencies 
- exposes port 8000
- defines the command to run the Fast API. 
    - `uvicorn` handles web requests and serves the FastAPI app.
    - `app.main:app` points to the FastAPI instance in `main.py` under the app directory.
    - `--host 0.0.0.0` makes the app accessible outside the container.
    - `--port 8000` binds the server to port 8000 (matching the exposed port).

Build the container image with the following command:
```bash
docker build -t breast-cancer-inference .
```
Here, 
- `-t` names the Docker image.

This step takes some time usually when run for the first time.

Run the container locally and map port 8000 from the container to your host machine:
```bash
docker run -p 8000:8000 breast-cancer-inference
```
Here,
- `-p 8000:8000` maps host port 8000 to container port 8000. 

The FastAPI app is now running inside the container and accessible at http://127.0.0.1:8000.

You can stop a running Docker container using container ID or name:

```bash
# show running containers
docker ps
```

```bash
docker stop <container_id_or_name>
```

You have a containerized ML model served via FastAPI, ready to be deployed consistently across any environment.

The next step is deploying and scaling this container using Kubernetes for production-grade availability and management.

## **Deploy and Scale the classifier using Kubernetes**

Kubernetes (K8s) is a container orchestration platform to deploy, manage, and scale containers. It would allow us to run our FastAPI container reliably in production, enable horizontal scaling for handling multiple requests, and automate deployment and management of ML APIs.

If you are already familiar with kubernetes, you can skip the introduction section and proceed with the next steps. 

### **Brief introduction to Kubernetes**
Briefly explain what Kubernetes (K8s) is ...

Kubernetes manages containerized applications by scaling resourcing, managing container health and availability. And it is particularly helpful for machine learning applications. 

Kubernetes improves ML scalability by dynamically adjusting resources based on demand. This ensures optimal performance under varying loads and reduces the need for manual intervention.

For now, let's understand 3 components: pods, services, and deployments. 
- Pods: For machine learning applications, pods usually represent a containerized machine learning model or one phase of the model’s workflow. This can be achieved through either one container or a series of containers working with shared resources.
- Services: In order for multiple Kubernetes pods to be able to communicate and network with each other, they need services to define access through stable network endpoints. In that way, services provide the load balancing and discovery mechanisms that allow external applications to interact with containerized machine learning models and their components.
- Deployments: The scalability and agility that Kubernetes offers are powered by deployments. These declarations allow for pod creation and scaling in order to respond to changing demand or apply updates without any application downtime.

### **Prerequisites**

Before starting, ensure you have:
- docker image
- access to a Kubernetes cluster (local via Minikube, Kind, or cloud provider)
- kubectl installed and configured to communicate with your cluster

We have already built the Docker image `breast-cancer-inference`. 




### Setting up Kubernetes
### Creating a Kubernetes Deployment
### Creating a Kubernetes Service

## Autoscaling the Model Deployment
### Monitoring the Autoscaling

## Monitoring and Logging

> ## **What to learn next?**
> ML model deployment is not the last stage in model management. Learn how to continuously validate/monitor data and train model:
> * [XXXX](/tutorials/XXXXX/main/tutorial/)
{: .details}