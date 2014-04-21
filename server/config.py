ACCEPTED_COMMANDS = ['off', 'on', 'set', 'read', 'option']

SERVER_IP = '0.0.0.0'
SERVER_PORT = 7527
BUFFER_SIZE = 1024

REPLY_PORT = 7537

PWM_MIN = 0
PWM_MAX = 100

# Turn off PWM after SAFETY_INTERVAL * SAFETY_MAX_FAILURES seconds
SAFETY_INTERVAL = 0.1  # seconds
SAFETY_MAX_FAILURES = 10  # count

# Use a PWM mock for testing
DEBUG_PWM_LIB = False
