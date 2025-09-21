from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_typing


@dataclass(frozen=True)
class IntervalRole(ABC, DataClassWithDefaultArgument):
    """Represents the role of an interval in a pattern. 
    E.g. The tritone in the blues scale should be noted as the "blue note"
    
    """

    @abstractmethod
    def text_for_guitar_image(self) -> str: ...