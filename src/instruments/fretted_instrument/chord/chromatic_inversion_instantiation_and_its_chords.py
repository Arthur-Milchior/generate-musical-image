
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import cache
from typing import ClassVar, Dict, Generator, Generic, List, Tuple, Type, Union

from instruments.fretted_instrument.chord.chord_decomposition_anki_note import ChordDecompositionAnkiNote
from instruments.fretted_instrument.chord.chord_on_fretted_instrument import ChordOnFrettedInstrument, FrettedInstrumentChordFrozenList
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.black_only import BlackOnly
from instruments.fretted_instrument.position.fretted_position_maker.maker_with_letters.fretted_position_maker_for_interval import FrettedPositionMakerForInterval
from lily.sheet import lily_chord_sheet
from solfege.pattern.inversion.inversion_pattern import InversionPattern,  InversionPatternsGetterType
from solfege.pattern_instantiation.inversion.chromatic_inversion_instantiation import ChromaticInversionInstantiation
from solfege.value.interval.set.interval_list import IntervalList
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.clef import Clef
from solfege.value.note.note import Note
from solfege.value.note.set.note_list import NoteList
from utils.csv import CsvGenerator
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.easyness import ClassWithEasyness
from utils.recording.recorded_container import RecordedContainer
from utils.util import T, assert_iterable_typing, assert_typing, img_tag

@dataclass(frozen=True, unsafe_hash=True)
class ChromaticInversionInstantiationAndItsChords(RecordedContainer[ChordOnFrettedInstrument], CsvGenerator, DataClassWithDefaultArgument, ClassWithEasyness, ABC, Generic[InversionPatternsGetterType]):
    """
    For a `InversionPatternsGetterType`, record the list of chord with this inversion(pattern)

    Csv is:
    name, other names, instrument, source, description, for chord (1, 2, 3, 4, 5, 6, 7, remaining): (the chord black, chord colored)
    """
    instrument: FrettedInstrument
    """The instrument these fingerings are played on."""
    key: ChromaticInversionInstantiation
    """The pattern, potentially inversed, with a lowest note."""
    fretted_instrument_chords: List[ChordOnFrettedInstrument] = field(hash=False, compare=False, default_factory=list)
    """All instantiations of the pattern `key` on `instrument`"""

    #pragma mark - InversionPatternGetter

    def get_inversion_pattern(self) -> InversionPattern:
        """The chord pattern (with its inversion) this container is collecting fingerings for."""
        return self.key.pattern

    def append(self, fretted_instrument_chord: ChordOnFrettedInstrument) -> None:
        """Register one more fingering of the chord, then keep `fretted_instrument_chords` sorted by ease of
        play. Asserts `fretted_instrument_chord`'s actual chromatic intervals from its lowest note match one of
        the interval lists expected for `key`'s pattern, and that it isn't already registered."""
        assert_typing(fretted_instrument_chord, ChordOnFrettedInstrument)
        expected_chromatic_intervals_lists = self.get_inversion_pattern().get_interval_lists()
        actual_chromatic_intervals = fretted_instrument_chord.intervals_frow_lowest_note_in_base_octave()
        assert actual_chromatic_intervals in [expected_chromatic_intervals_list.get_chromatic_interval_list() for expected_chromatic_intervals_list in expected_chromatic_intervals_lists], f"""{actual_chromatic_intervals} not in {expected_chromatic_intervals_lists}"""
        assert fretted_instrument_chord not in self.fretted_instrument_chords
        self.fretted_instrument_chords.append(fretted_instrument_chord)
        self.fretted_instrument_chords.sort(key = lambda chord: chord.best_chord_key())

    def is_smaller_than_known_chord(self, small_chord: ChordOnFrettedInstrument) -> bool:
        """Whether some already-registered chord strictly contains `small_chord` (via `ChordOnFrettedInstrument.__lt__`)."""
        for big_chord in self.fretted_instrument_chords:
            if small_chord < big_chord:
                return True
        return False

    def sort(self) -> None:
        """Sort the list of chords. Starting with smallest number of frets, and in case of equality greater number of notes"""
        self.fretted_instrument_chords.sort(key=lambda fretted_instrument_chord: (fretted_instrument_chord.number_of_frets(allow_open=False), -fretted_instrument_chord.number_of_distinct_notes()))

    def maximals(self) -> FrettedInstrumentChordFrozenList:
        """Return the elements of the list that are not strictly contained in other elements of the list."""
        self.sort()
        return FrettedInstrumentChordFrozenList(fretted_instrument_chord for fretted_instrument_chord in self.fretted_instrument_chords if not self.is_smaller_than_known_chord(fretted_instrument_chord))

    def decompositions(self) -> List[ChordDecompositionAnkiNote]:
        """Return ChordDecompositionAnkiNote for all maximal chords sorted by easyness"""
        return sorted([
            ChordDecompositionAnkiNote(self.instrument, self.key, chord)
            for chord in self.maximals()
        ], key=lambda decomposition: decomposition.easy_key())

    def all_fretted_instrument_chords(self) -> FrettedInstrumentChordFrozenList:
        """All registered fingerings (not just the maximal ones), as a `FrettedInstrumentChordFrozenList`."""
        return FrettedInstrumentChordFrozenList(self.fretted_instrument_chords)

    def __iter__(self) -> Generator[ChordOnFrettedInstrument]:
        """Iterate over the registered fingerings, sorted (see `sort`)."""
        self.sort()
        yield from self.fretted_instrument_chords

    def names(self) -> List[str]:
        """The chord's notation(s): the tonic-based name (e.g. "Cmaj7"), plus, for a non-root inversion, a second
        "<chord>/<bass note>" slash-notation name."""
        inversion = self.get_inversion_pattern()
        chromatic_lowest_note: ChromaticNote = self.key.lowest_note
        lowest_note = inversion.intervals_with_all_notes().best_enharmonic_starting_note(chromatic_lowest_note)
        tonic = inversion.get_tonic(lowest_note)
        note_name = tonic.get_name_up_to_octave(alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO)
        lowest_note_name = chromatic_lowest_note.get_name_up_to_octave(alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO)
        chord_pattern_notation = inversion.base.notation
        if chord_pattern_notation is None:
            chord_pattern_notation = inversion.base.first_of_the_names()
        chord_notation = f"{note_name}{chord_pattern_notation}"
        if inversion.inversion == 0:
            assert tonic.get_chromatic() == chromatic_lowest_note
            return [chord_notation]
        else:
            return [f"""{chord_notation}/{lowest_note_name}"""]

    def lily_field(self, fretted_instrument_chord : PositionOnFrettedInstrument, interval_list: IntervalList) -> str:
        """Render `interval_list` (from the container's lowest note) as staff notation and return its `<img>` tag.
        `fretted_instrument_chord` is currently unused."""
        lowest_chromatic_note: ChromaticNote = self.key.lowest_note
        lowest_note: Note = Note.from_chromatic(lowest_chromatic_note)
        note_list: NoteList = interval_list.from_note(lowest_note)
        sheet = lily_chord_sheet(note_list, Clef.TREBLE)
        lily_file = sheet.maybe_generate()
        return img_tag(lily_file)

    # Used for anki:

    def __len__(self) -> int:
        """How many fingerings have been registered."""
        return len(self.fretted_instrument_chords)

    def first_name(self) -> str:
        """The chord's primary notation (see `names`)."""
        return self.names()[0]

    def other_names(self) -> str:
        """Any secondary notation(s) from `names` (typically the slash-chord form for an inversion), comma-joined."""
        names = self.names()
        assert_iterable_typing(names, str)
        other_names = names[1:]
        return ", ".join(other_names)

    def source_field(self) -> str:
        """The chord pattern's Wikipedia (or other) source(s), as clickable links -- see ChordPattern.source."""
        pattern = self.get_inversion_pattern().base
        links = ", ".join(f'<a href="{url}">{url}</a>' for url in pattern.source)
        return links.replace('"', "'")

    def description_field(self) -> str:
        """The chord pattern's description -- see ChordPattern.description. May contain HTML links."""
        pattern = self.get_inversion_pattern().base
        return pattern.description.replace('"', "'")

    def plain_and_numbered_field(self, folder_path: str, fretted_chord: ChordOnFrettedInstrument) -> Tuple[str, str]:
        """Generate the svg for the `fretted_chord` and its decompositions. Add the csv for decomposition in chord_decompositions"""
        is_open = fretted_chord.is_open()
        transposed_chord, transposition = fretted_chord, 0 if fretted_chord.is_open() else fretted_chord.transpose_to_fret_one()
        pos_of_lowest_note = transposed_chord.get_most_grave_note()
        chromatic_lowest_note = pos_of_lowest_note.get_chromatic()
        chromatic_inversion_pattern: ChromaticInversionInstantiation = self.key
        chromatic_interval_list: IntervalList = chromatic_inversion_pattern.get_intervals()
        lowest_note = chromatic_interval_list.best_enharmonic_starting_note(chromatic_lowest_note)
        tonic = chromatic_inversion_pattern.pattern.get_tonic(lowest_note)
        chromatic_tonic = tonic.get_chromatic().in_base_octave()
        fpm = FrettedPositionMakerForInterval.make(tonic=chromatic_tonic, pattern=chromatic_inversion_pattern.pattern.base)
        return (
            img_tag(transposed_chord.save_svg(folder_path, instrument=self.instrument, fretted_position_maker=BlackOnly(), absolute=is_open)),
            img_tag(transposed_chord.save_svg(folder_path, instrument=self.instrument, fretted_position_maker=fpm, absolute=is_open)),
            #self.lily_field(transposed_chord, self.key.get_identical_inversion_pattern().easiest_inversion().get_interval_list()),
        )
    
    #pragma mark - ClassWithEasyness

    def easy_key(self) -> Tuple[Tuple[int, int], int]:
        """The easiest list of chords are the chords for the easiest pattern and then the one which has the easiest instantiation."""
        return (self.key.easy_key(), self.fretted_instrument_chords[0].easy_key())

    #Pragma mark - CsvGenerator

    def csv_content(self, folder_path: str) -> Generator[str]:
        """Yield this container's Anki fields: name, other names, instrument, source, description, then up to 7
        maximal chords each as a (plain diagram, colored diagram) pair, padded with blanks if fewer than 7
        exist, followed by any further maximal chords' diagrams comma-joined into two overflow fields."""
        yield self.first_name()
        yield self.other_names()
        yield self.instrument.get_name()
        yield self.source_field()
        yield self.description_field()
        maximals = self.maximals()
        individual_maximals, other_maximals = maximals[:7], maximals[7:]
        for fretted_chord in individual_maximals:
            yield from self.plain_and_numbered_field(folder_path, fretted_chord)
        nb_empty = 7- len(maximals)
        yield from [""] * (2 * nb_empty)
        # Remaining maximals
        triples = [self.plain_and_numbered_field(folder_path, fretted_chord) for fretted_chord in other_maximals]
        yield ", ".join(blacks for blacks, _ in triples)
        yield ", ".join(colored for _, colored in triples)
    
    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Dict:
        """Default `fretted_instrument_chords` to an empty list when not supplied."""
        default = super()._default_arguments_for_constructor(args, kwargs)
        default["fretted_instrument_chords"] = list()
        return default

    def __post_init__(self) -> None:
        """Validate the types of `key` and `fretted_instrument_chords`."""
        assert_typing(self.key, ChromaticInversionInstantiation)
        assert_typing(self.fretted_instrument_chords, list)
        assert_iterable_typing(self.fretted_instrument_chords, ChordOnFrettedInstrument)
        super().__post_init__()

    # Must be implemented by subclasses

    absolute: ClassVar[bool]
    """Same As IdenticalInversionPatternsGetterType. Declared but never assigned/overridden here or by any known
    subclass; not currently read anywhere in this class."""

    # The anki field for the partition if any.
