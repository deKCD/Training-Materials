## List of commands

| Command             | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| `pwd`               | print current (working) directory            |
| `ls`                | list contents of the current directory                       |
| &#10551; `-l`    | **l**ong (detailed) listing |
| &#10551; `-h` | with **h**uman readable numbers |
| `cd`                | change to another directory                                  |
| `mkdir`             | make a new directory                                         |
| `mv`                | move or rename a file or directory                           |
| `cp`                | copy file                                                    |
| &#10551; `-r`       | copy directory tree (**r**ecursively)                        |
| `file` | determine file type |
| `echo`              | print a line of text                                   |
| `less`              | display contents of a file (press q to quit)                 |
| `tail` | output the last part of a file |
| &#10551; `-f` | **f**ollow appended data as the file grows |
| `grep`              | list text lines containing a particular string of text |
| &#10551; `-v` | output only non-matching lines |
| `wc` | count lines, words, and bytes in a file |
| `cat`               | concatenate (combine) two or more files                      |
| `df`                | show disk free information                                   |
| &#10551; `-h` | with **h**uman readable numbers |
| `find`              | find files in a directory tree                               |
| `man`               | display program manual for a command                         |
| `ps -x`         | list one's own running programs / processes (e**x**tended list) |
| `kill`              | kill process                                                 |
| &#10551; `-9`       | kill process immediately (SIGKILL=**9**)           |
| `rm`                | remove a file                                                |
| &#10551; `-r`       | remove a directory tree (**r**ecursively)                    |
| `rmdir`             | remove an empty directory                                    |
| `chmod`             | change mode (security permissions) of file or directory      |
| &#10551; `ugo+-rwx` | **u**ser (owner), **g**roup, **o**ther (world), add(**+**), remove(**-**), **r**ead, **w**rite, **e**xecute |
| `./myprogram` | run the local executable file `myprogram` |
| `sed 's/ab/cd'` | transform text, e. g. replace all occurrences of 'ab' with 'cd' |
| `wget` | network downloader (downloads files from the Web) |
| `gzip` | compress a file |
| `gunzip` | uncompress a file |
| `*`                 | wildcard representing any combination of characters          |
| **Places** |  |
| `~`                 | your home directory                                          |
| `.`                 | current directory                                            |
| `..`                | parent directory                                             |
| **Pipes** |  |
| `>`                 | send output to a file                                        |
| `>>`                | append (add) output to a file                                |
| `\|`                 | pipe output from one command as input to another             |