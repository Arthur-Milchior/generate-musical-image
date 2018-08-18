import os


def debug(s, *args, **kwargs):
    #print(s, *args, **kwargs)
    pass

def ensureFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
