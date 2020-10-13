import os

intervalNotationFiles = []


def isChordNull(chordlabel):
    if chordlabel[0] == 'N' or chordlabel[0] == 'n':
        chordroot = 'NA'
        return chordroot

def getRoot(chordlabel):
    chordroot = ''
    for pitch in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        idx = chordlabel.find(pitch)
        if idx != -1:
            chordroot = pitch
            # handle sharps and flats
            if chordlabel[idx] != chordlabel[-1]:
                if (chordlabel[idx + 1] == 'b') or (chordlabel[idx + 1] == '#'):
                    chordroot = chordroot + chordlabel[idx + 1]
            return chordroot
    chordroot = 'X'
    return chordroot

def getType(croot, clabel):
    typetext = ''
    if clabel[-len(croot):] == croot:
        typetext = 'maj'
    if clabel.find(':') == clabel[-1]:
        typetext = 'maj'
    else:
        ## jkm: rewrite the logic of this stage to
        ##  a) reference expandable chord library (of weirder chords)
        ##  b) to prevent short circuiting or overwriting of chord type once coded -  (to improve on simple brute force find string approach)
        for chordtype in ['7', '9', 'maj', 'maj7', 'maj9', 'min', 'min7', 'min9', 'majmin7', 'dim', 'dim7', 'hdim', 'aug','sus']:
            typestartidx = clabel.find(chordtype)
            if typestartidx != -1:
                typetext = clabel[typestartidx:]
    # if clabel.find('(') != -1 or clabel.find(')') != -1:
    #     typetext = convertParentheticals(clabel)
    return typetext

def discardBass(chordlabel):
    bassfreelabel = chordlabel
    if chordlabel.find('/') != -1:
        bassfreelabel = chordlabel[:chordlabel.find('/')]
        return bassfreelabel
    return bassfreelabel

def standardizeRoot(croot, chordtype):
    if croot == 'Cb':
        return 'B'
    if croot == 'C#' and chordtype == 'maj':
        return 'Db'
    if croot == 'Db' and chordtype == 'min':
        return 'C#'
    if croot == 'D#':
        return 'Eb'
    if croot == 'E#':
        return 'F'
    if croot == 'Fb':
        return 'E'
    if croot == 'F#' and chordtype == 'maj':
        return 'Gb'
    if croot == 'Gb' and chordtype == 'min':
        return 'F#'
    if croot == 'G#' and chordtype == 'maj':
        return 'Ab'
    if croot == 'Ab' and chordtype == 'min':
        return 'G#'
    if croot == 'A#':
        return 'Bb'
    if croot == 'B#':
        return 'C'
    else: return croot

def removeParentheticals(chordlabel): ## warning: invalidates label sets using only long form chord factor notation
    myLabel = chordlabel
    openPar = myLabel.find('(')
    closePar = myLabel.find(')')
    if openPar != -1 and closePar != -1:
        if openPar < closePar:
            myLabel = myLabel[:openPar] + myLabel[closePar+1:]
    else:
        myLabel.replace('(','')
        myLabel.replace(')','')
    return myLabel

def convertParentheticals(chordlabel): ## converts label sets using only long form chord factor notation
    myLabel = chordlabel
    openPar = myLabel.find('(')
    closePar = myLabel.find(')')
    if openPar != -1 and closePar != -1:
        if openPar < closePar:
            parLabel = myLabel[openPar:closePar+1]
            return parentheticalToText(parLabel)
    else:
        myLabel.replace('(','')
        myLabel.replace(')','')
    return myLabel

def parentheticalToText(parLabel):
    if parLabel == '(3,#5)':
        return 'aug'
    if parLabel == '(3)' or parLabel == '(3,5)':
        return 'maj'
    if parLabel == '(3,b7)' or parLabel == '(3,5,b7)':
        return '7'
    ##  the order of the following 2 if statements is logically important
    if parLabel.find('(b3') != -1 and parLabel.find('9') != -1:
        return 'min9'
    if parLabel.find('9') != -1:
        return 'maj9'
    if parLabel == '(3,5,7)':
        return 'maj7'
    if parLabel == '(b3,5)':
        return 'min'
    if parLabel == '(b3,5,b7)':
        return 'min7'
    if parLabel == '(b3,5,7)':
        return 'majmin7'
    if parLabel == '(b3,b5)':
        return 'dim'
    if parLabel == '(b3,b5,6)':
        return 'dim7'
    if parLabel == '(b3,b5,b7)':
        return 'hdim'
    if parLabel.find('3') == -1 and (parLabel.find('9') or parLabel.find('4')):
        return 'sus'
    else:
        return 'NA'

def formatTime(timevalue):
    decimalidx = timevalue.find('.')
    standardTime = timevalue[:decimalidx + 3]
    return standardTime

def cleanChordDesc(inputFilepath, outputFilepath):
   with open(inputFilepath, 'r+') as fp:
        with open(outputFilepath, 'w+') as nf:
            rootnames = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
            for line in fp:
                linetext = line
                if linetext.find('\n') != -1:
                    linetext = linetext[: linetext.find('\n')]  # remove newline control characters from chordlabel
                # todo: cleanup disused code?
                newtext = ''
                ## parse labeldata line
                contents = linetext.split()
                starttime = contents[0]
                endtime = contents[1]
                chordtext = contents[2]
                #  todo: cleanup: are the following 2 lines used?
                chordroot = ''
                chordtype = ''

                # # standardize time value formats
                starttime = formatTime(starttime)
                endtime = formatTime(endtime)

                ## Remove parenthetical details (chord components, etc.) ## warning: invalidates label sets using only long form chord factor notation
                # chordtext = removeParentheticals(chordtext)

                ##  Determine chord root
                if isChordNull(chordtext):
                    chordroot = isChordNull(chordtext)
                else:
                    chordroot = getRoot(chordtext)

                ##  determine chordtype
                chordtextnoroot = discardBass(chordtext)
                ##  detect longform Harte notation and convert to shortform notation
                chordtextnoroot = convertParentheticals(chordtextnoroot)
                ##  standardize shorthand chord type spelling
                chordtype = getType(chordroot, chordtextnoroot)

                # # standardize enharmonic spellings
                chordroot = standardizeRoot(chordroot, chordtype)

                # # assemble the new line of chord data and write to output
                newchorddescription = chordroot + ':' + chordtype
                newline = (starttime + '\t' + endtime + '\t' + newchorddescription)
                # print(newline)
                nf.writelines(newline + '\n')


