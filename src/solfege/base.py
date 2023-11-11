#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .interval import DiatonicInterval, SolfegeInterval, TooBigAlteration  # , _Interval
from .note import DiatonicNote, ChromaticNote, Note, _Note


class IntervalWithNoRole(MyException):
    """Raised when the difference between base note and an interval has no role. I.e. is 1 or 2."""
    pass


class _NoteWithBase(_Note):
    """
    Classes for notes with base. They are a note, with an additional information representing the tonic.
    """

    def __init__(self, toCopy=None, base=None, **kwargs):
        super().__init__(toCopy=toCopy, **kwargs)
        self.base = None
        if isinstance(toCopy, _NoteWithBase):
            base = toCopy.getBase()
        if base is not None:
            self.addBase(base)

    def __add__(self, other):
        sum_ = super().__add__(other)
        base = self.getBase()
        if base is not None:
            sum_.addBase(base)
        return sum_

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        return super().__eq__(other) and self.getBase() == other.getBase()

    def addBase(self, base):
        assert (base is not None)
        self.base = base
        if self.__class__ != base.__class__:
            raise Exception("Adding a base of a type %s distinct from the class %s" % (base.__class__, self.__class__))

        # if self.hasNumber():
        #     role=self.__class__.role[(self.getNumber()-base.getNumber())%self.__class__.modulo]
        #     if role is None:
        #         raise IntervalWithNoRole#Exception("Adding base %s whose number is %d to note %s, (interval=%s)  the role is None, from %s[%d%%%d=%d]"%(base,base.getNumber(),self,self.interval,self.__class__.role,self.interval.getNumber(),self.__class__.modulo,self.interval.getNumber()%self.__class__.modulo))
        #     self.role= role
        #     #debug("The role of %s is %s"%(self,role))

    def getInterval(self):
        """interval between the note and its base"""
        if "interval" not in self.dic:
            if self.base is None or self.value is None:
                self.dic["interval"] = None
            else:
                self.dic["interval"] = self - self.base
        return self.dic["interval"]

    def getRole(self):
        """The role of this note, assuming its in a major scale"""
        if "role" not in self.dic:
            interval = self.getInterval()
            interval = interval.get_number() % self.modulo
            role = self.role[interval]
            self.dic["role"] = role
        return self.dic["role"]

    def getBase(self):
        return self.base


class DiatonicNoteWithBase(_NoteWithBase, DiatonicNote):
    # Saved as the interval from middle C
    role = ["Tonic", "supertonic", "mediant", "subdominant", "dominant", "submediant", "leading"]


class ChromaticNoteWithBase(_NoteWithBase, ChromaticNote):
    RelatedDiatonicClass = DiatonicNoteWithBase

    def getColor(self, color=True):
        if color:
            dic = {"unison": "black", "third": "violet", "fifth": "red", "interval": "green", None: None}
            return dic[self.getRole()]
        else:
            return "black"

    def get_diatonic(self):
        """Assuming no base is used"""
        if "diatonic" not in self.dic:
            if self.getNumber() is None:
                diatonic = None
            elif self.getBase() is None:
                raise Exception("Diatonic asked when the current note %s has no base" % self)
            elif self == self.getBase():
                # If we can't use the base to determine the diatonic note, we take the more likely one
                diatonic = super().get_diatonic()
                diatonic.addBase(diatonic)
            else:
                # Otherwise, we use the role to figure out which diatonic note to use
                role = self.getRole()
                diatonicNumber = {"unison": 0, "third": 2, "fifth": 4, "interval": 6}[role]
                diatonicIntervalBaseOctave = DiatonicInterval(diatonic=diatonicNumber)
                octave = self.getInterval().get_octave()
                diatonicInterval = diatonicIntervalBaseOctave.add_octave(octave)
                diatonic = self.base.get_diatonic() + diatonicInterval
                diatonic.addBase(self.base.get_diatonic())
                debug("Note %s's diatonic is not base. Its interval is %s and its diatonic is %s" % (
                self, diatonicInterval, diatonic))
            self.dic["diatonic"] = diatonic
        return self.dic["diatonic"]

    def getNote(self):
        note = super().getNote(Class=NoteWithBase)
        base = self.getBase()
        if self is base:
            note.addBase(note)
        elif base is not None:
            note.addBase(base.getNote())
        return note


class NoteWithBase(ChromaticNoteWithBase, Note):
    IntervalClass = SolfegeInterval
    DiatonicClass = DiatonicNote
    ChromaticClass = ChromaticNote
    """A note of the scale, as an interval from middle C."""

    def get_name(self, forFile=None):
        """The name of this note.

        Args: `forFile` -- whether we should avoid non ascii symbol"""
        diatonic = self.get_diatonic()
        try:
            alteration = self.get_alteration()
        except TooBigAlteration as tba:
            tba.addInformation("Note", self)
            raise
        diatonicName = diatonic.get_name().upper()
        alterationName = alteration.get_name(forFile=forFile)
        return "%s%s" % (diatonicName, alterationName)

    def correctAlteration(self):
        return self.get_alteration().printable()


ChromaticNoteWithBase.RelatedSolfegeClass = NoteWithBase
