
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Dict, Generator, Generic, Optional, Tuple, Type, TypeVar

from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.easyness import KeyType
from utils.recording.recorded_container import RecordedContainerType
from utils.recording.recording_var_type import RecordedType
from utils.util import assert_dict_typing, assert_iterable_typing, assert_typing


@dataclass(frozen=True)
class RecordKeeper(ABC, Generic[KeyType, RecordedType, RecordedContainerType], DataClassWithDefaultArgument): # type: ignore
    """Associate a key to a set of RecordedType. The exact set is of type RecordedContainerType"""

    # Must be implemented by subclasses
    _key_type: ClassVar[Type]
    """Same as KeyType"""
    _recorded_type: ClassVar[Type]
    """Same as RecordedType"""
    _recorded_container_type: ClassVar[Type]
    """Same as RecordedContainerType"""

    # Must be implemented by subclass

    @abstractmethod
    def is_key_valid(self, key: KeyType) -> bool:
        """Whether the key is a valid entry. assert if not."""
        return NotImplemented

    @abstractmethod
    def _new_container(self, key: KeyType) -> RecordedContainerType:
        """Build a fresh, empty `RecordedContainerType` for `key`. Called by `_get_or_create_recorded_container`
        the first time something registers under a key not seen before."""

    # public

    _records: Dict[KeyType, RecordedContainerType]
    """Associate the key to the set of recorded type"""

    def register(self, key: KeyType, recorded: RecordedType):
        """Record `recorded` under `key`: asserts `key`/`recorded` have the expected types and that `is_key_valid
        (key)`, then appends `recorded` to that key's container (creating the container on first use)."""
        assert_typing(key, self._key_type, exact=True)
        assert_typing(recorded, self._recorded_type)
        assert self.is_key_valid(key)
        container = self._get_or_create_recorded_container(key)
        assert_typing(container, self._recorded_container_type)
        container.append(recorded)

    def _get_or_create_recorded_container(self, key: KeyType) -> Optional[RecordedContainerType]:
        """Return the existing container for `key`, creating and storing a new one via `_new_container` if none
        exists yet."""
        assert self.is_key_valid(key)
        assert_typing(key, self._key_type)
        container = self.get_recorded_container(key)
        if container is None:
            container = self._new_container(key)
            assert_typing(container, self._recorded_container_type)
            self._records[key] = container
            return container 
        return container

    def get_recorded_container(self, key: KeyType) -> Optional[RecordedContainerType]:
        """Given a set of interval, return the object having this set of interval_list."""
        assert self.is_key_valid(key)
        assert_typing(key, self._key_type, exact=True)
        assert_dict_typing(self._records, self._key_type, self._recorded_container_type)
        if key in self._records:
            container = self._records[key]
            assert_iterable_typing(container, self._recorded_type)
            return container
        return None
    
    def __iter__(self) -> Generator[Tuple[KeyType, RecordedContainerType]]:
        """Iterate over `(key, container)` pairs, like `dict.items()`."""
        return iter(self._records.items())

    def __repr__(self):
        """Show the configured types but elide the (potentially large) `_records` content."""
        return f"{self.__class__.__name__}(_recorded_type={self._recorded_type}, _key_type={self._key_type}, _recorded_container_type={self._recorded_container_type}, _records=...)"

    # pragma mark - DataClassWithDefaultArgument

    def __post_init__(self):
        """Sanity-check that `_records` is a plain `dict`."""
        assert_typing(self._records, dict)

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        """Default `_records` to a fresh empty `dict` when not explicitly supplied."""
        default = super()._default_arguments_for_constructor(args, kwargs)
        default["_records"] = dict()
        return default


RecordKeeperType = TypeVar("RecordKeeperType", bound = RecordKeeper)
"""Type variable for a concrete `RecordKeeper` subclass."""
