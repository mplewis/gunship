import pygame
import socket

UDP_IP = '192.168.1.116'
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pygame.init()
print pygame.joystick.get_count()
j = pygame.joystick.Joystick(0)
j.init()
print 'Initialized joystick: %s' % j.get_name()


def get():
    out = [0] * (j.get_numaxes() + j.get_numbuttons())
    it = 0  # iterator
    pygame.event.pump()

    #Read input from the two joysticks
    for i in range(0, j.get_numaxes()):
        out[it] = j.get_axis(i)
        it += 1
    #Read input from buttons
    for i in range(0, j.get_numbuttons()):
        out[it] = j.get_button(i)
        it += 1
    return out


def test():
    last_val = 0
    curr_val = 0
    was_armed = False
    while True:
        armed = get()[8]

        if not armed and was_armed:
            print 'Disarmed.'
            curr_val = 1
            sock.sendto(str(curr_val), (UDP_IP, UDP_PORT))
        elif armed and not was_armed:
            print 'ARMED!'

        if armed:
            curr_val = get()[3]
            if last_val != curr_val:
                sock.sendto(str(curr_val), (UDP_IP, UDP_PORT))

        if last_val != curr_val:
            print curr_val

        last_val = curr_val
        was_armed = armed

if __name__ == '__main__':
    test()
