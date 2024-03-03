import RPi.GPIO as GPIO
import time
import board
import neopixel

# Configuration for PIR sensor
inputPin = 14  # GPIO pin for the PIR sensor
GPIO.setmode(GPIO.BCM)  # Use Broadcom SOC channel numbering
GPIO.setup(inputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Configuration for NeoPixel
NUM_PIXELS = 249  # The number of LEDs in your strip
PIN_NEO_PIXEL = board.D18  # The pin that the NeoPixel strip is connected to
pixels = neopixel.NeoPixel(PIN_NEO_PIXEL, NUM_PIXELS, auto_write=False)

leds_on_duration = 5  # Time in seconds after which LEDs turn off, configurable
motion_detected = False  # To track if motion is detected
SNAKE_LENGTH = 8
REVERSE = False

def snake_animation_once():
    direction = 1
    head = 0
    for _ in range(NUM_PIXELS + SNAKE_LENGTH):
        # Set the color of the snake
        for i in range(SNAKE_LENGTH):
            if head - i * direction >= 0 and head - i * direction < NUM_PIXELS:
                pixels[head - i * direction] = (255 // (i + 1), 0, 0)  # The color of the snake fades from the head to the tail
        pixels.show()  # Update the display
        tail = head - SNAKE_LENGTH * direction  # Clear the tail of the snake
        if tail >= 0 and tail < NUM_PIXELS:
            pixels[tail] = (0, 0, 0)
        head += direction  # Move the head of the snake
        if REVERSE and (head == NUM_PIXELS - 1 or head == 0):  # Reverse the direction if needed
            direction = -direction
        if not REVERSE and head == NUM_PIXELS:  # Wrap around to the start if not reversing
            head = 0
        time.sleep(0.001)
    pixels.fill((0, 0, 0))  # Turn off all pixels after completing the animation
    pixels.show()

def check_motion_detected():
    global motion_detected
    start_time = time.time()
    while time.time() - start_time < leds_on_duration:
        if GPIO.input(inputPin):
            motion_detected = True
            break
        time.sleep(0.1)
    if motion_detected:
        print("Motion detected during countdown. Turning off LED strip.")
        pixels.fill((0, 0, 0))  # Turn off all pixels immediately
        pixels.show()
    else:
        print("LED strip will turn off after the countdown.")

try:
    print("Waiting for motion...")
    while True:
        if GPIO.input(inputPin):  # Check if the input is HIGH (motion detected)
            print("Motion detected! Running snake animation.")
            snake_animation_once()
            motion_detected = False  # Reset motion detected flag
            check_motion_detected()  # Check if motion is detected during the countdown
            if not motion_detected:
                print("Turning off LED strip.")
                pixels.fill((0, 0, 0))  # Ensure LEDs are turned off after the duration if no motion detected again
                pixels.show()
            motion_detected = False  # Reset for the next cycle
        time.sleep(0.1)  # Short delay to debounce and slow down the loop
except KeyboardInterrupt:
    print("Program exited")
    pixels.fill((0, 0, 0))  # Ensure LEDs are turned off when exiting
    pixels.show()
    GPIO.cleanup()  # Clean up GPIO on CTRL+C exit
