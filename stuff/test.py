import board
import neopixel
import time
import termios, fcntl, sys, os
from flask import Flask, request, jsonify

# Configuration
NUM_PIXELS = 70
PIXEL_PIN = board.D18
BRIGHTNESS = 0.01
AUTO_WRITE = True
WHITE = (255,255,255)
BLACK = (0,0,0)
import led_mapping
from led_mapping import led_matrix, char_mappings, abc, number_mappings

app = Flask(__name__)

# Initialize NeoPixel
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=AUTO_WRITE)

# Initialize LED buffer
LED_BUFFER = [(0, 0, 0) for _ in range(NUM_PIXELS)]

# Function to set an individual LED color
def led_on(led_id, color=WHITE, clear=True):
    if 0 <= led_id < NUM_PIXELS:
        pixels[led_id] = color

def led_off(led_id, color=BLACK, clear=True):
    if 0 <= led_id < NUM_PIXELS:
        pixels[led_id] = color

def on(color=WHITE):
    # Use the fill() method to set all pixels to the specified color
    pixels.fill(color)

def off():
    on((0, 0, 0))

def display_letter(character, color=WHITE):
    char_upper = character.upper()  # Convert to uppercase for consistent lookup

    if char_upper in char_mappings: 
        led_positions = char_mappings[char_upper]
    elif char_upper in number_mappings:
        led_positions = number_mappings[char_upper]
    else: 
        return  # Do nothing if the character is not found in either mapping

    pixels.fill((0, 0, 0)) 
    for pos in led_positions:
        led_on(pos, color)

def display_sentence(sentence, color=(255,255,0), delay=0.05):
    """Displays a sentence letter by letter, with an optional delay between letters.

    Args:
        sentence (str): The sentence to display.
        color (tuple, optional): RGB color tuple for the letters. Defaults to WHITE.
        delay (float, optional): Delay in seconds between displaying each letter. Defaults to 0.5.
    """

    import time  # Import the time module for the delay

    for character in sentence:
        display_letter(character, color)
        time.sleep(delay) 
    off()

def custom_message():
    msg = input('Enter your message: ')
    display_sentence(msg)

fd = sys.stdin.fileno()  # Get file descriptor for standard input

oldterm = termios.tcgetattr(fd)  # Save old terminal settings
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO  # Configure for raw input
termios.tcsetattr(fd, termios.TCSANOW, newattr)

# ###################################################################################
# try:
#     while True:
#         try:
#             display_letter(os.read(fd, 1).decode('utf-8'))
#         except OSError:
#             pass 
# finally:
#     termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)  # Restore terminal settings#
# ####################################################################################


@app.route('/led/on', methods=['POST'])
def turn_led_on():
    data = request.get_json()
    led_id = data.get('led_id')
    color = data.get('color', (255, 255, 255))  # Default to white if not specified
    led_on(led_id, color)
    return jsonify({"message": f"LED {led_id} turned on with color {color}"}), 200

@app.route('/led/off', methods=['POST'])
def turn_led_off():
    data = request.get_json()
    led_id = data.get('led_id')
    led_off(led_id)
    return jsonify({"message": f"LED {led_id} turned off"}), 200

@app.route('/leds/on', methods=['POST'])
def turn_all_leds_on():
    data = request.get_json()
    color = data.get('color', (255, 255, 255))  # Default to white if not specified
    on(color)
    return jsonify({"message": "All LEDs turned on"}), 200

@app.route('/leds/off', methods=['GET'])
def turn_all_leds_off():
    off()
    return jsonify({"message": "All LEDs turned off"}), 200

@app.route('/led/display_letter', methods=['POST'])
def api_display_letter():
    data = request.get_json()
    character = data.get('character')
    color = data.get('color', (255, 255, 255))  # Default to white if not specified
    display_letter(character, color)
    return jsonify({"message": f"Displayed letter {character}"}), 200

@app.route('/led/display_sentence', methods=['POST'])
def api_display_sentence():
    data = request.get_json()
    sentence = data.get('sentence')
    color = data.get('color', (255, 255, 0))  # Default to yellow if not specified
    delay = data.get('delay', 0.05)
    display_sentence(sentence, color, delay)
    return jsonify({"message": f"Displayed sentence: {sentence}"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
