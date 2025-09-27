

from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

from utils.recording.recording_var_type import RecordedType


class RecordedContainer(ABC, Generic[RecordedType]):
    """Behaves like a list of RecordedType but can have more complex behavior.
    
    Should not be called "value" as this word is already used for interval and notes."""
    @abstractmethod
    def append(self, pattern: RecordedType):...

    @abstractmethod
    def __iter__(self) -> Iterable[RecordedType]:...

RecordedContainerType = TypeVar("RecordedContainerType", bound=RecordedContainer[RecordedType])
ChromaticRecordedContainerType = TypeVar("ChromaticRecordedContainerType", bound=RecordedContainer[RecordedType])
