import os

doDebug = False
def debug(string, params=None):
    if not doDebug:
        return
    if params:
        print(string%params)
    else:
        print(string)

def ensureFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
