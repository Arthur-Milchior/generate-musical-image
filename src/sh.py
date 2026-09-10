import os
import sys

def assertNotUnitTest() -> None:
    """No-op guard intended to forbid running shell commands from a unit test; disabled by the early `return` (dead code below it), so it currently never raises."""
    return
    if 'unittest' in sys.modules.keys():
        print("exception")
        raise Exception("")

def shell(command: str) -> None:
    """Run `command` in the system shell via `os.system`, after the (currently disabled) `assertNotUnitTest` guard."""
    assertNotUnitTest()
    os.system(command)