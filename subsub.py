import functools
import time

print_now = functools.partial(print, flush=True)

print_now("Subsub: started")
for i in range(30):
    print_now("Subsub: alive")
    time.sleep(3)
print_now("Subsub: finished")
