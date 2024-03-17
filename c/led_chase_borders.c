#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h> // For sleep/usleep functions
#include "ws2811.h"

#define TARGET_FREQ     WS2811_TARGET_FREQ
#define GPIO_PIN        18
#define DMA             10
#define BRIGHTNESS      50
#define STRIP_TYPE      WS2811_STRIP_GRB // Adjust based on your LED strip
#define FADE_DELAY      5000 // Delay in microseconds for fade effect

// Define borders
int left_border[] = {63, 47, 31, 15};
int right_border[] = {71, 55, 39, 23, 7};
int top_border[] = {78, 77, 76, 75, 74, 73, 72};
int bottom_border[] = {0, 1, 2, 3, 4, 5, 6};
int border_sizes[] = {4, 5, 7, 7}; // Sizes of the borders

ws2811_t ledstrip = {
    .freq = TARGET_FREQ,
    .dmanum = DMA,
    .channel = {
        [0] = {
            .gpionum = GPIO_PIN,
            .count = 79,
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

void setLEDColor(int led, uint8_t red, uint8_t green, uint8_t blue) {
    ledstrip.channel[0].leds[led] = (red << 16) | (green << 8) | blue;
}

void fadeLED(int led, int fade_in) {
    for (int brightness = 0; brightness <= 255; brightness += 5) {
        uint8_t value = fade_in ? brightness : 255 - brightness;
        setLEDColor(led, value, value, value); // Adjust colors as needed
        ws2811_render(&ledstrip);
        usleep(FADE_DELAY);
    }
}

void chaseWithFade(int* border, int size) {
    for (int i = 0; i < size; i++) {
        fadeLED(border[i], 1); // Fade in
        fadeLED(border[i], 0); // Fade out
    }
}

int main() {
    if (ws2811_init(&ledstrip) != WS2811_SUCCESS) {
        fprintf(stderr, "ws2811_init failed: %s\n", ws2811_get_return_t_str(ws2811_init(&ledstrip)));
        return -1;
    }

    for (int cycle = 0; cycle < 3; cycle++) { // Run the animation three times
        chaseWithFade(left_border, border_sizes[0]);
        chaseWithFade(right_border, border_sizes[1]);
        chaseWithFade(top_border, border_sizes[2]);
        chaseWithFade(bottom_border, border_sizes[3]);
    }

    // Turn off all LEDs before exiting
    for(int i = 0; i < 79; i++) {
        setLEDColor(i, 0, 0, 0);
    }
    ws2811_render(&ledstrip);

    // Clean up
    ws2811_fini(&ledstrip);

    return 0;
}
