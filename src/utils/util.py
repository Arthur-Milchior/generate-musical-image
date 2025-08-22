import os
from typing import Iterable, List
import unittest

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
        assert e.__class__ == elt.__class__, "{it=}"
            

def assert_typing(value, type):
    assert value is not None
    assert isinstance(value, type), f"{value=} is not of {type=}"

def assert_optional_type(value, type):
    if value is not None:
        assert_typing(value, type)