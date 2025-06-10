---
layout: base
title: "Contributing"
---

## Instructions to add a new tutorial

To add a new tutorial from the original tutorial repository, run the following command:

```
git submodule add https://github.com/<user>/<tutorial> _tutorials/<tutorial>
```

By default, it adds content from the `main` branch. To select the specific branch, use `-b` argument, *e.g.*:

```
git submodule add -b <branch_name> https://github.com/<user>/<tutorial> _tutorials/<tutorial>
```

Place the tutorial content in a single `tutorial.md` in the tutorial root directory. To format the tutorial content, *i.e.* to wrap parts of the text in the special block quotes, please refer to the Software Carpenters' [Formatting episode](https://carpentries.github.io/lesson-example/04-formatting/index.html#special-blockquotes)

### Edit the tutorial

The `tutorial.md` should have the following structure:

```
---
layout: hands_on_tutorial
title: Title of the tutorial
description: Description of the tutorial
slug: slugified title
time_estimation: ""
questions:
  - Which questions are addressed by the tutorial?
objectives:
  - The learning objectives of the tutorial
key_points:
- The take-home messages
- They will appear at the end of the tutorial
version: tutorial version
contributors:
  - name: Full name
    orcid: ORCID ID
---

## Section title

Enter your tutorial content here.
```

Leave the `layout: hands_on_tutorial` as default. 

To create a proper inline image link, use `![figure-title](/tutorials/<tutorial-folder>/<image-folder>/<image>){: .responsive-img }`. Add `{: .responsive-img }` to place the image within the text width. 


## Instructions to create a new learning pathway

To add a new learning pathway, create `<pathway_title>.md` file in `_pathways` folder. The `<pathway_title>.md` should have the following structure:

```
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

Leave the `layout: pathway` as default. 