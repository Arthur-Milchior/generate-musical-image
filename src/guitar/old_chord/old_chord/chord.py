# from enum import Enum
# from typing import Dict, Optional, Tuple
# import lily.lily
# from solfege.value.interval.set_of_intervals import intervals
# from solfege.value.interval import ChromaticInterval
# from solfege.value.note.note import Note
# from solfege.value.note.with_tonic import ChromaticNoteWithTonic
# from guitar.old_chord.util import MINIMAL_NUMBER_OF_STRINGS_IN_A_CHORD
# from solfege.pattern.chord.chord_pattern import ChordPattern
# from guitar.position.fret import NOT_PLAYED, OPEN_FRET, Fret
# from guitar.position.guitar_position import GuitarPosition
# from guitar.position.set_of_guitar_positions import SetOfGuitarPositions
# from guitar.position.string import String
# from utils.util import assert_all_same_class

# class GuitarChordKind(Enum):
#     TRANSPOSABLE = "transposable"
#     OPEN = "open"
#     NOT_A_CHORD = "not_a_chord"



# class GuitarChord(SetOfGuitarPositions):
#     """A chord. That is, a fret by string. 0 for empty string.
#     We assume at least one note is played.
#     """

#     def __init__(self, frets: Tuple[Fret, Fret, Fret, Fret, Fret, Fret, ]): # type: ignore
#         """dic: a 6-tuple. The element at index i corresponds to string i+1. It's 0 for free string, None for not played, and otherwise the fret number."""
#         positions = frozenset({GuitarPosition(i + 1, frets[i]) for i in range(0, 6)})
#         super().__init__(positions)
#         self.tuple = frets
#         assert [position for position in positions  if position is not None], positions# at least one position is played


#     def anki(self):
#         """return the tuple (pos1,pos3,pos5,posn)

#         pos1 is the string of length 6, whose x represents a string not played, . a string played, but not for note tonic, and 1 represents a string played for the tonic.
#         pos3, pos5  are similar for third and fifth. posn is used for 6th or 7th
#         """
#         text = ""
#         for (number, intervals()) in [("1", {ChromaticInterval(0)}),
#                                         ("3", {ChromaticInterval(3), ChromaticInterval(4)}),
#                                         ("5", {ChromaticInterval(6), ChromaticInterval(7)}),
#                                         ("n", {ChromaticInterval(9), ChromaticInterval(10), ChromaticInterval(11)})]:
#             text += ","
#             for i in self.chord:
#                 interval = self.chord[i].get_interval()
#                 if interval is None:
#                     text += "x"
#                 else:
#                     if interval in intervals():
#                         text += number
#                     else:
#                         text += "."
#         return text

#     def file_name_base(self):
#         return "".join(fret.name() for fret in self.tuple)

#     def file_name(self):
#         return self.file_name_base()

#     def playable(self):
#         """At most three frets not being on fret 0 or 1"""
#         number_of_fret_greater_than_one = 0  # nb of fret >1 played.
#         number_of_fret_one = 0  # nb of fret 1 played
#         min_fret = None  # least non 0 fret played
#         max_fret = None  # greatest fret played
#         for fret in self.tuple:
#             if fret.value is None:
#                 continue
#             if fret.value > 0:
#                 min_fret = min(fret, min_fret) if min_fret is not None else fret
#             max_fret = max(fret, max_fret) if max_fret is not None else fret
#             if fret.value == 1:
#                 number_of_fret_one += 1
#             if fret.value > 1:
#                 number_of_fret_greater_than_one += 1

#         if max_fret - min_fret > 4:
#             return False
#         elif self.is_open():
#             if number_of_fret_greater_than_one + number_of_fret_one > 4:
#                 return False
#         else:  # not open chord
#             if number_of_fret_greater_than_one > 3:
#                 return False
#         return True

#     def enough_strings(self):
#         return len(self.chord) >= MINIMAL_NUMBER_OF_STRINGS_IN_A_CHORD

#     def is_chord(self):
#         """Whether this is both a standard chord, with at least 4 note, and can actually be played"""
#         return self.is_standard_chord() and self.playable() and self.enough_strings()

#     def _lowest_fret(self) -> Optional[Fret]:
#         return min(pos.fret for pos in self.chord if pos is not None) if self.chord else None

#     def is_open(self) -> bool:
#         lowest_fret = self._lowest_fret()
#         return lowest_fret is not None and lowest_fret == OPEN_FRET

#     def is_lowest_fret_one(self):
#         lowest_fret = self._lowest_fret()
#         return lowest_fret is not None and lowest_fret == Fret(1)

#     def is_open_chord(self):
#         """whether one string is played open, and it is actually a chord"""
#         return self.is_open() and self.is_chord()

#     def is_transposable_chord(self):
#         """whether it is a chord, and its minimal element is one"""
#         return self.is_lowest_fret_one() and self.is_standard_chord() and self.playable() and self.enough_strings()

#     def in_chords_list(self):
#         """Whether the chord played by this set of guitar position belongs to """
#         return True if ChordPattern.get_patterns_from_chromatic_interval(self.intervals_frow_lowest_note()) else False

#     def lily_in_scale(self):
#         return lily.lily.chord(self.notes())

#     def kind(self):
#         """transposable(1 as first string), open, or None"""
#         if self.is_open():
#             return GuitarChordKind.OPEN
#         elif self.is_lowest_fret_one():
#             return GuitarChordKind.TRANSPOSABLE
#         else:
#             return GuitarChordKind.NOT_A_CHORD
      

#     def anki(self):
#         """A string containing the kind of Third, of fifth, and of quality"""
#         return f"{self.third()},{self.fifth()},{self.quality()}"

#     # def contains_wrong_note(self):
#     #     """Whether it contains an interval which should not be present in a standard reversed chord"""
#     #     if ChromaticInterval(1) in self.intervals_frow_lowest_note():
#     #         return  True
#     #     if ChromaticInterval(2) in self.intervals_frow_lowest_note():
#     #         return  True
#     #     if ChromaticInterval(5) in self.intervals_frow_lowest_note():
#     #         return  True
#     #     return  False

#     # def is_standard_chord(self):
#     #     """Given a set of note, is it a standard chord. I.e.:
#     #     -has a tonic
#     #     -has a third
#     #     -has a fifth diminshed only if its third is minor
#     #     -has either a fifth or a quality
#     #     """
#     #     if self.contains_wrong_note():
#     #         return  False
#     #     third = self.third()
#     #     if third == Third.BOTH or third == Third.NONE:
#     #         return  False
#     #     fifth = self.fifth()
#     #     if fifth == Fifth.MULTIPLE or fifth == Fifth.NONE or fifth == Fifth.NOT_APPLICABLE:
#     #         return  False
#     #     quality = self.quality()
#     #     if quality == Quality.MULTIPLE:
#     #         return  False
#     #     if not self.contains_tonic():
#     #         return  False
#     #     if not self.contains567():
#     #         return  False
#     #     return True

#     def get_pattern_name(self):
#         chord = ChordPattern.get_patterns_from_chromatic_interval(self.intervals_frow_lowest_note())
#         if chord is None:
#             return None
#         else:
#             return chord.first_of_the_names()

#     def get_really_descriptive_name(self, withKind=True):
#         """Name of chord, assuming it is standard"""
#         if self.is_fifth_dimished():
#             fifthName = "-Dim"
#         elif self.is_fifth_augmented():
#             fifthName = "-Aug"
#         else:
#             # if self.isFifthJust():
#             fifthName = ""
#         # else:
#         #     fifthName = "-None"
#         quality_name = self.quality()
#         if quality_name:
#             quality_name = f"-{quality_name}"
#         if quality_name == "-6" and self.is_fifth_dimished():
#             quality_name = "-dim7"
#             fifthName = ""
#         if quality_name == "-7maj" and self.is_fifth_augmented():
#             quality_name = "-7"

#         if withKind:
#             if self.is_open():
#                 pos = "open-"
#             else:
#                 pos = "transposable-"
#         else:
#             pos = ""
#         return f"{pos}{self.third()}{fifthName}{quality_name}"
