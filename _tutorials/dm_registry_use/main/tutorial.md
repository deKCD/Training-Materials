---
layout: tutorial_hands_on

title: Using the cross-domain Data-Management Platform registry
description: A step by step overview on how to use the registry.
slug: using-the-cross-domain-data-management-platform-registry
time_estimation: HM
questions:
  - How to start looking for a Data-Management Solution?
  - What benefits are there from having a cross-domain registry?
  - How to extend a Data-Management solution using APIs and other platforms?
objectives:
  - Using the registry with confidence,
  - Being able to contribute to it,
  - Knowing its limits and what to do around them,
key_points:
- The take-home messages
- They will appear at the end of the tutorial
version:
    - main
life_cycle: tutorial lifecycle
contributions:
  authorship:
  - Alain Becam
  editing: 
  funding: DeKCD Project
---

## Table of Contents
* [Scope]
* [Prerequisites](#prerequisites)
* [Setting-up a Data Management Solution, a short overview](#Setting-up_a_Data_Management_Solution,_a_short_overview)
  * [Goals and Purposes](#Goals and Purposes)
  * [Means](#Means)
  * [Constraints](#Constraints)


## **Scope**

This tutorial is not a comprehensive guide of doing Data Management, but a "been there done that" introduction followed by how to use the [DeKCD registry of FAIR data management platforms for the Cloud](https://dekcd.github.io/FAIR-DMP-Registry/). It is mostly on the technical side of Data Management.

## **Prerequisites**

To follow this tutorial:

- Knowledge of what is a Data Management Platform,
- Knowledge of the FAIR principles.

For a good use of the registry:

- Knowledge of Linux and Containers (Docker),
- Knowledge of API

## **Setting-up a Data Management Solution, a short overview**

The registry is mostly a technical overview and as such this section is mostly scoped to the technical aspect.
Several online resources help with a Data Management Plan, making it FAIR and various aspects, such as [RDM Kit (in Life Sciences)](https://rdmkit.elixir-europe.org/), [FairCookBook](https://faircookbook.elixir-europe.org/content/home.html), [Data Stewardship Wizard](https://ds-wizard.org/), [FairWizard](https://fair-wizard.com/)

### **Goals and Purposes**

The choice of a Data Management Solution is deeply dependent on the given goals and purposes. A solution for supporting a 1 year work could use a simple web-application installed using Docker on a local server, while a solution meant for 10 years and several project might benefit from being on the cloud, uses several connected web-applications.
Unfortunately there is no silver bullet, as the best solution will depend on your specific conditions, if you are part of a consortium proposing some infrastructure, if your institution offer some solutions, if you have the mean to get a technical person for the duration of the project.

### **Means**

Some Data Management platform are easy to set-up, easy to update and easy to use. Some are not, but they might address your needs better. In that case, it is probably good to consider the highest point of friction: what will cost the most on the long run. But also critical points: what cannot be accepted.

A critical point is the impossibility to do updates. If your datamanagement platform is online, it needs to be updated for security reasons. It might not be too critical if the application is behind a VPN, but that can change and might be a bigger problem then.

Point of frictions are the ease of use, the difficulty to update and the difficulty to set-it-up, from most important to less important, as a difficult to use application might simply be avoided. Users might also use some of their own solutions, making future data-management really difficult. But you have to be able to set-it-up and update it, and a difficult set-up might turn an emergency into a long downtime.

Similarly, an assembly can be desirable, one application closer to the lab communicating with a sharing platform, for instance. But the API communication needs to be secure, robust and well documented (also on your set-up). 

Versioning is always a good option for all your customisations, API, templating, parameter... When the customisation is not easily versionable, it is a good idea, when it is available as text, to work on a versioned copy. This work particularly well with a test set-up, which is also always good to have: apply the working changes only on test, and apply them on production only when commited in the Version Control System.

### **Constraints**

Constraints might be funding constraint, data usage constraint due to data privacy policy but also non-commercial use only of a software or data...

They might be considered as a chain: your Data Management platform needs to pass all elements of the chain.

Some constraints might be extremely costly, like adapting a GPL licensed platform in a commercial environment: the licence forces to share all changes, which could be a no-go for a private entity. A non-respect of the data privacy could get some fee, and a leak of personal data could be devastating.

They have strong connections with your means. You should have some leeway in order to manage constraint: i.e. the setup should not be so complex that the person(s) managing it can only focus on the needed technical aspect.

Some decisions related to constraints must also be made before setting-up the platform. For instance if you work on patient-related data and need encrypted storage, you need to choose a platform supporting it.

