#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import debug_file
from util import *

class _Interval:
    """This class is the basis for each kind of interval. It should never be used directly.
    It allows to represent a number, access it.
    It also allows to add it to another such element, negate it, while generating an object of its subclass.
    Such elements can be compared, and basically hashed (the hash being the number itself)

    The number can't be setted, because the object is supposed to be immutable.

    Inheriting class which are instancied should contain the following variable:
    * modulo: number of note by octave (7 for diatonic, 12 for chromatic)
    * ClassToTransposeTo: the class of object to generate. If it's None, the class of self is used.
    * RelatedDiatonicClass: class to which a chromatic object must be converted when a diatonic object is required.
    * RelatedSolfegeClass: the class to which a diatonic and chromatic object must be converted.
"""
    ClassToTransposeTo=None
    def __init__(self,value=None,toCopy=None,callerClass=None,none=None,**kwargs):
        """If the interval is passed as argument, it is copied. Otherwise, the value is used. none, if true, means that there is no value and it is acceptable"""
        super().__init__(**kwargs)
        self.dic=dict()
        if none:
            self.value=None
            return
        if toCopy is not None:
            if not isinstance(toCopy,callerClass):
                raise Exception("An interval: %s is not of the class %s"%(toCopy,callerClass))
            number = toCopy.getNumber() if toCopy.hasNumber() else None
        else:
            number = value
        if not isinstance(number,int):
            raise (Exception ("A result which is not a number but %s.\n value:%s, toCopy:%s, callerClass:%s,none:%s"%(number,value,toCopy,callerClass,none)))
        self.value=number

    def isNote(self):
        return False

    def hasNumber(self):
        return isinstance(self.value,int)

    def getNumber(self):
        if not isinstance(self.value,int):
            raise Exception("A number which is not int but %s"%self.value)
        return self.value

    def __eq__(self,other):
        # if not isinstance(other,Interval):
        #     return False
        if self.__class__!=other.__class__:
            raise Exception("Comparison of two distinct classes: %s and %s"%(self.__class__,other.__class__))
        return self.getNumber() == other.getNumber()

    def __add__(self,other):
        """Same class than self. Sum of both intervals"""
        if not isinstance(other,int):
            otherNumber = other.getNumber()
        else:
            otherNumber=other
        sum_=self.getNumber()+otherNumber
        ret=self.__class__(value=sum_)
        #debug("Adding %s and %s we obtain %s",(self,other,ret))
        return ret

    def __neg__(self):
        """Same class than self, inverse interval"""
        Class = self.ClassToTransposeTo or self.__class__
        return self.__class__(value=-self.getNumber())

    def __sub__(self,other):
        """Same class than self. This interval minus the other one"""
        neg=-other
        if neg.isNote():
           raise Exception("Neg is %s, which is a note" %neg)
        return (self+ neg)

    def __hash__(self):
        return self.getNumber()

    def __le__(self,other):
        if isinstance(other, _Interval):
            other= other.getNumber()
        return self.getNumber()<= other

    def __lt__(self,other):
        if isinstance(other, _Interval):
            other= other.getNumber()
        return self.getNumber()< other

    def __repr__(self):
        return "%s(%d)"%(self.__class__.__name__,self.getNumber())

    def getOctave(self):
        return math.floor(self.getNumber()/self.__class__.modulo)

    def addOctave(self,nb):
        """Same note with nb more octave"""
        Class= self.ClassToTransposeTo or self.__class__
        return Class(value=self.getNumber()+nb*self.__class__.modulo)

    def getSameNoteInBaseOctave(self):
        """Same note in the base octave"""
        return self.addOctave(-self.getOctave())

    def sameNotesInDifferentOctaves(self,other):
        """Whether self and other are same note, potentially at distinct octaves"""
        return self.getSameNoteInBaseOctave() != other.getSameNoteInBaseOctave()

    def differenceInBaseOctave(self,other):
        Class= self.ClassToTransposeTo or self.__class__
        return Class((self.getNumber() -other.getNumber()) %self.__class__.modulo)


class DiatonicInterval(_Interval):
    """An interval, where we count the number of notes in the major scale,
    and ignore the notes which are absent. B and B# can't be
    distinguished, since A# does not really exists. However this would
    allow to distinguish between B# and C"""
    modulo = 7
    def __init__(self,diatonic=None,value=None, **kwargs):
        if diatonic is not None:
            value=diatonic
        super().__init__(value=value,callerClass=DiatonicInterval, **kwargs)

    def __add__(self,other):
        if not isinstance(other, DiatonicInterval):
            raise Exception("Adding a DiatonicInterval interval to something which is not a DiatonicInterval but %s"%other)
        return super().__add__(other)


    def getChromatic(self,scale="Major"):
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

    def lilyOctave(self):
        """The string which allow to obtain correct octave in lilypond."""
        octave = self.getOctave()
        octaveShift = octave +1
        if octaveShift>0:
            return  "'"*octaveShift
        elif octaveShift<0:
            return ","*(-octaveShift)
        else:
            return ""

DiatonicInterval.IntervalClass = DiatonicInterval

class ChromaticInterval(_Interval):
    modulo=12

    """the diatonic class to which such a chromatic class must be converted"""
    RelatedDiatonicClass=DiatonicInterval

    """A chromatic interval. Counting the number of half tone between two notes"""
    def __init__(self, chromatic=None, value=None,**kwargs):
        if value is None:
            value=chromatic
        super().__init__(value=value, callerClass=ChromaticInterval, **kwargs)

    def __add__(self,other):
        if not isinstance(other, ChromaticInterval):
            raise Exception("Adding a ChromaticInterval interval to something which is not a ChromaticInterval but %s"%other)
        return super().__add__(other)

    def getDiatonic(self):
        """If this note belong to the diatonic scale, give it.
        Otherwise, give the adjacent diatonic note."""
        if "diatonic" not in self.dic:
            diatonic=self.RelatedDiatonicClass(diatonic=[0,0,1,2,2,3,3,4,5,5,6,6][self.getSameNoteInBaseOctave().getNumber()]+7*self.getOctave())
            self.dic["diatonic"]=diatonic
            debug("Diatonic of %s is %s"%(self,diatonic))
        return self.dic["diatonic"]

    def getAlteration(self):
        chromaticFromDiatonic=self.getDiatonic().getChromatic()
        chromatic=self.getChromatic()
        try:
            alt=Alteration(chromatic=chromatic.getNumber()-chromaticFromDiatonic.getNumber())
        except TooBigAlteration as tba:
            tba.addInformation("Solfege interval",self)
            raise
            #debug("The alteration of %s is %s" % (self,alt))
        return alt

    def getSolfege(self,diatonic=None):
        """A note. Same chromatic. Diatonic is as close as possible (see getDiatonicNote) or is the note given."""
        if diatonic is None:
            diatonic=self.getDiatonic().getNumber()
        return self.RelatedSolfegeClass(diatonic=diatonic,chromatic=self.getNumber())

    def getName(self,kind=None,octave=True,side=False):
        """The name of the interval.

        octave -- For example: if this variable is set true, the name is given as "supertonic and one octave".
        Otherwise, if it is set to None, the variable is given as "eight"

        side -- Whether to add "increasing" or "decreasing"

        kind -- if a number is given, then we consider that we want major/minor, and not a full name
        todo
        """
        if self<0:
            name = (-self).getName(kind=kind,octave=octave,side=False)
            if side:
                return name+" decreasing"
            else:
                return name
        if octave:
            nbOctave=self.getOctave()
            pos=self.getNumber()%12
            name=""
            if nbOctave>1:
                name+="%d octaves"%nbOctave
            if nbOctave==1:
                name+="An octave"
            nameBis= ["" if nbOctave else "unison", "second minor", "second major", "third minor", "third major", "fourth","tritone","fifth", "sixth minor", "sixth major", "seventh minor","seventh major"][pos]
            if nameBis:
                name+= "and "+nameBis
            if side:
                name+=" increasing"
            return name
        # if (kind %7)  in [0,3,4]:
        #     return ["diminished","","augmented"][self.getNumber()+1]
        # else:
        #     return ["diminished","minor","major","augmented"][self.getNumber()+2]
ChromaticInterval.IntervalClass = ChromaticInterval

class TooBigAlteration(Exception):
    def __init__(self,value):
        self.value=value
        super().__init__()

    def __str__(self):
        text="number %d corresponds to no Alteration.\n%s"%(self.value,super().__str__())
        return text


class Alteration(ChromaticInterval):
    def printable(self):
        """Whether the alteration is at most 2 half tone, and thus printable with at most 2 symbols."""
        number=self.getNumber()
        return number is not None and  abs(number) <=2

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        if not self.printable():
            raise TooBigAlteration(self.getNumber())

    def __add__(self,other):
        raise Exception("Adding alteration ?")
#        return Diatonic(self.getNumber()+other.getNumber())

    def getSameNoteInBaseOctave(self):
        raise Exception("Alteration has no base octave")

    def lily(self):
        """Text to obtain this alteration in Lilypond"""
        return ["eses","es","","is","isis"][self.getNumber()+2]

    def getName(self,kind=None):
        if kind is None:
            return ["♭♭","♭","","#","𝄪"][self.getNumber()+2]
        if kind == "file":
            return ["double bemol","bemol","","sharp","double sharp"][self.getNumber()+2]

class SolfegeInterval(ChromaticInterval):
    """A class for a solfege interval. Composed of both a diatonic interval and a chromatic interval."""
    DiatonicClass=DiatonicInterval
    ChromaticClass=ChromaticInterval
    def __init__(self,chromatic=None, diatonic=None, alteration=None,toCopy=None,none=None,**kwargs):
        """If toCopy is present, it is copied

        Otherwise, chromatic and diatonic are used.
        Otherwise if chromatic is present, it supposed to be the exact value.
        otherwise, alteration should be present, and chromatic is the sum of diatonic and alteration
        """
        if none:
            self.initNone(none)
        elif toCopy:
            self.initCopy(toCopy)
        else:
            self.diatonic=self.DiatonicClass(diatonic=diatonic)
            if chromatic is not None:
                self.initChromaticPresent(chromatic)
            else:
                self.initChromaticAbsent(alteration)

    def initNone(none):
        super().__init__(none=none)

    def initCopy(toCopy):
        if not isinstance(toCopy,SolfegeInterval):
            raise Exception
        super().__init__(chromatic=toCopy.getNumber())
        self.diatonic=toCopy.getDiatonic()

    def initChromaticPresent(self,chromatic):
        if not isinstance(chromatic,int):
            raise Exception("Chromatic is not int but %s"%(str(chromatic)))
        super().__init__(chromatic=chromatic)

    def initChromaticAbsent(self,alteration):
        if alteration is not None:
            if  not isinstance(alteration,int):
                raise Exception("Alteration is not int but %s"%(str(alteration)))
            super().__init__(chromatic=self.diatonic.getChromatic().getNumber()+alteration)
        else:
            raise Exception("No alteration, no toCopy, no chromatic, no none")

    ###### End of inits

    def __eq__(self,other):
        diatonicEq = self.getDiatonic() == other.getDiatonic()
        chromaticEq = super().__eq__(other)
        return diatonicEq and chromaticEq

    def __hash__(self):
        return hash(self.getChromatic())

    def __neg__(self):
        Class= self.ClassToTransposeTo or self.__class__
        return Class(chromatic=-self.getNumber(),diatonic=-self.getDiatonic().getNumber())

    def getChromatic(self):
        return self.ChromaticClass(chromatic=self.getNumber())

    def getDiatonic(self):
        return self.diatonic

    def __repr__(self):
        return "%s(%d,%d)"%(self.__class__.__name__,self.getChromatic().getNumber(),self.getDiatonic().getNumber())

    def __add__(self,other):
        if not isinstance(other, SolfegeInterval):
            raise Exception("Adding a solfege interval to something which is not a solfege interval")
        diatonic = self.getDiatonic().getNumber()+other.getDiatonic().getNumber()
        chromatic=self.getChromatic().getNumber()+other.getChromatic().getNumber()
        Class= self.ClassToTransposeTo or self.__class__
        interval=Class(chromatic=chromatic, diatonic=diatonic)
        #debug("Adding %s and %s we obtain %s",(self,other,interval))
        return interval

    def addOctave(self,nb):
        Class= self.ClassToTransposeTo or self.__class__
        return Class(chromatic=self.getChromatic().addOctave(nb).getNumber(),diatonic=self.getDiatonic().addOctave(nb).getNumber())

    def getOctave(self):
        return self.getDiatonic().getOctave()

    def getSameNoteInBaseOctave(self):
        octaveToAdd=-self.getOctave()
        Class= self.ClassToTransposeTo or self.__class__
        chromatic=self.getChromatic().addOctave(octaveToAdd).getNumber()
        diatonic=self.getDiatonic().addOctave(octaveToAdd).getNumber()
        return Class(chromatic=chromatic,diatonic=diatonic)

ChromaticInterval.RelatedSolfegeClass = SolfegeInterval
SolfegeInterval.IntervalClass = SolfegeInterval
