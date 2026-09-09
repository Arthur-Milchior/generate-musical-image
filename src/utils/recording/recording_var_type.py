"""Shared type variables for the `utils.recording` package (kept in their own module to avoid import cycles
between `record_keeper.py`, `recorded_container.py` and `recordable.py`)."""

from typing import TypeVar

RecordedType = TypeVar("RecordedType")
"""The type of value being recorded/looked up (e.g. a `SolfegePattern` subclass)."""

KeyType = TypeVar("Key")
"""The type of key values are recorded under (e.g. an `IntervalList`)."""
