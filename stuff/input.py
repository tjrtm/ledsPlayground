import serial
import board
import neopixel
import time

# LED Configuration
LED_COUNT = 24
BRIGHTNESS = 0.1

# Initialize LEDs
leds = neopixel.NeoPixel(board.D18, LED_COUNT, brightness=BRIGHTNESS)

# Setup Serial Connection
ser = serial.Serial('/dev/ttyGS0', 9600)  # Adjust '/dev/ttyGS0' as needed

def handle_command(cmd):
    """Handle incoming commands to control the LEDs."""
    if cmd == 'chase':
        chase_effect(leds)
    elif cmd.startswith('color'):
        _, r, g, b = cmd.split(',')
        set_color(leds, int(r), int(g), int(b))
    elif cmd == 'off':
        leds.fill((0, 0, 0))

def chase_effect(leds, delay=0.1):
    # Your existing chase_effect function
    pass

def set_color(leds, r, g, b):
    """Set the entire strip to a single color."""
    color = (r, g, b)
    leds.fill(color)

while True:
    if ser.in_waiting > 0:
        command = ser.readline().decode('utf-8').strip()
        print(command)
        handle_command(command)
