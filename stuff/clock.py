import datetime
import board
import neopixel
import threading
import time
import pytz  # For timezone support

# LED Configuration
LED_COUNT = 24
HOUR_COLOR = (30, 0, 0)  # Red
MINUTE_COLOR = (35, 15, 0)  # Orange
SECOND_COLOR = (0, 40, 0)  # Green
OFF_COLOR = (0, 0, 0)  # Off
BRIGHTNESS = 0.1

# Time Configuration
NON_WORKING_START = datetime.time(0, 55, tzinfo=pytz.timezone('Europe/Vilnius'))  # Example with timezone
NON_WORKING_END = datetime.time(7, 0, tzinfo=pytz.timezone('Europe/Vilnius'))
ENABLE_NON_WORKING_HOURS = False

# Initialize LEDs
leds = neopixel.NeoPixel(board.D18, LED_COUNT, brightness=BRIGHTNESS)


def calculate_led_positions(hour, minute, second):
    """Calculates the LED positions for the hour, minute, and second hands."""
    hour_led = (9 + hour * 2) % LED_COUNT
    minute_led = (9 + minute * LED_COUNT // 60) % LED_COUNT
    second_led = (9 + second * LED_COUNT // 60) % LED_COUNT
    return hour_led, minute_led, second_led


def update_clock():
    """Updates the LED clock display."""
    prev_second_leds = []

    while True:
        now = datetime.datetime.now(pytz.timezone('Europe/Vilnius'))

        # Non-working hours logic
        if ENABLE_NON_WORKING_HOURS and is_within_non_working_hours(now):
            leds.fill(OFF_COLOR)
            time.sleep(1)  # Check again in a second
            continue

        # Calculate LED positions
        hour_led, minute_led, second_led = calculate_led_positions(now.hour % 12, now.minute, now.second)

        # Reset only previous second LEDs
        for prev_led in prev_second_leds:
            if prev_led not in [hour_led, minute_led]:
                leds[prev_led] = OFF_COLOR

        leds[hour_led] = HOUR_COLOR
        if minute_led != hour_led:
            leds[minute_led] = MINUTE_COLOR
        leds[second_led] = SECOND_COLOR  # Simple second display for now

        prev_second_leds = [second_led]
        leds.show()
        time.sleep(1)


def is_within_non_working_hours(now):
    """Checks if the current time falls within non-working hours."""
    if NON_WORKING_START <= now.time() <= NON_WORKING_END:
        return True
    elif NON_WORKING_START > NON_WORKING_END:  # If non-working hours cross midnight
        return now.time() >= NON_WORKING_START or now.time() <= NON_WORKING_END
    else:
        return False


if __name__ == '__main__':
    update_clock_thread = threading.Thread(target=update_clock, daemon=True)
    update_clock_thread.start()

    # Keep the script running
    while True:
        time.sleep(1)
