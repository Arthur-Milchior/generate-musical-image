"""
generates pair on note on distinct string. Show 6 frets in the images.
Generate an anki note, with this image, and the distance between both strings, assuming one of the fret is 0
"""
from guitar.pos import Pos, SetOfPos
import os
from util import *
import guitar.util

leafFolder = "pair/"
imageFolder = guitar.util.imageFolder + leafFolder
ankiFolder = guitar.util.ankiFolder + leafFolder
max_fret_distante = 4

first_fret = 0
last_fret = 6

ensureFolder(imageFolder)
ensureFolder(ankiFolder)
anki = ""
anki0 = ""
for string in range(1, 6):
    for string_ in range(string + 1, 7):
        for pos in range(first_fret, last_fret + 1):
            for pos_ in range(first_fret, last_fret + 1):
                pos1 = Pos(string, pos)
                pos2 = Pos(string_, pos_)
                sop = SetOfPos(set([pos1, pos2]))
                dif = (pos2 - pos1).get_number()
                difString = "+%d" % dif if dif > 0 else str(dif)
                fileName = "%d%d-%d%d.svg" % (string, pos, string_, pos_)
                with open("%s%s" % (imageFolder, fileName), "w") as f:
                    sop.draw(f, nbFretMin=6)
                if (pos <= 1 or pos_ <= 1):
                    name = (pos2 - pos1).get_name()
                    if pos and pos_:
                        anki += """strings %d and %d,%s,%s,%s\n""" % (string, string_, fileName, name, difString)
                    else:
                        string_name = str(string) if pos else "%d open" % string
                        string_name_ = str(string_) if pos_ else "%d open" % string_
                        anki0 += """strings %s and %s,%s,%s,%s\n""" % (
                        string_name, string_name_, fileName, name, difString)
with open(ankiFolder + "/anki.csv", "w") as f:
    f.write(anki)
    f.write(anki0)
