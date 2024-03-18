import board
import neopixel
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

# Configuration
NUM_PIXELS = 79
PIXEL_PIN = board.D18
BRIGHTNESS = 0.9
AUTO_WRITE = True
DEFAULT_COLOR = (255, 255, 255)  # Default color to display when adjusting brightness

app = Flask(__name__)
CORS(app)

pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=AUTO_WRITE)

def rgb_to_brightness(rgb):
    """Converts an RGB value to a brightness level."""
    max_value = max(rgb)  # Find the maximum value in the RGB tuple
    # Map the max value from 10-255 range to 0.01-0.9 range
    brightness = 0.01 + (max_value - 10) * (0.89 / (255 - 10))
    return round(max(0.01, min(0.9, brightness)), 2)  # Ensure brightness is within bounds and rounded

def fade_to_brightness(new_brightness, color=DEFAULT_COLOR):
    """Fades the brightness to a new value over 0.5 seconds while turning the LEDs on to a specified color."""
    step = (new_brightness - pixels.brightness) / 10  # Calculate step for 10 iterations
    for _ in range(10):
        pixels.brightness += step
        pixels.fill(color)  # Ensure LEDs display the color during brightness adjustment
        time.sleep(0.05)  # Total of 0.5 seconds for transition

@app.route('/leds/brightness/<rgb>', methods=['GET'])
def adjust_brightness_by_rgb(rgb):
    """Endpoint to adjust brightness based on an RGB value."""
    rgb_tuple = tuple(map(int, rgb.split(',')))
    new_brightness = rgb_to_brightness(rgb_tuple)
    fade_to_brightness(new_brightness)
    return jsonify({"success": True, "message": f"Brightness adjusted to {new_brightness} based on RGB {rgb}"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
