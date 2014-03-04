import pygame

pygame.init()
print '%s joystick(s) found.' % pygame.joystick.get_count()
j = pygame.joystick.Joystick(0)
j.init()
print 'Initialized joystick: %s' % j.get_name()


def get():
    out = [0] * (j.get_numaxes() + j.get_numbuttons())
    it = 0  # iterator
    pygame.event.pump()

    # Read input from the axes
    for i in range(0, j.get_numaxes()):
        out[it] = j.get_axis(i)
        it += 1
    # Read input from the buttons
    for i in range(0, j.get_numbuttons()):
        out[it] = j.get_button(i)
        it += 1
    return out


def test():
    last_vals = get()
    while True:
        curr_vals = get()
        for index, val in enumerate(curr_vals):
            if last_vals[index] != val:
                print '%02d' % index, val
        last_vals = curr_vals

if __name__ == '__main__':
    test()
