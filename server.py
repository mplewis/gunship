import socket
from Adafruit_BBIO import PWM

UDP_IP = '0.0.0.0'
UDP_PORT = 5005

PWM_PIN = 'P9_22'
PWM_START_DUTY = 0
PWM_FREQ = 100

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

PWM.start(PWM_PIN, PWM_START_DUTY, PWM_FREQ)

print 'Serving on IP %s, port %s' % (UDP_IP, UDP_PORT)
print 'PWM on pin %s at freq. %s' % (PWM_PIN, PWM_FREQ)

while True:
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    try:
        new_pwm = ((100 - (float(data) + 1) * 50) * 0.1) + 10
        if new_pwm > 100:
                new_pwm = 100
        if new_pwm < 0:
                new_pwm = 0
        PWM.set_duty_cycle(PWM_PIN, new_pwm)
        print 'New PWM: %s' % new_pwm
    except TypeError:
        print 'TypeError: %s' % data
