# Music Player

A Python-based music player with a graphical user interface built using Pygame for audio playback and Tkinter for the interface. This player supports multiple audio formats and provides basic music playback controls.

## Features
- **Multiple Format Support**: Plays MP3, WAV, OGG, FLAC, and M4A files
- **Playlist Management**: Load and manage music folders as playlists
- **Basic Controls**: Play, pause, stop, next, and previous track navigation
- **Volume Control**: Adjustable volume slider
- **Graphical Interface**: User-friendly Tkinter-based GUI
- **Track Information**: Display current track name and position in playlist
- **Folder Loading**: Load all audio files from a directory automatically

## Prerequisites
- Python 3.x
- Pygame (for audio playback)
- Tkinter (usually included with Python)

## Installation
```bash
pip install pygame
```

## How to Run
```bash
python main.py
```

## Supported Audio Formats
- MP3 (.mp3)
- WAV (.wav)
- OGG (.ogg)
- FLAC (.flac)
- M4A (.m4a)

## User Interface

### Main Window Components
1. **Playlist Display**: Shows all loaded tracks with file names
2. **Control Buttons**:
   - Load Folder: Select directory containing music files
   - Play/Pause: Toggle playback
   - Stop: Stop current playback
   - Previous: Go to previous track
   - Next: Go to next track
3. **Volume Control**: Slider for adjusting volume (0-100%)
4. **Status Area**: Shows current playback status and track information

### Keyboard Shortcuts
- **Space**: Play/Pause
- **S**: Stop
- **N**: Next track
- **P**: Previous track
- **Up/Down Arrow**: Volume control
- **Left/Right Arrow**: Seek (if implemented)

## Usage

### Loading Music
1. Click the "Load Folder" button
2. Select a directory containing audio files
3. The player will automatically scan for supported audio formats
4. All found files will be added to the playlist

### Playback Controls
- **Play**: Starts playback from the selected track
- **Pause**: Temporarily stops playback
- **Stop**: Completely stops playback
- **Next/Previous**: Navigate through the playlist
- **Volume**: Adjust playback volume

### Track Selection
- Click on any track in the playlist to select and play it
- The currently playing track is highlighted in the playlist

## Technical Details

### Audio Backend
- Uses Pygame's mixer module for audio playback
- Supports multiple audio formats through SDL backend
- Volume control from 0.0 (silent) to 1.0 (maximum)

### File Handling
- Recursively scans selected directories for audio files
- Supports common audio file extensions
- Handles file path validation and error checking

### GUI Framework
- Built with Tkinter for cross-platform compatibility
- Responsive interface with real-time updates
- Clean and intuitive layout

## Customization

### Adding New Audio Formats
The player can be extended to support additional formats by modifying the `audio_extensions` set in the `load_playlist` method:

```python
audio_extensions = {'.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac', '.wma'}
```

### Modifying UI Layout
The GUI is built with Tkinter and can be customized by modifying the `setup_ui` method:
- Change window size and title
- Modify button labels and positions
- Add new UI elements
- Customize colors and fonts

### Enhanced Features
Potential enhancements include:
- Playlist saving and loading
- Equalizer controls
- Audio effects
- Lyrics display
- Album art display
- Keyboard shortcuts
- Mini-player mode
- System tray integration

## File Structure
```
music-player/
├── main.py          # Main application
└── requirements.txt # Python dependencies
```

## Troubleshooting

### Common Issues
1. **No sound**: Check volume levels and audio device connections
2. **File not playing**: Ensure file format is supported and not corrupted
3. **Pygame installation issues**: Reinstall pygame or check dependencies
4. **Tkinter not available**: Install tkinter package if missing

### Pygame Installation
If you encounter issues with Pygame installation:
```bash
# On Windows
pip install pygame

# On macOS
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer
pip install pygame

# On Linux (Debian/Ubuntu)
sudo apt-get install python3-pygame
```

### Audio Format Support
Some formats may require additional codecs:
- MP3: Requires MP3 codec support in Pygame
- FLAC: May require additional libraries on some systems
- M4A: AAC support varies by system

## Performance Considerations
- Large playlists may take time to load
- Memory usage increases with many loaded tracks
- Real-time UI updates every second for status

## Future Enhancements
- Audio visualization
- Equalizer and audio effects
- Internet radio streaming
- Podcast support
- Smart playlists
- Audio bookmarks
- Sleep timer
- Crossfade between tracks
- Replay gain
- CD ripping
- Audio conversion
- Mobile app version
- Web interface
- Voice control integration
- Lyrics synchronization
- Album art fetching
- Last.fm scrobbling
- Podcast directory
- Audio normalization
- Batch processing
- Audio editing tools

## Legal Considerations
- Ensure you have rights to play the audio files
- Respect copyright laws for distributed music
- Include proper attribution for used libraries

## Support
For issues and feature requests, please check the documentation or source code comments. The player is designed to be modular and can be extended with additional functionality as needed.
