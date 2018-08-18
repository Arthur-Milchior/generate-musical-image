#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

list_chromatic =[0,2,4,5,7,9,11]
blacks = {1,3,6,8, 10}

class Name:
    """Associating tonic, supertonic, etc.. to its number of interval"""
    def __init__(self,name):
        self.di = name

    def toChromaticInterval(self):
        return 12*self.octave() + list_chromatic[self.di % 7]

    def __add__(self,other):
        return Name(self.di+other.di)

    def getKeyName(self):
        return ["c","d","e","f","g","a","b"][self.di %7]
    def getTitleName(self):
        return ["C","D","E","F","G","A","B"][self.di %7]

    def octave(self):
        return math.floor(self.di/7)

    def addOctave(self,nb):
        return Name(self.di+nb*7)
    
    def printOctave(self):
        octave = self.octave()
        octaveShift = octave +1
        if octaveShift>0:
            return  "'"*octaveShift
        elif octaveShift<0:
            return ","*(-octaveShift)
        else:
            return ""
    def __eq__(self,other):
        return self.di == other.di
    def sameNoteDistinctOctave(self,other):
        return not((self.di -other.di) %7)
    def baseOctave(self):
        return Name(self.di % 7)

class Alteration:
    def __init__(self, alteration):
        self.alt = alteration

    def correct(self):
        return  -2 <= self.alt <=2

    def __str__(self):
        return ["eses","es","","is","isis"][self.alt+2]
    def __eq__(self,other):
        return self.alt == other.alt
    def nameForFile(self):
        return ["bemol","","sharp"][self.alt+1]
    def nameForTitle(self):
        return ["♭","","#"][self.alt+1]
    def getTitleName(self):
        return ["♭♭","♭","","#","##"][self.alt+2]

class Interval:
    """An interval, which is composed of a number of diatonic note, and number of half-tone to add to it."""
    def __init__(self,name, alteration,usingChromaticInterval=False):
        self.diatonicInterval=name
        octave= math.floor(name.di/7)
        noteInBaseOctave = name.di % 7
        if usingChromaticInterval:
            self.alteration=Alteration(alteration-list_chromatic[noteInBaseOctave]-(12*octave))
        else: 
            self.alteration = alteration

    def toChromaticInterval(self):
        return self.diatonicInterval.toChromaticInterval()+self.alteration.alt

    def __repr__(self):
        return "(%d,%d)"%(self.diatonicInterval.di,self.alteration.alt)
        
    def __add__(self,other):
        name = self.diatonicInterval+other.diatonicInterval
        alteration=self.toChromaticInterval()+other.toChromaticInterval()
        return Interval(name,alteration, usingChromaticInterval=True)

    def addOctave(self,octave):
        return Interval(self.diatonicInterval.addOctave(octave),self.alteration)

    def __eq__(self,other):
        return self.alteration == other.alteration and self.diatonicInterval == other.diatonicInterval
    def debug(self):
        return "name:%d, alteration:%d, octave:%d"%(self.diatonicInterval.di, self.alteration.alt,self.diatonicInterval.octave())

    def baseOctave(self):
        return Interval(self.diatonicInterval.baseOctave(),self.alteration)

class Note:
    """A note of the scale, as an interval from middle C."""
    
    def __init__(self, interval):
        self.interval = interval

    def printLily(self):
        return self.interval.diatonicInterval.getKeyName()+str(self.interval.alteration)+self.interval.diatonicInterval.printOctave()

    def nameForFile(self):
        return self.interval.diatonicInterval.getTitleName()+self.interval.alteration.nameForFile()
    def nameForTitle(self):
        return self.interval.diatonicInterval.getKeyName()+self.interval.alteration.nameForTitle()
    
    def isBlack(self):
        return (self.interval.toChromaticInterval()%12) in blacks

    def addOctave(self,octave):
        return Note(self.interval.addOctave(octave))
    
    def __add__(self,interval):
        return Note(self.interval+interval)

    def correctInterval(self):
        return  -2 <= self.interval.alt <=2
    def __eq__(self,other):
        return self.interval == other.interval
    def debug(self):
        return self.interval.debug()

    def getTitleName(self):
        return self.interval.diatonicInterval.getTitleName()+self.interval.alteration.getTitleName()
    
    def baseOctave(self):
        return Note(self.interval.baseOctave())

    def nbSemiToneFromC(self):
        return self.interval.toChromaticInterval()
    
    def __hash__(self):
        return self.nbSemiToneFromC()
    def octave(self):
        return self.interval.diatonicInterval.octave()

#Twelve notes around middle C (with F#=Gb twice), and the number of bemol to add for this key
twelve_notes=[
    (Note(Interval(Name(0),Alteration(0))),0),#C
    (Note(Interval(Name(-3),Alteration(0))),-1),#G
    (Note(Interval(Name(3),Alteration(0))),1),#F
    (Note(Interval(Name(1),Alteration(0))),-2),#D
    (Note(Interval(Name(-1),Alteration(-1))),2),#Bb
    (Note(Interval(Name(-2),Alteration(0))),-3),#A
    (Note(Interval(Name(2),Alteration(-1))),3),#Eb
    (Note(Interval(Name(2),Alteration(0))),-4),#E
    (Note(Interval(Name(-2),Alteration(-1))),4),#Ab
    (Note(Interval(Name(-1),Alteration(0))),-5),#B
    (Note(Interval(Name(1),Alteration(-1))),5),#Db
    (Note(Interval(Name(3),Alteration(1))),-6),#F0,#
    (Note(Interval(Name(-3),Alteration(-1))),6),#Gb
]

