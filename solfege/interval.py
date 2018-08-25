#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from util import *
from .scales import Scale
class _Interval:
    """This class is the basis for each kind of interval. It should never be used directly.
    It allows to represent a number, access it.
    It also allows to add it to another such element, negate it, while generating an object of its subclass.
    Such elements can be compared, and basically hashed (the hash being the number itself)

    The number can't be setted, because the object is supposed to be immutable.
"""

    def __init__(self,value):
        self.value=value
    def getNumber(self):
        return self.value
    def __sub__(self,other):
        return (self+ (-other))
    def __eq__(self,other):
        # if not isinstance(other,Interval):
        #     return False
        return self.getNumber() == other.getNumber()

    def __neg__(self):
        return self.__class__(-self.getNumber())

    def __add__(self,other):
        if not isinstance(other,int):
            otherNumber = other.getNumber()
        else:
            otherNumber=other
        ret=self.__class__(self.getNumber()+otherNumber)
        #debug("Adding %s and %s we obtain %s",(self,other,ret))
        return ret
    def __hash__(self):
        return self.getNumber()
    def __le__(self,other):
        return self.getNumber()<= other.getNumber()
    def __repr__(self):
        return "%s:%d"%(self.__class__,self.value)
    
    
class DiatonicInterval(_Interval):
    """An interval, where we count the number of notes in the major scale, and ignore the notes which are absent. B and B# can't be distinguished, since A# does not really exists. However this would allow to distinguish between B# and C"""
    def __init__(self,diatonic):
        if isinstance(diatonic, DiatonicInterval):
            diatonic=diatonic.getNumber()
        super().__init__(diatonic)
        

    def getChromaticInterval(self,scale="Major"):
        """
        Give the chromatic interval associated to the current diatonic interval in some scale.
          By default, the scale is the major one."""
        #TODO scale= Scale.dic[scale] currently, only major is used
        return ChromaticInterval(12*self.getOctave() + [0,2,4,5,7,9,11][self.getNumber() % 7])

    def getName(self,showOctave=True):
        size = abs(self.getNumber())
        text=""
        if size>7:
            text="%d octave(s) and "%(size/7)
        text+=["unison","second","third","fourth","fifth","sixth","seventh"][size%7]
        if self.getNumber()>0:
            text+=" increasing"
        elif self.getNumber()<0:
            text+=" decreasing"
        return text
    
    def getOctave(self):
        return math.floor(self.getNumber()/7)

    def addOctave(self,nb):
        return DiatonicInterval(self.getNumber()+nb*7)
    
    def lilyOctave(self):
        octave = self.getOctave()
        octaveShift = octave +1
        if octaveShift>0:
            return  "'"*octaveShift
        elif octaveShift<0:
            return ","*(-octaveShift)
        else:
            return ""
    def sameNoteDistinctOctave(self,other):
        return not((self.getNumber() -other.getNumber()) %7)
    def baseOctave(self):
        return DiatonicInterval(self.getNumber() % 7)

class ChromaticInterval(_Interval):
    """A chromatic interval. Counting the number of half tone between two notes"""
    def __init__(self, chromatic):
        if isinstance(chromatic, ChromaticInterval):
            chromatic=chromatic.getNumber()
        if not isinstance(chromatic,int):
            raise (Exception ("A chromatic interval which is not a number, but %s"%(repr(alteration))))
        super().__init__(chromatic)
    def addOctave(self,nb):
        return ChromaticInterval(self.getNumber()+nb*12)
   
    def getName(self,kind=None):
        if (kind %7)  in [0,3,4]:
            return ["diminshed","","augmented"][self.getNumber()+1]
        else:
            return ["diminshed","minor","major","augmented"][self.getNumber()+2]

    def baseOctave(self):
        return ChromaticInterval(self.getNumber()%12)

    def distinctOctave(self,other):
        return self.baseOctave()==other.baseOctave()
    

class Alteration(ChromaticInterval):
    def printable(self):
        return  abs(self.getNumber()) <=2
    def __init__(self,interval):
        super().__init__(interval)
        if not self.printable():
            raise Exception("number %d corresponds to no Alteration"%self.getNumber())
        
    def __add__(self,other):
        raise Exception("Adding alteration ?")
#        return Diatonic(self.getNumber()+other.getNumber())
    def baseOctave(self):
        raise Exception("Alteration has no base octave")
    def lily(self):
        return ["eses","es","","is","isis"][self.getNumber()+2]
    def getName(self,kind=None):
        if kind is None:
            return ["♭♭","♭","","#","𝄪"][self.getNumber()+2]
        if kind == "file":
            return ["double bemol","bemol","","sharp","double sharp"][self.getNumber()+2]

class SolfegeInterval(ChromaticInterval):
    """A class for a solfege interval. Composed of both a diatonic interval and a chromatic interval."""
    def __init__(self,chromatic=None, diatonic=None, addingBothIntervals=False):
        if addingBothIntervals:
            chromatic=diatonic.getChromaticInterval()+chromatic
        super().__init__(chromatic)
        # if isinstance(chromatic,int):
        #     chromatic=ChromaticInterval(chromatic)
        if isinstance(diatonic,int):
            diatonic=DiatonicInterval(diatonic)
        if diatonic is None or not isinstance(diatonic,DiatonicInterval) :
            raise Exception("diatonic is not correct, but %s"%(str(diatonic)))
        self.diatonic=diatonic
    def __neg__(self):
        return SolfegeInterval(chromatic=-self.getChromaticInterval(),diatonic=-self.getDiatonicInterval())
    def __sub__(self,other):
        return (self+ (-other))
    def getChromaticInterval(self):
        return ChromaticInterval(self)

    def getDiatonicInterval(self):
        return self.diatonic

    def getAlteration(self):
        chromaticFromDiatonic=self.getDiatonicInterval().getChromaticInterval()
        chromatic=self.getChromaticInterval()
        alt=Alteration(chromatic-chromaticFromDiatonic)
        #debug("The alteration of %s is %s" % (self,alt))
        return alt

    def __repr__(self):
        return "(%d chromatic,%d diatonic)"%(self.getChromaticInterval().getNumber(),self.getDiatonicInterval().getNumber())

    def __add__(self,other):
        diatonic = self.getDiatonicInterval()+other.getDiatonicInterval()
        chromatic=self.getChromaticInterval()+other.getChromaticInterval()
        interval=SolfegeInterval(chromatic=chromatic, diatonic=diatonic)
        #debug("Adding %s and %s we obtain %s",(self,other,interval))
        return interval

    def addOctave(self,nb):
        return SolfegeInterval(chromatic=self.getChromaticInterval().addOctave(nb),diatonic=self.getDiatonicInterval().addOctave(nb))
    
    def __eq__(self,other):
        return self.getDiatonicInterval() == other.getDiatonicInterval() and self.getChromaticInterval() == other.getChromaticInterval()
            
    def baseOctave(self):
        octave=-self.getDiatonicInterval().getOctave()
        return SolfegeInterval(chromatic=self.getChromaticInterval().addOctave(octave),diatonic=self.getDiatonicInterval().addOctave(octave))


    def getOctave(self):
        return self.getDiatonicInterval().getOctave()
    def __hash__(self):
        return hash(self.getChromaticInterval())

