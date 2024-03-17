#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include "ws2811.h"

#define TARGET_FREQ WS2811_TARGET_FREQ
#define GPIO_PIN 18
#define DMA 10
#define LED_COUNT 79
#define BRIGHTNESS 10
#define STRIP_TYPE WS2811_STRIP_GRB
#define ANIMATION_DELAY 50000 // Adjust for animation speed
#define SPIRAL_LENGTH 4 // Adjust for the length of the spiral
#define FADE_AMOUNT 40 // Adjust for fade effect

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

void fade_leds(ws2811_led_t *leds, int count, int fade_amount) {
    for (int i = 0; i < count; i++) {
        uint8_t r = (leds[i] >> 16) & 0xFF;
        uint8_t g = (leds[i] >> 8) & 0xFF;
        uint8_t b = leds[i] & 0xFF;
        r = (r <= fade_amount) ? 0 : r - fade_amount;
        g = (g <= fade_amount) ? 0 : g - fade_amount;
        b = (b <= fade_amount) ? 0 : b - fade_amount;
        leds[i] = (r << 16) | (g << 8) | b;
    }
}

int main() {
    if (ws2811_init(&ledstrip) != WS2811_SUCCESS) {
        fprintf(stderr, "LED strip initialization failed\n");
        return -1;
    }

    while (1) { // Infinite loop for continuous animation
        for (int position = 0; position < LED_COUNT; position++) {
            fade_leds(ledstrip.channel[0].leds, LED_COUNT, FADE_AMOUNT);
            
            for (int i = 0; i < SPIRAL_LENGTH; i++) {
                int led_index = (position + i) % LED_COUNT;
                int brightness_factor = (SPIRAL_LENGTH - i) * (255 / SPIRAL_LENGTH); // Gradually reduce brightness
                ws2811_led_t color = (brightness_factor << 8); // Red color with fading effect
                ledstrip.channel[0].leds[led_index] = color;
            }

            if (ws2811_render(&ledstrip) != WS2811_SUCCESS) {
                fprintf(stderr, "Error rendering\n");
                break; // Exit on render error
            }

            usleep(ANIMATION_DELAY);
        }
    }

    ws2811_fini(&ledstrip);
    return 0;
}
