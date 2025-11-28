### **Part 1**

#### **01 - Accessing SimpleVM**

When accessing a Unix system running as a virtual machine in the cloud one would normally log into it via **se**cure **sh**ell (`ssh`) and would be getting presented with a terminal. SSH also works with IP address, so you can specify the port with the flag `-p`. 
For the sake of this tutorial the access route to the terminal is via web browser.
Every participant has access to a prepared virtual machine running a web-based development environment called Theia IDE.

> ## Generate a new ssh key
> You can generate a new public/private SSH key pair on your local machine.
> 
> > ## Important
> > You can distribute your public key to other servers, but your private key must be kept secure and never shared.
> >
> {: .keypoints}
> 
> After you generate the key, you can add the public key (e.g. `KEY.pub`) to your account on GitHub.com to enable authentication for Git operations over SSH.
> ```bash
> ssh-keygen
> ```
> 
> This creates a new SSH key, using the provided email as a label.
> When you are prompted to "Enter a file in which to save the key", you can press Enter to accept the default file location.
> 
> Please note that if you created SSH keys previously, ssh-keygen may ask you to rewrite another key, in which case we recommend creating a custom-named SSH key.
> To do so, type the default file location and replace id_ALGORITHM with your custom key name.
> ```
> Enter a file in which to save the key (/home/YOU/.ssh/id_ALGORITHM):[Press enter]
> ```
> 
> At the prompt, type a secure passphrase.
> ```
> Enter passphrase (empty for no passphrase): [Type a passphrase]
> Enter same passphrase again: [Type passphrase again]
> ```
> 
{: .hands_on}

#### **Accessing Theia IDE**

This workshop is powered by [SimpleVM](https://cloud.denbi.de/about/project-types/simplevm/).
Every participant should have received a mail containing the actual link to their VM.
If you did not receive a mail containing a link to a VM, please contact your tutor.

After successful login the Theia IDE screen appears. The screen is usually divided into 3 sections:
Editor pane in the center, file browser on the left, terminal at the bottom.
This tutorial will primarily focus on the use of the terminal.

> ## Hands On: Access your private VM
> Access to your own private virtual machine works different from what is used here. You would usually run an SSH client to connect to the machine using a key file and would then be presented with a single terminal command prompt, e.g.:
> 
> > ## Code In
> > ```bash
> > ssh -i ~/.ssh/mykeyfile ubuntu@myprivatevm.example.com
> > ```
> {: .code-in}
> 
{: .hands_on}

#### **02 - Opening a terminal window**

If not yet open go to -> _Terminal_ -> _new Terminal_ to open a new terminal.

![Opening a terminal window](/tutorials/unix-course/images/Terminal.png){: .responsive-img }

It is possible to have more than one terminal open at the same time.

#### **03 - Creating a directory to work in**

Before we actually start clone this github repository so we have all files in place we need for this small exercise.

```bash
cd ~
git clone https://github.com/deNBI/unix-course.git
```

This will create the directory `unix-course` within your user's home directory.
We can now move on with the exercise.

> ## Taks
> 1. Open the manual page of the command `pwd` by entering `man pwd`.
> 2. Find out your current (working) directory. *(1 command)*
> 3. If your current directory is not your home directory, please move to it. *(1 command)*
> 4. Now create a directory called `pi_calculation` and enter the new directory. *(2 commands)*
> 5. Confirm that your current directory has changed. *(1 command)*
>
> > ## Solution
> > ```bash
> > pwd
> > cd ~
> > mkdir pi_calculation
> > cd pi_calculation
> > pwd
> > ```
> {: .solution}
> 
{: .hands_on}

#### **04 - Running a simple program**

A simple program that (slowly) approximates the number pi is available as a file at `~/unix-course/calculate_pi`.

> ## Tasks
> 1. Please copy this program into your current directory. *(1 command)*
> 2. Inspect the file you just copied to get information about its file type. *(1 command)*
> 3. Please make the file executable (for you as the owner only). *(1 command)*
> 4. Now run the executable and watch how the pi approximation gets better over time. *(1 command)*
> 5. Stop the running program by pressing the key combination `Ctrl+c`.
>
> > ## Solution
> > ```bash
> > cp ~/unix-course/calculate_pi .
> > file calculate_pi
> > chmod u+x calculate_pi
> > ./calculate_pi
> > ```
> {: .solution}
>
{: .hands_on}

#### **05 - Running in background and saving output**

We would like to save the results of the pi calculation program to a file instead of just displaying them on the screen.

> ## Tasks
> 1. Please run the pi executable again but this time send its output to a file called `pi_results.txt` in the same directory. *(1 command)*
> 2. Open a second terminal and enter a command that allows you to watch the output lines being written to the results file. **Note:** Bear in mind that a new terminal always starts in your home directory. *(2 commands)*
> 3. Stop following the results file. *(1 key combination)*
> 
> > ## Solution
> > ```bash
> > ./calculate_pi > pi_results.txt 
> > cd pi_calculation
> > tail -f pi_results.txt
> > # Ctrl+c
> > ```
> {: .solution}
>
{: .hands_on}

#### **06 - Inspecting and terminating a running program**

The pi approximation will probably run for about an hour but we would like to terminate it earlier.

> ## Tasks
> 1. List your own running programs. *(1 command)*
> 2. Use the process ID (PID) of the still running pi calculation to terminate it. The PID is in the first column of the program list. *(1 command)*
> 3. Verify that the pi calculation has stopped. *(1 command or action)*
> 4. Inspect the contents of the results file that the pi calculation has generated. *(1 command)*
> 5. Check the file size of the results file. *(1 command)*
> 6. Check the free disk space available on your file system. *(1 command)*
>
> 
> > ## Solution
> > ```bash
> > ps -x
> > kill <id of the process>
> > ps -x     # or look at the first terminal
> > less pi_results.txt
> > ls -lh
> > df -h .
> > ```
> {: .solution}
>
{: .hands_on}