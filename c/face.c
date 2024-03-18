#include <opencv2/opencv.hpp>
#include <stdio.h>

using namespace cv;

// Dummy function for LED brightness control - to be replaced with actual control logic
void set_leds_brightness(int brightness) {
    // Placeholder: Implement LED control logic here
    printf("LED brightness set to: %d\n", brightness);
}

int main() {
    VideoCapture cap(0); // Open the default camera
    if (!cap.isOpened()) {
        printf("Error: Could not open camera.\n");
        return -1;
    } else {
        printf("camera detected\n");
    }

    CascadeClassifier faceCascade;
    if (!faceCascade.load("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")) {
        printf("Error: Could not load face cascade.\n");
        return -1;
    } else {
        printf("cascade module loaded \n");
    }

    Mat frame, gray;
    std::vector<Rect> faces;
    double knownDistance = 30.48; // Known distance from camera to face in cm (1 foot)
    double knownWidth = 14.0;     // Known width of the face in cm
    double focalLength = 0.0;     // Focal length (initially unknown)

    while (true) {
        cap >> frame; // Capture a frame
        if (frame.empty()) break; // Check for failure

        cvtColor(frame, gray, COLOR_BGR2GRAY); // Convert to grayscale
        faceCascade.detectMultiScale(gray, faces, 1.1, 4, 0, Size(30, 30)); // Detect faces

        if (faces.size() == 0) {
            set_leds_brightness(0); // Turn off LEDs if no faces are detected
        }

        for (size_t i = 0; i < faces.size(); i++) {
            Rect face = faces[i];
            rectangle(frame, Point(face.x, face.y), Point(face.x+face.width, face.y+face.height), Scalar(255, 0, 0), 2);

            // Calculate focal length (once)
            if (focalLength == 0.0) {
                focalLength = (face.width * knownDistance) / knownWidth;
            }

            // Calculate distance to face
            double distance = (knownWidth * focalLength) / face.width;
            printf("Distance to face: %.2f cm\n", distance);

            // Dummy call for LED brightness control
            int brightness = static_cast<int>((1 - (distance / knownDistance)) * 255);
            set_leds_brightness(brightness);
        }

        if (waitKey(30) >= 0) break; // Exit loop if any key is pressed
    }

    cap.release(); // When everything done, release the video capture object
    return 0;
}
