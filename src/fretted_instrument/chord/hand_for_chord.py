

from dataclasses import dataclass
from enum import Enum
from turtle import done
from typing import List, Optional, Tuple

from fretted_instrument.chord.fretted_instrument_chord import Barred, ChordOnFrettedInstrument
from fretted_instrument.chord.playable import Playable
from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from fretted_instrument.position.fret.fret import Fret
from fretted_instrument.position.fret.fret_deltas import FretDelta
from fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from fretted_instrument.position.string.string import String, StringFrozenList
from utils.frozenlist import FrozenList
from utils.util import assert_typing


@dataclass(frozen=True)
class HandForChordForFrettedInstrument:
    instrument: FrettedInstrument

    """The thumb. If played, it's on the first string."""
    zero_fret: Optional[Fret] = None

    """The index for potentially a barred note. """
    one: Optional[PositionOnFrettedInstrument] = None
    barred: Barred = Barred.NO
    two: Optional[PositionOnFrettedInstrument] = None
    three: Optional[PositionOnFrettedInstrument] = None
    four: Optional[PositionOnFrettedInstrument] = None
    opens: StringFrozenList = StringFrozenList() 

    @staticmethod
    def _make_hand_for_only_zero(fretted_instrument_chord: ChordOnFrettedInstrument):
        """Special case of `make` where no closed strings are present. Of course, no left-hand finger are used. """
        #It's easier to consider this case separately
        return HandForChordForFrettedInstrument(fretted_instrument_chord.instrument, opens =[pos.string for pos in fretted_instrument_chord if pos.fret.is_open()])

    @staticmethod
    def make(fretted_instrument_chord: ChordOnFrettedInstrument, potential_thumb: bool = False):
        assert_typing(fretted_instrument_chord, ChordOnFrettedInstrument)
        assert not potential_thumb
        # Searching whether there is any closed position.
        for pos in fretted_instrument_chord:
            if pos.fret.is_closed():
                return HandForChordForFrettedInstrument.make_hand_for_closed(chord_on_fretted=fretted_instrument_chord, potential_thumb=potential_thumb)
        #It's easier to consider the case where all notes are open separately
        return HandForChordForFrettedInstrument._make_hand_for_only_zero(fretted_instrument_chord)

    @staticmethod
    def make_hand_for_closed(chord_on_fretted: ChordOnFrettedInstrument, potential_thumb:bool = False) -> Optional["HandForChordForFrettedInstrument"]:
        assert_typing(chord_on_fretted, ChordOnFrettedInstrument)
        assert not potential_thumb
        #TODO deal with thumb
        barred = chord_on_fretted.is_barred()
        # Ordered according to fret, and in case of equality string.
        played_positions_remaining_to_finger = list(sorted(chord_on_fretted.played_positions(), key=lambda pos: (pos.fret.value, pos.string.value)))
        # Remove open fret
        opens: List[String] = []
        while played_positions_remaining_to_finger and played_positions_remaining_to_finger[0].fret.is_open():
            # Pop 0 is not efficient. But the list has 6 elements so it does not matter.
            open = played_positions_remaining_to_finger.pop(0)
            opens.append(open.string)
        one = played_positions_remaining_to_finger.pop(0)
        if barred != Barred.NO:
            while played_positions_remaining_to_finger and played_positions_remaining_to_finger[0].fret == one.fret:
                # covered by the bar.
                played_positions_remaining_to_finger.pop(0)
        if len(played_positions_remaining_to_finger) > 3:
            return None
        four = played_positions_remaining_to_finger.pop() if played_positions_remaining_to_finger else None
        if len(played_positions_remaining_to_finger) == 2:
            three = played_positions_remaining_to_finger.pop()
            two = played_positions_remaining_to_finger.pop()
        elif not played_positions_remaining_to_finger:
            two = three = None  
        else:
            position = played_positions_remaining_to_finger.pop()
            if position.fret.value <= one.fret.value + 1:
                two = position
                three = None
            else:
                three = position
                two = None
        assert not played_positions_remaining_to_finger
        return HandForChordForFrettedInstrument(instrument = chord_on_fretted.instrument, zero_fret = None, one=one, barred=barred, two=two, three=three, four=four, opens=StringFrozenList(opens))

    def playable(self) -> Playable:
        non_zero_position = [self.one, self.two, self.three, self.four]
        optional_frets = [self.zero_fret] + [pos.fret if pos is not None else None for pos in non_zero_position]
        for lower_finger in range(4): #e.g. index
            lower_fret = optional_frets[lower_finger] # expected to be the lowest fret value.
            if lower_fret is None:
                continue
            for higher_finger in range(lower_finger+1, 5): # e.g. pink
                higher_fret = optional_frets[higher_finger-1] #expected to be the greatest fret value
                if higher_fret is None or lower_fret is None:
                    continue
                delta = higher_fret - lower_fret # expected to be non negative. (Exception if lower finger is the thumb)
                fret_delta: FretDelta = self.instrument.finger_to_fret_delta[lower_finger][higher_finger]
                if not fret_delta.contains_delta(delta.value):
                    return Playable.NO
        return Playable.EASY
    
    def __post_init__(self):
        for pos in (self.zero_fret, self.one, self.two, self.three, self.four):
            if pos is not None:
                assert pos.fret.is_played()
        if self.barred is not Barred.NO:
            assert self.one is not None
            assert self.one.string != self.instrument.last_string()
            """Barred mean two strings at least"""

    def not_barred_positions(self):
        l = [PositionOnFrettedInstrument(self.instrument, self.instrument.string(1), self.zero_fret) if self.zero_fret else None, self.one if not self.barred else None, self.two, self.three, self.four]
        return [pos for pos in l if pos is not None]
    
    def positions(self):
        positions = self.not_barred_positions()
        if self.barred:
            barred_fret = self.one.fret
            barred_string = self.one.string
            while barred_fret <= self.instrument.last_string():
                positions.append(PositionOnFrettedInstrument(self.instrument, barred_string, barred_fret))
                barred_string += 1
        return ChordOnFrettedInstrument.make(positions)

    def are_all_fingers_useful(self):
        """Returns false if a finger is hidden by another one."""
        strings = []
        for pos in self.not_barred_positions():
            if pos is not None:
                string = pos.string
                if string in strings:
                    return False
                strings.append(string)

        """Looking whether the bar hides another finger"""
        if self.barred:
            for pos in self.not_barred_positions():
                if pos.fret <= self.one.fret and pos.string >= self.one.string:
                    return False
        return True
        