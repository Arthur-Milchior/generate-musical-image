"""Generates an image for every note which can be played on the guitar on a string, either open, or with fret between 1 and 5""".
import os
from util import *
from .util import *
from .chord import *
folder="guitar/solo/images"
ensureFolder(folder)
for string in range(1,7):
    for pos in range(0,6):
        with open("%s/%d%d.svg"%(folder,string,pos),"w") as f:
            Pos(string,pos).draw(f)
