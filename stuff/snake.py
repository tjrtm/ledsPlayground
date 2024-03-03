import time
import board
import neopixel

# Configuration
NUM_PIXELS = 79  # The number of LEDs in your strip
PIN_NEO_PIXEL = board.D18  # The pin that the NeoPixel strip is connected to
SNAKE_LENGTH = 12  # The length of the snake
REVERSE = False  # Set to True if you want the animation to reverse at the end of the strip

# Initialize the NeoPixel strip
pixels = neopixel.NeoPixel(PIN_NEO_PIXEL, NUM_PIXELS, brightness=0.008, auto_write=False)

def snake_animation():
    direction = 1
    head = 0
    while True:
        # Set the color of the snake
        for i in range(SNAKE_LENGTH):
            if head - i * direction >= 0 and head - i * direction < NUM_PIXELS:
                # The color of the snake fades from the head to the tail
                pixels[head - i * direction] = (0, 255 // (i + 1), 0)

        # Update the display
        pixels.show()

        # Clear the tail of the snake
        tail = head - SNAKE_LENGTH * direction
        if tail >= 0 and tail < NUM_PIXELS:
            pixels[tail] = (10, 10, 10)

        # Move the head of the snake
        head += direction

        # If the head of the snake has reached the end of the strip, reverse the direction
        if REVERSE and (head == NUM_PIXELS - 1 or head == 0):
            direction = -direction

        # If the head of the snake has reached the end of the strip and we're not reversing, wrap around to the start
        if not REVERSE and head == NUM_PIXELS:
            head = 0

        # Wait for a bit
        time.sleep(0.5)

# Run the snake animation
snake_animation()
