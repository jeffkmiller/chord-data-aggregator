# chord-data-aggregator

Repository for ISMIR2020 Late Breaking Demo

    A DATA-CLEANSING FRAMEWORK FOR AGGREGATING ANNOTATED DATASETS FROM MIREX AUTOMATED CHORD ESTIMATION ARCHIVES
    Jeff Miller    Johan Pauwels    Mark Sandler
    Centre for Digital Music, Queen Mary University of London
    {j.k.miller, j.pauwels, mark.sandler}@qmul.ac.uk
     
    ABSTRACT
    Identification and availability of suitable data sources is a well-known difficulty in music information retrieval re-search. For studies requiring annotated data, this can be compounded by inconsistent presentation formats, differ-ences in methodologies, and annotation errors. By build-ing a framework to apply automated data cleansing and standardization techniques to a collection of MIREX evaluation output data, we were able to extract a large, labelled chord data set for use in a harmonic modelling study. 

IMPORTANT: This repository does not include the MIREX ACE (Automation Chord Estimation) challenge data. The source data can be downloaded from https://github.com/ismir-mirex/ace-output. The entire ace-output-master directory and its contents must be placed within the ./source_data folder of the local chord-data-aggregator instance.

Purpose:
Chord aggregator collects chord annotation from the MIREX ACE (Automated Chord Estimation) output archives.
It selects the relevant files, removes duplicates, standardizes the musical representation of the contents, and displays the estimations
in regular intervals, allowing side by side comparison of the results.

Output:
a) Multiple outputs for chord estimations of a given recording are written to a csv file in time-aligned columns.
b) An index file containing details of the chord annotation source file for each column.

Usage:
To run the script:
1) Install the files and the included empty directory structure into an empty directory,
which can have any name.
2) At a terminal, set your working directory to the ./code directory of the installation.
3) Type "python collect_files.py YOURSEARCHTEXT" (note: replace YOURSEARCHTEXT with the filename text you are searching for.

Current limitations:
Currently, only a single recording can be harvested at a time, based on file title.
Future improvements will include the ability to harvest and aggregate chord labels from multiple recordings.
