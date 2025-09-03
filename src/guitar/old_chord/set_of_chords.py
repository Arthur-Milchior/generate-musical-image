# from typing import Counter, Dict, Generator, List, Union
# from guitar.position.guitar_position import HIGHEST_FRET, GuitarPosition
# from utils.util import MyException
# from guitar.old_chord.util import *
# from guitar.old_chord.old_chord.chord import GuitarChord


# class IntervalWithNoRole(MyException):
#     """Raised when the difference between base note and an interval has no role. I.e. is 1 or 2."""
#     pass


# class SetOfSameChord:
#     def __init__(self, kind,
#                  # name,
#                  patternName,
#                  third,
#                  fifth,
#                  quality,
#                  minChromatic=None,
#                  ):
#         self.kind = kind
#         self.minChromatic = minChromatic
#         # self.name=name
#         self.patternName = patternName
#         self.third = third
#         self.fifth = fifth
#         self.quality = quality
#         self.set_ = []

#     # def getName(self):
#     #     return self.name
#     def getPatternName(self):
#         return self.patternName

#     def addChord(self, chord: GuitarChord):
#         """Add the chord to the set, if it is not contained in a chord, with same starting position, same name, and both open or both transposable. Remove chords contained in 'chord', if they satisfy the preceding conditions. 

#         return whether the chord was added.
#         """
#         toremove = []
#         for chord_ in self.set_:
#             if chord_.is_included_in(chord):
#                 toremove.append(chord_)
#             if chord.is_included_in(chord_):
#                 return False
#         for chord_ in toremove:
#             self.set_.remove(chord_)
#         self.set_.append(chord)
#         return True

#     def __len__(self):
#         return len(self.set_)

#     def __lt__(self, other):
#         return len(self) < len(other)

#     def __iter__(self):
#         return iter(self.set_)

#     # def __iter__(self):
#     #     return self
#     def getOneElement(self)->GuitarChord:
#         return self.set_[0]

#     def getMinChromatic(self):
#         """Return the minimal chromatic note of an element of the set. Assuming it is the same for each element as indicated during the creation"""
#         # In practice, it is the minimal position of each element for open chords, not for transposed one
#         return self.minChromatic

#     def debug(self):
#         return str(self.set_)

#     def __repr__(self):
#         text = "Set_of_same_chord "
#         min_ = self.getMinChromatic()
#         if min_:
#             text += min_.get_note_name(withOctave=True)
#         text += self.getPatternName()
#         text += repr(self.set_)
#         return text


# class SetOfGuitarChords:

#     """Associate to open/transposable, and chord name, and potentially the smallest note played, the GuitarChord."""
#     sets: List[SetOfSameChord]
#     chords: Dict[str, Dict[str,Union[GuitarChord, Dict[GuitarPosition, GuitarChord]]]]
#     def __init__(self):
#         self.chords = {
#             "transposable": dict(),
#             "open": dict()
#         }
#         self.sets = []

#     def addChord(self, patternName: str, chord: GuitarChord, kind, minChromatic=None):
#         """
#         Add the chord to this set considering pattern name, and kind.
#         Also consider minChromatic if it is present"""
#         container = self.chords[kind]
#         if patternName not in container:
#             if minChromatic:
#                 container[patternName] = dict()
#             else:
#                 set_ = SetOfSameChord(kind, patternName, chord.third(), chord.fifth(), chord.quality())
#                 self.sets.append(set_)
#                 container[patternName] = set_
#         container = container[patternName]
#         if minChromatic:
#             if minChromatic not in container:
#                 set_ = SetOfSameChord(kind, patternName, chord.third(), chord.fifth(), chord.quality(),
#                                       minChromatic=minChromatic)
#                 self.sets.append(set_)
#                 container[minChromatic] = set_
#             container = container[minChromatic]
#         container.addChord(chord)

#     def getGreatests(self) -> GuitarChord:
#         greatests = []
#         greatest = None
#         for set_ in self:
#             if greatest is None or greatest < set_:
#                 greatests = [set_]
#                 greatest = set_
#             elif set_ < greatests[0]:
#                 continue
#             else:
#                 greatests.append(set_)
#         return set_

#     def __iter__(self):
#         return iter(self.sets)


# allChords = SetOfGuitarChords()


# def genFret(list_frets=[]) -> Generator[GuitarChord]:
#     """Generator for every fingering satisfying the fact that the distance between fret is at most fretDifMax

#     The guitar may have string played empty, string not played, and string played, nothing that there is already a string played at lowest_fret and at highest_fret.
#     list_frets -- the first fret played.
#     nbPlayed
#     """
#     nb_empty = Counter(list_frets)[None]
#     highest_fret = max(fret in list_frets) if any(list_frets) else None
#     lowest_fret = min(fret in list_frets) if any(list_frets) else None
#     if nb_empty  > 6 - MINIMAL_NUMBER_OF_STRINGS_IN_A_CHORD :
#         # there is already too much strings not played.
#         return
#     if len(list_frets) == 6:
#         try:
#             chord = GuitarChord(list_frets)
#         except IntervalWithNoRole:
#             return
#         yield chord
#         return
#     lowest_reachable_fret = max({1, highest_fret - fretDifMax}) if highest_fret else 1
#     highest_rechable_fret = min({HIGHEST_FRET, lowest_fret + fretDifMax}) if lowest_fret else HIGHEST_FRET
#     for fret in [None, 0] + list(range(lowest_reachable_fret, highest_rechable_fret + 1)):
#         newlist_frets = list_frets + [fret]
#         yield from genFret(newlist_frets)


# for chord in genFret():
#     kind = chord.kind()
#     patternName = chord.get_pattern_name()
#     if not (kind and patternName and chord.playable()):
#         continue
#     if kind == "open":
#         minChromatic = min(chord).get_chromatic()
#         allChords.addChord(patternName, chord, kind, minChromatic)
#     else:
#         allChords.addChord(patternName, chord, kind)

