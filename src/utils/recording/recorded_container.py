

from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

from utils.recording.recording_var_type import RecordedType


class RecordedContainer(ABC, Generic[RecordedType]):
    """Behaves like a list of RecordedType but can have more complex behavior.
    
    Should not be called "value" as this word is already used for interval and notes."""
    @abstractmethod
    def append(self, pattern: RecordedType) -> None:
        """Add `pattern` to the container. Subclasses decide what happens on a duplicate/conflicting key (see
        e.g. `SingletonContainer.same_key_behavior`)."""

    @abstractmethod
    def __iter__(self) -> Iterable[RecordedType]:
        """Iterate over the recorded values currently held."""

RecordedContainerType = TypeVar("RecordedContainerType", bound=RecordedContainer[RecordedType])
"""Type variable for a concrete `RecordedContainer` subclass."""

ChromaticRecordedContainerType = TypeVar("ChromaticRecordedContainerType", bound=RecordedContainer[RecordedType])
"""Same shape as `RecordedContainerType`; used specifically for record keepers indexed by chromatic-interval
lists (see `solfege/pattern/interval_list_to_pattern.py`, `solfege/pattern/chromatic_interval_list_to_patterns.py`)."""
