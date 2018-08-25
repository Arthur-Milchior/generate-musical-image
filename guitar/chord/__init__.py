"""Consider each way to place fingers on at least four of the six strings.
If its a chord, satisfying some condition, the image is generated, and an anki note is also generated. 
"""

#anki: open/tranposable, starting note(for open),position of tonic (for transposable), 3, 5, 7 (,image,1, 3, 5, 7)*n
from solfege.interval import *
from util import *
from .util import *
modDebug = True
minNumberString = 4 if not modDebug else 2
fretDifMax = 4 if not modDebug else 2
lastFret = 12 if not modDebug else 5
maxChordNumber = 0
maxChord=""
considerOpen = False



class Chord(SetOfPos):
    """A chord. That is, a fret by string. 0 for empty string"""
    def __init__(self,dic):
        self.chord = {string:fret for string,fret in dic.items () if fret is not None}
        SetOfPos.__init__(self, {Pos(string,fret) for string,fret in dic.items ()})
        self.hts = Hts(self)
        self.numberChord = len(self.chord)

    def anki(self):
        """(pos1,pos3,pos5,posn)"""
        text = ""
        for (number,hts) in [("1",{Chromatic(0)}),("3",{Chromatic(3),Chromatic(4)}), ("5",{Chromatic(6),Chromatic(7)}), ("n",{Chromatic(9),Chromatic(10),Chromatic(11)})]:
            text +=","
            for i in range(1,7):
                if i not in self.chord:
                    text += "x"
                else:
                    d  = Pos(i,self.chord[i]) - self.minPos
                    if d in hts:
                        text +=number
                    else:
                        text +="."
        return text
            
    def playable(self):
        """At most three frets not being on fret 0 or 1"""
        nbGtOne=0#nb of fret >1 played. 
        nbOne=0#nb of fret 1 played
        m =12#least non 0 fret played
        M = -1 #greatest fret played
        for pos in self.poss :
            if pos.fret is  None:
                continue
            if pos.fret>0:
                m = min(m, pos.fret)
            M = max (M,pos.fret)
            if pos.fret == 1:
                nbOne +=1
            if pos.fret>1:
                nbGtOne+=1
            
        if  M-m>4:
            debug("More than four fret of difference between bottom and top")
            return False
        if self.isOpen():
            if nbGtOne + nbOne > 4:
                debug ("Open string and %d elements which are >0"% (nbGtOne+nbOne))
                return False
        else:#not open chord
            if nbGtOne>3:
                debug ("Closed string and %d elements which are >1"% nbGtOne)
                return False
        debug("Playable")
        return True
    def atLeastFourString(self):
        r = self.numberChord>=minNumberString
        if r:
            debug("At least %d string"%minNumberString)
            return True
        else:
            debug("Only %d strings played"% self.numberChord)
            return False
        
    def isStandardChord(self):
        standard=self.hts.isStandardChord()
        debug("Is it standard: %s"%standard)
        return  standard
    def isOpenChord(self):
        return self.isOpen() and self.isStandardChord() and self.playable() and self.atLeastFourString()
    def isTransposableChord(self):
        return self.isOneMin() and self.isStandardChord() and self.playable()  and self.atLeastFourString()
    def isAcceptable(self):
        return (self.onePresent() or self.isOpen()) and self.isStandardChord() and self.playable() and self.atLeastFourString()
    def kind(self):
        """transposable, open, or None"""
        if self.isStandardChord() and self.playable() and self.atLeastFourString():
            if self.isOpen():
                return "open"
            if self.isOneMin():
                return "transposable"
            else:
                return None
    
    def __str__(self):
        return str(self.chord)
        # return str(SetOfPos(self))
    # def __init__(self, base, quality, interval, renversement, string, fret):
        # self.base = base
        # self.quality = quality
        # self.interval = interval
        # self.renversement = renversement
        # self.string = string
        # self.fret = fret
        

class Hts:
    """The set of chromatic interval (coded as integers) between the notes and the lowest note"""
    def __init__(self, sop):
        minPos = sop.findMinPos()
        self.hts = {pos - minPos for pos in sop if pos.fret is not None}
    def isMinor(self):
        return ChromaticInterval(3) in self.hts
    def isMajor(self):
        return ChromaticInterval(4) in self.hts
    def third(self):
        if self.isMinor():
            if self.isMajor():
                return False
            return  "min"
        if self.isMajor():
            return "Maj"
        debug("no Third")
        return False
    def isFifthDimished(self):
        return ChromaticInterval(6) in self.hts
    def isFifthJust(self):
        return ChromaticInterval(7) in self.hts
    def fifth(self):
        """If the 5th is diminished, and third is minor return "diminished". 
        If the 5th is just, return the empty string.
        Otherwise return false
        """
        if self.isFifthDimished(): #exactly one of them
            if self.isFifthJust():
                return False
            if self.isMinor() and (not self.is7min()) and (not self.is7maj()):
                return "diminished"
            return False
        if self.isFifthJust():
            return "just"

    def hasNotQuality(self):
        return not (self.is6() or self.is7min() or self.is7maj())
    def is6(self):
        return ChromaticInterval(9) in self.hts
    def is7min(self):
        return ChromaticInterval(10) in self.hts
    def is7maj(self):
        return ChromaticInterval(11) in self.hts
    def quality(self):
        if self.is6():
            if self.is7min() or self.is7maj():
                debug("6 and 7")
                return  False
            return  "6"
        if self.is7min():
            if self.is7maj():
                debug("both 7")
                return  False
            return  "7min"
        if self.is7maj():
            return  "7maj"
        return ""
    def containsTonic(self):
        return ChromaticInterval(0) in self.hts
    def anki(self):
        """Third, fifth, 7th"""
        return "%s,%s,%s"%(self.third(),self.fifth(),self.quality())
    def contains567(self):
        return (ChromaticInterval(7) in self.hts
                or
                self.quality())
    def wrongNote(self):
        if ChromaticInterval(1) in self.hts:
            debug("Contains half tone")
            return False
        if ChromaticInterval(2) in self.hts:
            debug("Contains tone")
            return False
        if ChromaticInterval(5) in self.hts:
            debug("contains fourth")
            return False
        if ChromaticInterval(8) in self.hts:
            debug("Contains 6th bemol")
            return False
        return True
    def isStandardChord(self):
        "Given a set of notes, is it a standard chord"
        if self.wrongNote():
            debug("Contains wrong note")
            return False
        if not self.third():
            debug("Has no third")
            return False
        if self.fifth() is False:
            debug("Has no fifth")
            return False
        if self.quality is False:
            debug("wrong quality")
            return False
        if not self.containsTonic():
            debug("has no tonic")
            return False
        if not self.contains567():
            debug("Has no interval at least 5th")
            return False
        return True
    def isNonStandard(self):
        return not self.isStandardChord()

    def reversed(self):
        m = 13 
        for ht in self.s:
            transposed = {ht_ % 12 : ht_ in self.s}
            if isStandardChord(transposed) and ht<m and (not is6(transposed)):
                m = ht
        if m==13:
            return False
        else:
            return m
    def __str__(self):
        """Name of chord, assuming it is standard"""
        if self.isFifthJust():
            fifthName = ""
        elif self.isFifthDimished():
            fifthName = "-Dim"
        else:
            fifthName = "-None"
        qualityName=self.quality()
        if qualityName:
            qualityName = "-%s" % qualityName
        if qualityName == "-6" and fifthName:
            qualityName= "-dim7"
        return ("%s%s%s"%(self.third(), fifthName, qualityName))


def list2dic(l):
    return {i+1:l[i] for i in range(0,len(l))}
containedChord = Chord(list2dic([1,None,3,2,1,1]))
containingChord = Chord(list2dic([1,3,3,2,1,1]))


chords={"transposable": {i: set() for i in range(minNumberString,7)}, "open": {i: set() for i in range(minNumberString,7)}}
for first_fret in range(1,lastFret+1):
    print("first_fret is %d"% first_fret)
    frets = [i for i in range(first_fret,min(lastFret+1, first_fret+fretDifMax))]
    frets.append(None)
    frets.append(0)
    for f1 in frets:
        if f1 is not None:
            print("f1 is %d"% f1)
        for f2 in frets:
            for f3 in frets:
                for f4 in frets:
                    for f5 in frets:
                        for f6 in frets:
                            chord =Chord({1:f1,
                                          2:f2,
                                          3:f3,
                                          4:f4,
                                          5:f5,
                                          6:f6})
                            debug("Considering chord %s"%chord)
                            kind = chord.kind()
                            if kind == "open" and chord.minFret >first_fret:
                                #It will be added later, when i is the value on the minFret. Not sure that equality of chords works, and useless to test it.
                                continue
                            if  kind == "transposable"  :
                                chords_kind=chords[kind]
                                chord_kind_numberChord=chords_kind[chord.numberChord]
                                chord_kind_numberChord.add(chord)
                                    
            

"""filter chords contained in another chord of this set.
Bool state whether this chord is knowt to be included into another one"""
for kind in chords:
    for size in range(minNumberString,6):
        print("Filtering chords of size %d"%size)
        s = set()
        for chord in chords[kind][size]:
            supersetFound = False
            for chord_ in chords[kind][size+1]:
                if chord < chord_ and chord.minPos == chord_.minPos:
                    debug(chord,end="")
                    debug("deleted, because contained in",end="")
                    supersetFound=True
                    debug(chord_)
                    break
            if not supersetFound:
                debug(chord,end="")
                debug("kept")
                s.add(chord)
        chords[kind][size]=s

"""draw chords and add them to the list of chords """
opens_chord_base = dict()
opens_base_chord = dict()
transposable  = dict()
#classify
for kind in chords:
    found= dict()#The set of name of string found
    for i in chords[kind]:
      for chord in chords[kind][i]:
        minPos = chord.findMinPos()
        chordName = str(chord.hts)
        folder = "guitar/chord/%s/%s" % (kind, chordName)
        fileName = ("%d-%d-%s"%(minPos.string, minPos.fret, chordName))

        #edit name and folder for open file
        if kind == "open":
            base = minPos.name()
            folder +="/%s"%base
            fileName = "%s%s"%(base, fileName)
            if chordName not in opens_chord_base:
                opens_chord_base[chordName]=dict()
            if base not in opens_chord_base[chordName]:
                opens_chord_base[chordName][base] = set()

            if base not in opens_base_chord:
                opens_base_chord[base]=dict()
            if chordName not in opens_base_chord[base]:
                opens_base_chord[base][chordName] = set()
        else:
            if chordName not in transposable:
                transposable[chordName]=dict()
            if minPos not in transposable[chordName]:
                transposable[chordName][minPos]= set()
            
        #in case of name conflict, add a number.
        if fileName in found:
            debug("name %s already found"%fileName)
            found[fileName]+=1
            if found[fileName] > maxChordNumber:
                maxChordNumber=found[fileName]
                maxChord = "%s %s"%(kind,fileName)
            number = "-"+str(found[fileName])
        else:
            found[fileName]=1
            number=""
        fileName=fileName+number+".svg"

        #adding chord to set of chords.
        if kind == "open":
            opens_chord_base[chordName][base].add((fileName,chord))
            opens_base_chord[base][chordName].add((fileName,chord))
        else:
            transposable[chordName][minPos].add((fileName, chord))
        path = "%s/%s" %(folder,fileName)
        ensureFolder(folder)
        with open (path, "w") as f:
            chord.draw(f)
    
index = """<html><head><title>All transposable chord on a standard guitar</title></head>
<body>
Here is the list of the chords, satisfying the followins properties:
<ul><li>
At least four strings are played.
</li><li>
Either a string is opened. Otherwise a finger on fret 1 is played.
</li><li>
At most four fingers used. First string is potentially barred. (Either entirely, or not at all. Todo: allow partial bar)
</li><li>
No more than four frets of difference between lowest and highest fret played.
</li><li>
The chord is not contained in another chord with the same lowest note
</li><li>
The chord is not reversed (todo: do it)
</li>
</ul>
The set of chords:
<ul>
"""

anki = ""
for chordName in transposable:
  for minPos in transposable[chordName]:
    ankiLine = """transposable,,<img src="%i%i.svg"/>,%s"""%(minPos.string,minPos.fret,chord.hts.anki())
    local = """<html><head><title>List of transposable %s chords</title></head>
    <body>List of the %d transposable %s chords<br/>""" %( chordName, len(transposable[chordName][minPos]), chordName)
    folder = "guitar/chord/transposable/%s" %(chordName)
    ensureFolder(folder)
    for (fileName, chord) in transposable[chordName][minPos]:
        local +="""<img src="%s"/>""" % fileName
        ankiLine += """",<img src="%s"/>,%s"""%(fileName, chord.anki())
    ankiLine += (",,,,,"*(maxChordNumber-len(transposable[chordName][minPos])))
    local += """<br/><a href="../..">List of chords</a>,<a href="../open/%s">the open %s</a></body></html>"""% (chordName, chordName)
    path = "%s/index.html"%folder
    ensureFolder(folder)
    with open(path,"w") as f:
        f.write(local)
    print("Adding transposable %s to index" % chordName)
    index += """<li><a href='%s'>transposable %s</li>"""%(folder, chordName)
    anki += "%s\n"% ankiLine

ensureFolder("guitar")
if considerOpen:
  ensureFolder("guitar/chord/open")
  for chordName in opens_chord_base:
    chordFile = """<html><head><title>List of open %s chords</title></head>
    <body>List of the open %s chords.<ul>""" %(chordName, chordName)
    for base in opens_chord_base[chordName]:
        ankiLine = """open,%s,,%s"""%(base,chord.hts.anki())
        chordFile +="""<li><a href="%s/">%s</a></li>"""%(base,base)
        chordBaseFile = """<html><head><title>List of open %s %s chords</title></head>
        <body>List of the %d open %s %s chords<br/>""" %(base, chordName, len(opens_chord_base[chordName][base]), base, chordName)
        folder = "open/%s/%s" %(chordName, base)
        for (fileName,chord) in opens_chord_base[chordName][base]:
            chordBaseFile +="""<img src="%s"/>""" % fileName
            ankiLine += """",<img src="%s"/>%s"""%(fileName, chord.anki())
        ankiLine += (",,,,,"*(maxChordNumber-len(opens_chord_base[chordName][base])))
        chordBaseFile += """<br/><a href="../../..">List of chords</a>,<a href="../transposable/%s">the transposable %s chords</a></body></html>"""% (chordName, chordName)
        path = "guitar/chord/%s/index.html"%folder
        with open(path,"w") as f:
            f.write(chordBaseFile)
        print("Adding open %s %s to index" % (base,chordName))
        index += """<li><a href='%s'>open %s %s</li>"""%(folder, base, chordName)
        anki += "%s\n"% ankiLine
    chordFile += """</ul></body></html>"""
    ensureFolder("guitar/chord/open/%s"%chordName)
    with open("guitar/chord/open/%s/index.html"%chordName,"w") as f:
        f.write(chordFile)
  with open("guitar/chord/open/index.html","w") as f:
    f.write(chordFile)
    
  for base in opens_base_chord:
    baseFile = """<html><head><title>List of open %s chords</title></head>
    <body>List of the open %s chords.<ul>""" %(base, base)
    for chordName in opens_base_chord[base]:
        baseFile +="""<li><a href="../%s/%s/">%s</a></li>"""%(base, chordName,chordName)
    baseFile += """</ul></body></html>"""
    folder = "guitar/chord/open/%s"%base
    path = folder + "/index.html"
    with open(path,"w") as f:
        f.write(baseFile)


index += "</ul></body></hmtl>"
with open("guitar/chord/anki.csv","w") as f:
    f.write(anki)
with open("guitar/chord/index.html","w") as f:
    f.write(index)
print("There is up to %d version of the same chord, i.e. chord %s"%(maxChordNumber,maxChord))
