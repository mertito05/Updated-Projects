# Drawing App

A Python-based drawing application built with Pygame that provides a variety of drawing tools and features. This app allows users to create digital artwork with different brushes, shapes, and colors.

## Features
- **Multiple Drawing Tools**: Freehand drawing, lines, rectangles, circles, ellipses
- **Color Palette**: 12 predefined colors with easy selection
- **Brush Size**: Adjustable brush thickness (1-50 pixels)
- **Fill Tool**: Flood fill for coloring enclosed areas
- **Eraser**: Remove drawn elements
- **Real-time Preview**: See shapes before finalizing
- **Clear Canvas**: Reset the drawing area
- **Save Functionality**: Export drawings as PNG images
- **Keyboard Shortcuts**: Quick access to common functions

## Prerequisites
- Python 极
- Pygame library

## Installation
```bash
pip install pygame
```

## How to Run
```bash
python main.py
```

## User Interface

### Toolbar
The top toolbar contains:
- **Color Buttons**: 12 color swatches for quick color selection
- **Tool Buttons**: Drawing tools (draw, line, rectangle, circle, ellipse, fill, eraser)
- **Size Indicator**: Current brush size display
- **Clear Button**: Reset the canvas

### Drawing Area
The main area below the toolbar is where you can create your artwork.

## Tools and Usage

### Freehand Drawing
- Select the "draw" tool
- Click and drag to draw freehand lines
- Brush size determines line thickness

### Shape Tools
- **Line**: Click and drag to create straight lines
- **Rectangle**: Click and drag to create rectangles
- **Circle**: Click to set center, drag to set radius
- **Ellipse**: Click and drag to create ellipses

### Fill Tool
- Select the "fill" tool
- Click on any enclosed area to fill it with the current color
- Works with areas bounded by lines of any color

### Eraser
- Select the "eraser" tool
- Click and drag to erase drawn elements
- Uses the background color (white by default)

## Color Palette
The app includes 12 predefined colors:
- Black, White, Red, Green, Blue
- Yellow, Purple, Orange, Cyan, Pink
- Brown, Gray

## Keyboard Shortcuts
- **Up Arrow**: Increase brush size
- **Down Arrow**: Decrease brush size
- **C**: Clear the canvas
- **S**: Save drawing as PNG file

## Technical Details

### Drawing Surface
- Uses Pygame's Surface for efficient drawing operations
- Maintains separate drawing surface for persistence
- Real-time rendering with 60 FPS

### Flood Fill Algorithm
- Implements a simple queue-based flood fill
- Handles edge cases and bounds checking
- Efficient for moderate-sized areas

### Shape Drawing
- Preview shapes during mouse movement
- Finalize shapes on mouse release
- Anti-aliased drawing for smooth lines

## File Structure
```
drawing-app/
├── main.py          # Main application
├── drawing.png      # Saved drawings (auto-generated)
└── requirements.txt # Python dependencies
```

## Customization

### Adding New Colors
Modify the `colors` list in the `__init__` method:
```python
self.colors = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    # Add more RGB tuples...
]
```

### Adding New Tools
1. Add tool name to `self.tools` list
2. Implement drawing method
3. Add tool handling in `draw()` and `finalize_shape()` methods

### Changing Canvas Size
Modify the `width` and `height` in the `__init__` method:
```python
self.width, self.height = 1024, 768  # Larger canvas
```

## Troubleshooting

### Common Issues
1. **Pygame not installed**: Run `pip install pygame`
2. **No display**: Ensure you have a graphical environment
3. **Performance issues**: Reduce canvas size for better performance
4. **Fill tool not working**: Ensure area is properly enclosed

### Pygame Installation
```bash
# Windows
pip install pygame

# macOS
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer
pip install pygame

# Linux (Ubuntu/Debian)
sudo apt-get install python3-pygame
```

## Future Enhancements
- Layer support
- Undo/Redo functionality
- Custom color picker
- Gradient fills
- Text tool
- Image import/export
- Brush patterns
- Zoom functionality
- Pressure sensitivity support
- Animation tools
- Export to various formats
- Plugin system
- Collaborative drawing
- 3D drawing tools
- Vector graphics support
- Template library
- Drawing tutorials
- Auto-save feature
- Version history
- Cloud storage integration

## Legal Considerations
- Ensure proper licensing for distributed artwork
- Include attribution for Pygame library
- Respect copyright when using imported images

## Support
For issues and feature requests, check the source code comments. The application is designed to be modular and extensible for custom drawing needs.
