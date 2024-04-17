import board
import neopixel
import time

# Configuration for the LED matrix
NUM_PIXELS = 79
PIXEL_PIN = board.D18
BRIGHTNESS = 1
AUTO_WRITE = False
TEXT_COLOR = (255, 255, 0)  # Yellow text color
BACKGROUND_COLOR = (0, 0, 255)  # Dark blue background color

# Initialize the LED strip
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=AUTO_WRITE)

# Import LED matrix mapping and character mappings
from led_mapping import led_matrix, char_mappings

def fade_color(color, fade_factor):
    """Apply fade effect to the color."""
    return tuple(int(c * fade_factor) for c in color)

def display_char(char, offset_x, position, total_length):
    """Displays a single character at a given horizontal offset with fading based on position."""
    if char in char_mappings:
        for led_index in char_mappings[char]:
            # Calculate x, y based on the full LED matrix
            for row_index, row in enumerate(led_matrix['full']):
                if led_index in row:
                    y = row_index
                    x = row.index(led_index)
                    break
            x += offset_x  # Apply horizontal offset
            if 0 <= x < 7:  # Check if the x position is within the display bounds
                # Apply fading based on the position of the character
                fade_factor = 1 - abs(position - x) / total_length
                faded_color = fade_color(TEXT_COLOR, fade_factor)
                pixel_index = led_matrix['full'][y][x]
                pixels[pixel_index] = faded_color

def clear_display():
    """Sets all pixels to the background color."""
    pixels.fill(BACKGROUND_COLOR)
    pixels.show()

def scroll_text(text, speed=0.1):
    """Scrolls text from right to left across the LED matrix."""
    text = text.upper()  # Convert all text to uppercase
    length = len(text)
    max_offset = 7 + length * 6  # Calculate the maximum offset needed to scroll all text off-screen
    total_length = 7 + length * 6  # Total animation length for fading calculation
    for offset in range(max_offset):
        clear_display()
        for i, char in enumerate(text):
            char_position = 7 - offset + i * 6  # Position of each character
            display_char(char, char_position, i * 6, total_length)  # Pass position to adjust fading
        pixels.show()
        time.sleep(speed)

if __name__ == "__main__":
    try:
        while True:
            scroll_text("HELLO WORLD ")
    except KeyboardInterrupt:
        pixels.fill((0, 0, 0))
        pixels.show()
        print("Animation stopped by user.")
