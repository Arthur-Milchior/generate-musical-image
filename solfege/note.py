#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import solfege.interval
from interval import *
from util import *

class DiatonicNote(DiatonicInterval):
    """A diatonic note"""
    #Saved as the interval from middel C
    def __init__(self,interval):
        if isinstance(interval,DiatonicInterval):
            interval= interval.getNumber()
        super().__init__(interval)
    def __add__(self,other):
        return DiatonicNote(other+self)
    def getName(self):
        return ["c","d","e","f","g","a","b"][self.getNumber() %7]

class ChromaticNote(ChromaticInterval):
    def __init__(self,interval):
        if isinstance(interval,ChromaticInterval):
            interval= interval.getNumber()
        super().__init__(interval)
    def __add__(self,other):
        return ChromaticNote(other+self)
    def getName(self):
        return ["Tonic","Tonic#","Supertonic","Mediant♭","mediant","subdominant","subdominant#","dominant","submediant♭","submediant","subtonic","leading"][self.getNumber() %12]
    

class Note(SolfegeInterval):
    """A note of the scale, as an interval from middle C."""
    
    def __init__(self,alteration=None,diatonic= None,interval=None,addingBothIntervals=True):
        #debug("Creating a note with input alteration %s, diatonic %s, interval %s and addingBothIntervals %s",(alteration,diatonic,interval,addingBothIntervals))
        if interval:
            diatonic= interval.getDiatonicInterval()
            alteration=interval.getAlteration()
            #debug("Since there is an interval, diatonic %s, alteration %s",(diatonic,alteration))
        if not isinstance(diatonic,Diatonic):
            diatonic=DiatonicNote(diatonic)
            #debug("diatonic was not a Diatonic, it is now %s",(diatonic))
        if not isinstance(alteration,Alteration):
            alteration=Alteration(alteration)
            #debug("alteration was not an Alteration, it is now %s",(alteration))
        super().__init__(chromatic=alteration,diatonic=diatonic,addingBothIntervals=addingBothIntervals)
        #debug("this note is now %s",self)


    
    def printLily(self):
        return "%s%s%s" % (self.getDiatonicInterval().getName(),self.getAlteration().lily(),self.getDiatonicInterval().lilyOctave())
    
    def getName(self,kind=None):
        diatonic = self.getDiatonicInterval()
        alteration=self.getAlteration()
        diatonicName=diatonic.getName().upper()
        alterationName=alteration.getName(kind=kind)
        return "%s%s" %(diatonicName,alterationName)
    

    def addOctave(self,nb):
        return Note(interval=super().addOctave(nb))
    
    def __add__(self,interval):
        return self.__class__(interval=interval+self)

    def correctAlteration(self):
        return  self.getAlteration().printable()

    
    def baseOctave(self):
        base=super().baseOctave()
        #debug("base octave of %s is %s"%(self,base))
        return Note(interval=base)
    
#Twelve notes around middle C (with F#=Gb twice), and the number of bemol to add for this key
twelve_notes=[
    (Note(diatonic=0,alteration=0),0),#C
    (Note(diatonic=-3,alteration=0),-1),#G
    (Note(diatonic=3,alteration=0),1),#F
    (Note(diatonic=1,alteration=0),-2),#D
    (Note(diatonic=-1,alteration=-1),2),#Bb
    (Note(diatonic=-2,alteration=0),-3),#A
    (Note(diatonic=2,alteration=-1),3),#Eb
    (Note(diatonic=2,alteration=0),-4),#E
    (Note(diatonic=-2,alteration=-1),4),#Ab
    (Note(diatonic=-1,alteration=0),-5),#B
    (Note(diatonic=1,alteration=-1),5),#Db
    (Note(diatonic=3,alteration=1),-6),#F#
    (Note(diatonic=-3,alteration=-1),6),#Gb
]

#debug("The twelve notes are %s",repr(twelve_notes))
