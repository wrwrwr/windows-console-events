import functools
import signal
import subprocess
import time
# import winsound

from signals import Signals

print_now = functools.partial(print, flush=True)


def handler(signum, frame):
    print_now("Sub: handler for {}".format(Signals(signum).name))
    # winsound.Beep(signum * 1000, 500)


print_now("Sub: started")
print_now("Sub: creating Subsub, no flags")
subsub = subprocess.Popen(('python', 'subsub.py'))

for sig in Signals:
    try:
        signal.signal(sig, handler)
        print_now("Sub: registered handler for {}".format(sig.name))
    except ValueError:
        pass

for i in range(30):
    print_now("Sub: alive")
    time.sleep(3)
print_now("Sub: finished")
