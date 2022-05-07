# GUI-for-barrnap

This graphical  user interface (GUI) for [barrnap program](https://github.com/tseemann/barrnap), BAsic Rapid Ribosomal RNA Predictor, was created as python project for the python course in [Bioinnformatics Institute](https://bioinf.me/en) 2021-2022. 

The goal of the project was to produce a simple graphical interface for any command-line bioinformatical tool. We chose to work with barrnap, because it has a limited amount of options, it can be run on a small data on a normal laptop (unlike e.g. genome assembler) and its output is a simple text (gff) file. 

We used the [PySimpleGUI library](https://pysimplegui.readthedocs.io/en/latest/) to create the GUI. 

### Why use barrnap GUI? 

1) Our graphical interface allows to predict ribosomal RNAs through barrnap even for the people who are not familiar with the command line: chose file from files browser, run the script by pressing 'submit buttons', etc. 
2) To allow the user to blast the hits immidiately, we added the output in fasta format.
3) One of the problems of using GUIs is that it's hard to reproduce; for this purpose, we added detailed log files that are written automatically in the `barrnap_logs` folder and contain not only barrnap native log, but also the working directory and time of running the script. 

### What exactly does barrnap do? 

From the barrnap manual: 

> Barrnap predicts the location of ribosomal RNA genes in genomes. It supports bacteria (5S,23S,16S), archaea (5S,5.8S,23S,16S), metazoan mitochondria (12S,16S) and eukaryotes (5S,5.8S,28S,18S). It takes FASTA DNA sequence as input, and write GFF3 as output. It uses the new nhmmer tool that comes with HMMER 3.1 for HMM searching in RNA:DNA style. Multithreading is supported and one can expect roughly linear speed-ups with more CPUs.

## Installation

### Requirements

GUI requirements:
 - Linux of Mac command-line (it is possible to run on Windows with WSL istalled)
 - Python3
 - conda 

Barrnap requirements: 
 - Perl 5.xx (core modules only)
 - nhmmer (part of HMMER 3.x)
 - bedtools >= 2.27.0

The script should install all the libraries and barrnap program automatically. However, if you encounter a problem with the installation, you may want to install them manually: 

`conda install -c bioconda -c conda-forge barrnap`

`pip3 install loguru`

`pip3 install pysimplegui`

### Downloading 

You can download all the files you need to launch barrnap GUI from our github: 

`git clone https://github.com/alvlako/GUI-for-barrnap.git`

or 

`wget https://github.com/alvlako/GUI-for-barrnap.git`

You can also download `.zip` archive from our github by pressing 'Code' > 'Download zip'

### Installing 

#### Mac and Linux 

To install on Mac or Linux, simply run the '.exe' file. It should install all the dependencies automatically. 

#### Windows 

We do not recommend using GUI-for-barrnap on Windows. If, however, you have an unbearable, pressing desire to use GUI-for-barrnap on Windows, you may try the following: 

Install Windows Subsystem for Linux. 

Install wsl graphical inteface: 

1) Go to https://sourceforge.net/projects/vcxsrv/, download the program and install it on Windows (by executing vcxsrv-64.1.20.14.0.installer.exe file). 
You should see the icon of xLaunch on your desktop or access it through the start menu. 
2) Launch XLaunch. Choose "One Large Window", "Start No Client", check the "Disable access control" option. You should see big black window appear. 

Now, go to wsl command line. Make sure you are using bash shell (you may need to type 'bash' if your default shell is fish). 
You may want to activate conda or virtualenv virtual environment. 

You need install xfce4: 

```
sudo apt-get install xfce4
cd ~
nano .bashrc
```
Now, as a last line of the opened file, write `export DISPLAY=:0.0`

Exit wsl and run it again (again, you may need to type 'bash' if your default shell is fish, and if you were using the virtual env, you need to activate it). 
To check that  xfce4 works, try running

```
startxfce4
```
If the black screen changes to sort of 'Desktop', you are good to go! 

You may need to install barrnap: 

```
conda install -c bioconda -c conda-forge barrnap 
```

Now you can load GUI_barrnap_log.py. 
Open new wsl window, go to the directory with GUI_barrnap_log.py, make sure you are in the same shell and env where you installed all the dependencies. 

Run:

```
python GUI_barrnap_log.py
```
Inside the XLaunch Desctop, you should see the window with the barrnap options!

## Usage 

To launch the script, open the `barrnap_final` file or type 
`python GUI_barrnap.py`

The window with barrnap options will appear. 
Choose your fasta file with the sequence where you want to find rRNAs (you can try our `GCF_000005845.2_ASM584v2_genomic.fna` example file!). 
Choose where you want to save the fasta file with found rRNAs. 
Then, choose the kingdom (bac, mito, arc or euk), number of threads, length cutoff, value at which the program should reject genes as too short, and e-value. You can see the detailed description of the options by pressing "HELP" button. 

Then, press the `Submit` button or just hit `Enter` on your keyboard. Barrnap will run automatically! 

You will see the window with the log file appear. Here, you can choose where to save your resulting gff file. Press `save` to actually save the file. Then, press `Exit` and close the first window by pressing the red cross in the upper right corner.

The resulting files are a fasta file with rRNAs and a gff file with their coordinates. 

All the log files are also saved in the barrnap_logs folder, which is creared automatically. The example of a barrnap log `barrnap_log_file_2022-05-06_21-05-55.log`: 

```
2022-05-06 at 21:05:55 | INFO | All the packages are installed
2022-05-06 at 21:05:55 | INFO | Barrnap is checked
2022-05-06 at 21:06:08 | INFO | Working directory: /mnt/c/Users/emeli/Documents/bioinfme/python/pyproject/GUI-for-barrnap
2022-05-06 at 21:06:08 | INFO | Input file that will be used: /mnt/c/Users/emeli/Documents/bioinfme/python/pyproject/mito.fna
2022-05-06 at 21:06:08 | INFO | Barrnap was called with the following arguments:
 barrnap /mnt/c/Users/emeli/Documents/bioinfme/python/pyproject/mito.fna --kingdom mito --outseq rRNA.fasta --threads 1 --outseq rRNA.fasta --lencutoff 0.8 --outseq rRNA.fasta --reject 0.25 --outseq rRNA.fasta --evalue 1e-06 --outseq rRNA.fasta
2022-05-06 at 21:06:08 | INFO | [barrnap] This is barrnap 0.9
[barrnap] Written by Torsten Seemann
[barrnap] Obtained from https://github.com/tseemann/barrnap
[barrnap] Detected operating system: linux
[barrnap] Adding /home/vera/miniconda3/lib/barrnap/bin/../binaries/linux to end of PATH
[barrnap] Checking for dependencies:
[barrnap] Found nhmmer - /home/vera/miniconda3/bin/nhmmer
[barrnap] Found bedtools - /home/vera/miniconda3/bin/bedtools
[barrnap] Will use 1 threads
[barrnap] Setting evalue cutoff to 1e-06
[barrnap] Will tag genes < 0.8 of expected length.
[barrnap] Will reject genes < 0.25 of expected length.
[barrnap] Using database: /home/vera/miniconda3/lib/barrnap/bin/../db/mito.hmm
[barrnap] Scanning /mnt/c/Users/emeli/Documents/bioinfme/python/pyproject/mito.fna for mito rRNA genes... please wait
[barrnap] Command: nhmmer --cpu 1 -E 1e-06 --w_length 3878 -o /dev/null --tblout /dev/stdout '/home/vera/miniconda3/lib/barrnap/bin/../db/mito.hmm' '/mnt/c/Users/emeli/Documents/bioinfme/python/pyproject/mito.fna'
[barrnap] Found: 12S_rRNA gi|13272612|gb|AF346967.1| L=948/954 649..1596 + 12S ribosomal RNA
[barrnap] Found: 16S_rRNA gi|13272612|gb|AF346967.1| L=1544/1585 1676..3219 + 16S ribosomal RNA
[barrnap] Found 2 ribosomal RNA features.
[barrnap] Sorting features and outputting GFF3...
[barrnap] Writing hit sequences to: rRNA.fasta
[barrnap] Running: bedtools getfasta -s -name+ -fo 'rRNA.fasta' -fi '/mnt/c/Users/emeli/Documents/bioinfme/python/pyproject/mito.fna' -bed '/tmp/pv04lNYzvn'
[barrnap] Done.

2022-05-06 at 21:06:08 | INFO | Elapsed time (h:mm:ss): 0:00:00.333592
2022-05-06 at 21:06:08 | INFO | Work finished
2022-05-06 at 21:06:08 | INFO | 

    Seemann T
    barrnap 0.9 : rapid ribosomal RNA prediction
    https://github.com/tseemann/barrnap

    Graphical user interface (GUI) for Barrnap was created as Bioinformatics Institute student project
    https://github.com/alvlako/GUI-for-barrnap

    Thank you and wellcome to Barrnap GUI!
    
2022-05-06 at 21:06:11 | INFO | Application has completed its work. Have a nice day!
```

## Available 

![image](https://user-images.githubusercontent.com/56854264/167154394-d65e3c21-abfe-4f73-80ae-fbb34575f697.png)
![image](https://user-images.githubusercontent.com/56854264/167154476-a7575769-f27f-4a6b-a743-796ce24a1a05.png)
![image](https://user-images.githubusercontent.com/56854264/167154802-ed2584ac-e3bb-43b9-ba3b-618cd842e1ab.png)

## Contributors

- Mikhail Fofanov [@MVFofanov](https://github.com/MVFofanov)
- Alexandra Kolodyazhnaya [@alvlako](https://github.com/alvlako)
- Vera Emelianenko [@Vera-Emelianenko](https://github.com/Vera-Emelianenko) 

## References 

We created the GUI for the barrnap program. 

If you use Barrnap in your work, please cite:

    Seemann T
    barrnap 0.9 : rapid ribosomal RNA prediction
    https://github.com/tseemann/barrnap

The GUI was created using [PySimpleGUI library.](https://pysimplegui.readthedocs.io/en/latest/) 

The test data (GCF_000005845.2_ASM584v2_genomic.fna) is taken from NCBI database: [Escherichia coli str. K-12 substr. MG1655 (E. coli) reference genome ](https://www.ncbi.nlm.nih.gov/data-hub/genome/GCF_000005845.2/). 

