import os
max_fret_distante = 4
from  util import *
zeroPath = "pair/0"
ensureFolder(zeroPath)
anki = ""
for string in range(1,6):
        for string_ in range(string+1,7):
                for pos in range(0,1):
                        for pos_ in range(0,1):
                                pos1 =Pos(string,pos)
                                pos2 = Pos(string_,pos_)
                                sop = SetOfPos(set([pos1,pos2]))
                                with open("%s/%d%d-%d%d.svg"%(zeroPath,string,pos, string_,pos_),"w") as f:
                                        sop.draw(f,nbFretMin= 6)
with open ("pair/anki.csv", "w") as f:
        f.write(anki)
for string in range(1,6):
        for string_ in range(string+2,7):
                for dpos in range(-max_fret_distante,max_fret_distante+1):
                        pos1 =Pos(string,5)
                        pos2 = Pos(string_,5+dpos)
                        sop = SetOfPos(set([pos1,pos2]))
                        name = (pos2-pos1).name()
                        if dpos<0:
                                imgDif = """<img src="%d%d-%d%d.svg"/>""" %(string,6,string_,6+dpos)
                        elif dpos>0:
                                imgDif = """<img src="%d%d-%d%d.svg"/>""" %(string,1,string_,1+dpos)
                        else: #dpos=0
                                imgDif = """<img src="%d%d-%d%d.svg"/>""" %(string,3,string_,3)
                        anki += """strings %d and %d,%s,%s\n"""%(string,string_,imgDif,name) 
with open ("pair/anki.csv", "w") as f:
        f.write(anki)
