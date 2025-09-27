from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Dict, Generator, Generic, Iterable, List, Optional, Tuple, Type, TypeVar, Union

from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.easyness import KeyType
from utils.recording.record_keeper import RecordKeeperType
from utils.util import assert_dict_typing, assert_iterable_typing, assert_typing


@dataclass(frozen=True)
class Recordable(ABC, Generic[KeyType, RecordKeeperType]):
    record: bool = field(compare=False)

    #Must be implemented by subclasses.
    
    """The record keeper. If unset, it'll be created while being accessed. Use a different one for testing. 
    This one will contains all registered objects."""
    _record_keeper: ClassVar[RecordKeeperType]
    """The type of the record keeper. Used only to assert correct typing. same as RecordKeeperType."""
    _record_keeper_type: ClassVar[Type]
    """The type of the key of the record keeper. Used only to assert typing. Same a keyType."""
    _key_type: ClassVar[Type]

    @classmethod
    @abstractmethod
    def _new_record_keeper(cls) -> RecordKeeperType:...
    
    #public

    @classmethod
    def get_record_keeper(cls) -> RecordKeeperType:
        try:
            record_keeper = cls._record_keeper
        except AttributeError:
            record_keeper = cls._record_keeper = cls._new_record_keeper()
        assert record_keeper is not NotImplemented
        return record_keeper

    def _associate_keys_to_self(self,
                                keys: Optional[Union[List[KeyType], KeyType]] = None,
                                record_keeper: Optional[RecordKeeperType]=None):
        from solfege.pattern.interval_list_to_pattern import IntervalListToPattern
        record_keeper_: IntervalListToPattern
        if record_keeper is None:
            record_keeper_ = self.get_record_keeper()
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