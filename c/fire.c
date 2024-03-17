#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <time.h>
#include "ws2811.h"

#define TARGET_FREQ WS2811_TARGET_FREQ
#define GPIO_PIN 18
#define DMA 10
#define LED_COUNT 79
#define BRIGHTNESS 100
#define STRIP_TYPE WS2811_STRIP_GRB

ws2811_t ledstrip = {
    .freq = TARGET_FREQ,
    .dmanum = DMA,
    .channel = {
        [0] = {
            .gpionum = GPIO_PIN,
            .count = LED_COUNT,
            .invert = 0,
            .brightness = BRIGHTNESS,
            .strip_type = STRIP_TYPE,
        },
        [1] = {
            .gpionum = 0,
            .count = 0,
            .invert = 0,
            .brightness = 0,
        },
    },
};

int rand_range(int min, int max) {
    return rand() % (max - min + 1) + min;
}

int adjust_color(int current_color, int target_color) {
    if (current_color < target_color) {
        return current_color + 1;
    } else if (current_color > target_color) {
        return current_color - 1;
    } else {
        return current_color;
    }
}

void fireplace_effect() {
    srand(time(NULL));
    int target_red[LED_COUNT];
    int target_green[LED_COUNT];
    int green_led_position = LED_COUNT; // Initialize outside of visible range
    time_t last_update_time = time(NULL);

    for (int i = 0; i < LED_COUNT; i++) {
        target_red[i] = rand_range(0, 255);
        target_green[i] = rand_range(250, 255);
    }

    while (1) {
        time_t current_time = time(NULL);
        
        // Update the green LED's position every second
        if (current_time - last_update_time >= 1) {
            green_led_position = rand_range(80, 100); // Random bottom row, add range to use matrix
            last_update_time = current_time;
        }

        for (int i = 0; i < LED_COUNT; i++) {
            // Update the fireplace colors
            uint32_t current_color = ledstrip.channel[0].leds[i];
            int red = (current_color >> 16) & 0xFF;
            int green = (current_color >> 8) & 0xFF;
            int blue = 0;

            red = adjust_color(red, target_red[i]);
            green = adjust_color(green, target_green[i]);

            // Apply the fireplace colors
            ledstrip.channel[0].leds[i] = (red << 16) | (green << 8) | blue;

            // Randomly adjust target colors for dynamic effect
            if (rand() % 10 == 0) {
                target_red[i] = rand_range(100, 255);
                target_green[i] = rand_range(0, 60);
            }
        }

        // Move the green LED up
        if (green_led_position < LED_COUNT) {
            // Clear the path of the green LED
            for (int i = 0; i < LED_COUNT; i++) {
                if (i % 7 == green_led_position % 7) { // Clear only the column where the green LED moves
                    ledstrip.channel[0].leds[i] &= 0xFFFF00; // Remove blue color component
                }
            }
            // Set the current position to green
            ledstrip.channel[0].leds[green_led_position] = 0xFF0000; // RED
            green_led_position += 7; // Move up one row
            if (green_led_position < 0 || green_led_position >= LED_COUNT) {
                green_led_position = LED_COUNT; // Reset position
            }
        }

        // Render the LED strip
        if (ws2811_render(&ledstrip) != WS2811_SUCCESS) {
            break;
        }

        usleep(10000); // Adjust as needed for desired effect speed
    }
}

int main() {
    if (ws2811_init(&ledstrip) != WS2811_SUCCESS) {
        fprintf(stderr, "LED strip initialization failed\n");
        return -1;
    }

    fireplace_effect();

    ws2811_fini(&ledstrip);
    return 0;
}
