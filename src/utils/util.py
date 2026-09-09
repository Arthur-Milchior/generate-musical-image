from dataclasses import dataclass
import itertools
import os
from typing import Callable, Dict, Iterable, List, Optional, Self, Type, TypeVar
import unittest
import traceback

imageFolder = "../image/"
"""Default output folder for generated images (relative path, seemingly superseded by `consts.generate_root_folder`
in current code)."""

ankiFolder = "../image/"
"""Default output folder for Anki-related output (relative path, seemingly superseded by
`consts.generate_root_folder` in current code)."""

doDebug = False
"""Global switch: when `False` (the default), `debug()` below is a no-op."""


def debug(string, params=None):
    """Print `string` (formatted with `%` against `params` if given) iff `doDebug` is `True`, else do nothing."""
    if not doDebug:
        return
    if params:
        print(string % params)
    else:
        print(string)


def delete_file_if_exists(file_path):
    """Remove `file_path` if it exists; no-op otherwise."""
    if os.path.exists(file_path):
        os.remove(file_path)

def ensure_folder(folder):
    """Create `folder` (and any missing parents) if it doesn't already exist."""
    if not os.path.exists(folder):
        os.makedirs(folder)


def list2dic(l):
    """Generate a dictionnary, similar to the list, but index starting at 1"""
    return {i + 1: l[i] for i in range(0, len(l))}


class MyException(Exception):
    """An exception that accumulates arbitrary `key: value` debugging context (`addInformation`) and renders it
    as its message."""

    def __init__(self):
        """Start with no attached information."""
        self.dic = dict()

    def addInformation(self, key, value):
        """Attach a `key: value` pair of debugging context, to be shown in `str(self)`."""
        self.dic[key] = value

    def __str__(self):
        """Render the attached information dict."""
        return str(self.dic)

def indent(str: str, nb_space: int = 2):
    """Indent every non-empty line of `str` by `nb_space` spaces; empty lines are left untouched."""
    return "\n".join(f"""{" " * (nb_space if line else 0)}{line}""" for line in str.split("\n"))


def tests_modules(modules: List):
    """Run every `unittest.TestCase` found in each module of `modules`, printing verbose results (legacy
    `unittest`-based test runner, mostly superseded by `pytest` — see `src/README.md`)."""
    for module in modules:
        # try to load all testcases from given module, hope your testcases are extending from unittest.TestCase
        suite = unittest.TestLoader().loadTestsFromModule(module)
        # run all tests with verbosity
        unittest.TextTestRunner().run(suite)

def assert_all_same_class(it: Iterable):
    """Assert every element of `it` has the same `__class__` as the first. No-op (and returns `True`) if `it` is
    falsy (e.g. an empty list)."""
    if not it:
        return True
    elt = list(it)[0]
    for e in it:
        assert e.__class__ == elt.__class__, f"{it=}"

def assert_string_equal(string1, string2):
    """Assert `string1 == string2`, and on failure report the position and a short excerpt around the first
    differing character instead of dumping both full strings."""
    for i, (c1, c2) in enumerate(itertools.zip_longest(string1, string2)):
        if c1 != c2:
            max_char_c1 = min (i+10, len(string1))
            max_char_c2 = min (i+10, len(string2))
            assert False, f"""First difference at position {i}: "{string1[i: max_char_c1]}"!="{string2[i: max_char_c2]}" """

def assert_typing(value, type, exact:bool=False):
    """Assert `value` is not `None` and is an instance of `type` (or, if `exact`, that its class is exactly
    `type` rather than a subclass)."""
    assert value is not None
    if exact:
        assert value.__class__ == type, f"{value=}:{value.__class__} is not exactly {type=}"
    else:
        assert isinstance(value, type), f"{value=}:{value.__class__} is not of {type=}"

def assert_iterable_typing(it: Iterable, type, exact:bool = False):
    """Assert that each element of `it` has type `type`. Note that it consumes the iterable if it's a generator."""
    assert it is not None
    try:
        iterator= iter(it)
    except:
        print(f"{it=} is not iterable")
        raise
    for elt in iterator:
        assert_typing(elt, type, exact=exact)

def assert_increasing(it: Iterable):
    """Assert each element of `it` is strictly greater than the previous one."""
    for first, second in itertools.pairwise(it):
        assert first < second

def assert_decreasing(it: Iterable):
    """Assert each element of `it` is strictly less than the previous one."""
    for first, second in itertools.pairwise(it):
        assert first > second

def assert_dict_typing(d:Dict, type_key: Type, type_value:Type):
    """Assert `d` is not `None` and every key/value pair has type `type_key`/`type_value` respectively."""
    assert d is not None
    for key, value in d.items():
        assert_typing(key, type_key)
        assert_typing(value, type_value)

def assert_optional_typing(value, type, exact:bool = False):
    """Like `assert_typing`, but a `None` value is always accepted."""
    if value is not None:
        assert_typing(value, type, exact=exact)

def traceback_str():
    """Return the current call stack (not an active exception's traceback) rendered as a string, for debugging."""
    try:
        raise Exception()
    except Exception as e:
        return "".join(traceback.format_list(traceback.extract_stack()))

def sorted_unique(it: Iterable):
    """Return the distinct elements of `it` as a sorted list (elements must be hashable and support `<`)."""
    s = frozenset(it)
    l = list(s)
    l.sort()
    return l

def save_file(file_path: str, file_content: str):
    """Write `file_content` to `file_path`, overwriting it if it already exists."""
    with open(file_path, "w") as f:
        f.write(file_content)

def img_optional_tag(filename: Optional[str]):
    """Return an `<img>` tag for `filename`, or `""` if `filename` is `None`."""
    if filename is None:
        return ""
    return img_tag(filename)

def img_tag(filename:str):
    """Return `<img src='filename'/>` for the given `filename`."""
    assert_typing(filename, str)
    return f"""<img src='{filename}'/>"""

T = TypeVar("T")
def optional_min(it: Iterable[T]) -> Optional[T]:
    """None if it is None, else min(it)"""
    l = list(it)
    if l:
        return min(l)
    return None

def optional_max(it: Iterable[T]) -> Optional[T]:
    """None if it is None, else max(it)"""
    l = list(it)
    if l:
        return max(l)
    return None

def min_optional(it: Iterable[T]) -> Optional[T]:
    """Minimal of the non None elements."""
    return min(elt for elt in it if elt is not None)

def max_optional(it: Iterable[T]) -> Optional[T]:
    "maximal of the non None elements."
    return max(elt for elt in it if elt is not None)


def assert_equal_length(l: List):
    """Assert every element of `l` has the same `len()` as the first (e.g. to check a batch of rows/lists line
    up before zipping them). `l` must be non-empty."""
    length = len(l[0])
    for elt in l:
        assert len(elt) == length, f"{l[0]} and {elt} have length {length} and {len(elt)} respectively."