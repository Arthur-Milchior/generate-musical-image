from dataclasses import dataclass
from typing import Generator, Tuple

from instruments.fretted_instrument.fretted_instrument.abstract_fretted_instrument import (
    AbstractFrettedInstrument,
)
from instruments.fretted_instrument.fretted_instrument.tuning import Tuning
from instruments.fretted_instrument.position.positions_consts import DISTANCE_BETWEEN_STRING
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from consts import generate_root_folder
from utils.util import assert_typing, ensure_folder


@dataclass(frozen=True, unsafe_hash=True)
class FrettedInstrument(DataClassWithDefaultArgument):
    """A concrete, playable fretted instrument: an `AbstractFrettedInstrument` (frets/strings/clef/finger-spread
    limits) combined with a specific `Tuning`. This is the object passed around everywhere else in
    `fretted_instrument/` (chord, scale, note, pair generation) to know how many strings/frets there are, what
    note each string plays open, and how far fingers may be spread."""

    _instrument: AbstractFrettedInstrument
    """The tuning-independent instrument family (guitar, bass, ukulele, ...)."""
    _tuning: Tuning
    """The open-string notes this particular instrument is strung with."""

    def __repr__(self) -> str:
        """E.g. "Guitar" for the default guitar tuning, capitalizing `get_name()`."""
        name = self.get_name()
        initial = name[0]
        initial = initial.upper()
        return f"{initial}{name[1:]}"

    def get_name(self) -> str:
        """The instrument's identifier used in generated file/folder names: the instrument family name, plus the
        tuning's name suffixed with "_" if the tuning isn't the default (unnamed) one."""
        tuning_name = self._tuning._name
        instrument_name = self._instrument._name
        if tuning_name is None:
            return instrument_name
        return f"{instrument_name}_{tuning_name}"

    def string(self, index: int) -> "String":
        """The `String` at 1-based `index` (string 1 is the first/lowest-indexed string of the tuning)."""
        assert_typing(index, int)
        return self._tuning.string(index)

    def strings(self) -> "Strings":
        """All of the instrument's strings, as a `Strings` collection."""
        return self._tuning.strings()

    def clef(self) -> "Clef":
        """The clef this instrument's notation is written in."""
        return self._instrument.clef

    def number_of_strings(self) -> int:
        """How many strings the instrument has."""
        return self._instrument.number_of_strings

    def number_of_frets(self) -> int:
        """How many frets the instrument has (excluding the open/nut position)."""
        return self._instrument.number_of_frets

    def last_string(self) -> "String":
        """The highest-indexed string of the tuning."""
        return self._tuning.last_string()

    def pair_of_string_with_distinct_intervals(self) -> Generator[Tuple["String", "String"], None, None]:
        """See `Tuning.pair_of_string_with_distinct_intervals`: one representative pair of strings for each
        distinct open-string interval, used to generate note-pair Anki cards without duplicating identical
        intervals."""
        return self._tuning.pair_of_string_with_distinct_intervals()

    def last_fret(self) -> "Fret":
        """The highest playable (relative) `Fret` on this instrument, i.e. `Fret.make(number_of_frets(), True)`."""
        from instruments.fretted_instrument.position.fret.fret import Fret

        return Fret.make(self.number_of_frets(), True)

    def lowest_note(self) -> "ChromaticNote":
        """The lowest open-string note across all strings."""
        return min(self._tuning.open_string_chromatic_note)

    def highest_note(self) -> "ChromaticNote":
        """The highest note reachable on the instrument: the highest open-string note plus the last fret's interval."""
        return self.last_fret().get_chromatic() + max(self._tuning.open_string_chromatic_note).get_chromatic()

    def generated_folder_name(self) -> str:
        """The output folder for this instrument's generated files (created if missing), under
        `<generate_root_folder>/fretted/<instrument name>/<tuning name, or "default">`."""
        tuning_name = self._tuning._name
        if tuning_name is None:
            tuning_name = "default"
        path = f"{generate_root_folder}/fretted/{self._instrument._name}/{tuning_name}"
        ensure_folder(path)
        return path

    def width(self) -> int:
        """The pixel width of the instrument's diagram, based on its number of strings."""
        return int(DISTANCE_BETWEEN_STRING * self.number_of_strings())

    def max_distance_between_two_closed_frets(self) -> int:
        """The largest fret span allowed between any two fingers when playing a chord -- used to decide how many
        frets a diagram needs to show."""
        return max(
            delta.deltas[1]
            for dic in self._instrument.finger_to_fret_delta_chord.values()
            for delta in dic.values()
        )

    def finger_to_fret_delta(self, lower_finger: int, higher_finger: int, chord: bool) -> "FretDelta":
        """The number of fret that we can have between both fingers"""
        d = self._instrument.finger_to_fret_delta_chord if chord else self._instrument.finger_to_fret_delta_scale
        return d[lower_finger][higher_finger]

    # pragma mark - DataClassWithDefaultArgument

    def __post_init__(self) -> None:
        """Assert the tuning has exactly as many open strings as the instrument has strings."""
        assert self._instrument.number_of_strings == len(
            self._tuning.open_string_chromatic_note
        )
        super().__post_init__()
