import os
max_fret_distante = 4
from  util import *
ensureFolder("pair")
anki = ""
for string in range(1,6):
        for string_ in range(string+1,7):
                for pos in range(1,7):
                        for pos_ in range(1,7):
                                pos1 =Pos(string,pos)
                                pos2 = Pos(string_,pos_)
                                sop = SetOfPos(set([pos1,pos2]))
                                with open("pair/%d%d-%d%d.svg"%(string,pos, string_,pos_),"w") as f:
                                        sop.draw(f,nbFretMin= 6)
with open ("pair/anki.csv", "w") as f:
        f.write(anki)
for string in range(1,6):
        for string_ in range(string+1,7):
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
                        anki += """%s above <img src="%d%d.svg"/>, %s +%d strings and %d frets\n"""%(name, string, 3, imgDif, string_-string, dpos)
                        anki += """%s below <img src="%d%d.svg"/>, %s -%d strings and %d frets\n"""%(name, string_, 3, imgDif, string_-string, dpos)
                        anki += """interval of %s,%s\n"""% (imgDif,name)
with open ("pair/anki.csv", "w") as f:
        f.write(anki)
