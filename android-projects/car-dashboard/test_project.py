#!/usr/bin/env python3
"""
Test script to verify the Car Dashboard Android project structure.
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and print status."""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists and print status."""
    if os.path.isdir(dir_path):
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ {description}: {dir_path} - NOT FOUND")
        return False

def main():
    print("🧪 Testing Car Dashboard Android Project Structure")
    print("=" * 60)
    
    # Base project directory
    base_dir = "android-projects/car-dashboard"
    
    # Check essential files
    essential_files = [
        ("build.gradle.kts", "Project Build File"),
        ("settings.gradle.kts", "Settings File"),
        ("AndroidManifest.xml", "Android Manifest"),
        ("README.md", "Documentation")
    ]
    
    for file_name, description in essential_files:
        file_path = os.path.join(base_dir, file_name)
        check_file_exists(file_path, description)
    
    print()
    
    # Check app directory structure
    app_dir = os.path.join(base_dir, "app")
    app_files = [
        ("build.gradle.kts", "App Build File"),
        ("proguard-rules.pro", "ProGuard Rules")
    ]
    
    for file_name, description in app_files:
        file_path = os.path.join(app_dir, file_name)
        check_file_exists(file_path, description)
    
    print()
    
    # Check main source directories
    main_dirs = [
        ("src/main/java/com/cardashboard", "Main Package"),
        ("src/main/java/com/cardashboard/ui/screens", "UI Screens"),
        ("src/main/java/com/cardashboard/service", "Services"),
        ("src/main/java/com/cardashboard/utils", "Utilities"),
        ("src/main/java/com/cardashboard/navigation", "Navigation"),
        ("src/main/java/com/cardashboard/ui/theme", "Theming")
    ]
    
    for dir_suffix, description in main_dirs:
        dir_path = os.path.join(app_dir, dir_suffix)
        check_directory_exists(dir_path, description)
    
    print()
    
    # Check key Kotlin files
    kotlin_files = [
        ("CarDashboardApp.kt", "Main Application Class"),
        ("MainActivity.kt", "Main Activity"),
        ("AppNavigation.kt", "Navigation Setup"),
        ("Theme.kt", "Theme Configuration"),
        ("Typography.kt", "Typography Settings")
    ]
    
    for file_name, description in kotlin_files:
        file_path = os.path.join(app_dir, "src/main/java/com/cardashboard", file_name)
        check_file_exists(file_path, description)
    
    print()
    
    # Check screen files
    screen_files = [
        ("DashboardScreen.kt", "Dashboard Screen"),
        ("NavigationScreen.kt", "Navigation Screen"),
        ("MediaScreen.kt", "Media Screen"),
        ("PhoneScreen.kt", "Phone Screen"),
        ("MessagingScreen.kt", "Messaging Screen"),
        ("WeatherScreen.kt", "Weather Screen"),
        ("ParktronicScreen.kt", "Parktronic Screen"),
        ("AutopilotScreen.kt", "Autopilot Screen"),
        ("SettingsScreen.kt", "Settings Screen")
    ]
    
    for file_name, description in screen_files:
        file_path = os.path.join(app_dir, "src/main/java/com/cardashboard/ui/screens", file_name)
        check_file_exists(file_path, description)
    
    print()
    
    # Check service files
    service_files = [
        ("LocationService.kt", "Location Service"),
        ("MediaService.kt", "Media Service"),
        ("BluetoothService.kt", "Bluetooth Service"),
        ("VoiceService.kt", "Voice Service"),
        ("ParktronicService.kt", "Parktronic Service"),
        ("AutopilotService.kt", "Autopilot Service")
    ]
    
    for file_name, description in service_files:
        file_path = os.path.join(app_dir, "src/main/java/com/cardashboard/service", file_name)
        check_file_exists(file_path, description)
    
    print()
    
    # Check utility files
    utility_files = [
        ("PermissionsUtils.kt", "Permissions Utility")
    ]
    
    for file_name, description in utility_files:
        file_path = os.path.join(app_dir, "src/main/java/com/cardashboard/utils", file_name)
        check_file_exists(file_path, description)
    
    print()
    print("=" * 60)
    print("✅ Project structure verification completed!")
    print("📋 Next steps:")
    print("  1. Open the project in Android Studio")
    print("  2. Build the project to check for compilation errors")
    print("  3. Run on an emulator or device")
    print("  4. Test each screen and service functionality")

if __name__ == "__main__":
    main()
