---
layout: contributing
title: Contribution
description: Guidelines for contributing, including adding new content or editing existing materials.
---

We highly recommend reading [Ten simple rules for making training materials FAIR](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007854#abstract0){:target="_blank"} before creating a new training material and following the **FAIR (Findable, Accessible, Interoperable, Reusable)** principles for training materials. 

## Table of Contents
* [Add a new tutorial](#add-a-new-tutorial)
    * [Edit the tutorial](#edit-the-tutorial)
    * [Format the content](#format-the-content)
        * [Boxes](#boxes)
        * [Images](#images)
* [Create a new learning pathway](#create-a-new-learning-pathway)
* [Preview the website](#preview-the-website)


## **Add a new tutorial**
-------------------------
To add a new tutorial, create a new folder in `_tutorials` folder and  place the tutorial content in a single `tutorial.md` within the tutorial directory (or a subdirectory if you have multiple versions of the same tutorial).

When creating a new tutorial, add the folder name (slug) to the `_data/tutorial_groups.yml` file. This links your tutorial to an existing tutorial group.
If your tutorial belongs to a new category that does not yet exist, create a new group entry in `_data/tutorial_groups.yml` with a clear description of the group.


Then, commit the changes to the new branch and submit a pull request.

### **Edit the tutorial**
-------------------------
The `tutorial.md` should have the following structure:

```
---
layout: tutorial_hands_on

title: Title of the tutorial
description: Description of the tutorial
slug: slugified title
time_estimation: HM
questions:
  - Which questions are addressed by the tutorial?
objectives:
  - The learning objectives of the tutorial
key_points:
- The take-home messages
- They will appear at the end of the tutorial
version: tutorial version
life_cycle: tutorial lifecycle
contributions:
  authorship:
  - author 1
  - author 2
  editing: 
  funding: 
---

## Section title

Enter your tutorial content here.
```

The tutorial requires the metadata to be included at the top:
* keep the layout as `tutorial_hands_on` by default.
* `title`: the title of the tutorial will appear on the **Collection of Tutorials** page.
* `time_estimation`: the estimated time needed to complete the hands-on tutorial. It must match the following regular expression pattern:
      ```/^(?:([0-9]+)[Hh])?(?:([0-9]+)[Mm])?(?:([0-9.]+)[Ss])?$/```
* `questions`: a list of questions that will be addressed in the tutorial.
* `objectives`: a list of learning objectives for the tutorial.
* `key_points`: a list of take-home messages that will appear at the end of the tutorial.
* `contributions`: a list of tutorial contributors broken down into broad categories to help contributors identify how they contributed to a specific tutorial. Examples include `authorship`, `editing`, `funding`, `testing`, `infrastructure`, and `translation`.

> ## Development status of tutorials
> The development status of tutorials follows a framework similar to that of the [Carpentries](https://docs.carpentries.org/> resources/curriculum/lesson-life-cycle.html). Training materials are classified into four categories: **alpha**, **beta**, **stable**, and **deprecated**.
> 
> - **Alpha:** the tutorial is in the early stages of development. Its content may be incomplete, untested, and subject to significant changes. This status typically applies until a complete first draft is available.
> - **Beta:** the tutorial is in the testing phase, being reviewed and taught by other instructors. Feedback from pilot workshops is actively incorporated, and further revisions are likely.
> - **Stable:** the tutorial is considered complete, reliable, and well-maintained. Only minor updates are expected, with no major changes anticipated. 
> - **Deprecated:** the tutorial is no longer maintained and may be removed in the future.
> 
{: .details}

The following information can also be included in the tutorial metadata:
* `zenodo_link`: link to the input data for the tutorial on Zenodo.
* `follow_up_training`: a list of resources that the reader of the material could follow at the end of the tutorial.

For additional information that could be included in the tutorial metadata, please refer to the [GTN tutorial.](https://training.galaxyproject.org/training-material/topics/contributing/tutorials/create-new-tutorial-content/tutorial.html){:target="_blank"}


If you have any data or images that you would like to add to the tutorial, please place them in the tutorial directory.


### **Format the content**

#### **Boxes**

To improve the learning experience in our tutorial, we define some boxes to highlight content. Below is an example of the "Task box with solutions":

```markdown
> ## Questions
> 1. Question 1
> 2. Question 2
>  
> > ## Answers
> > 1. Answer 1
> > 2. Answer 2
> > 
> {: .solution}
>
{: .question}
```
which will look like this:

> ## Questions
> 1. Question 1
> 2. Question 2
>  
> > ## Answers
> > 1. Answer 1
> > 2. Answer 2
> > 
> {: .solution}
>
{: .question}

There are several boxes that you can use to format the content of your training material: `{: .overview}`, `{: .key_points}`, `{: .tip}`, `{: .warning}`, `{: .comment}`, `{: .hands_on}`, `{: .question}`, `{: .solution}`, `{: .details}`, `{: .feedback}`, `{: .code-in}`, and `{: .code-out}`.

> ## Tasks
> 1. Create each box and see how it looks.
> 2. Create one with a nested box.
> 
{: .hands_on}

### **Examples**

> ## Tasks
> 1. List of tasks
> 2. ...
> 
{: .hands_on}


> ## Details
> Here put some text...
> 
{: .details}


> ## Tip
> Here put some useful information...
> 
{: .tip}


> ## Comment
> Here put some comments...
> 
{: .comment}

> ## Code In
> ```bash
> ls -lh
> ```
>
> ```python
> import pandas as pd
> ```
> 
{: .code-in}

> ## Code Out
> ```bash
> # code output
> ```
> 
{: .code-out}

> ## Questions
> 1. Question 1
> 2. Question 2
>  
> > ## Answers
> > 1. Answer 1
> > 2. Answer 2
> > 
> {: .solution}
>
{: .question}

#### **Images**

To create a proper inline image link, use `![figure-title](/tutorials/<tutorial-folder>/<image-folder>/<image>){: .responsive-img }`. Add `{: .responsive-img }` to place the image within the text width.


> ## Additional resources
> If you need an additional materials to learn how to format the tutorial content, *i.e.* to wrap parts of the text in the special block quotes, please refer to the Software Carpenters' [Formatting episode.](https://carpentries.github.io/lesson-example/04-formatting/index.html#special-blockquotes){:target="_blank"}
> 
> Please also refer to the [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet){:target="_blank"} to learn more how to use Markdown.
> 
{: .details}


## **Create a new learning pathway**
------------------------------------
To add a new learning pathway, create `<pathway_title>.md` file in `_pathways` folder. The `<pathway_title>.md` should have the following structure:

```markdown
---
layout: pathway
title: Title of the Learning Pathway
description: Description of the Learning Pathway
tags: []
pathway:
  - section: "Module 1: Title of the Module
    description: Description of the Module
    tutorials:
      - name: tutorial name
        version: main

  - section: "Module 1: ..."
    description: ...
    tutorials:
      - name: ...
        version: ...
editorial_board:
  - name: ...
    orcid: ...
---
```

Keep the `layout: pathway` as default. Commit changes to the new branch and pull a request.

## **Preview the website**
--------------------------
To preview your own training materials locally, use provided devcontainer. To use it, you need to have [Visual Studio Code](https://code.visualstudio.com/) installed. Open the repository in VS Code and it will prompt you to reopen the folder in the container. After that, you can run the Jekyll server as follows: 

```bash
bundle exec jekyll serve --config _config.yml,_config_dev.yml
```
