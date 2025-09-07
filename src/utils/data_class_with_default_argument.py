
from dataclasses import dataclass
from typing import Callable, Dict, List, Self


@dataclass(frozen=True)
class DataClassWithDefaultArgument:
    """Must always be added as last ancestor."""

    @classmethod
    def make(cls, *args, **kwargs) -> Self:
        args, kwargs = cls._clean_arguments_for_constructor(args, kwargs)
        default_args = cls._default_arguments_for_constructor()
        default_args.update(kwargs)
        return cls(*args, **default_args)

    def __post_init__(self):
        hash(self) #check that hash can be computed
    
    @staticmethod
    def arg_to_kwargs(args, kwargs, name, clean: Callable = lambda x: x):
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
            assert name in kwargs
            arg = kwargs[name]
        kwargs[name] = clean(arg)
        return (args, kwargs)
    
    @staticmethod
    def _maybe_arg_to_kwargs(args, kwargs, name, clean: Callable = lambda x:x):
        """Clean the value associated to name, by default the first of args, if it exists. Otherwise do nothing."""
        if not args and name not in kwargs:
            return (args, kwargs)
        return DataClassWithDefaultArgument.arg_to_kwargs(args, kwargs, name, clean)

    @classmethod
    def _default_arguments_for_constructor(cls):
        """Returns the association from argument name to default argument value.
        Class inheriting must call super."""
        return dict()
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Ensure that any value is changed so that it gets the correct type. E.g. transform list in frozenlist
        and pair of int in interval.
        Class inheriting must call super."""
        return (args, kwargs)