import datetime
import board
import neopixel
import threading
import time
import socket
import serial
import logging 

logger = logging.getLogger(__name__)  # Use the current module's name
logger.setLevel(logging.DEBUG)  # Capture debug-level messages and above
# Create a file handler for logging
file_handler = logging.FileHandler('led_controller.log')
file_handler.setLevel(logging.DEBUG)
# Create a console handler to also print logs
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Optionally, show only INFO and above on the console
# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)



# LED Configuration
LED_COUNT = 24
OFF_COLOR = (0, 0, 0)  # Off
BRIGHTNESS = 1

leds = neopixel.NeoPixel(board.D18, LED_COUNT, brightness=BRIGHTNESS)

# Setup Serial Connection
ser = serial.Serial('/dev/ttyGS0', 9600)  # Adjust '/dev/ttyGS0' as needed

def handle_command(cmd):
    logger.debug(f"Received command: {cmd}")  # Log received command
    if cmd == 'chase':
        chase_effect(leds)
    elif cmd.startswith('color'):
        _, r, g, b = cmd.split(',')
        set_color(leds, int(r), int(g), int(b))
    elif cmd == 'off':
        leds.fill((0, 0, 0))
    elif cmd == 'on':
        leds.fill((255, 255, 255))
    else:
        logger.warning(f"Unrecognized command: {cmd}")  # Log unrecognized commands

def chase_effect(leds, delay=0.001, num_cycles=5):  
    colors = [(20, 20, 20), (20, 20, 20), (20, 20,  20)] 
    color_index = 0
    brightness_step = 0.01

    for _ in range(num_cycles):  
        for brightness in range(len(leds) * 2):  # Extended range for circular effect
            for i in range(len(leds)):
                offset_brightness = (brightness - i) % len(leds)  # Circular offset
                led_brightness = max(0, 1 - abs(offset_brightness) / len(leds))
                leds[i] = [int(c * led_brightness) for c in colors[color_index]]

            color_index = (color_index + 1) % len(colors) 

            leds.show()  
            time.sleep(delay)

    
def set_color(leds, r, g, b):
    """Set the entire strip to a single color."""
    color = (r, g, b)
    leds.fill(color)

while True:
    if ser.in_waiting > 0:
        command = ser.readline().decode('utf-8').strip()
        logger.info(f"Received signal: {command}")  # Log received signal
        try:
            handle_command(command)
        except Exception as e: 
            logger.error("Error handling command:", exc_info=True)  # Log exceptions