
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Generic, Iterable, List, Optional, Type, TypeVar, Union

from solfege.value.interval.set.list import DataClassWithDefaultArgument
from utils.util import assert_dict_typing, assert_list_typing, assert_typing


RecordedType = TypeVar("RecordedType")
KeyType = TypeVar("Key")


class RecordedContainer(Generic[RecordedType]):
    """Behaves like a list of RecordedType but can have more complex behavior.
    
    Should not be called "value" as this word is already used for interval and notes."""
    def append(self, pattern: RecordedType):
        return NotImplemented

    def __iter__(self) -> Iterable[RecordedType]:
        return NotImplemented

RecordedContainerType = TypeVar("RecordedContainerType", bound=RecordedContainer[RecordedType])

@dataclass(frozen=True)
class RecordKeeper(Generic[KeyType, RecordedType, RecordedContainerType], DataClassWithDefaultArgument):
    """Associate a key to a set of RecordedType. The exact set is of type RecordedContainerType"""

    """Same as RecordedType"""
    _recorded_type: ClassVar[Type]
    """Same as KeyType"""
    _key_type: ClassVar[Type]
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type]
    
    """Associate the key to the set of recorded type"""
    _records: Dict[KeyType, RecordedType]


    def __post_init__(self):
        assert_typing(self._records, dict)

    @classmethod
    def _default_arguments_for_constructor(cls):
        kwargs = super()._default_arguments_for_constructor()
        kwargs["_records"] = dict()
        return kwargs
    
    def _new_container(self, key: KeyType) -> RecordedContainerType:
        return list()
    
    def register(self, key: KeyType, recorded: RecordedType):
        assert_typing(key, self._key_type, exact=True)
        assert_typing(recorded, self._recorded_type)
        if key not in self._records:
            container = self._new_container(key)
            assert_typing(container, self._recorded_container_type)
            self._records[key] = container
        self._records[key].append(recorded)

    def get_recorded_container(self, key: KeyType) -> RecordedContainerType:
        """Given a set of interval, return the object having this set of interval_list."""
        assert_typing(key, self._key_type, exact=True)
        assert_dict_typing(self._records, self._key_type, self._recorded_container_type)
        if key in self._records:
            recorded = self._records[key]
            assert_list_typing(recorded, self._recorded_type)
            return recorded
        return self._new_container(key)
    
    def __iter__(self):
        return iter(self._records.items())


RecordKeeperType = TypeVar("RecordKeeperType", bound = RecordKeeper)

@dataclass(frozen=True)
class Recordable(Generic[KeyType, RecordKeeperType]):
    record: bool = field(compare=False)
    _record_keeper: ClassVar[RecordKeeperType]
    _record_keeper_type: ClassVar[Type]
    _key_type: ClassVar[Type]

    @classmethod
    def _new_record_keeper(cls) -> RecordKeeperType:
        return NotImplemented

    @classmethod
    def _get_record_keeper(cls) -> RecordKeeperType:
        try:
            record_keeper = cls._record_keeper
        except AttributeError:
            record_keeper = cls._record_keeper = cls._new_record_keeper()
        assert record_keeper is not NotImplemented
        return record_keeper

    def _associate_keys_to_self(self,
                                keys: Optional[Union[List[KeyType], KeyType]] = None,
                                record_keeper: Optional[RecordKeeperType]=None):
        from solfege.pattern.interval_list_to_patterns import IntervalListToPatterns
        record_keeper_: IntervalListToPatterns
        if record_keeper is None:
            record_keeper_ = self._get_record_keeper()
        else:
            record_keeper_ = record_keeper
        assert_typing(record_keeper_, self._record_keeper_type)
        if keys is None:
            keys = self.interval_lists()
        elif isinstance(keys, self._key_type):
            keys = [keys]
        for key in keys:
            assert_typing(key, self._key_type)
            record_keeper_.register(key, self)