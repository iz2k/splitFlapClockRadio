import pigpio
import time

class rotary:
    last_A = 1
    last_B = 1
    last_gpio = 0

    last_event_time = time.time()
    debounce_time = 0

    def __init__(self, A=None, B=None, G=None, callback=None):
        if not A or not B:
            raise BaseException("Encoder pins must be specified!")
        self.pi = pigpio.pi()
        self.Enc_A = A
        self.Enc_B = B
        self.callback = callback

        self.pi.set_mode(self.Enc_A, pigpio.INPUT)
        self.pi.set_pull_up_down(self.Enc_A, pigpio.PUD_UP)
        self.pi.set_mode(self.Enc_B, pigpio.INPUT)
        self.pi.set_pull_up_down(self.Enc_B, pigpio.PUD_UP)

        self.pi.callback(self.Enc_A, pigpio.EITHER_EDGE, self.rotary_interrupt)
        self.pi.callback(self.Enc_B, pigpio.EITHER_EDGE, self.rotary_interrupt)

    def rotary_interrupt(self, gpio, level, tick):
        if gpio == self.Enc_A:
            self.last_A = level
        else:
            self.last_B = level;

        if gpio != self.last_gpio:
            self.last_gpio = gpio
            if gpio == self.Enc_A and level == 1:
                if self.last_B == 1:
                    if time.time() - self.last_event_time > self.debounce_time:
                        self.last_event_time = time.time()
                        if self.callback is not None:
                            self.callback(-1)
            elif gpio == self.Enc_B and level == 1:
                if self.last_A == 1:
                    if time.time() - self.last_event_time > self.debounce_time:
                        self.last_event_time = time.time()
                        if self.callback is not None:
                            self.callback(1)
