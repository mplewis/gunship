class PWM:
    @staticmethod
    def start(pin, duty, freq):
        print '*** PWM.start(%s, %s, %s)' % (pin, duty, freq)

    @staticmethod
    def set_duty_cycle(pin, duty):
        print '*** PWM.set_duty_cycle(%s, %s)' % (pin, duty)
