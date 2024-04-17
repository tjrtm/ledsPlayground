import curses
import time
import random
import board
import neopixel

# Configuration for the LED matrix
NUM_PIXELS = 79
PIXEL_PIN = board.D18
BRIGHTNESS = 0.5
AUTO_WRITE = False
COLOR_SNAKE = (0, 255, 0)  # Green
COLOR_FOOD = (255, 0, 0)   # Red
COLOR_BACKGROUND = (0, 0, 0)  # Black

# Import LED matrix mapping
from led_mapping import led_matrix

# Initialize the LED strip
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=AUTO_WRITE)

# Mapping function to map 2D positions to LED indices
def get_led_index(x, y):
    return led_matrix['full'][y][x]

def prompt_restart(stdscr):
    """Prompt the user to restart the game or exit."""
    stdscr.addstr(0, 0, "Game Over! Press 'R' to restart or 'Q' to quit.")
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key in (ord('r'), ord('R')):
            return True
        elif key in (ord('q'), ord('Q')):
            return False

def main(stdscr):
    # Curses initialization
    curses.curs_set(0)
    stdscr.nodelay(0)  # Wait for key press
    stdscr.timeout(-1)  # Disable automatic keypress timeout
    stdscr.clear()

    while True:  # Game restart loop
        # Initial snake settings
        mid_x, mid_y = 3, 5  # Middle of a 7x10 matrix
        snake = [(mid_x, mid_y)]
        direction = 0  # No movement initially
        food = (random.randint(0, 6), random.randint(0, 9))
        while food == (mid_x, mid_y):
            food = (random.randint(0, 6), random.randint(0, 9))

        pixels.fill(COLOR_BACKGROUND)
        pixels.show()
        pixels[get_led_index(*food)] = COLOR_FOOD
        pixels[get_led_index(*snake[0])] = COLOR_SNAKE
        pixels.show()

        # Main game loop
        while True:
            key = stdscr.getch()
            if key in (ord('w'), ord('W')):
                direction = 'UP'
            elif key in (ord('s'), ord('S')):
                direction = 'DOWN'
            elif key in (ord('a'), ord('A')):
                direction = 'LEFT'
            elif key in (ord('d'), ord('D')):
                direction = 'RIGHT'

            if direction:
                head_x, head_y = snake[0]
                if direction == 'UP':
                    head_y -= 1
                elif direction == 'DOWN':
                    head_y += 1
                elif direction == 'LEFT':
                    head_x -= 1
                elif direction == 'RIGHT':
                    head_x += 1

                # Check for collisions
                if head_x not in range(7) or head_y not in range(10) or (head_x, head_y) in snake:
                    break  # Game over

                snake.insert(0, (head_x, head_y))

                # Check if snake eats food
                if snake[0] == food:
                    while food in snake:
                        food = (random.randint(0, 6), random.randint(0, 9))
                    pixels[get_led_index(*food)] = COLOR_FOOD
                else:
                    tail = snake.pop()
                    pixels[get_led_index(*tail)] = COLOR_BACKGROUND

                pixels[get_led_index(*snake[0])] = COLOR_SNAKE
                pixels.show()

        # Game over and prompt restart
        if not prompt_restart(stdscr):
            break

        # Clear screen for new game
        stdscr.clear()

    # Game over clean-up
    pixels.fill(COLOR_BACKGROUND)
    pixels.show()

if __name__ == "__main__":
    curses.wrapper(main)
