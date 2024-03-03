import board
import neopixel
import time
import signal
import sys
import random
from datetime import datetime

# Configuration
num_pixels = 70
pixel_pin = board.D18
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.01, auto_write=False)


# Definitions of character and number mappings, etc.
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

letter_matrix = [
    [60, 59, 58],
    [50, 51, 52],
    [44, 43, 42],
    [34, 35, 36],
    [28, 27, 26],
    [18, 19, 20]
]

char_mappings = {
    'A': [60,59,58,50,52,44,43,42,34,36,28,26],
    'B': [60,59,58,50,52,44,43,34,36,28,27,26],
    'C': [60,59,58,50,44,34,28,27,26],
    'D': [60,59,50,52,44,42,34,36,28,27],
    'E': [60,59,58,50,44,43,42,34,28,27,26],
    'F': [60,59,58,50,44,43,34,28],
    'G': [60,59,58,50,44,43,42,34,36,28,27,26],
    'H': [60,58,50,52,44,43,42,34,36,28,26],
    'I': [59,51,43,35,27],
    'J': [59,58,52,42,36,27,28],
    'K': [60,58,50,51,44,34,35,28,26],
    'L': [60,50,44,34,28,27,26],
    'M': [60,58,50,51,52,44,43,42,34,36,28,26],
    'N': [60,58,50,52,44,43,42,34,36,28,26],
    'O': [60,59,58,50,52,44,42,34,36,28,27,26],
    'P': [60,59,58,50,52,44,43,42,34,28],
    'Q': [60,59,58,50,52,44,42,34,36,28,27,26,25],
    'R': [60,59,58,50,52,44,43,42,34,28,35,26],
    'S': [60,59,58,50,44,43,42,36,28,27,26],
    'T': [60,59,58,51,43,35,27],
    'U': [60,58,50,52,44,42,34,36,28,27,26],
    'V': [60,58,50,52,44,42,34,36,27],
    'W': [60,58,50,52,44,43,42,34,35,36,28,27,26],
    'X': [60,58,50,52,43,34,36,28,26],
    'Y': [60,58,50,52,44,43,42,35,27],
    'Z': [60,59,58,52,43,34,28,27,26],
    '!': [59,51,43,27],
    '?': [59,50,52,42,35,27],
    '+': [51,44,43,42,35],
    '-': [44,43,42]

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

snake_path = [35, 34, 44, 50, 51, 52, 42, 36, 26, 27, 28, 29, 33, 45, 49, 61, 60, 59, 58, 57, 53, 41, 37, 25, 21, 20, 19, 18, 17, 16, 30, 32, 46, 48, 62, 64, 65, 66, 67, 68, 69, 70, 56, 54, 40, 38, 24, 22, 8, 9, 10, 11, 12, 13, 14]

fire_colors = [(255, 0, 0),  # Red
               (255, 100, 0), # Orange
               (255, 200, 0), # Yellow
               (255, 255, 100)] #  Lighter Yellow

# Initialize a buffer with the same length as the number of pixels
led_buffer = [(0, 0, 0) for _ in range(num_pixels)]

# Function to set an individual LED color
def set_led_color(led_id, color):
    if 0 <= led_id < num_pixels:
        pixels[led_id] = color

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

# Function to update the LED buffer for animations
def update_led_buffer(snake_path, head_index, snake_length, direction):
    global led_buffer  # Ensure we are modifying the global buffer
    # Fade the tail
    for i in range(len(led_buffer)):
        r, g, b = led_buffer[i]
        led_buffer[i] = (max(r - 10, 0), max(g - 10, 0), max(b - 10, 0))
    # Light up the snake
    for i in range(snake_length):
        led_index = snake_path[(head_index + direction * i) % len(snake_path)]  # Ensure wrapping within path
        led_buffer[led_index] = (0, 255 - (i * 255 // snake_length), 0)  # Green snake

def apply_buffer_to_leds():
    for i in range(num_pixels):
        pixels[i] = led_buffer[i]
    pixels.show()

def snake_animation(snake_path, snake_length=10):
    direction = 1  # Start moving forward
    head_index = 0
    try:
        while True:
            update_led_buffer(snake_path, head_index, snake_length, direction)
            apply_buffer_to_leds()
            time.sleep(0.1)  # Increase delay for visibility

            # Update head index and direction
            head_index += direction
            if head_index >= len(snake_path) or head_index < 0:
                direction *= -1  # Change direction
                head_index += direction  # Adjust head index to stay within bounds
    except KeyboardInterrupt:
        clear_leds()
        print('Animation stopped.')

# Function to display characters or numbers
def display_character():
    clear_leds()  # Ensure a clear matrix before displaying a new character

    while True:  # Keep asking for input until a valid character is given
        char = input("Enter a single character to display: ").upper()  # Get input and convert to uppercase
        if len(char) == 1 and char in char_mappings:  # Validate: Must be a single character
            break  # Exit the loop if we have a valid character
        else:
            print("Invalid input. Please enter a single character.")
  
    for led_id in char_mappings[char]:
        set_led_color(led_id, (0, 255, 0))  # Green color for demonstration
    pixels.show()


def display_number(number):
    clear_leds()  # Ensure a clear matrix before displaying a new number
    if number in number_mappings:
        for led_id in number_mappings[number]:
            set_led_color(led_id, (0, 255, 0))  # Green color for demonstration
    pixels.show()

# Function to run number display sequence
def run_numbers():
    try:
        for number in number_mappings:
            display_number(number)
            time.sleep(1)  # Pause for visibility
            clear_leds()
    except KeyboardInterrupt:
        clear_leds()
        print('Number display stopped.')

# Fire animation corrected
def fire_animation():
    global led_buffer  # Use the global led_buffer for the animation
    try:
        while True:
            # Simulate fire by randomly choosing colors for the bottom row and fading upwards
            for i in range(num_pixels):
                if random.randint(0, 1):  # Randomly decide whether to update a pixel to simulate flickering
                    led_buffer[i] = random.choice(fire_colors)  # Choose a random fire color
                # Fade color upwards
                if i < num_pixels - 7:  # Avoid overflow
                    led_buffer[i] = tuple(max(0, val - 10) for val in led_buffer[i + 7])

            # Apply the updated buffer to the LEDs
            apply_buffer_to_leds()
            time.sleep(0.1)  # Short delay for animation speed
    except KeyboardInterrupt:
        clear_leds()
        print('Fire animation stopped.')
# Clock animation
def update_clock_display():
    now = datetime.now()
    hour, minute, second = now.hour % 12, now.minute, now.second

    # Hour to LED mapping as provided
    hour_led_mapping = {
        12: 67, 1: 58, 2: 53, 3: 40, 4: 37, 5: 26,
        6: 19, 7: 28, 8: 33, 9: 48, 10: 49, 11: 60
    }

    # Clear the LED matrix
    clear_leds()

    # Calculate positions
    hour_pos = hour_led_mapping.get(hour if hour else 12)  # 0 hour is treated as 12

    # For minutes and seconds, find the closest hour position
    minute_index = (minute // 5) % 12  # Divide the 60 minutes into 12 segments
    second_index = (second // 5) % 12  # Same for seconds

    # Map minute and second indices to the LED positions used for hours
    minute_pos = hour_led_mapping.get(minute_index + 1)  # +1 because dictionary keys start at 1, not 0
    second_pos = hour_led_mapping.get(second_index + 1)

    # Set colors for each hand
    hour_color = (255, 0, 0)  # Red for hours
    minute_color = (0, 0, 255)  # Green for minutes
    second_color = (0, 255, 0)  # Blue for seconds

    # Update LED colors for hour, minute, and second
    pixels.fill((0, 0, 0))  # Clear all first to avoid mixing colors
    pixels[hour_pos] = hour_color  # Set hour
    if minute_pos != hour_pos:  # Avoid overwriting the hour LED if they overlap
        pixels[minute_pos] = minute_color  # Set minute
    if second_pos not in [hour_pos, minute_pos]:  # Avoid overwriting hour and minute LEDs if they overlap
        pixels[second_pos] = second_color  # Set second

    # Update the display
    pixels.show()






########################################

display_character()
    