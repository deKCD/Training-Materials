---
layout: tutorial_hands_on

title: Using the De.KCD "Data Management Platform on the Cloud" guide
description: A hands-on tour of the step-by-step guide for setting up and running a Data Management platform, from a local install to Kubernetes.
slug: dm_cloud_guide_use
level: Introductory
time_estimation: 45 minutes
questions:
  - Which level of solution (hosted service, virtual machine, Docker, Kubernetes...) fits my project?
  - How do I find my way through the guide, the Onboarding page and the decision tree?
  - What should I check before and after setting up a Data Management platform?
  - How can I contribute to the guide?
objectives:
  - Understand the purpose and scope of the "Data Management Platform on the Cloud" guide.
  - Navigate the site and find a topic with the menus and the search.
  - Choose between the Onboarding page, the full step-by-step guide and the decision tree.
  - Use the guide to compare solutions and to read a typical Docker Compose file.
  - Know the limits of the guide and how to contribute to it.
requirements:
- Basic understanding of research data management.
- Interest in FAIR principles and cloud affinity.
- Having read the tutorial on the cross-domain Data-Management Platform repository is useful, but not required.
key_points:
- The guide is a technical quickstart: it helps to decide on a solution and to navigate its documentation, it does not replace it.
- Choose the simplest level that meets your current needs; always check for a hosted service first.
- The Onboarding page is the 15-minute version, the step-by-step page has the details, and the decision tree helps to choose.
- Contributions and corrections are welcome via GitHub issues and pull requests.
version:
    - main
life_cycle: "beta"
contributions:
  authorship:
  - Alain Becam
  editing: AB
  funding: deKCD/BMBF
---

<!--
SCREENSHOTS TO ADD (to be saved in ../../images/):
  DMCloud_Home.png               Home page with the three areas annotated (top menu, left menu, right menu)
  DMCloud_TopMenu.png            Top header: title, Home, About, Privacy Policy, GitHub logo, magnifying lens
  DMCloud_LeftMenu.png           Left menu with the list of all pages
  DMCloud_RightMenu.png          Right menu "On this page", with a sub-section visible
  DMCloud_Search.png             Search pop-up with "Proxmox" typed
  DMCloud_SearchResult.png       Result page after clicking the search result (section 13.3)
  DMCloud_Onboarding.png         Onboarding page, top part
  DMCloud_DecisionTree.png       Technical Platform decision tree page
  DMCloud_HostedServices.png     Section "5 When to..." with the Note on hosted services
  DMCloud_ComposeExample.png     Section 10.3, the first docker compose example with the two Warning/Caution boxes
  DMCloud_ProxmoxTable.png       Table "Proxmox vs. Kubernetes"
  DMCloud_GitHubIssue.png        GitHub repository abecam/DeKCD-DMOnTheCloud, "New issue" page
-->

> <agenda-title>Table of Contents</agenda-title>
>
> In this tutorial we will deal with:
>
> 1. TOC
> {:toc}
>
{: .agenda}


# **Scope**

This tutorial is not a course on Linux, Docker or Kubernetes. It is a guided tour of the [De.KCD - Data Management Platform on the Cloud, step by step](https://abecam.github.io/DeKCD-DMOnTheCloud/) guide: what it contains, how to find your way through it, and how to use it to choose and prepare a Data Management platform. It is mostly on the technical side of Data Management.

By *Data Management platform* we mean an online application with a data repository (a database or other), such as those listed in the [DeKCD registry of FAIR data management platforms for the Cloud](https://dekcd.github.io/FAIR-DMP-Registry/). If you do not know yet which platform you want, start with the registry (see the companion tutorial), then come back here to decide how to run it.

# **Prerequisites**

To follow this tutorial:

- Knowledge of what a Data Management Platform is,
- Knowledge of the FAIR principles.

For a good use of the guide:

- Some experience with a terminal (Linux),
- Notions of containers (Docker). These are explained in the guide, but it is easier if the words are not completely new.

# **Why a guide on the technical side?**

Several online resources cover the planning of Research Data Management, such as [RDMKit](https://rdmkit.elixir-europe.org/), which also links to related resources. The guide is **only focused on technical aspects**: how much effort, how complex, what security risk, what is gained. It tries to save time in three ways:

1. deciding which solution to adopt,
2. understanding enough of each solution to navigate efficiently through its documentation,
3. giving working and explained examples that can be used as they are or as a base for your own solution.

It goes from a simple local setup to a full Kubernetes-based set-up, with side pages on backups and security, data storage, pseudonymization, assemblies of applications, semantic graphs and the use of LLMs.

> A good order is to start with RDMKit for the general view of Research Data Management, then use this guide for the technical view, and finally the official documentation of the chosen tools.
{: .tip}

# Hands-on: Using the guide

## Step 1: Access the guide

1. Open your browser and go to [https://abecam.github.io/DeKCD-DMOnTheCloud/](https://abecam.github.io/DeKCD-DMOnTheCloud/).
2. Spend a few minutes exploring the page without reading it in detail: we will cover the menus next.

![Home page with the three menu areas](../../images/DMCloud_Home.png "The home page and its three menu areas"){: .responsive-img }

## Step 2: Find your way with the menus

The site is a [Quarto](https://quarto.org/) website, and the menus are on the top, the left, and the right:

- **Top menu**: *Home* (the step-by-step guide), *About*, *Privacy Policy*, and the GitHub logo linking to the source repository.
- **Left menu**: all pages of the guide.
- **Right menu** ("On this page"): the sections of the current page. Sub-sections are shown in the menu when you are in the parent section.

![Top menu](../../images/DMCloud_TopMenu.png "The top menu"){: .responsive-img }

The left menu lists the different pages:

![Left menu](../../images/DMCloud_LeftMenu.png "The left menu"){: .responsive-img }

| Page | Use it when... |
| --- | --- |
| Data Management Platform on the Cloud, step by step | you want the full explanation, with examples (the Home page) |
| Onboarding | you want a 15-minute summary with links to the details |
| Technical Platform decision tree | you have to decide which level of solution you need |
| Backups and Security | you are about to expose a platform or to store valuable data |
| Data Storage | you need to decide where and how the data is stored (e.g. object storage) |
| Pseudonymization | you work with sensitive data that must be protected before sharing |
| Building an Assembly | several applications have to work together |
| Semantic graphs | you need to understand RDF, knowledge graphs, ontologies |
| General Considerations for Using LLMs in Research Data Management | you consider using LLMs with your data |
| Kubernetes - step by step | you need an introduction to Kubernetes |

The right menu is the one used most of the time, as the step-by-step page is long (about 19 sections):

![Right menu](../../images/DMCloud_RightMenu.png "The right menu"){: .responsive-img }

> ## Hands On: Find the page about backups
>
> From the Home page, go to the page about backups and security.
>
> > ## Answer
> > Click on *Backups and Security* in the left menu.
> >
> > ![Selecting the page in the left menu](../../images/DMCloud_LeftMenu.png "Selecting the Backups and Security page"){: .responsive-img }
> {: .solution}
>
{: .question}

## Step 3: Using the search

The search, powered by Quarto, is accessed by clicking on the magnifying lens icon at the top right of the top menu. In the pop-up that appears, typing should automatically start a search. Clicking on one result leads to the paragraph containing it.

![Doing a search](../../images/DMCloud_Search.png "Doing a search"){: .responsive-img }

> ## details
> Depending on the size of the window, there could be 2 magnifying lenses. They both have the exact same function.
{: .details}

> ## Hands On: Find the section about Proxmox
>
> Using the search, look for Proxmox and find what it is used for compared to Kubernetes.
>
> > ## Answer
> > Click on the magnifying lens and type *Proxmox*. Select the result in the step-by-step page: it leads to section *13.3 Proxmox VE — Virtualisation Without VMware*. The sub-section *Proxmox vs. Kubernetes — when to use which* explains that Proxmox virtualises hardware (virtual machines and Linux containers) while Kubernetes orchestrates application containers: they work at different layers and can be combined.
> >
> > ![Search result](../../images/DMCloud_SearchResult.png "The section about Proxmox"){: .responsive-img }
> {: .solution}
>
{: .question}

## Step 4: Choose your entry point

There are three ways to start, depending on your time and your question.

- **Onboarding** (about 15 minutes): the condensed version. Each section ends with a pointer to the matching part of the full guide. It also proposes a suggested path for newcomers.
- **Decision tree**: a more detailed way to answer "when to go full cloud, or with a containerised solution?".
- **Step-by-step guide**: all the details. Each section assumes that you know the previous ones, so if you already know one, jump to the next.

![The Onboarding page](../../images/DMCloud_Onboarding.png "The Onboarding page"){: .responsive-img }

![The decision tree](../../images/DMCloud_DecisionTree.png "The decision tree page"){: .responsive-img }

> ## Hands On: Choose the right level
>
> You are a PhD student with a small analysis tool. You are the only user, nobody else needs to access the data, and you want to try the tool. Which level of solution is described as sufficient, and what is its limitation?
>
> > ## Answer
> > In section *5 When to…*, a very simple use case with a single application and a single user, without data sharing, can be handled with a local installation on a personal computer ("bare metal"). It is the simplest solution but the least scalable and the least secure: it is not recommended for production but useful for testing and development.
> {: .solution}
>
{: .question}

## Step 5: Check first if a hosted service exists

The guide insists on one point: **if your institution or consortium offers a suitable hosted service, it is generally the best option**, as it is maintained and updated by the provider. You still have to check the terms of service, the security measures, and the possibility to access the data and the API.

![Hosted services](../../images/DMCloud_HostedServices.png "The Note about hosted services in section 5"){: .responsive-img }

> ## Hands On: Find a service for your region
>
> You are a researcher at an Australian university and you need virtual machines for a research project. Which service listed in the guide could you check first?
>
> > ## Answer
> > In the Note of section *5 When to…*, the guide lists several services: De.NBI Cloud (Germany), the European Open Science Cloud and the EGI Federation (Europe), Gaia-X, the ACCESS program (USA), the Digital Research Alliance of Canada, and the **Nectar Research Cloud** in Australia, as well as national or institutional initiatives such as the GWDG Academic Cloud.
> >
> > Even then, a dedicated installation might still be needed for security and privacy concerns or for large, high-performance data.
> {: .solution}
>
{: .question}

## Step 6: Apply the common remarks

Section *6 Common remarks* is the one to read even if you skip the rest. It contains five principles:

1. **Keep the difficulty under control**: a solution you cannot maintain is a bad solution. Reuse existing, well-supported infrastructure.
2. **Decide the level of service**: the difference in cost between 1 night and 1 hour of downtime is probably smaller than between 1 hour and 1 minute.
3. **Plan for future problems, not future functionalities**: security issues, data loss and performance problems are costly to fix later. Avoid feature creep: build for what users *need*, not for what they *want*.
4. **Document all specific changes**: what, why, who, when, and how to revert.
5. **Use version control** for everything that can be changed (configuration, compose files, scripts).

> ## Hands On: Apply the principles
>
> Your platform has no way to export its customisations, but they are stored in an accessible database. What does the guide advise?
>
> > ## Answer
> > Section *6.5* advises writing a script or a program doing the export, to keep a consistent and versionable copy. Python is a good option. When the platform allows it, exporting to a text file (json, ini, xml) or using its API is better; both can be saved in a versioned folder. Commits should be manual with meaningful messages.
> {: .solution}
>
{: .question}

## Step 7: Read a Docker Compose file

Section *10 Moving to Docker compose* is the most hands-on part of the guide. Section *10.3* builds a compose file in three steps: a first simple version, one using YAML anchors so the database settings are not repeated, and a final one with a health check.

![Docker compose example](../../images/DMCloud_ComposeExample.png "The first Docker Compose example"){: .responsive-img }

Before using it, note that the guide marks two problems of the first version in a *Warning* and a *Caution* box.

> ## Hands On: Spot the problems
>
> Read the first compose file of section 10.3 and its Warning and Caution boxes. What are the two problems, and how are they solved in the later versions?
>
> > ## Answer
> > 1. The Postgres password and the Django secret key have a default value. This is fine for testing only: in a stable application they should come from an `.env` file, without default value.
> > 2. `depends_on: db` only means that the database container is started first, not that the database is ready. If the application needs the database at start (for instance for an automatic migration), it can fail. The final version adds a `healthcheck` on the database and uses `condition: service_healthy`.
> >
> > The YAML anchor (`x-postgres-env: &postgres-env`) removes a third risk: the database values being different in the two services.
> {: .solution}
>
{: .question}

> ## Hands On: Spot the namespace collision
>
> You have two instances of the same application:
> ```
> application1/testApp/docker-compose.yml
> application2/testApp/docker-compose.yml
> ```
> Is it a clean set-up? Why (not)?
>
> > ## Answer
> > No. The namespace is the name of the folder containing the compose file, here `testApp` for both. The two set-ups use the same Docker network, so only one database instance will be used by both applications, or there will be a binding error and one application will fail (the best outcome). See section *10.6*.
> {: .solution}
>
{: .question}

## Step 8: Compare the other solutions

The guide gives overviews of other solutions and a way to compare them:

- **Proxmox VE** (13.3): virtualisation with a web interface, snapshots and backups. A good step between managing servers by hand and OpenStack or Kubernetes.
- **OpenStack** (13.4): open-source cloud infrastructure for many servers and many groups. Often something you *use* rather than run yourself.
- **Lightweight and cloud-native orchestrators** (13.5): Nomad, Docker Swarm, Amazon ECS, Google Kubernetes Engine, serverless containers, Google Cloud Run, with a comparison table.
- **Apache Software Foundation solutions** (13.6): HTTP Server, Tomcat, Kafka, Spark, Airflow, Solr.

![Proxmox vs Kubernetes table](../../images/DMCloud_ProxmoxTable.png "The comparison table of Proxmox and Kubernetes"){: .responsive-img }

> ## Hands On: Combine two solutions
>
> Your group has three servers and wants to host a database, a web server and a backup service, and may later need to manage many application deployments with automatic scaling. What path does the guide suggest?
>
> > ## Answer
> > Section *13.3.2* suggests starting with Proxmox to host virtual machines for the different services. If the team grows and needs to manage many deployments with automated scaling, a Kubernetes cluster can run on top of Proxmox VMs. If the need is even higher, OpenStack offers a group of cloud-oriented solutions.
> {: .solution}
>
{: .question}

> The cloud solutions of Amazon, Google and Microsoft are generally billed per use, so the cost can grow very quickly if the usage grows. Set up alerts, or avoid them if the cost must be predictable.
{: .warning}

## Step 9: Do not forget the topics that matter at every level

The last sections of the guide apply whatever the level you choose: **Scalability** (14), **Databases** (15), **Security** (16), **Going to an assembly** (17), **Automatize the setup** (18: Puppet, Ansible, Terraform, CI/CD and GitOps) and **Many choices: tools, solutions and platforms** (19). The security section starts with the minimum: keep software up to date, give access only to those who need it, use encryption when needed, **back up regularly and test the restore**, and monitor for suspicious activity.

For the details, follow the links to the pages *Backups and Security*, *Data Storage*, *Pseudonymization* and *Building an Assembly*.

## Step 10: Be aware of what is NOT included

The guide does **not** provide:

- A complete documentation of each solution (it is meant to understand a solution and navigate its documentation),
- A full Data Management Plan or the non-technical aspects of Research Data Management (see RDMKit),
- Guarantees that a given solution fits your institution: existing servers, virtual machine infrastructure and local IT support cannot be planned for by the guide.

> ## warning
> Pitfall: the guide is aimed at non-sysadmins. For a production Kubernetes cluster, rely on your system administrators, and involve your IT support early.
{: .warning}

## Step 11: Contribute to the guide

The guide is open source, and contributions and corrections are welcome. The link to the [GitHub repository](https://github.com/abecam/DeKCD-DMOnTheCloud) is also provided on the top header with the GitHub logo:

1. **Create an issue** to report an error or suggest a change.
2. **Fork the repository** and submit a pull request to correct or extend a page.

![Creating an issue](../../images/DMCloud_GitHubIssue.png "Creating an issue on GitHub"){: .responsive-img }

Good contributions are, for instance, a platform-specific tip, a correction, a tested example, or a link to a good resource for a section.

# Conclusion

You now know what the **Data Management Platform on the Cloud** guide offers, and how to use it: start with the Onboarding page or the decision tree, choose the simplest level that fits your needs (after checking for a hosted service), use the step-by-step page for the details, and keep in mind the common remarks: control the difficulty, plan for problems, document and version your changes.

For questions or contributions, contact:  
**Alain Becam** – [Alain.Becam@bioquant.uni-heidelberg.de](mailto:Alain.Becam@bioquant.uni-heidelberg.de)  
Project site: [https://datenkompetenz.cloud/](https://datenkompetenz.cloud/)
