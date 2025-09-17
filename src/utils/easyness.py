from abc import ABC, abstractmethod


class ClassWithEasyness(ABC):

    @abstractmethod
    def easy_key(self):
        """Return a key which can be used in < to sort by easyness. The easiest note will be reviewed firsts."""
        return NotImplemented