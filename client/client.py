import config

import pygame
import socket
import json
from time import sleep


def shift_scale(value, curr_min, curr_max, target_min, target_max):
    curr_center = (curr_min + curr_max) / 2
    target_center = (target_min + target_max) / 2
    shift_amt = target_center - curr_center
    curr_range = curr_max - curr_min
    target_range = target_max - target_min
    scale_amt = target_range / curr_range
    shifted_scaled = (value * scale_amt) + shift_amt
    return shifted_scaled


def send_command(sock, cmd_obj):
    msg = json.dumps(cmd_obj)
    print msg
    sock.sendto(msg, (config.SERVER_IP, config.SERVER_PORT))


class Commands:
    def __init__(self, socket):
        self.sock = socket

    def off(self):
        send_command(self.sock, {'cmd': 'off'})

    def on(self):
        send_command(self.sock, {'cmd': 'on'})

    def set(self, pins):
        send_command(self.sock, {'cmd': 'set', 'pins': pins})


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
commands = Commands(sock)

pygame.init()
print pygame.joystick.get_count()
j = pygame.joystick.Joystick(0)
j.init()
print 'Initialized joystick: %s' % j.get_name()


def joystick_values():
    out = [0] * (j.get_numaxes() + j.get_numbuttons())
    it = 0  # iterator
    pygame.event.pump()
    # Read input from the two joysticks
    for i in range(0, j.get_numaxes()):
        out[it] = j.get_axis(i)
        it += 1
    # Read input from buttons
    for i in range(0, j.get_numbuttons()):
        out[it] = j.get_button(i)
        it += 1
    return out


send_set_commands = False


while True:
    sleep(config.CMD_INTERVAL)

    js = joystick_values()
    on_button = js[config.BUTTONS['on']]
    off_button = js[config.BUTTONS['off']]
    lift_axis = js[config.AXES['lift']]

    if off_button:
        send_set_commands = False
        commands.off()
        continue

    if on_button:
        send_set_commands = True
        commands.on()

    if send_set_commands:
        scaled_lift_axis = shift_scale(lift_axis, 1, -1, 0, 100)
        commands.set({'lift': scaled_lift_axis})
