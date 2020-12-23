from rpi_ws281x import Color, PixelStrip, ws

class NeoStrip:

    strip = None

    def __init__(self):
        # LED strip configuration:
        LED_COUNT = 32  # Number of LED pixels.
        LED_PIN = 10  # GPIO pin connected to the pixels (must support PWM!).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 10  # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL = 0
        LED_STRIP = ws.WS2811_STRIP_GRB

        # Create PixelStrip object with appropriate configuration.
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ,
                           LED_DMA, LED_INVERT, LED_BRIGHTNESS,
                           LED_CHANNEL, LED_STRIP)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def clearBuffer(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))

    def clear(self):
        self.clearBuffer()
        self.strip.show()


    def test(self):
        for r in range(255):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(r, 0, 0))
            self.strip.show()
        for r in range(255):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(255 - r, 0, 0))
            self.strip.show()

        for g in range(255):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(0, g, 0))
            self.strip.show()
        for g in range(255):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(0, 255 - g, 0))
            self.strip.show()

        for b in range(255):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(0, 0, b))
            self.strip.show()
        for b in range(255):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(0, 0, 255 - b))
            self.strip.show()

    def vol_update(self, volume):
        volumePosition = int(volume*(self.strip.numPixels()-1)/100)
        self.clearBuffer()
        for i in range(volumePosition):
            self.strip.setPixelColor(i, Color(0, 0, 20))

        # Color up
        for i in range(23):
            self.strip.setPixelColor(volumePosition, Color(0, 0, 25+i*10))
            self.strip.show()

        # Color down
        for i in range(23):
            self.strip.setPixelColor(volumePosition, Color(0, 0, 255 - i * 10))
            self.strip.show()


