import board
import neopixel
import time
import math

num_pixels = 24
pixel_pin = board.D18
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, auto_write=False)
pixels.brightness = 0.01
led_mapping = [
    [0, 1, 2, 3],
    [8, 7, 6, 5],
    [10, 11, 12, 13],
    [18, 17, 16, 15],
    [20, 21, 22, 23]
]

def get_led_index(x, y):
    if 0 <= y < len(led_mapping) and 0 <= x < len(led_mapping[0]):
        return led_mapping[y][x]
    return None

def clear_pixels():
    for i in range(num_pixels):
        pixels[i] = (0, 0, 0)
    pixels.show()

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def apply_fade_effect(color, distance, max_distance):
    fade_factor = max(0, 1 - (distance / max_distance))
    faded_color = tuple(int(c * fade_factor) for c in color)
    return faded_color

def ripple_effect(origin_x, origin_y, max_radius, color, steps, wait):
    while True:  # Loop to make the animation repeat
        for step in range(steps):
            radius = step / steps * max_radius
            clear_pixels()
            for y in range(5):
                for x in range(4):
                    dist = distance(x, y, origin_x, origin_y)
                    if dist <= radius:
                        led_index = get_led_index(x, y)
                        if led_index is not None:
                            faded_color = apply_fade_effect(color, dist, radius)
                            pixels[led_index] = faded_color
            pixels.show()
            time.sleep(wait)
        time.sleep(1)  # Pause before repeating the effect

from letters import get_digit_patterns  # Assuming you saved the digits in the letters.py file for simplicity

def display_digit(digit):
    patterns = get_digit_patterns()
    pattern = patterns.get(str(digit), "00000000000000000000")  # Default to all off if digit not found
    for y in range(5):
        for x in range(4):
            bit = int(pattern[y * 4 + x])
            led_index = get_led_index(x, y)
            pixels[led_index] = (255, 255, 255) * bit or (0, 0, 0)

# Example: Display the digit "2"
display_digit('2')
