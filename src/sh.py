import os
import sys

def assertNotUnitTest():
    return
    if 'unittest' in sys.modules.keys():
        print("exception")
        raise Exception("")

def shell(command: str):
    assertNotUnitTest()
    os.system(command)