"""Generates an image for every note which can be played on the guitar on a string, either open, or with fret between 1 and 5"""
import os
from util import *
import guitar.util
from guitar.pos import Pos

# from .chord import *
leafFolder = "solo/"
imageFolder = guitar.util.imageFolder + leafFolder
ankiFolder = guitar.util.ankiFolder + leafFolder

ensureFolder(imageFolder)
for string in range(1, 7):
    for pos in range(0, 6):
        with open("%s/%d%d.svg" % (imageFolder, string, pos), "w") as f:
            Pos(string, pos).draw(f)
