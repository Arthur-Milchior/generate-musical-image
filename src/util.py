import os

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


def ensureFolder(folder):
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
