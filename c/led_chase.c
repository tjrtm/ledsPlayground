#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h> // For sleep/usleep functions
#include "ws2811.h"

#define TARGET_FREQ     WS2811_TARGET_FREQ
#define GPIO_PIN        18
#define DMA             10
#define LED_COUNT       79
#define BRIGHTNESS      255
#define STRIP_TYPE      WS2811_STRIP_GRB // Change if your strip uses a different color order
#define CHASE_DELAY     50000 // Delay in microseconds between updates

int main() {
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

    if (ws2811_init(&ledstrip) != WS2811_SUCCESS) {
        fprintf(stderr, "ws2811_init failed: %s\n", ws2811_get_return_t_str(ws2811_init(&ledstrip)));
        return -1;
    }

    for (int cycle = 0; cycle < 2; cycle++) { // Run the animation twice
        for (int i = 0; i < LED_COUNT; i++) {
            // Turn all LEDs off
            for(int j = 0; j < LED_COUNT; j++) {
                ledstrip.channel[0].leds[j] = 0;
            }

            // Turn on the current LED
            ledstrip.channel[0].leds[i] = 0x00FF00; // Green, change color as needed

            if (ws2811_render(&ledstrip)) {
                fprintf(stderr, "ws2811_render failed: %s\n", ws2811_get_return_t_str(ws2811_render(&ledstrip)));
                ws2811_fini(&ledstrip);
                return -1;
            }

            usleep(CHASE_DELAY); // Wait for a bit before moving to the next LED
        }
    }

    // Turn off all LEDs before exiting
    for(int i = 0; i < LED_COUNT; i++) {
        ledstrip.channel[0].leds[i] = 0;
    }
    ws2811_render(&ledstrip);

    // Clean up
    ws2811_fini(&ledstrip);

    return 0;
}
