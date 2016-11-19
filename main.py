import argparse
import ctypes
import functools
import os
import subprocess
import sys
import time

from events import Events
from flags import Flags
from signals import Signals

parser = argparse.ArgumentParser(description="Test Windows console events.")
parser.add_argument('flags', help="sub creation flags (int or name)")
parser.add_argument('event', help="the event to generate (int or name)")
parser.add_argument('--mode', choices=('send', 'kill', 'gcce'), default='send',
                    help="the method of generating the event")
args = parser.parse_args()
try:
    flags = Flags.get(args.flags)
    flags_str = flags.name
except KeyError:
    flags = int(args.flags)
    flags_str = str(flags)
event = Events.get(args.event)
mode = args.mode

print_now = functools.partial(print, flush=True)
print_now("Main: started")
print_now("Main: creating Sub, with {}".format(flags_str))
sub = subprocess.Popen((sys.executable, 'sub.py'), creationflags=flags)
time.sleep(3)

print_now("Main: generating {}".format(event.name))
if mode == 'send':
    sub.send_signal(event)
elif mode == 'kill':
    os.kill(sub.pid, event)
else:
    if not ctypes.windll.kernel32.GenerateConsoleCtrlEvent(event, sub.pid):
        raise ctypes.WinError()

for i in range(30):
    print_now("Main: alive")
    time.sleep(3)
print_now("Main: finished")
