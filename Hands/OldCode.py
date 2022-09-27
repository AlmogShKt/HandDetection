from screeninfo import  get_monitors
from pynput.mouse import Button, Controller

for m in get_monitors():
    if m.is_primary:
        print(m)
