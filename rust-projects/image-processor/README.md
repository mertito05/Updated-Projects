# Image Processor

A simple command-line image processing tool written in Rust for basic image operations and metadata.

## Features

- List image files in a directory
- Get file information and metadata
- Create simple PPM format images with gradients
- Support for common image formats (jpg, png, gif, bmp, tiff, webp, ppm)

## Usage

1. Compile the project:
   ```bash
   cargo build
   ```

2. Run the executable:
   ```bash
   cargo run
   ```

3. Follow the interactive menu:
   - Choose option 1 to list image files in a directory
   - Choose option 2 to get file information
   - Choose option 3 to create a simple PPM image
   - Choose option 4 to exit

## Examples

### List Image Files
```bash
Enter directory path: ./images
Image files found:
- photo1.jpg
- photo2.png
- image.gif
Total: 3 image files
```

### Get File Information
```bash
Enter file path: image.jpg
File Information:
Path: image.jpg
Size: 102400 bytes
Is file: true
Is directory: false
Last modified: 2023-12-07T10:30:45.123456789Z
Created: 2023-12-07T10:30:45.123456789Z
Extension: jpg
```

### Create Simple Image
```bash
Enter output file name: gradient.ppm
Enter width: 200
Enter height: 200
PPM image created successfully: gradient.ppm
```

## PPM Format

The tool creates images in PPM (Portable Pixmap) format, which is a simple, text-based image format. The created images show a color gradient from red to blue horizontally, green to blue vertically, and a diagonal gradient for the blue channel.

## Supported Image Formats for Listing

- JPG/JPEG
- PNG
- GIF
- BMP
- TIFF
- WebP
- PPM

## Dependencies

- Standard Rust library only (no external dependencies)

## Building

```bash
cargo build --release
```

The executable will be available in `target/release/image-processor`

## Limitations

- This is a basic tool for educational purposes
- No actual image processing beyond PPM creation
- No support for reading or modifying existing image files beyond metadata
