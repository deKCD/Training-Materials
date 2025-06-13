---
layout: contributing
title: "Contributing"
---

## **Add a new tutorial**
-------------------------
To add a new tutorial, create a new folder in `_tutorials` folder and  place the tutorial content in a single `tutorial.md` in the tutorial directory (or subdirectory if you have several versions of the same tutorial). 

Commit changes to the new branch and pull a request.

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

Leave the `layout: tutorial_hands_on` as default. 

If you have any data or images that you would like to add to the tutorial, please place them in the tutorial directory.


#### **Format the content**

##### **Boxes**

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


##### **Images**

To create a proper inline image link, use `![figure-title](/tutorials/<tutorial-folder>/<image-folder>/<image>){: .responsive-img }`. Add `{: .responsive-img }` to place the image within the text width.


> ## Additional resources
> If you need an additional materials to learn how to format the tutorial content, *i.e.* to wrap parts of the text in the special block quotes, please refer to the Software Carpenters' [Formatting episode](https://carpentries.github.io/lesson-example/04-formatting/index.html#special-blockquotes).
> 
> Please also refer to the [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) to learn more how to use Markdown.
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

Leave the `layout: pathway` as default. Commit changes to the new branch and pull a request.