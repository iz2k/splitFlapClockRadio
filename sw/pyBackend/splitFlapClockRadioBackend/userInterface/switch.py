import pigpio
import time

class switch:
    # Default values for the switch
    sw_debounce = 300
    long_press_opt = False
    sw_short_callback = None
    sw_long_callback = None
    wait_time = time.time()
    long = False

    def __init__(self, I=None, G=None):

        def sw_rise(gpio, level, tick):
            if self.long_press_opt:
                if not self.long:
                    self.short_press()

        def sw_fall(gpio, level, tick):
            if self.long_press_opt:
                self.long = False
                press_time = time.time()
                while self.pi.read(self.I) == 0:
                    self.wait_time = time.time()
                    time.sleep(0.1)
                    if self.wait_time - press_time > 1:
                        self.long_press()
                        self.long = True
                        break
            else:
                self.short_press()

        if I is not None:
            self.I = I
            self.pi = pigpio.pi()
            self.pi.set_mode(I, pigpio.INPUT)
            self.pi.set_pull_up_down(self.I, pigpio.PUD_UP)
            self.pi.set_glitch_filter(self.I, self.sw_debounce)
            self.sw_falling = self.pi.callback(self.I, pigpio.FALLING_EDGE, sw_fall)
            self.sw_rising = self.pi.callback(self.I, pigpio.RISING_EDGE, sw_rise)

        # Set fake ground if specified
        if G is not None:
            self.pi.set_mode(G, pigpio.OUTPUT)
            self.pi.write(G, 0)

    def setup_switch(self, **kwargs):
        if 'debounce' in kwargs:
            self.sw_debounce = kwargs['debounce']
        if 'long_press' in kwargs:
            self.long_press_opt = kwargs['long_press']
        if 'sw_short_callback' in kwargs:
            self.sw_short_callback = kwargs['sw_short_callback']
        if 'sw_long_callback' in kwargs:
            self.sw_long_callback = kwargs['sw_long_callback']

    def short_press(self):
        self.sw_short_callback()

    def long_press(self):
        self.sw_long_callback()
