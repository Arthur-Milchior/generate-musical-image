from __future__ import annotations

from typing import Union

from solfege.interval.base import _Interval


class _Note(_Interval):
    IntervalClass = _Interval
    """A note. Similar to an interval.

    -To a note may be added or subtracted an interval, but not to a note
    -Two notes may be subtracted, leading to an interval.

    """

    def is_note(self):
        return True

    def __neg__(self):
        raise Exception("Trying to negate a note makes no sens.")

    def __sub__(self, other: Union[_Interval, _Note]):
        if isinstance(other, _Note):
            return self.sub_note(other)
        else:
            return self.sub_interval(other)

    def sub_interval(self, other: _Interval):
        return self + (-other)

    def sub_note(self, other: _Note):
        return self.IntervalClass(self.get_number() - other.get_number())

    def __add__(self, other: _Interval):
        if isinstance(other, _Note):
            raise Exception("Adding two notes")
        sum_ = super().__add__(
            other)  # Super still makes sens because a class inheriting _Note also inherits some other class.
        return sum_

    def __hash__(self):
        return super().__hash__()

    def get_octave(self, scientificNotation=False):
        """The octave.  By default, starting at middle c. If scientificNotation, starting at C0"""
        octave = super().get_octave()
        return octave + 4 if scientificNotation else octave
