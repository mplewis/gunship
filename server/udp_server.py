import config

import socket
import json
from Adafruit_BBIO import PWM


def reply(ip, data_obj):
    msg = json.dumps(data_obj)
    sock.sendto(msg, (ip, config.REPLY_PORT))


class Device:

    @staticmethod
    def off(ip):
        global device_enabled
        device_enabled = False
        print '[CMD] OFF'
        reply(ip, {'ack': 'off'})

    @staticmethod
    def on(ip):
        global device_enabled
        device_enabled = True
        print '[CMD] ON'
        reply(ip, {'ack': 'on'})

    @staticmethod
    def set(ip, pins):
        # Validate all pins and PWM values
        for name, pwm in pins.iteritems():
            if name not in PWM_PINS.keys():
                print '[NOPIN]', name, pins
                reply(ip, {'err': 'nopin',
                           'details': {'name': name, 'pins': pins}})
                return
            if pwm < config.PWM_MIN or pwm > config.PWM_MAX:
                print '[BADPWM]', name, pwm, pins
                reply(ip, {'err': 'badpwm',
                           'details': {'name': name, 'pwm': pwm,
                                       'pins': pins}})
                return
        # Set PWM values for pins
        for name, pwm in pins.iteritems():
            pin = PWM_PINS[name]
            PWM.set_duty_cycle(pin, pwm)
        print '[CMD] SET', pins
        reply(ip, {'ack': 'set'})

    @staticmethod
    def read(ip):
        print '[CMD] READ'
        reply(ip, {'ack': 'read'})

    @staticmethod
    def option(ip, options):
        print '[CMD] OPTION', options
        reply(ip, {'ack': 'option'})


with open('pins.json', 'r') as f:
    PWM_PINS = json.load(f)


device_enabled = False


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((config.SERVER_IP, config.SERVER_PORT))
print 'Serving on IP %s, port %s' % (config.SERVER_IP, config.SERVER_PORT)
print 'Replying on UDP port %s' % config.REPLY_PORT

for name, settings in PWM_PINS.iteritems():
    pin = settings['pin']
    duty = settings['pwm_start_duty']
    freq = settings['pwm_freq']
    PWM.start(pin, duty, freq)
    print ('Started PWM for %s on pin %s at duty %s, freq. %s' %
           (name, pin, duty, freq))

while True:
    raw_data, addr = sock.recvfrom(config.BUFFER_SIZE)
    (ip, port) = addr

    try:
        data = json.loads(raw_data)
    except ValueError:
        print '[MALFORM]', raw_data
        reply(ip, {'err': 'malform', 'details': {'data': raw_data}})
        continue

    if 'cmd' not in data:
        print '[NOCMD]', raw_data
        reply(ip, {'err': 'nocmd', 'details': {'data': data}})
        continue

    cmd = data['cmd']

    if not device_enabled and cmd != 'on':
        Device.off(ip)
        continue

    if cmd not in config.ACCEPTED_COMMANDS:
        print '[INVALCMD]', raw_data
        reply(ip, {'err': 'invalcmd', 'details': {'data': data}})
        continue

    if cmd == 'on':
        Device.on(ip)

    elif cmd == 'off':
        Device.off(ip)

    elif cmd == 'set':
        if 'pins' not in data:
            print '[SETNOPINS]', raw_data
            reply(ip, {'err': 'setnopins', 'details': {'data': data}})
            continue
        Device.set(ip, data['pins'])

    elif cmd == 'read':
        Device.read(ip)

    elif cmd == 'option':
        if 'options' not in data:
            print '[OPTNOOPTS]', raw_data
            reply(ip, {'err': 'optnoopts', 'details': {'data': data}})
            continue
        Device.option(ip, data['options'])
