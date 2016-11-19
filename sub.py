import functools
import signal
import subprocess
import sys
import time

from signals import Signals

print_now = functools.partial(print, flush=True)
print_now("Sub: started")
print_now("Sub: creating Subsub, no flags")
subsub = subprocess.Popen((sys.executable, 'subsub.py'))


def signal_handler(signum, frame):
    print_now("Sub: signal handler for {}".format(Signals(signum).name))

for sig in Signals:
    signal.signal(sig, signal_handler)
    print_now("Sub: registered signal handler for {}".format(sig.name))

for i in range(30):
    print_now("Sub: alive")
    time.sleep(3)
print_now("Sub: finished")
