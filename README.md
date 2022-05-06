# GUI-for-barrnap

This GUI for [barrnap program](https://github.com/tseemann/barrnap), BAsic Rapid Ribosomal RNA Predictor, was created as python project for python course in [Bioinnformatics Institute](https://bioinf.me/en) 2021-2022. 

The goal of the project was to produce a simple graphical interface for any command-line bioinformatical tool. We chose to work with barrnap, because it has a limited amount of options, it can be run on a small data on a normal laptop (unlike e.g. genome assembler) and its output is a simple gff file. 

Our graphical interface allows to predict ribosomal RNAs through barrnap even for the people who are not familiar with the command line: chose file from files browser, run the script by pressing 'submit buttons', etc. One of the problems of using GUIs is that it's hard to reproduce; for this purpose, we added detailed log files that are written automatically in the `barrnap_logs` folder and contain not only barrnap native log, but also the working directory and time of running the script. To allow the user to blast the hits immidiately, we added the output in fasta format.

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

The test data (GCF_000005845.2_ASM584v2_genomic.fna) is taken from NCBI database: [Escherichia coli str. K-12 substr. MG1655 (E. coli) reference genome ](https://www.ncbi.nlm.nih.gov/data-hub/genome/GCF_000005845.2/). 

