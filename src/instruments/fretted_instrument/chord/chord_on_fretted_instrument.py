from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Dict, List, Optional, Self, Union
from instruments.fretted_instrument.chord.playable import Playable
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument, PositionOnFrettedInstrumentFrozenList
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.constants import COLOR_FIFTH, COLOR_FOURTH, COLOR_QUALITY, COLOR_SECOND, COLOR_THIRD, COLOR_TONIC
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.interval_dependant_colored_position_maker import ColorsWithTonic
from instruments.fretted_instrument.position.fretted_position_maker.fretted_position_maker import FrettedPositionMaker
from instruments.fretted_instrument.position.string.string import String, StringFrozenList
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions import SetOfPositionOnFrettedInstrument
import itertools

from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern
from utils.frozenlist import FrozenList
from utils.util import assert_optional_typing, assert_typing, optional_max

class Barred(Enum):
    """Whether a chord fingering requires the index finger to bar across (cover) more than one string at the
    lowest closed fret. See `ChordOnFrettedInstrument.is_barred`."""

    NO = "NO"
    """No bar is needed: at most one string is closed at the lowest fret."""
    PARTIALLY = "PARTIALLY"
    """A bar is needed, but it doesn't need to reach the last string (an open string beyond the bar exists)."""
    FULLY = "FULLY"
    """A bar is needed and must extend all the way to the last string (no open string escapes it)."""

@dataclass(frozen=True, repr=False)
class ChordColors(ColorsWithTonic):
    """Coloring scheme for chord diagrams: one color per chromatic-interval-from-tonic role (2nd, 3rd, 4th, 5th,
    6th/7th), distinguishing them more finely than `ScaleColors`
    (`instruments/fretted_instrument/position/set/set_of_fretted_instrument_positions_with_fingers.py`) does."""

    #pragma mark - Colors

    #pragma mark - ColorsWithTonic
    def get_color_from_interval(self, chromatic_interval: ChromaticInterval):
        """The color to draw a note at `chromatic_interval` from the chord's tonic."""
        assert_typing(chromatic_interval, ChromaticInterval)
        return [COLOR_TONIC,
         COLOR_SECOND, COLOR_SECOND,
         COLOR_THIRD, COLOR_THIRD,
         COLOR_FOURTH,
         COLOR_FIFTH, COLOR_FIFTH, COLOR_FIFTH,
         COLOR_QUALITY, COLOR_QUALITY, COLOR_QUALITY][chromatic_interval.in_base_octave().value]
    
@dataclass(frozen=True, eq=False, order=False)
class ChordOnFrettedInstrument(SetOfPositionOnFrettedInstrument):
    """A `SetOfPositionOnFrettedInstrument` interpreted as one way of fingering a chord: exactly one (possibly
    not-played) position per string. Adds chord-specific queries (barring, playability, redundancy) on top of the
    generic position-set operations inherited from `SetOfPositionOnFrettedInstrument`."""

    @classmethod
    def make(cls, instrument: FrettedInstrument, frets: List[Union[Fret, int, None]], absolute: bool) -> Self:
        """Build a chord from one fret value per string of `instrument`: `frets[i]` (a `Fret`, an `int` fret
        number, or `None`/not-played) is the fret held on string `i+1`."""
        assert len(frets) == instrument.number_of_strings()
        l = []
        for fret in frets:
            if isinstance(fret, Fret):
                l.append(fret)
            else:
                assert_optional_typing(fret, int)
                l.append(Fret.make(fret, absolute=absolute))
        fretted_positions = [PositionOnFrettedInstrument(string, fret) for string, fret in itertools.zip_longest(instrument.strings(), l)]
        return cls(positions=PositionOnFrettedInstrumentFrozenList(fretted_positions), absolute=absolute)
    
    def get_fret(self, string: String) -> Optional[Fret]:
        """Return the note played on this string, if any."""
        assert_typing(string, String)
        fret = None
        for pos in self:
            assert_typing(pos.string, String)
            if pos.string == string:
                assert fret is None
                fret = pos.fret
        return fret if fret else Fret.make(None, self.absolute)
 
    def get_frets(self, instrument: Optional[FrettedInstrument]= None) -> List[Fret]:
        """the list of frets used in this string. Fret.make(none, a) for not played string."""
        if instrument is not None:
            frets = [self.get_fret(string) for string in instrument.strings()]
            return [Fret.make(None, self.absolute) if fret is None else fret for fret in frets]
        frets = dict()
        max_string = 0
        for pos in self:
            string = pos.string.value
            max_string = max(max_string, string)
            assert string not in frets
            frets[string] = pos.fret
        return [frets.get(string, Fret.make(None, self.absolute)) for string in range(1, max_string+1)]

    def __repr__(self):
        """E.g. `"ChordOnFrettedInstrument.make([None, 3, 2, 0, 1, 0])"` -- code that reconstructs this chord."""
        return f"""{self.__class__.__name__}.make([{", ".join(str(fret.value) for fret in self.get_frets())}])"""

    def chord_pattern_is_redundant(self):
        """Whether the same fingering pattern can be played higher on the fretted_instrument"""
        return self._min_fret(allow_open=True) > Fret.make(1, self.absolute)
    
    def is_barred(self):
        """Whether playing this chord requires barring the index finger (see `Barred`): `NO` if at most one
        string is closed at the lowest fret, `FULLY` if a bar at that fret would need to cover every string down
        to the last one, `PARTIALLY` if a bar is needed but an open string beyond it means it needn't reach the
        last string."""
        min_closed_strings = self.strings_at_min_fret(allow_open=False)
        if (not min_closed_strings):
            # The entire empty chord
            return Barred.NO
        if len(min_closed_strings) == 1:
            # Single closed string on this fret, so no need to bar.
            return Barred.NO
        open_strings = self.open_strings()
        if not open_strings:
            return Barred.FULLY
        min_closed_string = min(min_closed_strings)
        max_open_string = max(open_strings)
        if min_closed_string<max_open_string:
            # Some open string would be covered by the bar if we did it.
            return Barred.NO
        return Barred.PARTIALLY
    
    def has_not_played_in_middle(self):
        """Whether a not-played string is sandwiched between two played strings (e.g. x-2-x-2-x-x has a gap
        between its second and fourth strings) -- such chords are unplayable/unrealistic and get filtered out.
        Status can be not_played_start, then played, then not_played_end."""
        played_encountered = False
        not_played_after_played_encountered = False
        for fret in self.get_frets():
            if fret.is_not_played():
                if played_encountered:
                    not_played_after_played_encountered = True
            else:
                played_encountered = True
                if not_played_after_played_encountered:
                    return True
        return False
    
    def hand_for_fretted_instrument(self, instrument: FrettedInstrument) -> Optional["HandForChordForFrettedInstrument"]:
        """The `HandForChordForFrettedInstrument` (left-hand finger assignment) needed to play this chord on
        `instrument`, or `None` if no valid assignment exists (e.g. too many simultaneously-closed strings)."""
        from instruments.fretted_instrument.chord.hand_for_chord import HandForChordForFrettedInstrument
        return HandForChordForFrettedInstrument.compute_hand(instrument, self)

    def playable(self, instrument: FrettedInstrument) -> Playable:
        """Whether this chord can actually be fingered on `instrument`: `Playable.NO` if no valid hand
        configuration exists, otherwise the fingering's own `Playable` verdict (see `HandForChordForFrettedInstrument.playable`)."""
        from instruments.fretted_instrument.chord.hand_for_chord import HandForChordForFrettedInstrument
        hand: HandForChordForFrettedInstrument = self.hand_for_fretted_instrument(instrument)
        if hand is None:
            return Playable.NO
        return hand.playable()

    # Pragma mark - SetOfPositionOnFrettedInstrument

    def _svg_name_base(self, instrument:FrettedInstrument, fretted_position_maker: FrettedPositionMaker, minimal_number_of_frets: Optional[Fret] = None, *args, **kwargs):
        """The chord diagram's file-name stem: instrument, open/transposable, number of frets shown, the
        position-maker's identity, and the frets played on each string (joined with "_", "x" for not-played)."""
        fret_values = [fret.value for fret in self.get_frets(instrument)]
        frets = "_".join(str(value) if value is not None else "x" for value in fret_values)
        if minimal_number_of_frets is None:
            minimal_number_of_frets = self.last_shown_fret()
        return f"{instrument.get_name()}_chord_{"open" if self.absolute else "transposable"}_{minimal_number_of_frets.value}_frets_{str(fretted_position_maker) if fretted_position_maker else "black"}_{frets}"
        

"""Unused module-level cache placeholder, currently never populated or read."""
intervals_in_base_octave_to_fretted_instrument_chord: Dict[ChromaticIntervalListPattern, List[ChordOnFrettedInstrument]] = dict()

class FrettedInstrumentChordFrozenList(FrozenList[ChordOnFrettedInstrument]):
    """An immutable list of `ChordOnFrettedInstrument`."""
    type = ChordOnFrettedInstrument