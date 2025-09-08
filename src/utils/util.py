from dataclasses import dataclass
import itertools
import os
from typing import Callable, Dict, Iterable, List, Optional, Self, Type, TypeVar
import unittest
import traceback

imageFolder = "../image/"
ankiFolder = "../image/"
doDebug = False


def debug(string, params=None):
    if not doDebug:
        return
    if params:
        print(string % params)
    else:
        print(string)


def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def list2dic(l):
    """Generate a dictionnary, similar to the list, but index starting at 1"""
    return {i + 1: l[i] for i in range(0, len(l))}


class MyException(Exception):
    def __init__(self):
        self.dic = dict()

    def addInformation(self, key, value):
        self.dic[key] = value

    def __str__(self):
        return str(self.dic)

def indent(str: str, nb_space: int = 2):
    return "\n".join(f"""{" " * (nb_space if line else 0)}{line}""" for line in str.split("\n"))


def tests_modules(modules: List):
    for module in modules:
        # try to load all testcases from given module, hope your testcases are extending from unittest.TestCase
        suite = unittest.TestLoader().loadTestsFromModule(module)
        # run all tests with verbosity
        unittest.TextTestRunner().run(suite)

def assert_all_same_class(it: Iterable):
    if not it:
        return True
    elt = list(it)[0]
    for e in it:
        assert e.__class__ == elt.__class__, f"{it=}"
            

def assert_typing(value, type, exact:bool=False):
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
    for first, second in itertools.pairwise(it):
        assert first < second

def assert_decreasing(it: Iterable):
    for first, second in itertools.pairwise(it):
        assert first > second

def assert_dict_typing(d:Dict, type_key: Type, type_value:Type):
    assert d is not None
    for key, value in d.items():
        assert_typing(key, type_key)
        assert_typing(value, type_value)

def assert_optional_typing(value, type, exact:bool = False):
    if value is not None:
        assert_typing(value, type, exact=exact)

def traceback_str():
    try:
        raise Exception()
    except Exception as e:
        return "".join(traceback.format_list(traceback.extract_stack()))
    
def sorted_unique(it: Iterable):
    s = frozenset(it)
    l = list(s)
    l.sort()
    return l

def save_file(file_path: str, file_content: str):
    with open(file_path, "w") as f:
        f.write(file_content)

def img_tag(filename:str):
    return f"""<img src='{filename}'/>"""

T = TypeVar("T")
def optional_min(it: Iterable[T]) -> Optional[T]:
    l = list(it)
    if l:
        return min(l)
    return None

def optional_max(it: Iterable[T]) -> Optional[T]:
    l = list(it)
    if l:
        return max(l)
    return None


def assert_equal_length(l: List):
    length = len(l[0])
    for elt in l:
        assert len(elt) == length, f"{l[0]} and {elt} have length {length} and {len(elt)} respectively."