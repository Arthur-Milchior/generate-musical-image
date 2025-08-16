from __future__ import annotations

from typing import Optional

from lily.Lilyable.local_lilyable import LocalLilyable
from solfege.interval.interval import Interval, third_minor
from solfege.note import ChromaticNote, DiatonicNote
from solfege.note.abstract import low_and_high
from solfege.note.alteration import Alteration, alteration_symbols


class Note(Interval, ChromaticNote, LocalLilyable):
    IntervalClass = Interval
    DiatonicClass = DiatonicNote
    ChromaticClass = ChromaticNote
    """A note of the scale, as an interval from middle C."""

    def __init__(self, name: Optional[str] = None, *args, **kwargs):
        if name is not None:
            name = name.strip()
            diatonic_name = "".join(letter for letter in name if letter not in alteration_symbols)
            alteration_name = "".join(letter for letter in name if letter in alteration_symbols)
            diatonic = DiatonicNote.from_name(diatonic_name)
            chromatic_from_diatonic = diatonic.get_chromatic()
            alteration = Alteration.from_name(alteration_name)
            kwargs["diatonic"] = diatonic.get_number()
            kwargs["alteration"] = alteration
            kwargs["chromatic"] = (chromatic_from_diatonic + alteration).get_number()
        super().__init__(*args, **kwargs)

    def __neg__(self):
        raise Exception("Trying to negate a note makes no sens.")

    def sub_note(self, other: Note):
        diatonic = self.get_diatonic() - other.get_diatonic()
        chromatic = self.get_chromatic().__sub__(other)

        return Interval(
            diatonic=diatonic.get_number(),
            chromatic=chromatic.get_number()
        )

    def lily_in_scale(self):
        """For example "bes'"."""
        return f"{self.get_diatonic().lily_in_scale()}{self.get_alteration().lily_in_scale()}{self.get_diatonic().get_octave_name_lily()}"

    def get_symbol_name(self, fixed_length: bool = True):
        """The name of this note.

        For example "C#" or "C# "
        Args: usage -- see Alteration file."""
        return f"{self.get_diatonic().get_name_up_to_octave()}{self.get_alteration().get_symbol_name(fixed_length = fixed_length)}"

    def get_ascii_name(self, fixed_length: bool = True):
        """The name of this note.

        Example "C3sharp"

        Args: usage -- see Alteration file."""
        return f"{self.get_diatonic().get_name_with_octave()}{self.get_alteration().get_ascii_name(fixed_length=fixed_length)}"

    def get_name_up_to_octave(self, ascii: bool= False):
        if ascii:
            return self.get_ascii_name(fixed_length=False)
        raise NotImplemented

    def get_full_name(self, fixed_length: bool = True):
        """
        Example "C# 4" or "C#4"
        """
        return f"{self.get_symbol_name(fixed_length = fixed_length)}{self.get_octave() + 4}"

    def correctAlteration(self):
        """Whether the note has a printable alteration."""
        return self.get_alteration().printable()

    def adjacent(self, other: Note):
        """Whether `other` is at most two half-tone away"""
        lower, higher = low_and_high(self, other)
        diff = higher - lower
        assert diff.value > 0
        if diff.value <= 2:
            return True
        if diff.value > 3:
            return False
        if higher.get_in_base_octave().value in [0, 1, 2, 5, 6, 7]:  # C or F natural
            return False
        return True

    def is_white_key_on_piano(self):
        """Whether this note corresponds to a black note of the keyboard"""
        return not self.is_black_key_on_piano()

    def is_black_key_on_piano(self):
        """Whether this note corresponds to a black note of the keyboard"""
        blacks = {1, 3, 6, 8, 10}
        return (self.get_chromatic().get_number() % 12) in blacks

    def simplest_enharmonic(self):
        """Enharmonic note, with 0 alteration if possible or one of the same alteration"""
        enharmonic = self
        while enharmonic.get_alteration().value >= 2:
            # double sharp at least, let's add a diatonic note
            enharmonic += Interval(diatonic=1, chromatic=0)
        while enharmonic.get_alteration().value <= -2:
            # double flat at least, let's remove a diatonic note
            enharmonic += Interval(diatonic=-1, chromatic=0)
        if enharmonic.get_alteration().value == 1:
            # It's a sharp note. Let's check if adding a diatonic note lead to a white key
            above = enharmonic + Interval(diatonic=1, chromatic=0)
            if above.is_white_key_on_piano():
                return above
        if enharmonic.get_alteration().value == -1:
            # It's a flat note. Let's check if removing a diatonic note lead to a white key
            below = enharmonic + Interval(diatonic=-1, chromatic=0)
            if below.is_white_key_on_piano():
                return below
        return enharmonic

    def canonize(self, for_sharp: bool):
        """Enharmonic note, with no alteration if possible or a single sharp"""
        enharmonic = self
        while enharmonic.get_alteration().value > (1 if for_sharp else 0):
            # too many sharp least, let's add a diatonic note
            enharmonic += Interval(diatonic=1, chromatic=0)
        while enharmonic.get_alteration().value < (0 if for_sharp else -1):
            # too many flat, let's remove a diatonic note
            enharmonic += Interval(diatonic=-1, chromatic=0)
        if enharmonic.get_alteration().value == 1:
            # It's a sharp note. Let's check if adding a diatonic note lead to a white key
            above = enharmonic + Interval(diatonic=1, chromatic=0)
            if above.is_white_key_on_piano():
                return above
        if enharmonic.get_alteration().value == -1:
            # It's a flat note. Let's check if removing a diatonic note lead to a white key
            below = enharmonic + Interval(diatonic=-1, chromatic=0)
            if below.is_white_key_on_piano():
                return below
        return enharmonic

    def is_natural(self):
        return self.get_alteration() == Alteration(0)

    def is_sharp(self):
        return self.get_alteration() == Alteration(1)

    def is_flat(self):
        return self.get_alteration() == Alteration(-1)

    def is_double_sharp(self):
        return self.get_alteration() == Alteration(2)

    def is_double_flat(self):
        return self.get_alteration() == Alteration(-2)
