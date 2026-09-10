from collections.abc import Generator
from enum import Enum
from solfege.pattern.chord.chord_patterns import chord_patterns
from solfege.pattern.scale.scale_patterns import scale_patterns, chord_patterns_as_scales
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput
from utils import util
from solfege.value.key.key import Key 
from solfege.value.key.keys import sets_of_enharmonic_keys
from typing import Any, Optional, Dict, List, Self, assert_never
from solfege.pattern.scale.scale_pattern import ScalePattern
from operator import itemgetter
from _lily.lily import compile_
from dataclasses import dataclass
from utils.util import img_tag, save_file
from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.value.interval.interval import Interval
from solfege.value.note.note import Note
from consts import generate_root_folder

"""Generates per-instrument Anki scale/arpeggio CSVs for a handful of chromatic wind instruments (ocarinas,
tin whistle, recorder, harmonica). Distinct from `scale_number.py`, which generates the scale-degree ("scale
number") reference material instead.

Note: this module currently fails to import, because `compile_` (imported above from `_lily.lily`) no longer
exists there — see `generate/README.md` for the shared, pre-existing gap this is part of.
"""

folder_path = f"{generate_root_folder}/solfege/scales"
util.ensure_folder(folder_path)


class Direction(Enum):
    """Which order a scale's notes should be laid out in for one Anki field."""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    TOTAL = "total"
    REVERSE = "reverse"

@dataclass(frozen=True)
class Instrument:
    """Represents the information needed to generate scales"""

    name: str
    """Identifier used in file names (image/CSV) and as the default string representation."""

    lowest_instrument_note: Note
    """Lowest note this instrument can play."""

    highest_instrument_note: Note
    """Highest note this instrument can play."""

    transposition: Interval = Interval.make(0, 0)
    """Interval added when converting a written/concert pitch to this instrument's own notation (0 for
    non-transposing instruments)."""

    show_fingering: bool = True
    """Whether to include per-note fingering images in generated Anki fields."""

    image_extension: str = "png"
    """File extension used for this instrument's fingering images."""

    def difficulty(self, note: Note) -> Optional[int]:
        """Return `0` if `note` is within the instrument's playable range, else `None` (not playable)."""
        return 0 if self.lowest_instrument_note <= note <= self.highest_instrument_note else None

    def __str__(self) -> str:
        """The instrument's `name`."""
        return self.name

class ChromaticInstrumentWithDifficultNote(Instrument):
    """Chromatic instrument from lowest to highest

    difficulty_notes: map from chromatic note to the difficulty of playing it.
    """

    difficulty_notes: Dict[ChromaticNote, int]
    """Map from chromatic note (base octave) to the extra difficulty of playing it."""

    def __init__(self, name: str, lowest: Note, highest: Note, difficulty_notes: Dict[str, int], transposition: Optional[Interval]= None) -> None:
        """Build from a `{note name: extra difficulty}` map (`difficulty_notes`); note names are normalized to
        their chromatic, base-octave form as keys, and the max difficulty wins if a note is listed more than
        once."""
        super().__init__(name, lowest, highest)
        self.difficulty_notes = dict()
        for note, value in difficulty_notes.items():
            note = Note.from_name(note).get_chromatic().in_base_octave()
            self.difficulty_notes[note] = max(value, self.difficulty_notes.get(note, 0))

    def difficulty(self, note: Note) -> Optional[int]:
        """Return the extra difficulty recorded for `note` in `difficulty_notes`, or fall back to
        `Instrument.difficulty` (playable-range check) if it isn't specially listed."""
        return self.difficulty_notes.get(note.get_chromatic().in_base_octave(), super().difficulty(note))

    """
    transposition: Interval = Interval.make(0, 0)
    note_difficulties: Optional[Dict[str, int]] = None
    simple_notes: Optional[List[str]]"""


ocarina_harmorny_double = ChromaticInstrumentWithDifficultNote("ocarina_pendant", Note.from_name("C4"), Note.from_name("E5"),
                             {"C4#":1, "E♭4":1, })
ocarina_pendant = ChromaticInstrumentWithDifficultNote("ocarina_pendant", Note.from_name("C4"), Note.from_name("E5"),
                             {"C4#":1, "E♭4":1, })

ocarina_harmorny_triple = Instrument("ocarina_harmony_triple", Note.from_name("A4"), Note.from_name("E♭6"))
ocarina_transverse = Instrument("ocarina_transverse", Note.from_name("C4"), Note.from_name("C6"))
mv_ocarina = Instrument("mv_ocarina", Note.from_name("B3"), Note.from_name("E5"))
saxophone = Instrument("saxophone", Note.from_name("B♭3"), Note.from_name("A6"))
tin_whistle = ChromaticInstrumentWithDifficultNote("tin_whistle", Note.from_name("D4"), Note.from_name("D6"), 
                                                   {
                                                    "D4#":2,
                                                    "F4":2,
                                                    "G#4":2,
                                                    "B♭4":1,
                                                    "A#4":1,
                                                    "C5":1,
                                                   }, Interval.make(_chromatic=2, _diatonic=1),)
recorder = ChromaticInstrumentWithDifficultNote("recorder", Note.from_name("C4"), Note.from_name("D6"),
                                                   {
                                                       "C4#": 2,
                                                       "E4♭": 2,
                                                       "F4": 1,
                                                       "F#4": 1,
                                                       "G#4": 1,
                                                       "B4♭": 1,
                                                       "C5#": 2,
                                                       "D5": 1,
                                                   })
harmonica_diatonic = ChromaticInstrumentWithDifficultNote("harmonica_diatonic", Note.from_name("C3"), Note.from_name("C6"), {
    "D3♭": 1,
    "F#3": 1,
    "F3": 2,
    "B♭3": 1,
    "A3": 2,
    "A3♭": 3,
    "C#4": 1,
    "A♭4": 1,
    "E♭6": 2,
    "F#6": 2,
    "B6": 2,
    "B6♭": 3,
})
haromnica_chromatic = Instrument("harmonica_chromatic", Note.from_name("C3"), Note.from_name("C7#"))

instruments: List[Instrument] = [
#    ocarina_harmorny_double,
 #   ocarina_pendant,
  #  ocarina_harmorny_triple,
   # ocarina_transverse,
#    mv_ocarina,
 #   saxophone,
    tin_whistle,
    recorder,
    harmonica_diatonic,
    haromnica_chromatic
    ]

class Difficulties:
    """Accumulates per-note difficulty scores for one scale and orders itself by "easiest to play" — most
    weight given to how many notes hit the hardest difficulty level reached (`biggest`), then, tie-broken
    from hardest to easiest level, by how many notes hit each level (fewer hard notes sorts as easier)."""

    difficulties: Dict[int, int]
    """Map from difficulty level to how many notes of the scale hit that level."""

    biggest: int
    """The hardest difficulty level reached so far."""

    def __init__(self) -> None:
        """Start with no notes counted."""
        self.difficulties = dict()
        self.biggest = 0

    def add(self, d: int) -> Self:
        """Record one more note at difficulty level `d`; updates `biggest` if `d` is a new max. Returns `self`
        for chaining."""
        self.biggest = max(d, self.biggest)
        self.difficulties[d] = self.difficulties.get(d, 0) + 1
        return self

    def __eq__(self, value: "Difficulties") -> bool:
        """Equal iff the per-level note counts match exactly."""
        return self.difficulties == value.difficulties

    def __hash__(self) -> int:
        """Note: `self.difficulties` is a plain (unhashable) `dict`, so calling this currently raises
        `TypeError`; pre-existing bug, not fixed here (documentation-only pass)."""
        return hash(self.difficulties)

    def __lt__(self, other: "Difficulties") -> bool:
        """Easier-than comparison: fewer notes at the single hardest level reached (`biggest`) wins; ties are
        broken by comparing counts level by level, from hardest to easiest."""
        if self.biggest > other.biggest:
            return False
        if self.biggest < other.biggest:
            return True
        for d in range(self.biggest, -1, -1):
            if self.difficulties.get(d, 0) > other.difficulties.get(d, 0):
                return False
            if self.difficulties.get(d, 0) < other.difficulties.get(d, 0):
                 return True
        return False

    def __str__(self) -> str:
        """Render as the underlying `difficulties` dict, e.g. for debugging/logging."""
        return str(self.difficulties)

@dataclass
class AnkiNote:
    """One Anki note: a scale/arpeggio pattern played on one instrument, in one enharmonic key."""

    instrument: Instrument
    """The instrument this note is generated for."""

    scale_pattern: ScalePattern
    """The scale or arpeggio pattern being illustrated."""

    specific: str
    """Free-text label distinguishing scale from arpeggio notes (`"Scale"`/`"Arpeggio"`), stored as an Anki
    field."""

    set_of_enharmonic_keys: List[Key]
    """The enharmonically-equivalent keys to pick the tonic/spelling from (see `solfege.value.key.keys`)."""

    def csv_path(self) -> str:
        """Output CSV path for this note's instrument."""
        return f"{folder_path}/{self.instrument}.csv"

    def instrument_image(self) -> str:
        """`<img>` tag for this instrument's picture."""
        return util.img_tag(f"{self.instrument}.png")

    def interval(self) -> Interval:
        """Interval to transpose the key's tonic by to get this instrument's bass note (instrument transposition
        minus the pattern's own signature interval)."""
        return self.instrument.transposition - self.scale_pattern.interval_for_signature

    def scale_name(self) -> str:
        """The pattern's primary (first) name."""
        return self.scale_pattern.names[0]

    def scale_notation(self) -> str:
        """The pattern's notation string, or `""` if it has none."""
        return self.scale_pattern.notation or ""

    def bass_note(self) -> Note:
        """The lowest playable tonic for this note: `interval()` applied to the enharmonic key's note, then
        octave-shifted until it falls within the instrument's lowest octave."""
        bass_note = self.set_of_enharmonic_keys[0].note + self.interval()
        while bass_note < instrument.lowest_instrument_note:
            bass_note = bass_note.add_octave(1)
        while bass_note >= instrument.lowest_instrument_note.add_octave(1):
            bass_note = bass_note.add_octave(-1)
        return bass_note

    def scale_for_difficulty(self) -> Any:
        """The one-octave scale, starting at `bass_note()`, used to compute `difficulties()`."""
        return self.scale_pattern.from_note(
                        tonic=self.bass_note(),
                        number_of_octaves=1,
                        )

    def difficulties(self) -> Optional[Difficulties]:
        """None if not playable"""
        difficulties = Difficulties()
        for note in self.scale_for_difficulty().notes:
            difficulty = instrument.difficulty(note)
            if difficulty is None:
                return None
            difficulties = difficulties.add(difficulty)
        return difficulties

    def tonic_name(self) -> str:
        """`bass_note()`'s name, ASCII-symbol alterations, octave numbered from middle C = 4."""
        return self.bass_note().get_name_with_octave(
                    octave_notation=OctaveOutput.MIDDLE_IS_4,
                    alteration_output = AlterationOutput.SYMBOL,
                    note_output= NoteOutput.LETTER,
                    fixed_length = FixedLengthOutput.NO,
                )

    def key(self) -> str:
        "A value uniquely identifiying this anki note"
        return f"""\"{self.instrument} {self.scale_name().replace(",", "")} {self.tonic_name()} difficulty {self.difficulties()}\""""

    def anki_fields(self) -> Generator[str]:
        """Yield this note's Anki fields: first the header block (key, instrument image, blanks,
        tonic/scale name/notation, bass note images), then one field per `(start_octave, number_of_octaves,
        direction)` combination, generating and compiling each variant's LilyPond image along the way."""
        bass_note = self.bass_note()
        fields = [
            self.key(),
            self.instrument_image(),
            "", #hide single octave
            "",#practice single direction
            "", #signature
            "", #position
            self.tonic_name(),
            self.scale_name(),
            self.scale_notation(),
            self.specific,
            bass_note.image_html(),
            bass_note.add_octave(1).image_html(),
            bass_note.add_octave(2).image_html(),
            bass_note.add_octave(3).image_html(),
        ]
        yield from fields
        for (start_octave, number_of_octaves) in [(0, 1), (1,1), (0,2), (2,1), (1,2), (0,3)]:
            for direction in [Direction.INCREASING, Direction.DECREASING, Direction.TOTAL, Direction.REVERSE]:
                anki_field = AnkiField(self, start_octave, number_of_octaves, direction)
                yield anki_field.field()
                anki_field.generate_and_compile_lily()
    
    def anki_csv(self) -> str:
        """Render this note as one comma-joined CSV row of `anki_fields()`."""
        return ",".join(self.anki_fields())


@dataclass
class AnkiField:
    """Represents a field in anki"""

    anki_note: AnkiNote
    """The parent Anki note this field belongs to."""

    start_octave: int
    """Octave offset (added to the note's bass note) at which this scale variant starts."""

    number_of_octaves: int
    """How many octaves this scale variant spans."""

    direction: Direction
    """Whether this variant plays ascending, descending, or both (see `Direction`)."""

    def scale_lowest_note(self) -> Note:
        """The starting note for this variant: the parent note's bass note, shifted up by `start_octave`."""
        return self.anki_note.bass_note().add_octave(self.start_octave)

    def scale(self) -> Any:
        """Build this variant's note sequence per `direction`: ascending only, descending only, ascending then
        descending (`TOTAL`), or descending then ascending (`REVERSE`)."""
        increasing = self.anki_note.scale_pattern.from_note(
            tonic=self.scale_lowest_note(),
            number_of_octaves=self.number_of_octaves,
            )
        decreasing = self.anki_note.scale_pattern.descending().from_note(
            tonic=self.scale_lowest_note(),
            number_of_octaves=self.number_of_octaves,
            ).reverse()
        if self.direction is Direction.INCREASING:
            return increasing
        elif self.direction is Direction.DECREASING:
            return decreasing
        elif self.direction is Direction.TOTAL:
            return increasing.concatenate(decreasing)
        elif self.direction is Direction.REVERSE:
            return decreasing.concatenate(increasing)
        assert_never(self.direction)

    def playable(self) -> bool:
        """Whether this variant's starting note is still within the instrument's playable range."""
        return self.anki_note.bass_note() <= self.anki_note.instrument.highest_instrument_note

    def scale_note_name(self) -> str:
        """`scale_lowest_note()`'s name, ASCII alterations, octave numbered from middle C = 4."""
        return self.scale_lowest_note().get_name_with_octave(
                                octave_notation=OctaveOutput.MIDDLE_IS_4,
                                alteration_output = AlterationOutput.ASCII,
                                note_output = NoteOutput.LETTER,
                                fixed_length = FixedLengthOutput.NO)


    def svg_scale_file_name(self) -> str:
        """The file name without extension."""
        return f"""{self.anki_note.scale_name()}-{self.scale_note_name()}-{self.number_of_octaves}-{self.direction}"""

    def path(self) -> str:
        """Output path (without extension) for this variant's generated image."""
        return f"{folder_path}/{self.svg_scale_file_name()}"

    def lily(self) -> str:
        """This variant's LilyPond source."""
        return self.scale().lily()

    def generate_and_compile_lily(self) -> None:
        """Compile `lily()` to an SVG (no audio) at `path()`."""
        compile_(self.lily(), file_prefix=self.path(), wav = False)

    def svg_scale_html(self) -> str:
        """`<img>` tag for this variant's generated SVG."""
        return img_tag(f"{self.svg_scale_file_name()}.svg")

    def fingerings_html(self) -> List[str]:
        """Return one `<img>` tag per note in this variant, naming each instrument-specific fingering image."""
        field_parts = []
        for note_in_scale in self.scale().notes:
            chromatic_note: ChromaticNote = note_in_scale.get_chromatic()
            note_name = chromatic_note.get_name_with_octave(
                octave_notation=OctaveOutput.MIDDLE_IS_4,
                alteration_output = AlterationOutput.ASCII, 
                note_output = NoteOutput.LETTER, 
                fixed_length = FixedLengthOutput.NO
            )
            field_parts.append(img_tag(f"{self.anki_note.instrument}_{note_name}.{self.anki_note.instrument.image_extension}"))
        return field_parts            


    def field(self) -> str:
        """This variant's Anki field HTML: empty if not `playable()`, else the scale SVG plus, if the
        instrument wants fingerings, a line break and per-note fingering images."""
        if not self.playable():
            return ""
        field_parts = [self.svg_scale_html()]
        if self.anki_note.instrument.show_fingering:
            field_parts.append("<br/>")
            field_parts += self.fingerings_html()
        return "".join(field_parts)
            

all_csv = []
for instrument in instruments:
    instrument_image = img_tag(f"{instrument}.png")
    csv_path = f"{folder_path}/{instrument}.csv"
    anki_notes: List[str] = []
    for patterns, specific in ((chord_patterns_as_scales, "Arpeggio"), (scale_patterns, "Scale"), ):
        for scale_pattern in patterns:
            anki_notes_in_scale = []
            for set_of_enharmonic_keys in sets_of_enharmonic_keys:
                anki_note = AnkiNote(instrument, scale_pattern, specific, set_of_enharmonic_keys)
                anki_notes_in_scale.append((anki_note.difficulties(), anki_note.anki_csv()))

            anki_notes_in_scale.sort(key=itemgetter(0))
            for _, anki_note_csv in anki_notes_in_scale:
                anki_notes.append(anki_note_csv)
    csv = "\n".join(anki_notes)
    save_file(csv_path, csv)

