### **Part 3: Advanced Concepts**

#### **11 - Edit files**

Instead of using a graphical user interface for editing files,
you can directly manipulate files on the terminal.

> ## Tasks
> 1. Please move to your home directory. *(1 command)*
> 2. Download the sars-cov-2 genome again ([sars-cov-2-seq](https://openstack.cebitec.uni-bielefeld.de:8080/unix-course/seq.fasta)). *(1 command)*
> 3. Open the file in an editor. *(1 command)*
> 4. Remove all characters from the first line with the exception of the fasta id (>NC_045512.2). *(typing/removing text)*
> 5. Save the file and exit the editor. *(1 key combination and 2 keys)*
> 6. Output just the first 10 lines to ensure that the fasta header contains only the id now. *(1 command)*
>
> > ## Solution
> > ```bash
> > cd ~
> > wget "https://openstack.cebitec.uni-bielefeld.de:8080/unix-course/seq.fasta"
> > nano seq.fasta
> > # Moving the caret and pressing backspace to remove the characters
> > # Ctrl+x, then type y to save the buffer and press enter to confirm the filename
> > head seq.fasta
> > ```
> {: .solution}
>
{: .hands_on}