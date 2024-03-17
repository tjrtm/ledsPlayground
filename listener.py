import serial
import board
import neopixel
from led_mapping import char_mappings, number_mappings

# Serial communication configuration
serial_port = '/dev/ttyGS0'
baud_rate = 9600

# LED strip configuration
NUM_PIXELS = 79
PIXEL_PIN = board.D18
BRIGHTNESS = 0.01

# Initialize NeoPixel
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=True)

def led_on(index, color=(255, 255, 255)):
    if 0 <= index < NUM_PIXELS:
        pixels[index] = color

def led_off(index):
    led_on(index, (0, 0, 0))

def all_leds_on(color=(255, 255, 255)):
    pixels.fill(color)

def all_leds_off():
    pixels.fill((0, 0, 0))

def display_character(character, color=(255, 255, 255)):
    pixels.fill((0, 0, 0))  # Clear the display
    mapping = char_mappings.get(character.upper(), []) + number_mappings.get(character.upper(), [])
    for index in mapping:
        led_on(index, color)

def process_command(command):
    if command == "leds_on":
        all_leds_on()
    elif command == "leds_off":
        all_leds_off()
    else:
        print(f"Unknown command: {command}")

def listen_for_commands():
    try:
        with serial.Serial(serial_port, baud_rate, timeout=0.02) as ser:
            print("Listening for commands...")
            while True:
                ser.flushInput()  # Clear the buffer
                command = ser.readline().decode().strip()
                if command:  # If command is not empty
                    process_command(command)
    except Exception as e:
        print(f"Failed to listen on {serial_port}: {e}")

if __name__ == '__main__':
    listen_for_commands()
