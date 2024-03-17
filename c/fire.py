import time
import sys
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 79        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define functions:
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def parseColor(hexColor):
    """Parse a hex color string to an RGB color."""
    red = int(hexColor[0:2], 16)
    green = int(hexColor[2:4], 16)
    blue = int(hexColor[4:6], 16)
    return Color(red, green, blue)

def main(color="FF0000", infinite=False):
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    try:
        while True:
            colorWipe(strip, parseColor(color))  # Green wipe
            if not infinite:
                break
            time.sleep(1)  # Delay between animations
    except KeyboardInterrupt:
        colorWipe(strip, Color(0, 0, 0), 10)

if __name__ == "__main__":
    hexColor = "00FF00"  # Default to green
    infinite = False     # Default to run once

    if len(sys.argv) > 1:
        hexColor = sys.argv[1]
    if len(sys.argv) > 2:
        infinite = sys.argv[2] == "1"

    main(hexColor, infinite)
