from dataclasses import dataclass, field
from typing import Callable, ClassVar, Dict, List, Optional, Self, Tuple, Type

from utils.util import assert_typing

_CLEANED = "_clean_arguments_for_constructor"
_DEFAULT_ADDED = "_default_arguments_for_constructor"

@dataclass(frozen=True)
class DataClassWithDefaultArgument:
    """Must always be added as last ancestor. Order is creation time."""

    """The maximal value of `index`"""
    max_index: ClassVar[int] = 0

    @classmethod
    def make(cls, *args, **kwargs) -> Self:
        args = list(args)
        cleaned_args, cleaned_kwargs = cls._clean_arguments_for_constructor(args, kwargs)
        default_kwargs = cls._default_arguments_for_constructor(cleaned_args, cleaned_kwargs)
        new_kwargs = {**default_kwargs, **cleaned_kwargs}
        assert _CLEANED in new_kwargs, f"{cls} was not cleaned. {new_kwargs=}"
        assert _DEFAULT_ADDED in new_kwargs, f"{cls} didn't get its default value. {new_kwargs=}"
        del new_kwargs[_CLEANED]
        del new_kwargs[_DEFAULT_ADDED]
        return cls(*cleaned_args, **new_kwargs)

    # Protected methods
    
    @classmethod
    def clean_kwargs(cls, kwargs, name, clean: Optional[Callable] = None, type: Optional[Type] = None) -> Dict:
        assert name in kwargs
        value = kwargs[name]
        if clean is not None:
            value = clean(value)
        if type is not None:
            assert_typing(value, type)
        kwargs[name] = value
        return kwargs
    
    @classmethod
    def arg_to_kwargs(cls, args: List, kwargs: Dict, name, clean: Optional[Callable] = None, type: Optional[Type] = None) -> Tuple[List, Dict]:
        """If there is args, the first value is assumed to be name, not in kwargs, and is added in kwargs.
        Otherwise check that name in `kwargs`.

        Also clean the value with `clean`.

        Value is moved from args to kwargs.
        """
        if args:
            assert name not in kwargs, f"{name} already present in {kwargs}"
            kwargs[name] = args.pop(0)
        else:
            assert name in kwargs, f"Missing {name} when creating {cls.__name__}"
        kwargs = cls.clean_kwargs(kwargs, name, clean)
        return (args, kwargs)
    
    @classmethod
    def _maybe_arg_to_kwargs(cls, args: List, kwargs: Dict, name: str, clean: Callable = lambda x:x, type: Optional[Type] = None):
        """Clean the value associated to name, by default the first of args, if it exists. Otherwise do nothing."""
        if name not in kwargs and args:
            kwargs[name] = args.pop(0)
        if name in kwargs:
            kwargs = cls.clean_kwargs(kwargs, name, clean, type)
        return args, kwargs
        
    
    # Must be implemented by children classes.

    def __post_init__(self):
        hash(self) #check that hash can be computed

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs) ->Dict:
        """Returns the association from argument name to default argument value.
        Class inheriting must call super."""
        return {_DEFAULT_ADDED: True}
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Ensure that any value is changed so that it gets the correct type. E.g. transform list in frozenlist
        and pair of int in interval.
        Class inheriting must call super."""
        kwargs[_CLEANED] = True
        return (args, kwargs)
    
    # Default implementation:
    # # Pragma mark - DataClassWithDefaultArgument
    # @classmethod
    # def _default_arguments_for_constructor(cls, args, kwargs):
    #     kwargs = super()._default_arguments_for_constructor(args, kwargs)
    #     kwargs["key"] = value
    #     return kwargs
    
    # @classmethod
    # def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
    #     args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
    #     args, kwargs = cls.arg_to_kwargs(args, kwargs, "key", clean)
    #     return args, kwargs

    # def __post_init__(self):
    #     super().__post_init__()