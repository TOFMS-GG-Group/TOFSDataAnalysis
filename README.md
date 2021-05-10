# TOFSDataAnalysis Project

WHAT IS THIS?
-------------

This application is for preforming data analysis on time of flight mass spectrometery. Please refer to wiki to see throught explantion of the project and design goals.

FILES NEEDED FOR THIS PROCESS
-----------------------------

1. ```SIS.json``` this is all the data related single ion signal from your Inductively Coupled Plasma Time-of-Flight Mass Spectrometer (ICP-TOFMS). 
2. ```Data.h5``` this file may be named differntly but this the file containing all the data from your Spectrometer.

HOW TO USE THIS
---------------
If you already have a input.json file refer to step 14.

1. Follow the instruction above creating the files need to start the operation.
2. Run `pip install -r requirements.txt` to install dependencies.
3. Run 'python app.py' in the folder src/edu/iastate/tofmsdataanalysis/application.
4. Enter the alpha values as a comma seperated string.
5. Enter the Number of Ions.
6. Enter the Isotope Mapping e.g. `Ti:47Ti,49Ti` please note that make sure there are no spaces or extra new lines and make sure there is one mapping per line.
7. Enter the rate minimum and maximum.
8. Enter the nominal mass a comma seperated string.
9. Enter the SIS.json file path.
10. Enter the Signal file path e.g. Data.h5.
11. Enter the Cache file path. If you don't have one this is where it will be and its name.
12. Enter the Output file path location this is where files will be dumped to.
13. Then click Compute Critical Values then the results will be stored in the cachce folder as well as outputed to the command line. This step will also generate a input.json in the output folder.
14. If you already have a input.json file generated from the previous step or hand crafted put the location of the file in output file path and click Load and Compute.


DEVELOPMENT
-----------

If you want to work on this application we’d love your pull requests and tickets on GitHub!

1. If you open up a ticket, please make sure it describes the problem or feature request fully.
2. Please thoroughly test your feature of bug fix.

CREDITS
-------

Tyler Jaacks <tjaacks@iastate.edu> or <tylerjaacks@gmail.com>

Alexander Gundlach-Graham <alexgg@iastate.edu>

[Single-particle ICP-TOFMS with online microdroplet calibration for the simultaneous quantification of diverse nanoparticles in complex matrices](https://pubs.rsc.org/en/content/articlelanding/2019/en/c9en00620f#!divAbstract)

[Monte Carlo Simulation of Low-Count Signals in Time-of-Flight Mass Spectrometry and Its Application to Single-Particle Detection.](https://www.ncbi.nlm.nih.gov/pubmed/30240561)


