from dataclasses import dataclass

from instruments.fretted_instrument.fretted_instrument.abstract_fretted_instrument import (
    AbstractFrettedInstrument,
)
from instruments.fretted_instrument.fretted_instrument.tuning import Tuning
from instruments.fretted_instrument.position.consts import DISTANCE_BETWEEN_STRING
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from consts import generate_root_folder
from utils.util import assert_typing, ensure_folder


@dataclass(frozen=True, unsafe_hash=True)
class FrettedInstrument(DataClassWithDefaultArgument):
    _instrument: AbstractFrettedInstrument
    _tuning: Tuning

    def __repr__(self):
        name = self.get_name()
        initial = name[0]
        initial = initial.upper()
        return f"{initial}{name[1:]}"

    def get_name(self):
        tuning_name = self._tuning._name
        instrument_name = self._instrument._name
        if tuning_name is None:
            return instrument_name
        return f"{instrument_name}_{tuning_name}"

    def string(self, index: int):
        assert_typing(index, int)
        return self._tuning.string(index)

    def strings(self):
        return self._tuning.strings()

    def number_of_strings(self):
        return self._instrument.number_of_strings

    def last_string(self):
        return self._tuning.last_string()

    def pair_of_string_with_distinct_intervals(self):
        return self._tuning.pair_of_string_with_distinct_intervals()

    def last_fret(self):
        from instruments.fretted_instrument.position.fret.fret import Fret

        return Fret.make(self._instrument.number_of_frets, True)

    def lowest_note(self):
        return min(self._tuning.open_string_chromatic_note)

    def highest_note(self):
        return self.last_fret() + max(self._tuning.open_string_chromatic_note)

    def generated_folder_name(self):
        tuning_name = self._tuning._name
        if tuning_name is None:
            tuning_name = "default"
        path = f"{generate_root_folder}/fretted/{self._instrument._name}/{tuning_name}"
        ensure_folder(path)
        return path

    def width(self):
        return int(DISTANCE_BETWEEN_STRING * self.number_of_strings())

    def max_distance_between_two_closed_frets(self) -> int:
        return max(
            delta.deltas[1]
            for dic in self._instrument.finger_to_fret_delta.values()
            for delta in dic.values()
        )

    # pragma mark - DataClassWithDefaultArgument

    def __post_init__(self):
        assert self._instrument.number_of_strings == len(
            self._tuning.open_string_chromatic_note
        )
        super().__post_init__()
