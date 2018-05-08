import os
from  util import *

if not os.path.exists("solo"):
        os.makedirs("solo")
for string in range(1,7):
    for pos in range(0,6):
        with open("solo/%d%d.svg"%(string,pos),"w") as f:
            Pos(string,pos).draw(f)
