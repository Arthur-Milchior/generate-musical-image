# from dataclasses import dataclass
# from typing import Dict, List

# from instruments.fretted_instrument.finger_to_fret_delta import finger_to_fret_delta
# from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
# from solfege.value.interval.chromatic_interval import ChromaticInterval
# from utils.frozenlist import FrozenList


# @dataclass(frozen=True)
# class FrettedInstrumentPositionWithFinger(PositionOnFrettedInstrument):
#     finger: int

#     def __post_init__(self):
#         assert 1 <= self.finger <= 4
#         super().__post_init__()

#     @classmethod
#     def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
#         args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
#         args, kwargs = cls.arg_to_kwargs(args, kwargs, "finger")
#         return args, kwargs

#     def positions_for_interval(self, interval: ChromaticInterval):
#         l = []
#         for finger in range(1, 5):
#             if finger== self.finger:
#                 continue
#             fret_delta = finger_to_fret_delta[self.finger][finger]
#             for pos in self.positions_for_interval_with_restrictions(interval=interval, frets=fret_delta):
#                 l.append(FrettedInstrumentPositionWithFinger(finger=finger, string=pos.string, fret=pos.fret))
#         return l

# class FrettedInstrumentPositionWithFingerFrozenList(FrozenList[FrettedInstrumentPositionWithFinger]):
#     type = FrettedInstrumentPositionWithFinger