import board
import neopixel
import time
import random

num_pixels = 24
pixel_pin = board.D18
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)

# Mapping from your LED matrix layout
led_mapping = [
    [0, 1, 2, 3],
    [8, 7, 6, 5],
    [10, 11, 12, 13],
    [18, 17, 16, 15],
    [20, 21, 22, 23]
]

def clear_pixels():
    for i in range(num_pixels):
        pixels[i] = (0, 0, 0)
    pixels.show()

def get_random_led():
    y = random.randint(0, 4)  # Random row
    x = random.randint(0, 3)  # Random column
    return led_mapping[y][x]

def fade_led(led_index, up=True, max_brightness=255, steps=30, wait=0.01):
    step_size = max_brightness / steps
    if up:  # Fade in
        for brightness in range(0, max_brightness + 1, int(step_size)):
            pixels[led_index] = (brightness, brightness, brightness)
            pixels.show()
            time.sleep(wait)
    else:  # Fade out
        for brightness in range(max_brightness, -1, -int(step_size)):
            pixels[led_index] = (brightness, brightness, brightness)
            pixels.show()
            time.sleep(wait)

def raindrop_effect():
    while True:
        led_index = get_random_led()
        fade_led(led_index, up=True, steps=30, wait=0.01)  # Fade in
        fade_led(led_index, up=False, steps=30, wait=0.01)  # Fade out

# Start the raindrop effect
raindrop_effect()
