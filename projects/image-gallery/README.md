# Image Gallery

A desktop application for viewing and managing a collection of images with a graphical user interface.

## Features
- **GUI Interface**: Built with Tkinter for easy navigation
- **Image Support**: Supports JPG, JPEG, PNG, GIF, and BMP formats
- **Navigation**: Previous/Next buttons to browse through images
- **Image Management**: Add, remove, and clear images from the gallery
- **Persistent Storage**: Saves gallery data between sessions
- **Image Resizing**: Automatically resizes images to fit the window

## Prerequisites
- Python 3.x
- Pillow library for image processing

## Installation
```bash
pip install Pillow
```

## How to Run
```bash
python main.py
```

## Usage
1. **Add Images**: Click "Add Images" to select image files from your computer
2. **Navigate**: Use the Previous/Next buttons to browse through images
3. **Remove Images**: Remove the currently displayed image
4. **Clear Gallery**: Remove all images from the gallery

## Data Storage
The gallery stores image file paths in `gallery_data.json`. The actual image files remain in their original locations.

## Supported Formats
- JPG/JPEG
- PNG
- GIF
- BMP

## Note
This application requires the Pillow library for image processing. Make sure to install it before running the application.
