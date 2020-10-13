
import os
import pandas as pd
import csv


def createDataFrame(filename):
    ## Create dataframe for data
    datacolumnname = getDataColumnName(filename)
    colnames = ['timeframe',datacolumnname]
    # print("CWD is " + os.getcwd())
    mydataframe = pd.read_csv(filename, names=colnames, header=None)
    return mydataframe

def getDataColumnName(filename):
    oldmaxkey = max(dataColumnNames.keys())
    colName = oldmaxkey + 1
    dataColumnNames[colName] = filename
    return colName

def addColumnData(chorddataframe, newdatafilename):
    newdata = createDataFrame(newdatafilename)
    try:
        coldata = newdata[newdata.columns[-1]]
        newcolumnname = newdata.columns.values[-1]
        chorddataframe.insert(len(chorddataframe.columns), newcolumnname, coldata, allow_duplicates=True)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    return chorddataframe

def compileFileList(sourcefilepath):
    fullfilelist = os.listdir(sourcefilepath)
    filelist = []
    for filename in fullfilelist:
        if filename.endswith(".csv"):
            filelist.append(filename)
    filelist.sort()
    return filelist

def aggregateChordFiles(sourcefilepath):
    # print(os.getcwd())

    filelist = compileFileList(sourcefilepath)
    workdata = createDataFrame(sourcefilepath + filelist[0])
    for filename in filelist[1:]:
        if filename.endswith('.csv'):
            workdata = addColumnData(workdata, sourcefilepath + filename)  # add the new column to the dataframe
    ##  Save result to file in output (analysis, aka workdir) folder
    workdata.to_csv('aggregated_chord_labels.csv', encoding='utf-8', index=False)
    ##  Save filename index to csv file, ordered by key (columnname) ascending
    with open('column_source_index.csv', 'w', newline='') as csvfile:
        for colname in dataColumnNames:
            print(colname, dataColumnNames[colname])
            csvfile.writelines(str(colname) + ',' + dataColumnNames[colname] + '\n')
    print('Aggregated chord dataframe and source index files created.')

dataColumnNames = {0: 'timeframe'}
