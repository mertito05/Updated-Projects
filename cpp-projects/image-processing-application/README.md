# Image Processing Application

A C++ application for basic image processing operations using OpenCV library.

## Features

- Image loading and saving
- Basic image transformations (grayscale, resize, rotate)
- Image filtering (blur, sharpen, edge detection)
- Color space conversions
- Histogram equalization

## Requirements

- C++11 or later
- OpenCV library (version 4.x recommended)

## Installation

1. Install OpenCV:
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install libopencv-dev
   
   # On Windows, download from OpenCV website and set up environment variables
   ```

2. Compile the application:
   ```bash
   g++ main.cpp -o image_processor `pkg-config --cflags --libs opencv4`
   ```

## Usage

```bash
./image_processor input.jpg output.jpg [operation]
```

Available operations:
- grayscale: Convert to grayscale
- resize: Resize image
- blur: Apply Gaussian blur
- sharpen: Apply sharpening filter
- edges: Detect edges using Canny
- equalize: Histogram equalization

## Examples

```bash
# Convert to grayscale
./image_processor input.jpg output_grayscale.jpg grayscale

# Apply blur
./image_processor input.jpg output_blur.jpg blur

# Detect edges
./image_processor input.jpg output_edges.jpg edges
```

## Future Enhancements

- Batch processing
- GUI interface
- More advanced filters
- Image segmentation
- Machine learning integration
- Real-time video processing
