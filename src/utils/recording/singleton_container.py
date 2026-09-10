
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Generic, Iterable, Optional
from utils.recording.recorded_container import RecordedContainer
from utils.recording.recording_var_type import RecordedType


class SameKeyBehavior(Enum):
    "Keep the minimum value according to ease key"
    MINIMUM = "mimimum"

    """Don't record if the key is already set"""
    IGNORE = "ignore"

    """Record the new value, drop the old one."""
    REPLACE = "replace"

    """The same key must be associated to the same value"""
    ASSERT_SAME = "assert same"

    """The same key can't be present"""
    IMPOSSIBLE = "impossible"
    
@dataclass
class SingletonContainer(RecordedContainer[RecordedType], Generic[RecordedType]): # type: ignore
    """A `RecordedContainer` holding at most one value; `same_key_behavior` decides what happens when a second
    value tries to claim the same key (see `SameKeyBehavior`)."""

    same_key_behavior: SameKeyBehavior
    """Policy applied when `append` is called while a value is already recorded."""

    recorded_value: Optional[RecordedType] = None
    """The single recorded value, or `None` if nothing has been recorded yet."""

    #pragma mark - RecordedContainer
    def append(self, recorded: RecordedType) -> None:
        """Record `recorded`. If a value is already recorded, resolve the conflict according to
        `same_key_behavior` (assert-fail for `IMPOSSIBLE`, assert-equal for `ASSERT_SAME`, keep the easier of the
        two for `MINIMUM`, keep the old one for `IGNORE`, or overwrite for `REPLACE`)."""
        if self.recorded_value is None:
            self.recorded_value = recorded
            return
        previous_recorded = self.recorded_value
        assert self.same_key_behavior is not SameKeyBehavior.IMPOSSIBLE, f"associated to \n{previous_recorded}\n and we want to associate to \n{recorded}\n"
        if self.same_key_behavior == SameKeyBehavior.ASSERT_SAME:
            assert previous_recorded == recorded, f"associated to \n{previous_recorded}\n and we want to associate to \n{recorded}\n"
        elif self.same_key_behavior == SameKeyBehavior.MINIMUM:
            self.recorded_value = min(recorded, previous_recorded, key=lambda r: r.easy_key())

        elif self.same_key_behavior == SameKeyBehavior.IGNORE:
            pass
        else:
            assert self.same_key_behavior == SameKeyBehavior.REPLACE
            self.recorded_value = recorded




    def __iter__(self) -> Iterable[RecordedType]:
        """Yield the recorded value if there is one, else yield nothing."""
        if self.recorded_value is not None:
            yield self.recorded_value