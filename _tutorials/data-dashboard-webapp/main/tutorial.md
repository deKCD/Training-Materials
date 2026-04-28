---
layout: tutorial_hands_on

title: Build a Simple Dataset Web App on EMBL Cloud Infrastructure
description: Learn to create and deploy a web application using Python, Streamlit, Docker/Podman, and Kubernetes on EMBL cloud computing infrastructure
time_estimation: 2H
level: beginner
keywords: [FIXME]
questions:
  - How do I create a simple web application for data visualization?
  - How do I containerize an application using Docker or Podman?
  - How do I deploy a web application on Kubernetes cloud infrastructure?
  - What are the basic components needed for cloud deployment?
objectives:
  - Create a simple Python web app using Streamlit
  - Build a container image for your application
  - Deploy the application on EMBL Kubernetes infrastructure
  - Access your web app through a public URL
key_points:
  - A simple web app requires only 6 files and minimal code
  - Containers ensure your app runs consistently across different environments
  - Kubernetes enables cloud deployment and makes your app publicly accessible
  - Git is essential for version control and sharing your container images
  - Testing locally before deploying to the cloud saves time and catches errors early
version:
  - main
life_cycle: active
contributions:
  authorship:
    - Jacobo Miranda
  editing: 
  funding: 
---

![People hiking in a row on the ice of Perito Moreno glacier, Los Glaciares national park, Santa Cruz province, Patagonia Argentina]({{ "/tutorials/data-dashboard-webapp/images/perito-moreno-glacier.jpg" | relative_url }}){: .responsive-img }

## Introduction

In this tutorial we will create a simple web app for a toy dataset in Python, using a CSV file as the dataset, then we will run this web app on EMBL infrastructure so it will be available online.

The goal of this tutorial is to give you the basics of making a simple webapp that can run on cloud! It's not an in-depth tutorial, it's just enough for you to get an intuition of what is possible and hopefully enough to get inspired to learn how to make a real academic grade webapp.

It only uses 6 files and will do the bare minimum, but these steps can be the backbone of any cloud application.

> <agenda-title></agenda-title>
>
> In this tutorial, we will cover:
>
> 1. TOC
> {:toc}
>
{: .agenda}

## Prerequisites

Before starting this tutorial, you will need:

- A computer with bash, git, and Python installed
- Access to EMBL infrastructure (VPN if working remotely)
- Basic familiarity with the command line
- An EMBL account

> <tip-title>Installing required software</tip-title>
>
> If bash, git, or Python are not installed on your system, try [this installation guide](https://pad.bio-it.embl.de/s/E-xvGYFfp#).
>
{: .tip}

## Create Your Git Project

Version control is essential for tracking changes and sharing your code. We'll start by setting up a Git repository.

> <hands-on-title>Set up Git repository</hands-on-title>
>
> 1. Go to [`https://git.embl.de/`](https://git.embl.de/)
> 2. Click **New project**
> 3. Select **Create blank project**
> 4. Configure your project:
>    - **Project name**: `my-data-dashboard`
>    - **Visibility level**: Public
>
>    > <comment-title>Why public visibility?</comment-title>
>    > 
>    > The repository needs to be public so Kubernetes can access your container image later in the tutorial.
>    >
>    {: .comment}
>
> 5. Click **Create project**
>
{: .hands_on}

## Set Up Your Local Environment

Now we'll clone the repository to your computer and set up the project structure.

> <hands-on-title>Clone and configure the project locally</hands-on-title>
>
> 1. Create or navigate to your projects folder:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > cd ~/projects
>    > # Or create it if it doesn't exist
>    > mkdir -p ~/projects
>    > cd ~/projects
>    > ```
>    {: .code-in}
>
> 2. Clone your repository:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > git clone https://git.embl.de/<username>/my-data-dashboard.git
>    > cd my-data-dashboard
>    > ```
>    {: .code-in}
>
>    Replace `<username>` with your EMBL username.
>
{: .hands_on}

## Create the Application Files

We'll create three core files for our web application: the Python app, a data file, and a requirements file.

> <hands-on-title>Create application files</hands-on-title>
>
> 1. Create `app.py` with the following content:
>
>    > <code-in-title>Python (app.py)</code-in-title>
>    > ```python
>    > import streamlit as st
>    > import pandas as pd
>    > 
>    > st.write("# Data Dashboard")
>    > 
>    > df = pd.read_csv("data.csv")
>    > st.dataframe(df)
>    > ```
>    {: .code-in}
>
>    This simple app uses [Streamlit](https://streamlit.io/) to quickly build a web interface that displays your data.
>
> 2. Create `data.csv` with sample data:
>
>    > <code-in-title>CSV (data.csv)</code-in-title>
>    > ```csv
>    > a,b,c
>    > 1,2,3
>    > ```
>    {: .code-in}
>
> 3. Create `requirements.txt` to specify dependencies:
>
>    > <code-in-title>Text (requirements.txt)</code-in-title>
>    > ```text
>    > streamlit
>    > pandas
>    > ```
>    {: .code-in}
>
{: .hands_on}

## Test the App Locally

Before deploying to the cloud, it's important to test your application locally.

> <hands-on-title>Run the webapp on your computer</hands-on-title>
>
> 1. Create a conda environment:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > conda create -n my-data-dashboard-env python -y
>    > conda activate my-data-dashboard-env
>    > python -m pip install -r requirements.txt
>    > ```
>    {: .code-in}
>
> 2. Test Streamlit installation:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > streamlit hello
>    > ```
>    {: .code-in}
>
>    > <code-out-title></code-out-title>
>    > If everything went well, this will open a colorful webpage about Streamlit in your browser.
>    {: .code-out}
>
> 3. Stop the test server:
>    - Press `Ctrl+C` in the terminal
>
> 4. Run your application:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > streamlit run app.py
>    > ```
>    {: .code-in}
>
>    > <code-out-title></code-out-title>
>    > If successful, a simple webpage will open showing "Data Dashboard" with your data table.
>    {: .code-out}
>
{: .hands_on}

> <question-title></question-title>
>
> 1. What happens when you run `streamlit run app.py`?
> 2. How would you modify the app to display different data?
>
> > <solution-title></solution-title>
> >
> > 1. Streamlit starts a local web server and opens your default browser to display the app, typically at `http://localhost:8501`
> > 2. You can modify `data.csv` with your own data, as long as it's in CSV format that pandas can read
> >
> {: .solution}
>
{: .question}

> <tip-title>Congratulations!</tip-title>
>
> If you made it this far, you've successfully run a webapp on your computer! This is a great achievement!
>
> Now you can experiment on your computer before deploying to the cloud. Feel free to modify the dataset or try different Streamlit features. When you're ready, commit your changes to git and continue with the tutorial.
>
{: .tip}

## Containerize Your Application

Now we'll create a container image of your application. A container is like a snapshot of your code and its environment, ensuring it runs consistently anywhere.

> <details-title>Understanding Containers and Images</details-title>
>
> An **image** is like a snapshot or template that contains your code and all its dependencies. A **container** is a running instance of that image, providing an isolated environment for your application.
>
> We'll use **Podman**, which is free and open source. Podman commands are fully compatible with Docker, so you can replace `podman` with `docker` in any command if you prefer.
>
{: .details}

> <hands-on-title>Install Podman</hands-on-title>
>
> 1. Install Podman following [these instructions](https://podman.io/docs/installation)
>
> 2. Create and start your first Podman machine
>
> 3. Test your installation:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > podman info
>    > ```
>    {: .code-in}
>
{: .hands_on}

### Create the Containerfile

The containerfile tells Podman how to build your image.

> <hands-on-title>Create the containerfile</hands-on-title>
>
> 1. Create a file named `containerfile` (no extension) with the following content:
>
>    > <code-in-title>Containerfile</code-in-title>
>    > ```dockerfile
>    > FROM --platform=linux/amd64 python:3.13-slim
>    > 
>    > WORKDIR /app
>    > # Expose port you want your app on
>    > EXPOSE 8501
>    > 
>    > # Upgrade pip and install requirements
>    > COPY requirements.txt requirements.txt
>    > RUN pip install -U pip
>    > RUN pip install -r requirements.txt
>    > 
>    > # Copy app code and set working directory
>    > COPY . .
>    > 
>    > ENTRYPOINT []
>    > # Run
>    > CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
>    > ```
>    {: .code-in}
>
{: .hands_on}

> <details-title>Understanding the Containerfile</details-title>
>
> Let's break down what each part does:
>
> - `FROM --platform=linux/amd64 python:3.13-slim`: Start from a Python image, specifying the platform for compatibility
> - `WORKDIR /app`: Set the working directory to avoid issues with the root folder
> - `EXPOSE 8501`: Open port 8501 for web traffic
> - `COPY requirements.txt` and `RUN pip install`: Install Python dependencies
> - `COPY . .`: Copy all project files into the container
> - `CMD [...]`: Command to run when the container starts, including server configuration
>
{: .details}

### Build and Test the Container

> <hands-on-title>Build and run the container locally</hands-on-title>
>
> 1. Build the image:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > podman build -t my-data-dashboard:0.0.1 -f containerfile .
>    > ```
>    {: .code-in}
>
>    > <comment-title>First build takes time</comment-title>
>    >
>    > The first time you run this, it might take a while because it's downloading base images and dependencies. Subsequent builds will be much faster.
>    >
>    {: .comment}
>
> 2. Run the container:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > podman run -p 8501:8501 localhost/my-data-dashboard:0.0.1
>    > ```
>    {: .code-in}
>
>    > <tip-title>Accessing the containerized app</tip-title>
>    >
>    > Unlike running locally, this command doesn't automatically open a browser. Open your browser manually and navigate to `localhost:8501` to see your webapp.
>    >
>    {: .tip}
>
{: .hands_on}

> <question-title></question-title>
>
> 1. What is the difference between building an image and running a container?
> 2. Why do we need to specify port mapping with `-p 8501:8501`?
>
> > <solution-title></solution-title>
> >
> > 1. Building creates the image (template), running creates a container (active instance) from that image
> > 2. Port mapping connects the container's internal port 8501 to your computer's port 8501, allowing you to access the app through your browser
> >
> {: .solution}
>
{: .question}

### Upload the Image to Git Registry

Once your image works locally, upload it to the Git container registry so Kubernetes can access it.

> <hands-on-title>Push image to registry</hands-on-title>
>
> 1. Navigate to your project at `https://git.embl.de/<username>/my-data-dashboard`
>
> 2. Go to **Deploy** → **Container Registry**
>
> 3. Follow the instructions shown, adapting them for Podman:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > podman login registry.git.embl.de
>    > podman build -t registry.git.embl.de/<username>/my-data-dashboard:0.1.0 -f containerfile .
>    > podman push registry.git.embl.de/<username>/my-data-dashboard:0.1.0
>    > ```
>    {: .code-in}
>
>    Replace `<username>` with your EMBL username.
>
> 4. Verify the upload at `https://git.embl.de/<username>/my-data-dashboard/container_registry`
>
{: .hands_on}

## Deploy to Kubernetes

The final step is deploying your application to the cloud using Kubernetes.

> <details-title>What is Kubernetes?</details-title>
>
> Kubernetes (K8s) is a system for running applications on clusters of computers, often in the cloud. You use **kubectl** (a command-line tool) to communicate with the Kubernetes cluster and ask it to run your application.
>
> Think of Kubernetes as a manager that ensures your application runs smoothly on cloud infrastructure.
>
{: .details}

### Set Up Kubernetes Access

> <hands-on-title>Configure kubectl</hands-on-title>
>
> 1. Log in to [https://kubeportal.embl.de/](https://kubeportal.embl.de/)
>
>    > <comment-title>Remote access requirements</comment-title>
>    >
>    > If accessing remotely, you'll need:
>    > - EMBL VPN connection
>    > - [Two-factor authentication](https://www.embl.org/internal-information/it-services/embl-user-accounts-heidelberg/#vf-tabs__section-2fa) set up on your phone
>    >
>    {: .comment}
>
> 2. Create a tenant named `my-data-dashboard` with default cores and RAM
>
>    > <details-title>What is a tenant?</details-title>
>    >
>    > A **tenant** tells Kubernetes how many computing resources (CPU, RAM) your project needs. You can have multiple tenants for different projects, each with different resource requirements.
>    >
>    {: .details}
>
> 3. Install kubectl:
>    1. Download [this setup script](https://git.embl.de/grp-itservices/k8s-tenant-setup/-/raw/main/setup-prod.sh?ref_type=heads&inline=false)
>    2. Make it executable and run it:
>
>       > <code-in-title>Bash</code-in-title>
>       > ```bash
>       > chmod +x setup-prod.sh
>       > ./setup-prod.sh
>       > ```
>       {: .code-in}
>
> 4. Verify installation:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > kubectl version --short
>    > ```
>    {: .code-in}
>
> 5. Create a namespace for your tenant:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > kubectl create namespace my-data-dashboard-ns1
>    > ```
>    {: .code-in}
>
>    > <details-title>Understanding namespaces</details-title>
>    >
>    > **Namespaces** help organize resources within a tenant. They're useful for separating different environments (development, testing, production). The namespace name should start with your tenant name to help administrators track resources.
>    >
>    {: .details}
>
> 6. Verify your namespace at [https://kubeportal.embl.de/tenants/tenants](https://kubeportal.embl.de/tenants/tenants)
>
{: .hands_on}

### Create the Deployment Configuration

Now we'll create a YAML file that tells Kubernetes how to deploy your application.

> <hands-on-title>Create deploy-image.yaml</hands-on-title>
>
> 1. Create a file named `deploy-image.yaml`
>
> 2. Add a comment at the top (optional but helpful):
>
>    > <code-in-title>YAML comment</code-in-title>
>    > ```yaml
>    > # Replace the following strings:
>    > # <username> x6 times - your EMBL username
>    > # <username2> x2 times - your supervisor's EMBL username
>    > # <appname> x17 times - my-data-dashboard
>    > # After testing, create a ticket at https://itsupport.embl.de
>    > # to enable www.my-data-dashboard.embl.de
>    > ```
>    {: .code-in}
>
> 3. Add the deployment section:
>
>    > <code-in-title>YAML (deploy-image.yaml - Part 1)</code-in-title>
>    > ```yaml
>    > ---
>    > apiVersion: apps/v1
>    > kind: Deployment
>    > metadata:
>    >   labels:
>    >     owner-username: <username>  # your EMBL username
>    >     fallback-username: <username2>  # supervisor's username
>    >   name: <appname>-<username>
>    >   namespace: <appname>-ns1
>    > spec:
>    >   selector:
>    >     matchLabels:
>    >       app: <appname>
>    >   replicas: 1
>    >   template:
>    >     metadata:
>    >       labels:
>    >         app: <appname>
>    >     spec:
>    >       containers:
>    >         - name: <appname>
>    >           image: registry.git.embl.de/<username>/<appname>:0.1.0
>    >           imagePullPolicy: "Always"
>    >           ports:
>    >             - name: http
>    >               containerPort: 8501
>    >               protocol: TCP
>    >           resources:
>    >             limits:
>    >               cpu: 1
>    >               memory: 512Mi
>    >             requests:
>    >               cpu: 300m
>    >               memory: 128Mi
>    > ---
>    > ```
>    {: .code-in}
>
> 4. Add the ingress section (network access configuration):
>
>    > <code-in-title>YAML (deploy-image.yaml - Part 2)</code-in-title>
>    > ```yaml
>    > apiVersion: networking.k8s.io/v1
>    > kind: Ingress
>    > metadata:
>    >   annotations:
>    >     traefik.ingress.kubernetes.io/router.tls.certresolver: sectigo
>    >   name: <appname>-<username>
>    >   namespace: <appname>-ns1
>    > spec:
>    >   ingressClassName: internal-users
>    >   rules:
>    >   - host: <appname>.embl.de
>    >     http:
>    >       paths:
>    >       - backend:
>    >           service:
>    >             name: <appname>
>    >             port:
>    >               name: http
>    >         path: /
>    >         pathType: Prefix
>    >   tls:
>    >   - hosts:
>    >     - <appname>.embl.de
>    > ---
>    > ```
>    {: .code-in}
>
>    > <comment-title>Enabling the URL</comment-title>
>    >
>    > To enable the URL `www.<appname>.embl.de`, you need to create a ticket at [https://itsupport.embl.de/](https://itsupport.embl.de/) requesting web support. The name might already be taken, so be prepared to choose an alternative.
>    >
>    {: .comment}
>
> 5. Add the service section:
>
>    > <code-in-title>YAML (deploy-image.yaml - Part 3)</code-in-title>
>    > ```yaml
>    > apiVersion: v1
>    > kind: Service
>    > metadata:
>    >   name: <appname>
>    >   namespace: <appname>-ns1
>    > spec:
>    >   ports:
>    >   - name: http
>    >     port: 8501
>    >     protocol: TCP
>    >     targetPort: 8501
>    >   selector:
>    >     app: <appname>
>    > ```
>    {: .code-in}
>
> 6. Replace all instances of `<username>`, `<username2>`, and `<appname>` with your actual values
>
{: .hands_on}

### Deploy and Test

> <hands-on-title>Run your app in the cloud</hands-on-title>
>
> 1. Apply the deployment configuration:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > kubectl apply -f deploy-image.yaml
>    > ```
>    {: .code-in}
>
> 2. Check if your container is running:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > kubectl get pods -n my-data-dashboard-ns1
>    > ```
>    {: .code-in}
>
>    > <code-out-title></code-out-title>
>    > Note the NAME of your pod (something like `my-data-dashboard-<username>-<random-id>`). You'll need this for the next steps.
>    {: .code-out}
>
> 3. Test the service using port-forwarding:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > kubectl port-forward pod/<podname> 8501:8501 -n my-data-dashboard-ns1
>    > ```
>    {: .code-in}
>
>    Replace `<podname>` with the pod name from step 2.
>
> 4. Open your browser and navigate to `localhost:8501`
>
>    > <tip-title>Success!</tip-title>
>    >
>    > If you can see your Data Dashboard, congratulations! Your app is running in the cloud!
>    >
>    {: .tip}
>
> 5. To check the pod status and details:
>
>    > <code-in-title>Bash</code-in-title>
>    > ```bash
>    > kubectl describe pod <podname> -n my-data-dashboard-ns1
>    > ```
>    {: .code-in}
>
{: .hands_on}

> <question-title></question-title>
>
> 1. What is the purpose of port-forwarding in Kubernetes?
> 2. How would you update your app with new changes?
>
> > <solution-title></solution-title>
> >
> > 1. Port-forwarding creates a tunnel from your local computer to the pod in Kubernetes, allowing you to test the app before making it publicly accessible
> > 2. To update: modify your code, rebuild the container image with a new version number, push it to the registry, update the version in `deploy-image.yaml`, and run `kubectl apply -f deploy-image.yaml` again
> >
> {: .solution}
>
{: .question}

## Conclusion

Congratulations on completing this tutorial! You've successfully:

- Created a simple web application using Python and Streamlit
- Containerized the application with Podman
- Deployed it to EMBL's Kubernetes cloud infrastructure
- Made your application accessible (with port-forwarding, and potentially via a public URL)

This tutorial covered the fundamental workflow for cloud deployment. While we used a minimal example, these same principles apply to more complex applications. 

> <tip-title>Next Steps</tip-title>
>
> Now that you understand the basics, consider:
> - Expanding your dataset and adding more visualizations
> - Exploring Streamlit's advanced features
> - Learning more about Kubernetes resource management
> - Experimenting with different container configurations
> - Building more sophisticated data dashboards for your research
>
{: .tip}

Take some time to review each step and understand how they connect. In the future, you might want to deploy different types of applications using this same workflow!
