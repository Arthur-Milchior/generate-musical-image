#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Classes for notes. They are all represented as an interval from the middle C.
Difference between a note and an interval is:
-two notes can't be added(it's not actually checked)
-substracting notes lead to an interval
-the names are different
"""

import math
import solfege.interval
from solfege.interval import DiatonicInterval, ChromaticInterval, SolfegeInterval, Alteration, TooBigAlteration
from util import *


class _Note:
    """A note. Similar to an interval.

    -To a note may be added or substracted an interval, but not to a note
    -Two notes may be substracted, leading to an interval.

    """

    def isNote(self):
        return True

    def __neg__(self):
        raise Exception("Trying to negate a note makes no sens.")

    def __sub__(self, other):
        if isinstance(other, _Note):
            return self.subNote(other)
        else:
            return self.subInterval(other)
        # return self + (-other)
        # selfInterval=self.IntervalClass(toCopy=self)
        #         print(f"""
        # self:{self},
        # other:{other},
        # otherInterval:{otherInterval},
        # minusOtherInterval:{minusOtherInterval},
        # sub: {sub}.""")
        return sub

    def subInterval(self, other):
        subOtherInterval = -other
        sub = self + subOtherInterval
        return sub

    def subNote(self, other):
        return self.IntervalClass(self.getNumber() - other.getNumber())

    def __add__(self, other):
        if isinstance(other, _Note):
            raise Exception("Adding two notes")
        sum_ = super().__add__(
            other)  # Super still makes sens because a class inheriting _Note also inherits some other class.
        return sum_

    def __hash__(self):
        return super().__hash__()

    def getOctave(self, scientificNotation=False):
        """The octave.  By default, starting at middle c. If scientificNotation, starting at C0"""
        octave = super().getOctave()
        return octave + 4 if scientificNotation else octave


class DiatonicNote(_Note, DiatonicInterval):
    """A diatonic note"""
    # Saved as the interval from middle C
    IntervalClass = DiatonicInterval

    def getName(self):
        return ["c", "d", "e", "f", "g", "a", "b"][self.getNumber() % 7]

    # def __repr__(self):
    #     return Diatonic


class RoleNone(MyException):
    pass


class ChromaticNote(_Note, ChromaticInterval):
    IntervalClass = ChromaticInterval
    RelatedDiatonicClass = DiatonicNote
    role = ["unison", None, None, "third", "third", "third", "fifth", "fifth", "fifth", "interval", "interval",
            "interval"]

    def getColor(self, color=True):
        """Color to print the note in lilypond"""
        return "black"

    def getNoteName(self, withOctave=False):
        noteName = ["C", "C#", "D", "E♭", "E", "F", "F#", "G", "A♭", "A", "B♭", "B"][self.getNumber() % 12]
        octave = str(self.getOctave(scientificNotation=True)) if withOctave else ""
        return noteName + octave

    def getNote(self, Class=None):
        """A solfege note. Diatonic note is guessed. The default class is
        Note. May return None if no diatonic note can be guessed. """
        diatonic = self.getDiatonic()
        if diatonic is None:
            return None
        if Class is None:
            Class = Note
        diatonic = diatonic.getNumber()
        chromatic = self.getNumber()
        return Class(diatonic=diatonic, chromatic=chromatic)

    def lily(self, color=True):
        """Lilypond representation of this note. Colored according to
        getColor, unless color is set to False.
        """
        if ("lily", color) not in self.dic:
            diatonic = self.getDiatonic()
            try:
                alteration = self.getAlteration()
            except TooBigAlteration as tba:
                tba.addInformation("Note", self)
                tba.addInformation("Base note", self.base.getNote())
                tba.addInformation("Base pos", self.base)
                tba.addInformation("Interval", self.getInterval())
                tba.addInformation("Role", self.role)
                raise
            lily = f"{diatonic.getName()}{alteration.lily()}{self.getDiatonic().lilyOctave()}"
            if color:
                color = self.getColor()
                if color is None:
                    exception = MyException()
                    exception.addInformation("Note", self)
                    exception.addInformation("Base pos", self.base)
                    if self.base:
                        exception.addInformation("Base note", self.base.getNote())
                    else:
                        exception.addInformation("Base note", "no base")
                    exception.addInformation("Interval", self.getInterval())
                    exception.addInformation("Role", self.role)
                    raise exception
                lily = """\\tweak NoteHead.color  #(x11-color '%s)\n%s\n""" % (color, lily)
            self.dic[("lily", color)] = lily
        return self.dic[("lily", color)]


class Note(ChromaticNote, SolfegeInterval):
    IntervalClass = SolfegeInterval
    DiatonicClass = DiatonicNote
    ChromaticClass = ChromaticNote
    """A note of the scale, as an interval from middle C."""

    def __sub__(self, other):
        if isinstance(other, Note):
            return self.subNote(other)
        else:
            return self.subInterval(other)

    def subNote(self, other):
        diatonic = self.getDiatonic() - other.getDiatonic()
        chromatic = super().__sub__(other)
        print(f"""
        diatonic dif is {diatonic},""")

        return SolfegeInterval(
            diatonic=diatonic,
            chromatic=chromatic
        )

    def getName(self, kind=None):
        diatonic = self.getDiatonic()
        try:
            alteration = self.getAlteration()
        except TooBigAlteration as tba:
            tba.addInformation("Note", self)
            raise
        return f"{diatonic.getName().upper()}{alteration.getName(kind=kind)}"

    def correctAlteration(self):
        """Whether the note has a printable alteration."""
        return self.getAlteration().printable()


# Twelve notes around middle C (with F#=Gb twice), and the number of bemol to add for this key
twelve_notes = []
for (diatonic, alteration, nbBemol) in [(0, 0, 0),  # C
                                        (-3, 0, -1),  # G
                                        (3, 0, 1),  # F
                                        (1, 0, -2),  # D
                                        (-1, -1, 2),  # Bb
                                        (-2, 0, -3),  # A
                                        (2, -1, 3),  # Eb
                                        (2, 0, -4),  # E
                                        (-2, -1, 4),  # Ab
                                        (-1, 0, -5),  # B
                                        (1, -1, 5),  # Db
                                        (3, 1, -6),  # F#
                                        # (-3,-1,6),#Gb
                                        ]:
    note = Note(diatonic=diatonic, alteration=alteration)
    twelve_notes.append((note, nbBemol))
    # print("Diatonic %s, alteration=%s, note %s"%(diatonic,alteration,note))
#     (Note(diatonic=0,alteration=0),0),#C
#     (Note(diatonic=-3,alteration=0),-1),#G
#     (Note(diatonic=3,alteration=0),1),#F
#     (Note(diatonic=1,alteration=0),-2),#D
#     (Note(diatonic=-1,alteration=-1),2),#Bb
#     (Note(diatonic=-2,alteration=0),-3),#A
#     (Note(diatonic=2,alteration=-1),3),#Eb
#     (Note(diatonic=2,alteration=0),-4),#E
#     (Note(diatonic=-2,alteration=-1),4),#Ab
#     (Note(diatonic=-1,alteration=0),-5),#B
#     (Note(diatonic=1,alteration=-1),5),#Db
#     (Note(diatonic=3,alteration=1),-6),#F#
#     (Note(diatonic=-3,alteration=-1),6),#Gb
# C#
#
# G#

# D#

# A#

# E#

# B#
# ]

# debug("The twelve notes are %s",repr(twelve_notes))
ChromaticNote.RelatedSolfegeClass = Note
