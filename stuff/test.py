import board
import neopixel
import time
import signal
import sys
import random 

# Configuration
num_pixels = 70
pixel_pin = board.D18
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False)

# Initialize a buffer with the same length as the number of pixels
led_buffer = [(0, 0, 0) for _ in range(num_pixels)]

# LED Matrix Mapping
led_matrix = [
    [78, 77, 76, 75, 74, 73, 72],
    [64, 65, 66, 67, 68, 69, 70],
    [62, 61, 60, 59, 58, 57, 56],
    [48, 49, 50, 51, 52, 53, 54],
    [46, 45, 44, 43, 42, 41, 40],
    [32, 33, 34, 35, 36, 37, 38],
    [30, 29, 28, 27, 26, 25, 24],
    [16, 17, 18, 19, 20, 21, 22],
    [14, 13, 12, 11, 10, 9, 8],
    [0, 1, 2, 3, 4, 5, 6]
]

# Function to set an individual LED color
def set_led_color(led_id, color):
    if 0 <= led_id < num_pixels:
        pixels[led_id] = color
        pixels.show()

# Function to clear all LEDs
def clear_leds():
    for i in range(num_pixels):
        pixels[i] = (0, 0, 0)
    pixels.show()

# Graceful shutdown handler
def signal_handler(sig, frame):
    print('Interrupt received, shutting down...')
    clear_leds()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Update the LED buffer for snake animation
def update_led_buffer(snake_path, head_index, snake_length, direction):
    # Fade the tail
    for i in range(len(led_buffer)):
        r, g, b = led_buffer[i]
        # Adjust the fading effect here if needed
        led_buffer[i] = (max(r - 10, 0), max(g - 10, 0), max(b - 10, 0))

    # Light up the snake
    for i in range(snake_length):
        led_index = head_index + direction * i
        if 0 <= led_index < len(snake_path):
            led_position = snake_path[led_index]
            if 0 <= led_position < len(led_buffer):
                # Control the color of the snake here
                intensity = 255 - (i * 255 // snake_length)
                # For a red snake
                red = 0 # intensity
                green = 255  # Adjust this for different colors
                blue = 0   # Adjust this for different colors
                led_buffer[led_position] = (red, green, blue)


def apply_buffer_to_leds():
    for i in range(num_pixels):
        pixels[i] = led_buffer[i]
    pixels.show()

def snake_animation(snake_path, snake_length=1):
    direction = 1  # Start moving forward
    head_index = 0
    while True:
        update_led_buffer(snake_path, head_index, snake_length, direction)
        apply_buffer_to_leds()
        time.sleep(0.01)

        # Update head index and reverse direction at ends
        head_index += direction
        if head_index == len(snake_path) - snake_length and direction == 1:
            direction = -1  # Start moving backward
        elif head_index == 0 and direction == -1:
            direction = 1  # Start moving forward again

snake_path = [35, 34, 44, 50, 51, 52, 42, 36, 26, 27, 28, 29, 33, 45, 49, 61, 60, 59, 58, 57, 53, 41, 37, 25, 21, 20, 19, 18, 17, 16, 30, 32, 46, 48, 62, 64, 65, 66, 67, 68, 69, 70, 56, 54, 40, 38, 24, 22, 8, 9, 10, 11, 12, 13, 14]

# Start the animation
#snake_animation(snake_path)

# Compressed mappings for A, B, and C based on the given LED matrix layout
char_mappings = {
    'A': [77, 76, 75, 74, 73, 65, 61, 49, 45, 33, 29, 17, 13, 1]
}



number_mappings = {
    '1': [67, 59, 51, 43, 35, 27, 19],
    '2': [66, 67, 68, 58, 52, 42, 43, 44, 34, 28, 18, 19, 20],
    '3': [66, 67, 68, 58, 52, 42, 43, 44, 36, 26, 20, 19, 18],
    '4': [66, 68, 60, 58, 50, 52, 44, 43, 42, 36, 26, 20],
    '5': [66, 67, 68, 60, 50, 44, 43, 42, 36, 26, 20, 19, 18],
    '6': [66, 67, 68, 60, 50, 44, 43, 42, 34, 36, 28, 26, 18, 19, 20],
    '7': [66, 67, 68, 60, 58, 52, 42, 36, 26, 20 ],
    '8': [66, 67, 68, 60, 58, 50, 52, 44, 43, 42, 34, 36, 28, 26, 18, 19, 20],
    '9': [66, 67, 68, 60, 58, 50, 52, 44, 43, 42, 36, 26, 18, 19, 20],
    '0': [66, 67, 68, 60, 58, 50, 52, 44, 42, 34, 36, 28, 26, 18, 19, 20]
} 

# Explanation:
# - For A, LEDs are chosen to create two slanting lines meeting at a point on top and a crossbar in the middle.
# - For B, LEDs outline the perimeter of B and include lines to form the top, middle, and bottom horizontal strokes.
# - For C, LEDs form the perimeter of C without closing off the C shape.


def display_character(char):
    if char in char_mappings:
        # Turn off all LEDs before displaying a new character
        clear_leds()
        # Retrieve the LED positions for the character and light them up
        for pos in char_mappings[char]:
            set_led_color(pos, (0, 10, 0))  # Example: white color
        pixels.show()

def display_number(number):
    # Clear the LED matrix before displaying the new number
    clear_leds()
    # Retrieve the LED positions for the current number and light them up
    if number in number_mappings:
        for pos in number_mappings[number]:
            set_led_color(pos, (0, 10, 0))  # Set color to white
        pixels.show()


# Iterate through each number and display it
def run_numbers():        
    for number in number_mappings:
        display_number(number)
        time.sleep(0.5)  # Pause for 1 second between numbers
        clear_leds()  # Clear the display before showing the next number

# Test if all numbers displayed correct
# while True:
#     try:
#         run_numbers()
#     except(KeyboardInterrupt):
#         clear_leds()
#         print('stopped')

fire_colors = [(255, 0, 0),  # Red
               (255, 100, 0), # Orange
               (255, 200, 0), # Yellow
               (255, 255, 100)] #  Lighter Yellow

# Initialize two buffers, start with them blank
led_buffer_1 = [(0, 0, 0) for _ in range(num_pixels)]
led_buffer_2 = [(0, 0, 0) for _ in range(num_pixels)]

def fire_animation():
    buffer_index = 0
    while True:
        active_buffer = led_buffer_1 if buffer_index == 0 else led_buffer_2
        next_buffer = led_buffer_2 if buffer_index == 0 else led_buffer_1

        # Simulate fire:
        for y in range(10):  # Iterate over rows
            for x in range(7):  # Iterate over columns
                index_in_matrix = y * 7 + x  # Calculate the index in the linear led_matrix
                rand_shift = random.randint(0, 50)
                # Base of the fire is brighter
                brightness_index = min(i // 5, len(fire_colors) - 1) 
                color = fire_colors[brightness_index]

                # Adjust color with the random shift
                adjusted_color = (max(0, color[0] - rand_shift),
                                max(0, color[1] - rand_shift // 2),
                                0) 

                next_buffer[index_in_matrix] = adjusted_color  # Update the buffer

        # Swap buffers for smooth effect
        for i in range(num_pixels):
            brightness_index = min(i // 5, len(fire_colors) - 1) 
            color = fire_colors[brightness_index] 
            pixels[i] = active_buffer[i]
        pixels.show()

    buffer_index = (buffer_index + 1) % 2  
    time.sleep(0.02) 

fire_animation()     