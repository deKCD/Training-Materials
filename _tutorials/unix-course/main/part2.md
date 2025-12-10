### **Part 2**

#### **07 - Extracting data from text files**

Let's extract adverbs from a list of English words available inside `/usr/share/dict/words`.

For this we need to install a small ubuntu package that contains english and german dictionary words.
Installing packages in ubuntu is fairly easy and can be done using the `apt-get install` command. However, we need root priviliges to install a package for the whole system.
This can be done by granting ourself root priviliges for the execution of one single command with `sudo`. 
Please run the following command before we can proceed:

```bash
sudo apt-get install wamerican-small
```

> ## Tasks
> 1. Please move to your home directory. *(1 command)*
> 2. Now create a directory called `fun_with_words` and enter the new directory. *(2 commands)*
> 3. Filter the English words list for words ending in _…fully_ and save them to a file named `fully.txt` using the command below. The `$` sign inside the search string ensures that only word endings are matched.
> 4. Take a look at the contents of `fully.txt`. _(1 command)_
> 5. Repeat the same for the words ending in _…ously_ as well as _…ably_ and save them to their corresponding files. *(2 commands)*
> 6. Calculate the word counts of all three files. *(1 command)*
>
> > ## Solution
> > ```bash
> > cd ~
> > mkdir fun_with_words
> > cd fun_with_words
> > grep "fully$" /usr/share/dict/words > fully.txt
> > less fully.txt
> > grep "ously$" /usr/share/dict/words > ously.txt
> > grep "ably$" /usr/share/dict/words > ably.txt
> > wc ably.txt fully.txt ously.txt
> > ```
> {: .solution}
>
{: .hands_on}

#### **08 - Processing the extracted data**

> ## Tasks
> 1. Convert all the adverbs inside the three files from the previous section into adjectives. Name the resulting files `able.txt`, `ful.txt` and `ous.txt` _(3 commands)_
>
>    | adverb | adjective |
>    | ------ | --------- |
>    | …ably  | …able     |
>    | …fully | …ful      |
>    | …ously | …ous      |
>
> 2. Concatenate the contents of `able.txt`, `ful.txt` and `ous.txt` into a single file called `adjectives.sorted.txt`. Sort the lines alphabetically before saving. _(2 commands with a pipe in between)_
> 3. Take a look at the results. _(1 command)_
>
> > ## Solution
> > ```bash
> > sed 's/ably/able/' ably.txt > able.txt
> > sed 's/fully/ful/' fully.txt > ful.txt
> > sed 's/ously/ous/' ously.txt > ous.txt
> > cat able.txt ful.txt ous.txt | sort > adjectives.sorted.txt
> > less adjectives.sorted.txt
> > ```
> {: .solution}
>
{: .hands_on}

#### **09 - Downloading and compressing files**

There are two common command-line programs for downloading data from the Web: `wget` and `curl`. Both of them are similar in basic functionality, but with some differences. 


One can compress/decompress files in place:
> ```bash
> gzip infile
> gunzip infile
> ```

Alternatively, both `gzip` and `gunzip` can output their results to standard out using `-c` flag:

> ## Tasks
> 1. Please move to your home directory. *(1 command)*
> 2. Now, download the file at [seqs.fasta](https://openstack.cebitec.uni-bielefeld.de:8080/unix-course/seq.fasta) to the current directory using a network downloader. *(1 command)*
> 3. Take a look at the contents of the file. *(1 command)*
> 4. The downloaded file is an uncompressed text file of 30 Kilobytes in size. Please apply compression to the file so that it takes less disk space and check the effectiveness of the compression. *(2 commands)*
>
> > ## Solution
> > ```bash
> > cd ~
> > wget "https://openstack.cebitec.uni-bielefeld.de:8080/unix-course/seq.fasta"
> > less seq.fasta
> > gzip seq.fasta
> > ls -l seq.fasta.gz
> > ```
> {: .solution}
>
{: .hands_on}

#### **10 - Cleaning up**

> ## Tasks
> 1. Please enter your home and list its contents. *(2 commands)*
> 2. Please list the contents of the directory `fun_with_words` without moving into it. *(1 command)*
> 3. Now, delete all the files inside the directory `fun_with_words`. *(1 command)*
> 4. Delete the directory itself. *(1 command)*
> 5. The directory `pi_calculation` has to be cleaned up as well. This time, delete directory and contents in one go. *(1 command)*
> 6. Verify that both directories have been removed. *(1 command)*
> 7. Remove the compressed text file. *(1 command)*
> 8. That's it! Congratulations! You have mastered the Unix command-line essentials!
> 
> > ## Solution
> > ```bash
> > cd ~
> > ls
> > ls fun_with_words
> > rm fun_with_words/*
> > rmdir fun_with_words
> > rm -r pi_calculation
> > ls
> > rm seq.fasta.gz
> > ```
> {: .solution}
>
{: .hands_on}