# Voice Assistant

A Python-based voice assistant that can perform various tasks through voice commands. This assistant uses speech recognition for input and text-to-speech for responses, providing an interactive voice-controlled experience.

## Features
- **Voice Recognition**: Listen to and process voice commands
- **Text-to-Speech**: Respond with spoken answers
- **Time and Date**: Get current time and date information
- **Web Search**: Open web browser with search queries
- **Application Control**: Open common applications
- **Jokes**: Tell random jokes for entertainment
- **Extensible**: Easy to add new commands and functionality

## Prerequisites
- Python 3.x
- Microphone (for voice input)
- Speakers (for voice output)

## Installation
```bash
pip install SpeechRecognition pyttsx3
```

## Additional Setup
### Windows
- No additional setup required for basic functionality

### macOS
```bash
# Install portaudio for microphone support
brew install portaudio
```

### Linux
```bash
# Install required libraries
sudo apt-get install python3-pyaudio
sudo apt-get install libasound2-dev
```

## How to Run
```bash
python main.py
```

## Voice Commands

### Basic Commands
- **"Hello" / "Hi" / "Hey"**: Greet the assistant
- **"What time is it?"**: Get current time
- **"What's the date?"**: Get current date
- **"Tell me a joke"**: Hear a random joke
- **"Exit" / "Quit" / "Goodbye"**: Stop the assistant

### Search Commands
- **"Search for python tutorials"**: Open web browser with search results
- **"Search weather in New York"**: Search for weather information

### Application Commands
- **"Open notepad"**: Launch Notepad application
- **"Open calculator"**: Launch Calculator
- **"Open paint"**: Launch Microsoft Paint
- **"Open browser"**: Launch web browser
- **"Open word"**: Launch Microsoft Word
- **"Open excel"**: Launch Microsoft Excel

## Supported Applications
The assistant can open these Windows applications:
- Notepad (`notepad.exe`)
- Calculator (`calc.exe`)
- Microsoft Paint (`mspaint.exe`)
- Web Browser (`chrome.exe` - assumes Chrome is installed)
- Microsoft Word (`winword.exe`)
- Microsoft Excel (`excel.exe`)

## Customization

### Adding New Commands
1. Add a new method to the `VoiceAssistant` class
2. Update the `responses` dictionary with the command keyword
3. Add command processing logic in `process_command` method

### Example: Adding Weather Command
```python
def get_weather(self, location):
    # Implement weather API integration
    pass

# Add to responses
self.responses['weather'] = self.get_weather

# Add to process_command
elif 'weather' in command:
    location = extract_location(command)  # Implement location extraction
    self.get_weather(location)
```

### Changing Voice Properties
```python
# Change voice gender (0 for male, 1 for female)
self.engine.setProperty('voice', voices[1].id)

# Change speech rate
self.engine.setProperty('rate', 200)  # Faster speech
self.engine.setProperty('rate', 100)  # Slower speech
```

## Technical Details

### Speech Recognition
- Uses Google Speech Recognition API
- Handles ambient noise adjustment
- Supports timeout and phrase time limits

### Text-to-Speech
- Uses pyttsx3 for offline text-to-speech
- Supports multiple voices (system-dependent)
- Configurable speech rate

### Error Handling
- Handles unrecognized speech
- Manages network connectivity issues
- Graceful timeout handling

## File Structure
```
voice-assistant/
├── main.py          # Main application
└── requirements.txt # Python dependencies
```

## Troubleshooting

### Common Issues
1. **Microphone not working**: Check microphone permissions and connections
2. **Speech not recognized**: Speak clearly in a quiet environment
3. **No sound output**: Check speaker connections and volume
4. **Network errors**: Ensure internet connection for speech recognition

### Permission Issues
- On macOS/Linux, you may need to grant microphone access
- On Windows, check privacy settings for microphone

### Performance Tips
- Use a quality microphone for better recognition
- Speak clearly and at a moderate pace
- Reduce background noise when giving commands

## Future Enhancements
- Integration with weather APIs
- News headline reading
- Email reading and composition
- Calendar integration
- Smart home device control
- Multiple language support
- Custom wake word detection
- Voice training for better recognition
- Offline speech recognition
- Natural language processing
- Machine learning for command prediction

## Security Considerations
- Voice data is processed by Google's servers (for speech recognition)
- No voice data is stored locally
- Consider privacy implications of voice recordings

## Legal Compliance
- Inform users about voice data processing
- Provide privacy policy if collecting data
- Comply with data protection regulations (GDPR, CCPA)

## Support
For issues and feature requests, please check the documentation or source code comments. The assistant is designed to be extensible and can be customized for specific use cases.
