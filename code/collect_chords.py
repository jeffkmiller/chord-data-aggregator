""" Purpose:
    Chord aggregator collects chord annotation from the MIREX ACE (Automated Chord Estimation) output archives.
    It selects the relevant files, standardizes the formatting of the contents, and displays the estimations
    in regular intervals, allowing side by side comparison of the results.

    Output:
    a) Multiple outputs for chord estimations of a given recording are written to a csv file in time-aligned columns.
    b) An index file containing details of the chord annotation source file for each column included in a).

    Usage:
    To run the script:
    1) Install the files and the included empty directory structure into an empty directory,
    which can have any name.
    2) At a terminal, set your working directory to the ./code directory of the installation.
    3) Type "python collect_files.py <your case-sensitive filename search text>"

    Current limitations:
    1) Currently, only a single recording can be harvested at a time, based on file title.
    Future improvements will include the ability to harvest and aggregate chord labels from multiple recordings.
    2) If no instances of the filename search text are found, the program crashes. This will be corrected shortly.
"""


import os
import scelab_format as slf
import time_framer as tf
import remove_duplicates as rd
import data_file_handler as dfh


def removeWhitespace(inputString):
    outputString = inputString.replace(' ', '')
    return outputString

def stripFileNameExtension(filename):
    myFileName = os.path.splitext(filename)[0]
    return myFileName

def getBaseFileName(filename):
    workingFileName = filename.replace(sourceDirectory,'')
    workingFileName = workingFileName.replace('/','_')
    returnFileName = workingFileName.replace('._', '')
    return returnFileName

def createStandardChordFiles(chordfiles):
    counter = 0
    for filename in chordfiles:
        if os.path.splitext(filename)[1] != '.lab':
            continue
        else:
##          set file names
            basefilename = getBaseFileName(filename)
            cleanseddataname = stripFileNameExtension(basefilename) +  '.scf'
            outputfilename = stripFileNameExtension(basefilename) +  '.csv'

##          set file folders (i.e. paths to folders)
            cleansedFileFolder = workdir + cleansedpath
            outputFileFolder = workdir + outputpath

##          Assemble full  file  names and paths
            # print(os.getcwd())
            inputFilepath = filename ## relative path issue occuring here...
            cleansedFilepath = os.path.join(cleansedFileFolder, cleanseddataname)
            outputFilepath = os.path.join(outputFileFolder, outputfilename)

            slf.cleanChordDesc(inputFilepath, cleansedFilepath)
            tf.buildTimeFrame(cleansedFilepath, outputFilepath)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("searchtext", help="search for text in filename")
    args = parser.parse_args()

    ## Define environment variables and project file structure
    os.chdir('../')
    workdir = os.getcwd() + '/'

    ## Note: MIREX ACE data can be downloaded from https://github.com/ismir-mirex/ace-output
    sourceDirectory = 'source_data/ace-output-master/'
    inputpath = 'input/'
    cleansedpath = 'staging/cleansed_data/'
    outputpath = 'staging/time_standardized_data/'
    searchtext = args.searchtext
    # Define search text (i.e. song title) - uncomment for RDE testing
    # searchtext = 'Bohemian Rhapsody'

    ##  Remove duplicate files to prevent double counting of algorithm data
    distinctchordlist = rd.check_for_duplicates('.', workdir + sourceDirectory, searchtext)
    ##  Do the work: make the cleaned and time-aligned files
    createStandardChordFiles(distinctchordlist)
    os.chdir(workdir)
    ##  assemble standardized transcriptions into single dataframe and write to file
    dfh.aggregateChordFiles(workdir + outputpath)

    print("Finished creating de-duped, data-cleansed, time framed files.")
