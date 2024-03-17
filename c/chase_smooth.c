#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include "ws2811.h"

#define TARGET_FREQ WS2811_TARGET_FREQ
#define GPIO_PIN 18
#define DMA 10
#define LED_COUNT 79
#define BRIGHTNESS 255
#define STRIP_TYPE WS2811_STRIP_GRB
#define CHASE_DELAY 10000
#define TRAIL_LENGTH 1
#define FADE_AMOUNT 85

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

void fade_leds(ws2811_led_t *leds, int count) {
    for (int i = 0; i < count; i++) {
        uint8_t r = (leds[i] >> 16) & 0xFF;
        uint8_t g = (leds[i] >> 8) & 0xFF;
        uint8_t b = leds[i] & 0xFF;
        r = (r <= FADE_AMOUNT) ? 0 : r - FADE_AMOUNT;
        g = (g <= FADE_AMOUNT) ? 0 : g - FADE_AMOUNT;
        b = (b <= FADE_AMOUNT) ? 0 : b - FADE_AMOUNT;
        leds[i] = (r << 16) | (g << 8) | b;
    }
}

int main(int argc, char *argv[]) {
    ws2811_led_t color = 0xFF0000; // Default color: Red
    int animation_type = 0; // Default: run once

    if (argc > 1) {
        color = (ws2811_led_t)strtol(argv[1], NULL, 0);
    }

    if (argc > 2) {
        animation_type = atoi(argv[2]);
    }

    if (ws2811_init(&ledstrip) != WS2811_SUCCESS) {
        fprintf(stderr, "LED strip initialization failed\n");
        return -1;
    }

    do {
        for (int i = 0; i < LED_COUNT + TRAIL_LENGTH; i++) {
            fade_leds(ledstrip.channel[0].leds, LED_COUNT);
            for (int j = 0; j < TRAIL_LENGTH; j++) {
                int led_index = i - j;
                if (led_index >= 0 && led_index < LED_COUNT) {
                    ws2811_led_t trail_color = color; // Directly use provided color
                    // Calculate brightness reduction for the trail effect
                    int brightness_reduction = FADE_AMOUNT * j;
                    uint8_t red = ((trail_color >> 16) & 0xFF) > brightness_reduction ? ((trail_color >> 16) & 0xFF) - brightness_reduction : 0;
                    uint8_t green = ((trail_color >> 8) & 0xFF) > brightness_reduction ? ((trail_color >> 8) & 0xFF) - brightness_reduction : 0;
                    uint8_t blue = (trail_color & 0xFF) > brightness_reduction ? (trail_color & 0xFF) - brightness_reduction : 0;
                    
                    ledstrip.channel[0].leds[led_index] = (red << 16) | (green << 8) | blue;
                }
            }

            if (ws2811_render(&ledstrip) != WS2811_SUCCESS) {
                fprintf(stderr, "Error rendering\n");
                ws2811_fini(&ledstrip);
                return -1;
            }

            usleep(CHASE_DELAY);
        }
    } while(animation_type == 1);

    for (int i = 0; i < LED_COUNT; i++) {
        ledstrip.channel[0].leds[i] = 0;
    }
    ws2811_render(&ledstrip);
    ws2811_fini(&ledstrip);

    return 0;
}
