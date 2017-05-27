Bachelor's final project

Topic: "Application of machine learning algorithms in music emotion recognition"

Dissertation available at: https://misio.fis.agh.edu.pl/media/misiofiles/162daeb54191392a9cc3090f8ce28f58.pdf


# eMusic - Project of neural networks system which recognise emotion of the given audio. #

**General**

Project uses Essentia library for audio content analysis available here:

http://essentia.upf.edu/

and 

https://code.google.com/p/neurolab/

for neural networks.

Since Essentia Python bindings are written in Python2.7 whole project is also writtent using Python2.7


**How to get?**

git clone http://www.bitbucket.org/pawellll/inz.git


**How to run?**

If you're using PyCharm, just open it and run the project in IDE.

If not, open terminal, run main.py, but remember that it should be done from level of main folder
of the project in order to have proper file paths to resources, otherwise it's not going to work.

**Options**

 usage: main.py [-h] [-a] [-t] [-p] [-e] [-s FILE] [-n N]

Emusic

Arguments:

*  -h, --help  show this help message and exit
*  -a          Analyse songs during program execution. Otherwise it's going to
              load already processed songs if exist
*  -t          Train neural network during program execution. Otherwise it's
              going to load ready neural network if exists
*  -p          Plot comparison of neural network recognition and expected
              results. Use only with -e
*  -e          Evaluate neural network
*  -s FILE     Flag allows to analyse one song which is loaded and then
              analysed by neural network if any exist. Should be used without
              any other argument
*  -n N        Set amount of hidden neurons in net. By default 30


# Resources #

Dataset used:
http://cvml.unige.ch/databases/emoMusic/

Resources folder contains:
* manual for data set which is used for developing and evaluating neural network
* documentation for Essentia library used in this project
* clips folder containing all audio files used in this project
* annotations folder containing information about songs and information about their valence and arousal parameters
