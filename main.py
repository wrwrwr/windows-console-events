import argparse
import ctypes
import functools
import os
import subprocess
import time

from flags import Flags
from signals import Signals

print_now = functools.partial(print, flush=True)

parser = argparse.ArgumentParser(description="Test Windows console events.")
parser.add_argument('flags', help="sub creation flags (int or name)")
parser.add_argument('signal', help="the signal to send (int or name)")
parser.add_argument('--mode', choices=('send', 'kill', 'gcce'), default='send',
                    help="the method of sending the signal")
args = parser.parse_args()
try:
    flags = Flags.get(args.flags)
    flags_str = flags.name
except KeyError:
    flags = int(args.flags)
    flags_str = str(flags)
signal = Signals.get(args.signal)
if signal == 2:
    # Aliased as both SIGINT and CTRL_CLOSE_EVENT.
    signal_str = 'CTRL_CLOSE_EVENT'
else:
    signal_str = signal.name
mode = args.mode

print_now("Main: started")
print_now("Main: creating Sub, with {}".format(flags_str))
sub = subprocess.Popen(('python', 'sub.py'), creationflags=flags)
time.sleep(3)

print_now("Main: sending {}".format(signal_str))
if mode == 'send':
    sub.send_signal(signal)
elif mode == 'kill':
    os.kill(sub.pid, signal)
else:
    kernel32 = ctypes.windll.kernel32
    if not kernel32.GenerateConsoleCtrlEvent(int(signal), sub.pid):
        error = kernel32.GetLastError()
        raise ValueError("GCCE failed with {}".format(error))

for i in range(30):
    print_now("Main: alive")
    time.sleep(3)
print_now("Main: finished")