#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ws2811.h>

// Define your constants for LED control
#define TARGET_FREQ WS2811_TARGET_FREQ
#define GPIO_PIN 18
#define DMA 10
#define STRIP_TYPE WS2811_STRIP_RGB
#define LED_COUNT 79
#define MAX_BRIGHTNESS 100  // Adjust this value for safety and visual effect
#define FADE_STEPS 10
#define DELAY 10  // Delay between fade steps in milliseconds

// Define your LED matrix layout
int led_matrix[10][7] = {
    {78, 77, 76, 75, 74, 73, 72},
    {64, 65, 66, 67, 68, 69, 70},
    {62, 61, 60, 59, 58, 57, 56},
    {48, 49, 50, 51, 52, 53, 54},
    {46, 45, 44, 43, 42, 41, 40},
    {32, 33, 34, 35, 36, 37, 38},
    {30, 29, 28, 27, 26, 25, 24},
    {16, 17, 18, 19, 20, 21, 22},
    {14, 13, 12, 11, 10, 9, 8},
    {0, 1, 2, 3, 4, 5, 6}
};

ws2811_t ledstring = {
    .freq = TARGET_FREQ,
    .dmanum = DMA,
    .channel = {
        [0] = {
            .gpionum = GPIO_PIN,
            .count = LED_COUNT,
            .invert = 0,
            .brightness = MAX_BRIGHTNESS,
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

void setLedBrightness(int ledIndex, uint32_t color) {
    if (ledIndex >= 0 && ledIndex < LED_COUNT) {
        ledstring.channel[0].leds[ledIndex] = color;
    }
}

void clearAllLeds() {
    for (int i = 0; i < LED_COUNT; i++) {
        setLedBrightness(i, 0);
    }
    ws2811_render(&ledstring);
}

void fadeBetweenColumns(int fromCol, int toCol, int steps) {
    for (int step = 0; step <= steps; step++) {
        int brightness = (MAX_BRIGHTNESS * step) / steps;
        int fadeOutBrightness = MAX_BRIGHTNESS - brightness;

        // Fade in the toCol
        for (int row = 0; row < 10; row++) {
            int ledIndex = led_matrix[row][toCol];
            setLedBrightness(ledIndex, (brightness << 16) | (brightness << 8) | brightness);  // Adjust color as needed
        }

        // Fade out the fromCol
        if (fromCol >= 0) {
            for (int row = 0; row < 10; row++) {
                int ledIndex = led_matrix[row][fromCol];
                setLedBrightness(ledIndex, (fadeOutBrightness << 16) | (fadeOutBrightness << 8) | fadeOutBrightness);  // Adjust color as needed
            }
        }

        ws2811_render(&ledstring);
        usleep(DELAY * 100);  // Adjust timing as needed
    }
}

void animateVerticalLine() {
    int currentCol = 0;
    int previousCol = -1;
    int direction = 1;

    while (1) {
        int nextCol = currentCol + direction;

        if (nextCol >= 7 || nextCol < 0) {
            direction *= -1;  // Reverse the direction
            nextCol = currentCol + direction;
        }

        fadeBetweenColumns(previousCol, currentCol, FADE_STEPS);

        previousCol = currentCol;
        currentCol = nextCol;

        usleep(DELAY * 100 * 10);  // Pause before starting the next transition
    }
}

void animateHorizontalLine() {
    int row = 0; // Start at the first row
    int direction = 1; // Direction to move the line

    while (1) {
        clearAllLeds(); // Clear the matrix before drawing the new line

        // Light up the current row
        for (int col = 0; col < 7; col++) {
            int ledIndex = led_matrix[row][col];
            setLedBrightness(ledIndex, 0x00200000); // Set to a moderate brightness, adjust the color as needed
        }
        ws2811_render(&ledstring);
        usleep(DELAY * 100 * 20); // Delay to keep the line visible before moving

        row += direction;
        if (row >= 10 || row < 0) {
            direction *= -1; // Change direction
            row += direction; // Adjust to stay within bounds
        }
    }
}

void animateLines() {
    int currentCol = 0;
    int directionCol = 1;

    int currentRow = 0;
    int directionRow = 1;

    while (1) {
        clearAllLeds(); // Clear the matrix before drawing the new line

        // Light up the current column
        for (int row = 0; row < 10; row++) {
            int ledIndex = led_matrix[row][currentCol];
            setLedBrightness(ledIndex, 0x00200000); // Set to a moderate brightness, adjust the color as needed
        }

        // Light up the current row
        for (int col = 0; col < 7; col++) {
            int ledIndex = led_matrix[currentRow][col];
            setLedBrightness(ledIndex, 0x00200000); // Set to a moderate brightness, adjust the color as needed
        }

        ws2811_render(&ledstring);
        usleep(DELAY * 100 * 20); // Delay to keep the line visible before moving

        currentCol += directionCol;
        if (currentCol >= 7 || currentCol < 0) {
            directionCol *= -1; // Change direction
            currentCol += directionCol; // Adjust to stay within bounds
        }

        currentRow += directionRow;
        if (currentRow >= 10 || currentRow < 0) {
            directionRow *= -1; // Change direction
            currentRow += directionRow; // Adjust to stay within bounds
        }
    }
}

int main() {
    ws2811_return_t ret;

    if ((ret = ws2811_init(&ledstring)) != WS2811_SUCCESS) {
        fprintf(stderr, "ws2811_init failed: %s\n", ws2811_get_return_t_str(ret));
        return ret;
    }

    //animateVerticalLine();
    animateHorizontalLine();
    //animateLines();

    ws2811_fini(&ledstring);
    return 0;
}
