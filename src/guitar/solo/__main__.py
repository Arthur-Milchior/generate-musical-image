"""Generates an image for every note which can be played on the guitar on a string, either open, or with fret between
1 and 5"""
import guitar.util
from guitar.Position.guitar_position import GuitarPosition
from utils.util import ensure_folder

leafFolder = "solo/"
imageFolder = guitar.util.imageFolder + leafFolder
ankiFolder = guitar.util.ankiFolder + leafFolder

ensure_folder(imageFolder)
for string in range(1, 7):
    for pos in range(0, 6):
        with open("%s/%d%d.svg" % (imageFolder, string, pos), "w") as f:
            f.write(
                GuitarPosition(string, pos).svg()
            )