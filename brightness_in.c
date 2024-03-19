#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <math.h>
#include <ws2811.h>
#include <time.h>

// LED strip configuration
#define TARGET_FREQ WS2811_TARGET_FREQ
#define GPIO_PIN 18 // PWM0 output on GPIO18
#define DMA 10
#define STRIP_TYPE WS2811_STRIP_GRB // WS2812/SK6812RGB integrated chip+leds
#define NUM_LEDS 79
#define BRIGHTNESS 1 // Initial brightness (0-255)

// Serial communication configuration
#define SERIAL_PORT "/dev/ttyGS0"
#define BAUD_RATE B9600

// Utility functions
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

// LED control functions
float rgb_to_brightness(int r, int g, int b) {
    int max_value = fmax(r, fmax(g, b));
    float brightness = 0.01 + (max_value - 10) * (0.89 / (255 - 10));
    return fmax(0.01, fmin(0.9, brightness));
}

void fade_to_brightness(ws2811_t *ledstrip, float new_brightness) {
    float current_brightness = ledstrip->channel[0].brightness / 255.0f;
    float step = (new_brightness - current_brightness) / 10.0f;
    for (int i = 0; i < 10; i++) {
        current_brightness += step;
        if (current_brightness > 0.9f) current_brightness = 0.9f; // Ensuring max brightness of 0.9
        if (current_brightness < 0.01f) current_brightness = 0.01f; // Ensuring min brightness of 0.01
        ledstrip->channel[0].brightness = (int)(current_brightness * 255.0f);
        for (int led = 0; led < NUM_LEDS; led++) {
            ledstrip->channel[0].leds[led] = 0xFFFFFF; // Set all LEDs to white during transition
        }
        ws2811_render(ledstrip);
        usleep(100 * 1000); // 100ms delay for smooth transition
    }
}

void fade_to_brightness_and_color(ws2811_t *ledstrip, float new_brightness, int r, int g, int b) {
    float current_brightness = ledstrip->channel[0].brightness / 255.0f;
    float step = (new_brightness - current_brightness) / 10.0f;
    uint32_t color = (r << 16) | (g << 8) | b; // Combine RGB values into a single color

    for (int i = 0; i < 10; i++) {
        current_brightness += step;
        if (current_brightness > 0.9f) current_brightness = 0.9f; // Ensuring max brightness of 0.9
        if (current_brightness < 0.01f) current_brightness = 0.01f; // Ensuring min brightness of 0.01
        ledstrip->channel[0].brightness = (int)(current_brightness * 255.0f);

        // Set all LEDs to specified color during transition
        for (int led = 0; led < NUM_LEDS; led++) {
            ledstrip->channel[0].leds[led] = color;
        }
        ws2811_render(ledstrip);
        usleep(100 * 1000); // 100ms delay for smooth transition
    }
}

void off(ws2811_t *ledstrip) {
    ledstrip->channel[0].brightness = 0; // Set brightness to 0
    for (int led = 0; led < NUM_LEDS; led++) {
        ledstrip->channel[0].leds[led] = 0; // Turn off all LEDs
    }
    ws2811_render(ledstrip);
}

void fireplace_effect(ws2811_t *ledstrip, int duration) {
    srand(time(NULL));
    int target_red[NUM_LEDS], target_green[NUM_LEDS];
    for (int i = 0; i < NUM_LEDS; i++) {
        target_red[i] = rand_range(100, 255); // Simulate fire with reds and some randomness
        target_green[i] = rand_range(0, 60); // Low green values for fire effect
    }

    time_t start_time = time(NULL);
    while (time(NULL) - start_time < duration) {
        for (int i = 0; i < NUM_LEDS; i++) {
            uint32_t current_color = ledstrip->channel[0].leds[i];
            int red = (current_color >> 16) & 0xFF;
            int green = (current_color >> 8) & 0xFF;
            int blue = 0; // No blue in fire

            red = adjust_color(red, target_red[i]);
            green = adjust_color(green, target_green[i]);

            ledstrip->channel[0].leds[i] = (red << 16) | (green << 8) | blue;

            if (rand() % 10 == 0) { // Randomly adjust fire colors for dynamic effect
                target_red[i] = rand_range(100, 255);
                target_green[i] = rand_range(0, 60);
            }
        }
        ws2811_render(ledstrip);
        usleep(50 * 1000); // 50ms for a lively fire effect
    }
    printf("fire burn end \n");
    off(ledstrip); // Turn off LEDs after the fireplace effect
}

int main() {
    // Initialize the LED strip
    ws2811_t ledstrip = {
        .freq = TARGET_FREQ,
        .dmanum = DMA,
        .channel = {
            [0] = {
                .gpionum = GPIO_PIN,
                .count = NUM_LEDS,
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
        fprintf(stderr, "Failed to initialize LED strip\n");
        return -1;
    }

    // Setup serial communication
    int serial_port = open(SERIAL_PORT, O_RDWR);
    if (serial_port < 0) {
        fprintf(stderr, "Error opening serial port\n");
        return -1;
    }

    struct termios tty;
    memset(&tty, 0, sizeof tty);
    if (tcgetattr(serial_port, &tty) != 0) {
        fprintf(stderr, "Error from tcgetattr\n");
        return -1;
    }

    cfsetospeed(&tty, BAUD_RATE);
    cfsetispeed(&tty, BAUD_RATE);

    tty.c_cflag |= (CLOCAL | CREAD); // Ignore modem controls
    tty.c_cflag &= ~CSIZE;
    tty.c_cflag |= CS8;      // 8-bit characters
    tty.c_cflag &= ~PARENB;  // No parity bit
    tty.c_cflag &= ~CSTOPB;  // Only need 1 stop bit
    tty.c_cflag &= ~CRTSCTS; // No hardware flowcontrol

    // Setup for non-canonical mode
    tty.c_iflag &= ~(IGNBRK | BRKINT | PARMRK | ISTRIP | INLCR | IGNCR | ICRNL | IXON);
    tty.c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN);
    tty.c_oflag &= ~OPOST;

    // Fetch bytes as they become available
    tty.c_cc[VMIN] = 1;
    tty.c_cc[VTIME] = 1;

    if (tcsetattr(serial_port, TCSANOW, &tty) != 0) {
        fprintf(stderr, "Error from tcsetattr\n");
        return -1;
    }

    char read_buf[32];
    memset(&read_buf, '\0', sizeof(read_buf));

    while (1) {
        int num_bytes = read(serial_port, &read_buf, sizeof(read_buf));

        if (num_bytes > 0) {
            if (strncmp(read_buf, "brightness:", 11) == 0) {
                int r, g, b;
                sscanf(read_buf + 11, "%d,%d,%d", &r, &g, &b);
                float new_brightness = rgb_to_brightness(r, g, b);
                fade_to_brightness_and_color(&ledstrip, new_brightness, r, g, b); // Updated function call
            } else if (strncmp(read_buf, "off", 3) == 0) {
                off(&ledstrip);
            } else if (strncmp(read_buf, "fire", 4) == 0) {
                fireplace_effect(&ledstrip, 300); // Run fireplace effect for 300 seconds
            }
        }
        memset(&read_buf, '\0', sizeof(read_buf));
    }

    ws2811_fini(&ledstrip);
    close(serial_port);

    return 0;
}
