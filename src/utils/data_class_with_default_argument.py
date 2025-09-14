from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Self, Type

from utils.util import assert_typing

_CLEANED = "_clean_arguments_for_constructor"
_DEFAULT_ADDED = "_default_arguments_for_constructor"
@dataclass(frozen=True)
class DataClassWithDefaultArgument:
    """Must always be added as last ancestor."""

    @classmethod
    def make(cls, *args, **kwargs) -> Self:
        cleaned_args, cleaned_kwargs = cls._clean_arguments_for_constructor(args, kwargs)
        default_args = cls._default_arguments_for_constructor(cleaned_args, cleaned_kwargs)
        new_kwargs = {**default_args, **cleaned_kwargs}
        assert _CLEANED in new_kwargs, f"{cls} was not cleaned. {new_kwargs=}"
        assert _DEFAULT_ADDED in new_kwargs, f"{cls} didn't get its default value. {new_kwargs=}"
        del new_kwargs[_CLEANED]
        del new_kwargs[_DEFAULT_ADDED]
        return cls(*cleaned_args, **new_kwargs)
    
    # Protected methods
    
    @classmethod
    def arg_to_kwargs(cls, args, kwargs, name, clean: Callable = lambda x: x, type: Optional[Type] = None):
        """If there is args, the first value is assumed to be name, not in kwargs, and is added in kwargs.
        Otherwise check that name in `kwargs`.

        Also clean the value with `clean`.

        Value is moved from args to kwargs.
        """
        if args:
            assert name not in kwargs
            arg = args[0]
            args = args[1:]
        else:
            assert name in kwargs, f"Missing {name} when creating {cls.__name__}"
            arg = kwargs[name]
        output = clean(arg)
        if type is not None:
            assert_typing(output, type)
        kwargs[name] = output
        return (args, kwargs)
    
    @classmethod
    def _maybe_arg_to_kwargs(cls, args, kwargs, name, clean: Callable = lambda x:x):
        """Clean the value associated to name, by default the first of args, if it exists. Otherwise do nothing."""
        if not args and name not in kwargs:
            return (args, kwargs)
        return cls.arg_to_kwargs(args, kwargs, name, clean)
    
    # Must be implemented by children classes.

    def __post_init__(self):
        hash(self) #check that hash can be computed

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        """Returns the association from argument name to default argument value.
        Class inheriting must call super."""
        return {_DEFAULT_ADDED: True }
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Ensure that any value is changed so that it gets the correct type. E.g. transform list in frozenlist
        and pair of int in interval.
        Class inheriting must call super."""
        kwargs[_CLEANED] = True
        return (args, kwargs)