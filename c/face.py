import cv2
import numpy as np
import board
import neopixel

# Configuration for NeoPixel
LED_PIN = board.D18
NUM_LEDS = 79  # Adjust based on your setup
BRIGHTNESS = 1.0
ORDER = neopixel.GRB

# Initialize NeoPixel
pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False, pixel_order=ORDER)

def calculate_brightness(distance, max_distance):
    """Calculate brightness based on distance, inversely proportional."""
    return max(0, min(1, 1 - (distance / max_distance)))

def set_leds_brightness(brightness):
    """Set the brightness of all LEDs."""
    color = (int(255 * brightness), int(255 * brightness), int(255 * brightness))  # White color, adjust brightness
    for i in range(NUM_LEDS):
        pixels[i] = color
    pixels.show()

# Load the cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')

# To capture video from the webcam
cap = cv2.VideoCapture(0)

# Known parameters (adjust these based on your setup)
known_distance = 30.48  # known distance from the camera in cm
known_width = 14.0     # known width of the face in cm
focal_length = 0.0     # will be calculated

try:
    while True:
        # Read the frame
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            # If no faces detected, turn off LEDs
            set_leds_brightness(0)
        else:
            for (x, y, w, h) in faces:
                # Calculate focal length (once)
                if focal_length == 0.0:
                    focal_length = (w * known_distance) / known_width

                # Calculate distance to face
                distance = (known_width * focal_length) / w
                print(f"Distance to face: {distance:.2f} cm")

                # Adjust LED brightness based on distance
                brightness = calculate_brightness(distance, known_distance)
                set_leds_brightness(brightness)

        # Stop if escape key is pressed (in terminal, consider a different stopping mechanism)
        if cv2.waitKey(30) == 27:
            break
finally:
    # Release the VideoCapture object and turn off LEDs
    cap.release()
    set_leds_brightness(0)  # Ensure LEDs are turned off when stopping
