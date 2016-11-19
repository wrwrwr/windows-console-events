import ctypes
from ctypes import wintypes
import functools
import time

from events import Events

print_now = functools.partial(print, flush=True)
print_now("Subsub: started")


def event_handler(evtnum):
    print_now("Subsub: event handler for {}".format(Events(evtnum).name))
    return True

HandlerRoutine = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.DWORD)
c_event_handler = HandlerRoutine(event_handler)
if not ctypes.windll.kernel32.SetConsoleCtrlHandler(c_event_handler, True):
    raise ctypes.WinError()
print_now("Subsub: registered event handler")

for i in range(30):
    print_now("Subsub: alive")
    time.sleep(3)
print_now("Subsub: finished")
