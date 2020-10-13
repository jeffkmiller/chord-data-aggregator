import os
from decimal import Decimal


def buildTimeFrame(inputFilepath, outputFilepath):
    with open(inputFilepath, 'r+') as fp:
        with open(outputFilepath, 'w+') as nf:
            for line in fp:
                linetext = line
                # read startnum, endnum
                parsedline = linetext.split('\t')
                startnum = Decimal(parsedline[0])
                endnum = Decimal(parsedline[1])
                chordlabel = parsedline[2]
                chordlabel = chordlabel[: chordlabel.find('\n')]  # remove newline control characters from chordlabel
                # round appropriately
                precision = 1  # set number of decimal places here
                startround = round(startnum, precision)
                endround = round(endnum, precision)
                # iterate from startnum to endnum - 1, write newline w/ chord label in suitable time increments (0.1 - 0.05 secs)
                for step in range(int(startround * 100), int(endround * 100), 10):
                    timestamp = step / 100
                    expandedlinetext = (str(timestamp) + ',' + chordlabel)
                    nf.writelines(expandedlinetext + '\n')



