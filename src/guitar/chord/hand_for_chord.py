

from dataclasses import dataclass
from enum import Enum
from turtle import done
from typing import List, Optional, Tuple

from guitar.chord.guitar_chord import Barred, GuitarChord
from guitar.chord.playable import Playable
from guitar.position.fret.fret import NOT_PLAYED, Fret
from guitar.position.guitar_position import GuitarPosition
from guitar.position.set_of_guitar_positions import SetOfGuitarPositions
from guitar.position.string.string import String, strings
from utils.frozenlist import FrozenList
from utils.util import assert_typing


@dataclass(frozen=True)
class HandForGuitarChord:

    """The thumb. If played, it's on the first string."""
    zero_fret: Optional[Fret] = None

    """The index for potentially a barred note. """
    one: Optional[GuitarPosition] = None
    barred: Barred = Barred.NO
    two: Optional[GuitarPosition] = None
    three: Optional[GuitarPosition] = None
    four: Optional[GuitarPosition] = None
    opens: FrozenList[String] = FrozenList({}) 

    @staticmethod
    def make_hand_for_only_zero(guitar_chord: GuitarChord):
        return HandForGuitarChord(opens =[pos.string for pos in guitar_chord if pos.fret.is_open()])

    @staticmethod
    def make(guitar_chord: GuitarChord, potential_thumb: bool = False):
        assert_typing(guitar_chord, GuitarChord)
        assert not potential_thumb
        for pos in guitar_chord:
            if pos.fret.is_closed():
                return HandForGuitarChord.make_hand_for_closed(guitar_chord=guitar_chord, potential_thumb=potential_thumb)
        return HandForGuitarChord.make_hand_for_only_zero(guitar_chord)

    @staticmethod
    def make_hand_for_closed(guitar_chord: GuitarChord, potential_thumb:bool = False) -> Optional["HandForGuitarChord"]:
        assert_typing(guitar_chord, GuitarChord)
        assert not potential_thumb
        #TODO deal with thumb
        barred = guitar_chord.is_barred()
        # Ordered according to fret, and in case of equality string.
        played_positions_remaining_to_finger = list(sorted(guitar_chord.played_positions(), key=lambda pos: (pos.fret.value, pos.string.value)))
        # Remove open fret
        opens = []
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
        return HandForGuitarChord(zero_fret = None, one=one, barred=barred, two=two, three=three, four=four, opens=FrozenList(opens))

    def playable(self) -> Playable:
        easy = True
        if self.zero_fret is not None:
            zero_value = self.zero_fret.value
            for (pos, possible_strings, possible_frets) in [
                (self.one, (strings[3], strings[4], strings[5]), range(zero_value - 1, zero_value + 2)),
                (self.two, (strings[2], strings[3], strings[4], strings[5]), range(zero_value, zero_value + 3)),
                (self.three, strings, range(zero_value, zero_value + 3)),
                (self.four, strings, range(zero_value, zero_value + 3)),
            ]:
                if pos is not None:
                    if not pos.fret.value in possible_frets:
                        return Playable.NO
                    if not pos.string in possible_strings:
                        return Playable.NO
        restrictions : List[Tuple[GuitarPosition, GuitarPosition, List[int], List[int]]] = [
            (self.one, self.two, [0, 1], [2]),
            (self.one, self.three, [0, 1, 2], [3]),
            (self.one, self.four, [0, 1, 2, 3], [4]),
            (self.two, self.three, [0, 1], [2]),
            (self.two, self.four, [0, 1, 2], [3]),
            (self.three, self.four, [0, 1], [2]),
        ]
        for (first_pos, second_post, easy_frets_distance, hard_frets_distance) in restrictions:
            # TODO: the last finger string should not be two high about the previous to last
            if first_pos is not None and second_post is not None:
                fret_delta = second_post.fret.value - second_post.fret.value
                if fret_delta in hard_frets_distance:
                    easy = False
                elif fret_delta not in easy_frets_distance:
                    return Playable.NO
        return Playable.EASY if easy else Playable.YES

    def __post_init__(self):
        for pos in (self.zero_fret, self.one, self.two, self.three, self.four):
            if pos is not None:
                assert pos.fret.is_played()
        if self.barred is not Barred.NO:
            assert self.one is not None
            assert self.one.string != strings[5]
            """Barred mean two strings at least"""

    def not_barred_positions(self):
        l = [GuitarPosition(strings[0], self.zero_fret) if self.zero_fret else None, self.one if not self.barred else None, self.two, self.three, self.four]
        return [pos for pos in l if pos is not None]
    
    def positions(self):
        positions = self.not_barred_positions()
        if self.barred:
            barred_fret = self.one.fret
            barred_string = self.one.string
            while barred_fret <= strings[5]:
                positions.append(GuitarPosition(barred_string, barred_fret))
                barred_string += 1
        return GuitarChord.make(positions)

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
        