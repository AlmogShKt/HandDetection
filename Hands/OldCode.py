from screeninfo import  get_monitors
from pynput.mouse import Button, Controller

for m in get_monitors():
    if m.is_primary:
        print(m)
mouse = Controller()

# Read pointer position
print('The current pointer position is {0}'.format(
    mouse.position))

# Set pointer position
mouse.position = (0, 0)
print('Now we have moved it to {0}'.format(
    mouse.position))

mouse.move(750, 250)
mouse.position = (750, 250)

print('Now we have moved it to {0}'.format(
    mouse.position))
mouse.move(750, 250)
mouse.position = (750, 250)
print('Now we have moved it to {0}'.format(
    mouse.position))
mouse.move(750, 250)
mouse.position = (750, 250)
print('Now we have moved it to {0}'.format(
    mouse.position))
mouse.move(750, 250)
mouse.position = (750, 250)