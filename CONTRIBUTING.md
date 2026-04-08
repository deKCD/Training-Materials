---
layout: base_contributing
title: Contribution
description: Guidelines for contributing, including adding new content or editing existing materials.
---

We highly recommend reading [Ten simple rules for making training materials FAIR](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007854#abstract0){:target="_blank"} before creating a new training material and following the **FAIR (Findable, Accessible, Interoperable, Reusable)** principles for training materials. 

## Preview the website
---------------------------
There are two options to run the website locally and preview your training materials before pushing them.

**Option 1: Using Ruby and Bundler**

You need [Ruby](https://www.ruby-lang.org/en/documentation/installation/){:target="_blank"} and [Bundler](https://bundler.io/){:target="_blank"} installed. Then run:

```bash
# Install required gems
bundle install

# Start the Jekyll server
bundle exec jekyll serve --trace --livereload
```

Open `http://127.0.0.1:4000/training/` (`Server address`) in your browser to view the website.

**Option 2: Using Docker**

Build and run the containerized version:

```bash
# Build the Docker image
docker build . -t dekcd

# Run the container
docker run -it -p 4000:4000 dekcd
```

Then open `http://127.0.0.1:4000/training/` in your browser.


## Add a new tutorial
-------------------------
This section describes the required structure, conventions, and submission workflow for contributing a new tutorial. Please follow these guidelines to ensure consistency, reusability, and maintainability across the repository.

### Create the tutorial directory 
All tutorials must reside within the `_tutorials` directory. Each tutorial should have its own dedicated subfolder:
```
_tutorials/<tutorial-name>/
```

Within this folder, you may either:
* provide a single, self-contained file (`tutorial.md`), or
* organize the content into multiple smaller Markdown files (e.g., `part1.md`, `part2.md`)

**Recommended approach: modular structure**

Splitting content into smaller, logically coherent markdown files is strongly encouraged. This enables:
* reuse of content blocks across tutorials
* easier maintenance and updates
* reduced duplication

### Composing tutorials

#### **Metadata**

All tutorials must define their metadata at the very top of the main file `tutorial.md` using YAML front matter. **Do not** place metadata in auxiliary Markdown files (e.g., part1.md, part2.md).

Example:
```
---
layout: tutorial_hands_on
title: Introduction to basic Unix commands
description: "This is the introduction to the basic shell commands."
slug: unix-course
time_estimation: 2H30M
level: "Educational level"
keywords: [list of keywords]
questions:
  - Which questions are addressed by the tutorial?
objectives:
  - The learning objectives of the tutorial
key_points:
 - The take-home messages
 - They will appear at the end of the tutorial
version:
 - main
life_cycle: "Creative work status"
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
The following fields are mandatory unless stated otherwise:
* `layout`: use `tutorial_hands_on` as the default layout.
* `title`: tutorial title as displayed on the tutorial collection page.
* `description`: a concise summary of the tutorial content. 
* `slug`: 
* `time_estimation`: estimated duration of the tutorial. This must conform to the following pattern:
      ```/^(?:([0-9]+)[Hh])?(?:([0-9]+)[Mm])?(?:([0-9.]+)[Ss])?$/```
* `level`: the learners level of ability in the topic being taught according to the BioSchema [TrainingMaterial Profile 1.0-RELEASE](https://bioschemas.org/profiles/TrainingMaterial/1.0-RELEASE). Examples of skill levels include ***beginner***, ***intermediate*** or ***advanced***.
* `keywords`: keywords or tags used to describe the content. Multiple entries in a keywords list are delimited by commas.
  Example:
  ```keywords: ["bioinformatics", "python"]```
* `questions`: a list of key questions addressed by the tutorial.
* `objectives`: a list of learning objectives.
* `key_points`: summary points presented at the end of the tutorial.
* `version`: specifies the tutorial version (e.g., `main`).
* `life_cycle`: indicates the development status of a training material according to the BioSchema [TrainingMaterial Profile 1.0-RELEASE](https://bioschemas.org/profiles/TrainingMaterial/1.0-RELEASE). Options are ***Active***, ***Under development***, and ***Archived***.

  Example:
  ```life_cycle: "under development"```

> <details-title>Development status of tutorials</details-title>
> Tutorials follow a structured development model aligned with best practices from [Carpentries](https://docs.carpentries.org/resources/curriculum/lesson-life-cycle.html).
> - **Alpha:** early-stage development. Content may be incomplete, untested, and subject to significant changes. This status typically applies until a complete first draft is available.
> - **Beta:** actively tested and reviewed. Feedback from pilot workshops is actively incorporated, and further revisions are likely.
> - **Stable:** complete, reliable, and well-maintained tutorial. Only minor updates are expected.
> - **Deprecated:** the tutorial is no longer maintained and may be removed in the future.
> 
{: .details}

* `contributions`: categorized list of contributors. Examples include `authorship`, `editing`, `funding`, `testing`, `infrastructure`, and `translation`. In the `funding` section, list the name of the organization that supported the training material. Ensure that the organization’s name matches an entry in `_data/contributions.yml`. If your organization is not listed, please add its `name` to `_data/contributions.yml` and place the organization’s `logo` in `/assets/img/`.


The following fields are optional but recommended where applicable:
* `zenodo_link`: link to the input data for the tutorial on Zenodo.
* `follow_up_training`: a list of resources that the reader of the material could follow at the end of the tutorial.

For extended metadata options and advanced patterns, please refer to the [Galaxy Training Network tutorial guidelines.](https://training.galaxyproject.org/training-material/topics/contributing/tutorials/create-new-tutorial-content/tutorial.html){:target="_blank"}


#### **Modular structure**

If you choose a modular structure, assemble the final tutorial using Jekyll’s `include` directive:

{% raw %}
```markdown
Your introductory text.

{% include _tutorials/intro-python/main/part1.md %}

Additional content.
```
{% endraw %}

This approach allows flexible composition while keeping individual sections reusable.

A typical modular tutorial may look like:
```
_tutorials/
  intro-python/
    main/
      part1.md
      part2.md
      tutorial.md
```

If you have any data or images that you would like to add to the tutorial, please place them in the tutorial directory.

#### **Formatting tutorial content**

This section outlines the standardized components used to structure tutorial content, including instructional boxes and image handling.

##### **Boxes**

To enhance the learning experience, tutorials use a set of predefined "boxes" implemented via styled blockquotes. These visually distinguish different types of content such as tasks, explanations, tips, and assessments.

Example: Question and Solution Box
```markdown
> <question-title>Questions</question-title>
> 1. Question 1
> 2. Question 2
>  
> > <solution-title>Answers</solution-title>
> > 1. Answer 1
> > 2. Answer 2
> > 
> {: .solution}
>
{: .question}
```

This structure creates a nested box where solutions are revealed within the question block:
> <question-title>Questions</question-title>
> 1. Question 1
> 2. Question 2
>  
> > <solution-title>Answers</solution-title>
> > 1. Answer 1
> > 2. Answer 2
> > 
> {: .solution}
>
{: .question}

Box titles are defined using a custom HTML-like tag structure, such as <question-title>Your question title</question-title>, where the tag name specifies the box type and the enclosed text defines the displayed title.

The following boxes are available and should be used consistently:
* `{: .overview}` summaries
* `{: .key_points}` take-home messages
* `{: .tip}` practical advice or shortcuts
* `{: .warning}` important cautions
* `{: .comment}` explanatory notes
* `{: .hands_on}` or `{: .hands-on}` exercises or tasks
* `{: .question}` assessment questions
* `{: .solution}` answers to questions
* `{: .details}` supplementary information
* `{: .feedback}` learner feedback prompts
* `{: .code-in}` input code blocks
* `{: .code-out}` output or results

Foldable box types (`solution`, `tip`, `comment`, `details`) allow you to show or hide the content on the same page. The title line of these boxes is always visible, making it easier to scan long explanatory boxes and reducing visual overload in tutorials.

> <hands-on-title>Tasks</hands-on-title>
> 1. Create each box and see how it looks.
> 2. Create one with a nested box.
> 
{: .hands_on}

Usage examples:

> <hands-on-title>Tasks</hands-on-title>
> 1. List of tasks
> 2. ...
> 
{: .hands_on}

> <details-title>Details</details-title>
> Here put some text...
> 
{: .details}

> <tip-title>Tip</tip-title>
> Here put some useful information...
> 
{: .tip}

> <comment-title>Comment</comment-title>
> Here put some comments...
> 
{: .comment}

> <code-in-title>Code In</code-in-title>
> ```bash
> ls -lh
> ```
>
> ```python
> import pandas as pd
> ```
> 
{: .code-in}

> <code-out-title>Code Out</code-out-title>
> ```bash
> # code output
> ```
> 
{: .code-out}

> <question-title>Questions</question-title>
> 1. Question 1
> 2. Question 2
>  
> > <solution-title>Answers</solution-title>
> > 1. Answer 1
> > 2. Answer 2
> > 
> {: .solution}
>
{: .question}

##### **Working with images**

Images must be referenced using the `relative_url` filter:
```
![figure-title]({{ "/tutorials/<tutorial-folder>/<image-folder>/<image>" | relative_url }}){: .responsive-img }
```
* `![figure-title]()` this is standard Markdown image syntax. The text inside the brackets (`figure-title`) becomes the **alt text**, which improves accessibility and is displayed if the image fails to load.
* `{{ "/path/to/image" | relative_url }}` the `relative_url` ensures that the correct `baseurl` defined in `_config.yml` is automatically prepended. This prevents broken links when the site is hosted in a subdirectory.
* `{: .responsive-img }` CSS class ensures that images do not exceed content width and scale proportionally on smaller screens.

> <details-title>Additional resources</details-title>
> If you need an additional materials to learn how to format the tutorial content, *i.e.* to wrap parts of the text in the special block quotes, please refer to the Software Carpenters' [Formatting episode.](https://carpentries.github.io/lesson-example/04-formatting/index.html#special-blockquotes){:target="_blank"}
> 
> Please also refer to the [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet){:target="_blank"} to learn more how to use Markdown.
> 
{: .details}

### Supporting multiple versions
If your tutorial exists in multiple versions (e.g., adapted for different audiences or events), organize them using version-specific subdirectories:
```
_tutorials/<tutorial-name>/
  main/
    tutorial.md
  summer-school/
    tutorial.md
```

Each version should be self-contained or consistently structured using `include`.

### Assigning tutorial to a group
Tutorials are categorized into thematic groups (e.g., Unix, Metagenomics) for navigation and discoverability.
To register your tutorial:
* add the exact folder name (e.g., `intro-python`) to the `_data/tutorial_groups.yml` file
* place it under an appropriate existing group

If no suitable group exists:
* create a new group entry with a clear and concise description, or
* temporarily assign the tutorial to the **incubator** group. Final group placement may be reviewed and adjusted by the editorial board.

### Submit tutorial
Once your tutorial is ready to publish, create a new branch, commit your changes, submit a pull request for review. 
You may optionally [open an issue](https://github.com/deKCD/Training-Materials/issues){:target="_blank"} to describe your contribution before or alongside your pull request.

### Registering material in TeSS

If all the required metadata fields are completed correctly, tutorials can be registered in [TeSS](https://tess.elixir-europe.org/){:target="_blank"} with minimal additional effort. Using the [Bioschemas TrainingMaterial Profile](https://bioschemas.org/profiles/TrainingMaterial/1.0-RELEASE){:target="_blank"} ensures the metadata is machine-readable and interoperable, enabling automated harvesting, improving discoverability, and supporting seamless integration into the ELIXIR training ecosystem without manual curation.

## Create a new learning pathway
------------------------------------
Learning pathwayss organize multiple tutorials into coherent, structured curricula. Each pathway defines a sequence of modules, where each module groups related tutorials under a shared theme.

To define a new pathway create a markdown file named `<pathway_title>.md` and place it in the `_pathways` directory. 

Each pathway file must include YAML front matter describing its structure, modules, and associated tutorials.

Template:
```markdown
---
layout: pathway
title: Title of the Learning Pathway
description: A concise summary of the pathway’s scope and objectives.
tags: [a list of keywords]
pathway:
  - section: "Module 1: The module title"
    description: A short explanation of the module’s focus
    tutorials:
      - name: tutorial name
        version: main

  - section: "Module 2: The module title"
    description: A short explanation of the module’s focus
    tutorials:
      - name: another tutorial
        version: main
editorial_board:
  - name: contributor Name
    orcid: contributor ORCID
---
```

The `layout` field must be set to `pathway` to ensure correct rendering of the pathway page. Each tutorial entry must include `name` (which must exactly match the corresponding tutorial folder name) and `version` (selected from the available versions of that tutorial).

After defining the pathway, create a new branch, commit the pathway file, and submit a pull request for review.