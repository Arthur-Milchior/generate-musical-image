import util

modDebug = util.doDebug
fretDifMax = 3 if not modDebug else 2
lastFret = 12 if not modDebug else 2
maxChordNumber = 0
maxChord = ""

minNumberString = 4
imageFolder = util.imageFolder + "chord/"
ankiFolder = util.ankiFolder + "chord/"
