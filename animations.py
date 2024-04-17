import board
import neopixel
import time
import math

NUM_PIXELS = 79
PIXEL_PIN = board.D18
BRIGHTNESS = 1
AUTO_WRITE = False
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=AUTO_WRITE)

from led_mapping import led_matrix

# Function to calculate distance from the center
def distance_from_center(x, y):
    center_x, center_y = 3, 4  # Center of the 7x10 matrix
    return math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

# Generate a list of LEDs sorted by distance from the center
leds_by_distance = []
for y, row in enumerate(led_matrix['full']):
    for x, led in enumerate(row):
        dist = distance_from_center(x, y)
        leds_by_distance.append((led, dist))
leds_by_distance.sort(key=lambda x: x[1])

def color_gradient(fraction):
    """Calculate color based on fraction of the animation."""
    # This gradient goes from blue to white
    green = (0, 255, 0)
    blue = (0, 255, 0)
    white = (255, 255, 255)
    color = tuple(int(blue[i] + fraction * (white[i] - blue[i])) for i in range(3))
    return color

def water_ripple_effect():
    """Animate a water ripple effect from the center to the edges."""
    max_distance = max(dist for _, dist in leds_by_distance)
    steps = 50  # Number of steps in the ripple animation
    while True:
        for step in range(steps):
            fraction = step / steps
            for led, dist in leds_by_distance:
                if dist <= fraction * max_distance:
                    fade_fraction = 1 - (dist / (fraction * max_distance + 0.01))
                    color = color_gradient(fade_fraction)
                    pixels[led] = color
            pixels.show()
            time.sleep(0.01)
            # Fade out all LEDs slowly
            for i in range(NUM_PIXELS):
                r, g, b = pixels[i]
                pixels[i] = (max(r - 10, 0), max(g - 10, 0), max(b - 10, 0))
        time.sleep(0.05)  # Pause before repeating the ripple

def fade_color(start_color, end_color, step, total_steps):
    """ Calculate intermediate color for the fade effect """
    return tuple([
        start_color[i] + (end_color[i] - start_color[i]) * step // total_steps
        for i in range(3)
    ])

def animate_horizontal_lines():
    """ Animate horizontal lines moving from bottom to top with fade effect """
    while True:
        for row in range(10):  
            for step in range(10): 
                color = fade_color(WHITE, GREEN, step, 9)
                
                for pixel in led_matrix['full'][row]:
                    pixels[pixel] = color
                
                pixels.show()
                time.sleep(0.01)
                
                if step == 9:
                    for pixel in led_matrix['full'][row]:
                        pixels[pixel] = (0, 0, 0)
            
            pixels.fill((0, 0, 0))
            pixels.show()
            time.sleep(0.1)

if __name__ == "__main__":
    water_ripple_effect()