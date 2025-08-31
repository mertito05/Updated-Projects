# Car Dashboard Android App

A comprehensive car dashboard application built with Jetpack Compose for Android Automotive or in-car infotainment systems.

## Features

### 🚗 Dashboard Screen
- Real-time vehicle information display
- Speed, RPM, fuel level, and temperature monitoring
- Quick access to navigation, media, and phone functions
- Voice command activation button

### 🗺️ Navigation Screen
- Interactive maps with real-time location tracking
- Turn-by-turn navigation with voice guidance
- Destination search and route planning
- Traffic information and alternative routes

### 🎵 Media Screen
- Music playback with play/pause/skip controls
- Playlist management and audio source selection
- Volume control and equalizer settings
- Bluetooth audio streaming support

### 📞 Phone Screen
- Contact list with favorites
- Call history and recent calls
- Dial pad for manual number entry
- Bluetooth hands-free calling

### 💬 Messaging Screen
- SMS message viewing and composition
- Voice-to-text message dictation
- Contact integration for quick messaging
- Message read-aloud functionality

### 🌤️ Weather Screen
- Current weather conditions display
- 5-day weather forecast
- Location-based weather updates
- Weather alerts and warnings

### ⚙️ Settings Screen
- App appearance and theme settings
- Notification preferences
- Audio and volume controls
- Bluetooth device management
- Privacy and security settings

## Technical Architecture

### Services
- **LocationService**: Handles GPS and location tracking
- **MediaService**: Manages audio playback and media controls
- **BluetoothService**: Handles Bluetooth connectivity and device management
- **VoiceService**: Provides voice recognition and command processing

### Utilities
- **PermissionsUtils**: Centralized permission management
- **Navigation**: Jetpack Navigation for screen transitions
- **Material Design 3**: Modern UI components and theming

## Prerequisites

- Android Studio Flamingo or later
- Android SDK 34 (Android 14)
- Kotlin 1.8.0 or later
- Java 17 or later

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd android-projects/car-dashboard
```

2. Open the project in Android Studio

3. Build and run the app on an Android device or emulator

## Permissions

The app requires the following permissions:

- **Location**: `ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION`
- **Bluetooth**: `BLUETOOTH_CONNECT`, `BLUETOOTH_SCAN`
- **Audio**: `RECORD_AUDIO`
- **Phone**: `CALL_PHONE`, `READ_PHONE_STATE`
- **Contacts**: `READ_CONTACTS`
- **SMS**: `SEND_SMS`, `READ_SMS`

## Building for Automotive

To build for Android Automotive:

1. Ensure you have the Automotive OS SDK installed
2. Update the `build.gradle.kts` with automotive-specific dependencies
3. Test on an automotive emulator or compatible hardware

## Key Components

### Screens
- `DashboardScreen.kt` - Main dashboard with vehicle info
- `NavigationScreen.kt` - Maps and navigation
- `MediaScreen.kt` - Music and audio controls
- `PhoneScreen.kt` - Calling functionality
- `MessagingScreen.kt` - SMS messaging
- `WeatherScreen.kt` - Weather information
- `SettingsScreen.kt` - App configuration

### Services
- `LocationService.kt` - GPS and location management
- `MediaService.kt` - Audio playback and media
- `BluetoothService.kt` - Bluetooth device management
- `VoiceService.kt` - Voice recognition

### Utilities
- `PermissionsUtils.kt` - Permission handling
- `AppNavigation.kt` - Navigation setup
- `Theme.kt` - Material Design theming

## Dependencies

The project uses the following major dependencies:

- **Jetpack Compose**: Modern UI toolkit
- **Navigation**: Screen navigation
- **Location Services**: Google Play Services for location
- **Maps**: Google Maps integration
- **Media**: Android media playback
- **Bluetooth**: Android Bluetooth APIs
- **Speech Recognition**: Android speech APIs

## Development Guidelines

### Code Style
- Follow Kotlin coding conventions
- Use meaningful variable and function names
- Add comments for complex logic
- Use proper error handling

### Architecture
- Follow MVVM pattern with state management
- Use dependency injection for services
- Implement proper lifecycle management
- Handle permissions appropriately

### Testing
- Write unit tests for business logic
- Implement UI tests for screens
- Test on different screen sizes
- Verify automotive compatibility

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the code examples

## Roadmap

- [ ] Integration with vehicle CAN bus
- [ ] Advanced voice command processing
- [ ] Custom widget system
- [ ] Multi-language support
- [ ] Cloud synchronization
- [ ] Advanced analytics
- [ ] Plugin system for third-party integrations

## Acknowledgments

- Android Jetpack team for excellent libraries
- Material Design team for UI components
- Open source community for inspiration and tools
