#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

void printUsage() {
    cout << "Usage: image_processor input.jpg output.jpg [operation]" << endl;
    cout << "Available operations:" << endl;
    cout << "  grayscale - Convert to grayscale" << endl;
    cout << "  resize    - Resize image (50% smaller)" << endl;
    cout << "  blur      - Apply Gaussian blur" << endl;
    cout << "  sharpen   - Apply sharpening filter" << endl;
    cout << "  edges     - Detect edges using Canny" << endl;
    cout << "  equalize  - Histogram equalization" << endl;
}

Mat applyGrayscale(const Mat& input) {
    Mat output;
    cvtColor(input, output, COLOR_BGR2GRAY);
    return output;
}

Mat applyResize(const Mat& input) {
    Mat output;
    resize(input, output, Size(), 0.5, 0.5, INTER_LINEAR);
    return output;
}

Mat applyBlur(const Mat& input) {
    Mat output;
    GaussianBlur(input, output, Size(5, 5), 0);
    return output;
}

Mat applySharpen(const Mat& input) {
    Mat output;
    Mat kernel = (Mat_<float>(3, 3) << 
        0, -1, 0,
        -1, 5, -1,
        0, -1, 0);
    filter2D(input, output, -1, kernel);
    return output;
}

Mat applyEdges(const Mat& input) {
    Mat gray, blurred, edges;
    cvtColor(input, gray, COLOR_BGR2GRAY);
    GaussianBlur(gray, blurred, Size(5, 5), 0);
    Canny(blurred, edges, 50, 150);
    return edges;
}

Mat applyEqualize(const Mat& input) {
    Mat gray, output;
    cvtColor(input, gray, COLOR_BGR2GRAY);
    equalizeHist(gray, output);
    return output;
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        printUsage();
        return 1;
    }

    string inputFile = argv[1];
    string outputFile = argv[2];
    string operation = argv[3];

    // Load input image
    Mat image = imread(inputFile);
    if (image.empty()) {
        cerr << "Error: Could not load image " << inputFile << endl;
        return 1;
    }

    Mat result;

    // Apply selected operation
    if (operation == "grayscale") {
        result = applyGrayscale(image);
    } else if (operation == "resize") {
        result = applyResize(image);
    } else if (operation == "blur") {
        result = applyBlur(image);
    } else if (operation == "sharpen") {
        result = applySharpen(image);
    } else if (operation == "edges") {
        result = applyEdges(image);
    } else if (operation == "equalize") {
        result = applyEqualize(image);
    } else {
        cerr << "Error: Unknown operation '" << operation << "'" << endl;
        printUsage();
        return 1;
    }

    // Save output image
    if (!imwrite(outputFile, result)) {
        cerr << "Error: Could not save image " << outputFile << endl;
        return 1;
    }

    cout << "Successfully processed image. Output saved to " << outputFile << endl;
    return 0;
}
