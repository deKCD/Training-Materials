---
layout: tutorial_hands_on

title: Using the cross-domain Data-Management Platform repository
description: A step by step overview on how to use the repository.
slug: dm_repository_use
level: Introductory
time_estimation: 40 minutes
questions:
  - How to start looking for a Data-Management Solution?
  - What benefits are there from having a cross-domain repository?
  - How to extend a Data-Management solution using APIs and other platforms?
objectives:
  - Understand the purpose and scope of the Data Management Platforms repository.
  - Learn how to navigate and interpret the listed platforms.
  - Contribute new or updated information to the repository.
  - Being able to contribute to it,
  - Knowing its limits and what to do around them,
requirements:
- Basic understanding of research data management.
- Interest in FAIR principles and cloud affinity.
key_points:
- The repository lists cross-domain Data Management platforms with a FAIR and cloud focus.
- It does not replace a full Data Management Plan.
- Platforms can be generalist or specialist, depending on needs.
- Contributions are welcome via GitHub issues and pull requests.
version:
    - main
life_cycle: tutorial lifecycle
contributions:
  authorship:
  - Alain Becam
  editing: 
  funding: DeKCD Project
---

> <agenda-title>Table of Contents</agenda-title>
>
> In this tutorial we will deal with:
>
> 1. TOC
> {:toc}
>
{: .agenda}


# **Scope**

This tutorial is not a comprehensive guide of doing Data Management, but a "been there done that" introduction followed by how to use the [DeKCD registry of FAIR data management platforms for the Cloud](https://dekcd.github.io/FAIR-DMP-Registry/). It is mostly on the technical side of Data Management.

# **Prerequisites**

To follow this tutorial:

- Knowledge of what is a Data Management Platform,
- Knowledge of the FAIR principles.

For a good use of the repository:

- Knowledge of Linux and Containers (Docker),
- Knowledge of API

# **Setting-up a Data Management Solution, a short overview**

The repository is mostly a technical overview and as such this section is mostly scoped to the technical aspect.
Several online resources help with a Data Management Plan, making it FAIR and various aspects, such as [RDM Kit (in Life Sciences)](https://rdmkit.elixir-europe.org/), [FairCookBook](https://faircookbook.elixir-europe.org/content/home.html), [Data Stewardship Wizard](https://ds-wizard.org/), [FairWizard](https://fair-wizard.com/)

## **Goals and Purposes**

The choice of a Data Management Solution is deeply dependent on the given goals and purposes. A solution for supporting a 1 year work could use a simple web-application installed using Docker on a local server, while a solution meant for 10 years and several project might benefit from being on the cloud, uses several connected web-applications.
Unfortunately there is no silver bullet, as the best solution will depend on your specific conditions, if you are part of a consortium proposing some infrastructure, if your institution offer some solutions, if you have the mean to get a technical person for the duration of the project.

## **Means**

Some Data Management platform are easy to set-up, easy to update and easy to use. Some are not, but they might address your needs better. In that case, it is probably good to consider the highest point of friction: what will cost the most on the long run. But also critical points: what cannot be accepted.

A critical point is the impossibility to do updates. If your datamanagement platform is online, it needs to be updated for security reasons. It might not be too critical if the application is behind a VPN, but that can change and might be a bigger problem then.

Point of frictions are the ease of use, the difficulty to update and the difficulty to set-it-up, from most important to less important, as a difficult to use application might simply be avoided. Users might also use some of their own solutions, making future data-management really difficult. But you have to be able to set-it-up and update it, and a difficult set-up might turn an emergency into a long downtime.

Similarly, an assembly can be desirable, one application closer to the lab communicating with a sharing platform, for instance. But the API communication needs to be secure, robust and well documented (also on your set-up). 

Versioning is always a good option for all your customisations, API, templating, parameter... When the customisation is not easily versionable, it is a good idea, when it is available as text, to work on a versioned copy. This work particularly well with a test set-up, which is also always good to have: apply the working changes only on test, and apply them on production only when commited in the Version Control System.

## **Constraints**

Constraints might be funding constraint, data usage constraint due to data privacy policy but also non-commercial use only of a software or data...

They might be considered as a chain: your Data Management platform needs to pass all elements of the chain.

Some constraints might be extremely costly, like adapting a GPL licensed platform in a commercial environment: the licence forces to share all changes, which could be a no-go for a private entity. A non-respect of the data privacy could get some fee, and a leak of personal data could be devastating.

They have strong connections with your means. You should have some leeway in order to manage constraint: i.e. the setup should not be so complex that the person(s) managing it can only focus on the needed technical aspect.

Some decisions related to constraints must also be made before setting-up the platform. For instance if you work on patient-related data and need encrypted storage, you need to choose a platform supporting it.

# Introduction to the Data Management Platform Repository

The **Data Management Platforms (DMP) repository** is a curated collection of major platforms used in research data management.  
It emphasizes the FAIR principles (Findable, Accessible, Interoperable, Reusable) and evaluates how platforms integrate with cloud infrastructures.  
This tutorial will guide you through using the repository, understanding its scope, and contributing to it.

# Hands-on: Using the Repository

## Step 1: Access the Repository

1. Open your browser and go to [https://dekcd.github.io/FAIR-DMP-Registry/](https://dekcd.github.io/FAIR-DMP-Registry/).
2. Spend some time exploring the different menus, we will cover them later
  On the top header, the title and the Home link both return to the main page. About is a short description of the registry.
  The left column shows the different pages while the right column shows the topic in the current page.

## Step 2: Understand the Main Goals
The repository highlights platforms with:
- Reusability across domains,  
- Interoperability,  
- Affinity to cloud usage/set-ups,  
- Good documentation.

> Note: While most platforms align with FAIR principles, not all do completely.

## Step 3: Using the repository

### Using the menus

The menus are on the top, the left and the right:
- **Top Menu**: The Home page and the about page.
- **Left Menu**: All pages of the repository.
- **Right Menu**: The topics in the current page.

The top menu will typically be used once or twice, to check the About page.

![Image showing the top menu](../../images/About.png "The top menu"){: .responsive-img }

The Left menu will be used to select in which category to look for:

![Image showing the left menu](../../images/MainDMPlatformMenu.png "The left menu"){: .responsive-img }

The right menu will be used to go to a specific topic and most of the time to a specific domain. Some topics have subtopic that become visible in the menu when in the parent topic.

![Image showing the right menu](../../images/RightMenu.png "The right menu"){: .responsive-img }

> ## Hands On: Find a commercial DM platform for a domain
> 
> From the Home Page, navigate to the Commercials subtopic of Geomatics in the list of Major Data Management platforms.
> 
> > ## Answer
> > First click on the Major Data Management Platforms link in the left menu.
> > ![Selecting Major Data management in the left menu](../../images/MainDMPlatformMenu.png "Selecting Major Data management in the left menu"){: .responsive-img }
> > Then on Geomatics on the right menu, and finally on Commercials in the sub-menu.
> > ![Selecting in the right menu then in the submenu](../../images/CommercialsGeomatics.png "Selecting in the right menu then in the submenu"){: .responsive-img }
> {: .solution}
> 
{: .question}

### A typical entry

All entries are not identic, as there are some extra informations for some entries. But all entries should have a common base, and most entries will stick to it:

* Link with the Name, quick description pointing generally to the URL of the main web page or the documentation.
	+ Description and/or link to potential Docker image/Docker compose/Kubernetes manifest/…
	+ Link to API(s), quick clarification on how well documented it is.
	+ Interoperability **NONE/LOW/MEDIUM/HIGH** / No interoperability: explanation on why.
	+ **Not/Partly/Mostly/Fully** cross-domain: explanation on why.

> ## Hands On: Find details about a specific entry
> 
> In the Major Data Management Platforms page, find the details about pyiron, which is in Materials Science. Check if it is cross-domain.
> 
> > ## Answer
> > Click on Materials Science on the right menu, then eventually scroll down to find the details about pyiron, including if it is cross-domain.
> > ![Selecting in the right menu](../../images/MaterialsScience.png "Selecting in the right menu"){: .responsive-img }
> {: .solution}
> 
{: .question}

### Using the search

The Repository propose a search function, powered by the used document system, Quarto, which is accessed by clicking on the manifying lens icon at the top right of the top menu.

In the pop-up that appears, writing should automatically start a search.

![Doing a search](../../images/SearchIRODS.png "Doing a search"){: .responsive-img }

Clicking on one result should send to the paragraph containing the result. It is possible to use the browser "Search in Page" to go to the actual entry.

![Finding the entry using the browser search](../../images/SearchIRODSInPage.png "Finding the entry using the browser search"){: .responsive-img }

> ## details
> Depending on the size of the page, there could be 2 manifying lenses. They have both the exact same function.
{: .details}

> ## Hands On: Find details about a specific entry
> 
> Using the search, look for CIViC.
> 
> > ## Answer
> > Click on the manifying lens.
> > ![Clicking on the manifying lense](../../images/SearchCIViC1.png "Clicking on the manifying lense"){: .responsive-img }
> > Then type CIV in the search bar.
> > ![Typing in the search bar](../../images/SearchCIViC2.png "Typing in the search bar"){: .responsive-img }
> > Finally click on the search result.
> > ![Selecting the search result](../../images/SearchCIViC3.png "Selecting the search result"){: .responsive-img }
> > The result should roughly be in the middle of the page
> > ![Getting the entry](../../images/SearchCIViC_result.png "Getting the entry"){: .responsive-img }
> {: .solution}
> 
{: .question}

### Extras

The repository also lists, in a simplified format:
- **the major ontologies and thesauruses**,
![List of major ontologies and thesauruses](../../images/OntologiesThesauruses.png "List of major ontologies and thesauruses"){: .responsive-img }
- **the major taxonomies and classifications**,
![List of major taxonomies and classifications](../../images/Taxonomies.png "List of major taxonomies and classifications"){: .responsive-img }
- Some **Useful tools and platforms for Data Managements**, these are applications and tools that can be used together with Data Managements platforms, such as central authority providers that can help setting-up a Single Sign On (SSO, login once for several applications) **or** used by Data Management platforms, such as a S3 implementation, to store data in a cloud environment.
![List of useful tools and platforms](../../images/UsefulTools.png "List of useful tools and platforms"){: .responsive-img }

As for the Data Management Platforms, they do not pretend to be exhaustive and all contributions are welcome.

## Step 3: Generalists vs Specialists

TODO: Short explanation of the difference, cost and benefits

- **Generalist platforms**: e.g. NextCloud (supporting tasks), iRODS or RUCIO (registering/storing data).  
- **Specialist platforms**: e.g. Electronic Laboratory Notebooks for domain-specific work.  
- **Tip**: Combining both may be necessary. Interconnection often depends on available APIs and documentation.

TODO: question about using one generalist or a specialist platform,
question about using one with another (for instance Omero + NextCloud)

## Step 4: Consider Set-up Options

TODO: Short introduction, words about cost, benefits, difficulty and security

- Containerized set-up → simpler deployment and updates.  
- Kubernetes support → ensures 24/7 operation (if a Kubernetes cluster is already available).  
- API access → enables interoperability and data extraction.  

## Step 5: Be Aware of What’s NOT Included
The repository does **not** provide:
- A full Data Management Plan (e.g. retention policy, access rights).  
- Guarantees on platform lifetime or funding.  
- Alignment between scientists’ low-friction tools vs. institutes’ and funders’ FAIR requirements.  

> ## warning
> Pitfall: Modifying open-source software may block future updates. Prefer configuring over modifying.
{: .warning}

## Step 6: Next Technical Steps
A **Quickstart guide** (work in progress) is planned:
- From bare-metal to full Kubernetes deployments,  
- With details on costs, security, and support needs,  
- Vocabulary clarification for better understanding of existing documentation.

## Step 7: Contribute to the Repository
You can contribute via GitHub:
1. **Create an issue** to suggest a change.  
2. **Fork the repository** and submit a pull request to add or modify entries.  

A typical entry should include:
- Platform name & quick description (with link),  
- Links to Docker/Kubernetes manifests,  
- Links to APIs & documentation,  
- Interoperability level (None/Low/Medium/High),  
- Cross-domain applicability (Not/Partly/Mostly/Fully).

```Markdown
* [Name, quick description](https:URL of main web page)
	+ Description and/or link to potential Docker image/Docker compose/Kubernetes manifest/…
	+ Link to API(s), quick clarification on how well documented it is.
	+ Interoperability **NONE/LOW/MEDIUM/HIGH** / No interoperability: explanation on why.
	+ **Not/Partly/Mostly/Fully** cross-domain: explanation on why.
```

# Conclusion
You now know how to use and navigate the **Data Management Platforms repository**.  
It is a living resource focused on FAIR principles and cloud compatibility, and it depends on community contributions to grow and remain current.  

For questions or contributions, contact:  
**Alain Becam** – [Alain.Becam@bioquant.uni-heidelberg.de](mailto:Alain.Becam@bioquant.uni-heidelberg.de)  
Project site: [https://datenkompetenz.cloud/](https://datenkompetenz.cloud/)
