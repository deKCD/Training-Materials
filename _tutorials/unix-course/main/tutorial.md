---
layout: tutorial_hands_on
title: Introduction to basic Unix commands
description: "This is the introduction to the basic shell commands."
slug: unix-course
time_estimation: 2H
questions:
  - "What is a command shell and why would I use one?"
  - "How can I move around on my computer?"
  - "How can I see what files and directories I have?"
  - "How can I specify the location of a file or directory on my computer?"
objectives:
  - "Describe key reasons for learning shell."
  - "Navigate your file system using the command line."
  - "Access and read help files for `bash` programs and use help files to identify useful command options."
  - "Demonstrate the use of tab completion, and explain its advantages."
key_points:
  - "The shell gives you the ability to work more efficiently by using keyboard commands rather than a GUI."
  - "Useful commands for navigating your file system include: `ls`, `pwd`, and `cd`."
  - "Most commands take options (flags) which begin with a `-`."
  - "Tab completion can reduce errors from mistyping and make work more efficient in the shell."
version:
  - main
life_cycle: "beta"
contributions:
  authorship:
  - Christian Henke
  - Peter Belmann
  - Jan Krueger
  - Nils Hoffmann
  - Sebastian Juenemann
  - Viktor Rudko
  editing: 
  funding:
---

This tutorial will help you develop proficiency in the necessary Unix shell concepts.

## What is a command shell?

On Unix, every user has a unique user name. When they log onto the system, they are placed in a home directory, which is a portion of the disk space reserved just for them. When you log onto a Unix system, your main interface to the system is  called the Unix Shell. This is the program that presents you with the dollar sign (`$`) prompt. This prompt means that the shell is ready to accept your typed commands. It is often preceded by the user name as well as the current directory.

Unix commands are strings of characters typed in at the keyboard. To  run a command, you just type it in and press the *Enter* key. We will look at several of the most common commands below.
Commands often have _parameters_, e. g. a file to work on. These are typed in after the command and are separated by spaces, e. g. `less pi_results.txt` opens the file `pi_results.txt` for reading.
 
In addition, Unix extends the power of commands by using special flags or *switches*. Switches are usually preceded with a dash (`-`), e. g. `ls -lh`.

> ## List of commands
> 
> | Command             | Description                                                  |
> | ------------------- | ------------------------------------------------------------ |
> | `pwd`               | print current (working) directory            |
> | `ls`                | list contents of the current directory                       |
> | &#10551; `-l`    | **l**ong (detailed) listing |
> | &#10551; `-h` | with **h**uman readable numbers |
> | `cd`                | change to another directory                                  |
> | `mkdir`             | make a new directory                                         |
> | `mv`                | move or rename a file or directory                           |
> | `cp`                | copy file                                                    |
> | &#10551; `-r`       | copy directory tree (**r**ecursively)                        |
> | `file` | determine file type |
> | `echo`              | print a line of text                                   |
> | `head`              | View the first 10 lines of a file |
> | `sort`              | Sort lines of text files |
> | `less`              | display contents of a file (press q to quit)                 |
> | `tail` | output the last part of a file |
> | &#10551; `-f` | **f**ollow appended data as the file grows |
> | `grep`              | list text lines containing a particular string of text |
> | &#10551; `-v` | output only non-matching lines |
> | `wc` | count lines, words, and bytes in a file |
> | `cat`               | concatenate (combine) two or more files                      |
> | `df`                | show disk free information                                   |
> | &#10551; `-h` | with **h**uman readable numbers |
> | `find`              | find files in a directory tree                               |
> | `man`               | display program manual for a command                         |
> | `ps -x`         | list one's own running programs / processes (e**x**tended list) |
> | `kill`              | kill process                                                 |
> | &#10551; `-9`       | kill process immediately (SIGKILL=**9**)           |
> | `rm`                | remove a file                                                |
> | &#10551; `-r`       | remove a directory tree (**r**ecursively)                    |
> | `rmdir`             | remove an empty directory                                    |
> | `chmod`             | change mode (security permissions) of file or directory      |
> | &#10551; `ugo+-rwx` | **u**ser (owner), **g**roup, **o**ther (world), add(**+**), remove(**-**), **r**ead, **w**rite, **e**xecute |
> | `./myprogram` | run the local executable file `myprogram` |
> | `sed 's/ab/cd/'` | transform text, e. g. replace all occurrences of 'ab' with 'cd' |
> | `nano` | Command line text file editor | 
> | &#10551; `Ctrl-x`       | By using the key combination `Ctrl-x` in the editor, you can exit the editor and optionally save the file.|
> | `wget` | network downloader (downloads files from the Web) |
> | `gzip` | compress a file |
> | `gunzip` | uncompress a file |
> | `*`                 | wildcard representing any combination of characters          |
> | **Places** |  |
> | `~`                 | your home directory                                          |
> | `.`                 | current directory                                            |
> | `..`                | parent directory                                             |
> | **Pipes** |  |
> | `>`                 | send output to a file                                        |
> | `>>`                | append (add) output to a file                                |
> | `\|`                 | pipe output from one command as input to another             |
>
> Download as [PDF](/tutorials/unix-course/main/data/cheatsheet.pdf) or separate [MarkDown](/tutorials/unix-course/main/data/cheatsheet.md).
> 
{: .details}


## **Tutorial**

During this tutorial you will use many of the **commands above**. Your task is to **identify** 
**the correct commands and execute them**. Feel free to experiment. Take a look at the 
solution if absolutely necessary.

This tutorial is based on the [tutorial](https://gitlab.ub.uni-bielefeld.de/denbi/unix-course) that was created by the de.NBI Cloud Bielefeld administrators.
The first two sections (01 and 02) describe how to access the workshop environment for this tutorial.
Participants need a web browser and an active ELIXIR account. 

{ % include _tutorials/unix-course/main/part1.md %}

{ % include _tutorials/unix-course/main/part2.md %}

{ % include _tutorials/unix-course/main/part3.md %}




