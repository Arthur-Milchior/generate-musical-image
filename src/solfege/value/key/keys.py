
from solfege.value.interval.interval import Interval
from solfege.value.key.key import Key
from solfege.value.note.note import Note


key_of_C = Key.make(note=Note.from_name("C"))
key_of_A = Key.make(note=Note.from_name("A3"), number_of_sharps=3)

"""All keys, grouped by enharmonic, sorted by minimal number of alteration"""
sets_of_enharmonic_keys = [
    [
        key_of_C,
        Key.make(note=Note.from_name("D♭♭"), number_of_flats=12),
        Key.make(note=Note.from_name("B#3"), number_of_flats=12),
    ],
    [
        Key.make(note=Note.from_name("F3"), number_of_flats=1),
        Key.make(note=Note.from_name("E#"), number_of_sharps=11),
        Key.make(note=Note.from_name("G♭♭3"), number_of_flats=13),
    ],
    [
        Key.make(note=Note.from_name("G"), number_of_sharps=1),
        Key.make(note=Note.from_name("A♭♭3"), number_of_flats=11),
        Key.make(note=Note.from_name("F𝄪3"), number_of_flats=13),
    ],
    [
        Key.make(note=Note.from_name("B♭3"), number_of_flats=2),
        Key.make(note=Note.from_name("A#3"), number_of_sharps=10),
        Key.make(note=Note.from_name("C♭♭"), number_of_flats=14),
    ],
    [
        Key.make(note=Note.from_name("D"), number_of_sharps=2),
        Key.make(note=Note.from_name("E♭♭"), number_of_flats=10),
        Key.make(note=Note.from_name("C𝄪"), number_of_flats=14),
    ],
    [
        Key.make(note=Note.from_name("E♭"), number_of_flats=3),
        Key.make(note=Note.from_name("D#"), number_of_sharps=9),
    ],
    [
        key_of_A,
        Key.make(note=Note.from_name("B♭♭3"), number_of_flats=9),
    ],
    [
        Key.make(note=Note.from_name("A♭3"), number_of_flats=4),
        Key.make(note=Note.from_name("G#3"), number_of_sharps=8),
    ],
    [
        Key.make(note=Note.from_name("E"), number_of_sharps=4),
        Key.make(note=Note.from_name("F♭"), number_of_flats=8),
    ],
    [
        Key.make(note=Note.from_name("D♭"), number_of_flats=5),
        Key.make(note=Note.from_name("C#"), number_of_sharps=7),
    ],
    [
        Key.make(note=Note.from_name("B3"), number_of_sharps=5),
        Key.make(note=Note.from_name("C♭"), number_of_flats=7),
        Key.make(note=Note.from_name("A𝄪3"), number_of_sharps=7),
    ],
    [
        Key.make(note=Note.from_name("F#3"), number_of_flats=6),
        Key.make(note=Note.from_name("G♭3"), number_of_sharps=6),
    ],
]

for enharmonic_set in sets_of_enharmonic_keys:
    Key.add_enharmonic_set(enharmonic_set)

seven_sharps = Interval.make(_diatonic=0, _chromatic=1)  # when playing a C scale, have C# major signature, 3 sharps
three_sharps = Interval.make(_diatonic=5, _chromatic=9)  # when playing a C scale, have A major signature, 3 sharps
two_sharps = Interval.make(_diatonic=1, _chromatic=2)  # when playing a C scale, have D major signature, 2 sharps
one_sharp = Interval.make(_diatonic=4, _chromatic=7)  # when playing a C scale, have G major signature, 1 sharp
nor_flat_nor_sharp = Interval.make(_diatonic=0, _chromatic=0)  # when playing a C scale, have C signature
one_flat = Interval.make(_diatonic=3, _chromatic=5)  # when playing a C scale, have F major signature, 1 flat
two_flats = Interval.make(_diatonic=6, _chromatic=10)  # when playing a C scale, have Bb major signature, 2 flats
three_flats = Interval.make(_diatonic=2, _chromatic=3)  # when playing a C scale, have Eb major signature, 3 flats
four_flats = Interval.make(_diatonic=5, _chromatic=8)  # when playing a C scale, have Ab major signature, 4 flats
five_flats = Interval.make(_diatonic=1, _chromatic=1)  # when playing a C scale, have Bb major signature, 5 flats
height_flats = Interval.make(_diatonic=3, _chromatic=4)  # when playing a C scale, have Fb major signature, 8 flats including Bbb


