from .util import *
from .chord import GuitarChord
from util import debug
from solfege.base import IntervalWithNoRole

class SetOfSameChord:
    def __init__(self,kind,
                 #name,
                 patternName,
                 third,
                 fifth,
                 quality,
                 minChromatic=None,
    ):
        self.kind=kind
        self.minChromatic=minChromatic
        #self.name=name
        self.patternName=patternName
        self.third=third
        self.fifth=fifth
        self.quality=quality
        self.set_=[]

    # def getName(self):
    #     return self.name
    def getPatternName(self):
        return self.patternName
            
    def addChord(self,chord ):
        """Add the chord to the set, if it is not contained in a chord, with same starting position, same name, and both open or both transposable. Remove chords contained in 'chord', if they satisfy the preceding conditions. 

        return whether the chord was added.
        """
        toremove = []
        for chord_ in self.set_:
            if chord_<chord:
                toremove.append(chord_)
            if chord<chord_:
                return False
        for chord_ in toremove:
            self.set_.remove(chord_)
        self.set_.append(chord)
        return True

    def __len__(self):
        return len(self.set_)
    def __lt__(self,other):
        return len(self)< len(other)
    def __iter__(self):
        return iter(self.set_)
    # def __iter__(self):
    #     return self
    def getOneElement(self):
        return self.set_[0]
    def getMinChromatic(self):
        """Return the minimal chromatic note of an element of the set. Assuming it is the same for each element as indicated during the creation"""
        #In practice, it is the minimal position of each element for open chords, not for transposed one
        return self.minChromatic
    def debug(self):
        return str(self.set_)
    def __repr__(self):
        text= "Set_of_same_chord "
        min_=self.getMinChromatic()
        if min_:
            text+=min_.getNoteName(withOctave=True)
        text+=self.getPatternName()
        text+=repr(self.set_)
        return text
    
class SetOfChords:
    def __init__(self):
        self.chords={
            "transposable": dict(),
            "open": dict()
        }
        self.sets=[]

    def addChord(self,patternName,chord,kind,minChromatic=None):
        """
        Add the chord to this set considering pattern name, and kind.
        Also consider minChromatic if it is present"""
        container=self.chords[kind]
        if patternName not in container:
            if minChromatic:
                container[patternName]=dict()
            else:
                set_=SetOfSameChord(kind,patternName,chord.third(),chord.fifth(),chord.quality())
                self.sets.append(set_)
                container[patternName]=set_
        container =container[patternName]
        if minChromatic:
            if minChromatic not in container:
                set_=SetOfSameChord(kind,patternName,chord.third(),chord.fifth(),chord.quality(),minChromatic=minChromatic)
                self.sets.append(set_)
                container[minChromatic]=set_
            container=container[minChromatic]
        container.addChord(chord) 
        

    def getGreatests(self):
        greatests=[]
        greatest=None
        for set_ in self:
            if  greatest is None or greatest<set_:
                greatests=[set_]
                greatest=set_
            elif set_<greatests[0]:
                continue
            else:
                greatests.append(set_)
        return set_

    def __iter__(self):
        return iter(self.sets)

allChords = SetOfChords()


def genFret(minFret=None,maxFret=None,listFret=[],nbPlayed=0):
    """Generator for every fret satisfying the fact that the distance between fret is at most fretDifMax"""
    length=len(listFret)
    if nbPlayed+(6-length)<minNumberString:
        return
    if length==6:
        debug("--------------------------")
        debug(listFret)
        debug("Number of note played is %d"%nbPlayed)
        try:
            chord=GuitarChord(listFret)
        except IntervalWithNoRole:
            return
        debug("Yielding tab:")
        debug (chord.fileName())
        debug (chord.tab())
        debug (chord.getPatternName())
        yield chord
        return
    lowRange = max({1,maxFret-fretDifMax}) if minFret else 1
    highRange = min({lastFret,minFret+fretDifMax}) if maxFret else lastFret
    for fret in [None,0]+list(range (lowRange,highRange+1)):
        played = 0 if fret is None else 1
        if not listFret:
            print("first_fret is %s"% str(fret))
            debug(f"low range is {lowRange}")
            debug(f"high range is {highRange}")
            debug(f"min fret is {minFret}")
            debug(f"max fret is {maxFret}")
            debug(f"fretDifMax is {fretDifMax}")
        newListFret=listFret+[fret]
        if fret:
            newMinFret= min(minFret,fret) if minFret else fret
            newMaxFret= max(maxFret,fret) if maxFret else fret
        else:
            newMaxFret=maxFret
            newMinFret=minFret
        yield from genFret(newMinFret,newMaxFret,newListFret,nbPlayed+played)


for chord in genFret():
    kind = chord.kind()
    patternName=chord.getPatternName()
    if not (kind and patternName and chord.playable()):
        continue
    if kind=="open":
        minChromatic=chord.getMinPos().getChromatic()
        allChords.addChord(patternName,chord,kind,minChromatic)
    else:
        allChords.addChord(patternName,chord,kind)
