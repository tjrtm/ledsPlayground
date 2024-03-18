import board
import neopixel
import serial
import time

# Configuration
NUM_PIXELS = 79
PIXEL_PIN = board.D18
BRIGHTNESS = 0.9
AUTO_WRITE = True
SERIAL_PORT = '/dev/ttyGS0'  # Adjust as needed for your setup
BAUD_RATE = 9600

pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=AUTO_WRITE)

def rgb_to_brightness(rgb):
    max_value = max(rgb)
    brightness = 0.01 + (max_value - 10) * (0.89 / (255 - 10))
    return round(max(0.01, min(0.9, brightness)), 2)

def fade_to_brightness(new_brightness):
    step = (new_brightness - pixels.brightness) / 10
    for _ in range(10):
        pixels.brightness += step
        pixels.fill((255, 255, 255))  # Fill with white color during transition
        time.sleep(0.05)

# Setup serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
ser.flush()

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        if line.startswith('brightness:'):
            rgb_str = line.split(':')[1]
            rgb_values = tuple(map(int, rgb_str.split(',')))
            new_brightness = rgb_to_brightness(rgb_values)
            fade_to_brightness(new_brightness)
            print(f"Brightness adjusted to {new_brightness} based on RGB {rgb_str}")
