# APK Modifier - Build Instructions

This document explains how to build the APK Modifier application that integrates Python Flask server into an Android APK.

## Overview

The APK Modifier is a hybrid Android application that:
- Runs a Flask web server in the background using Chaquopy (Python for Android)
- Provides a WebView-based UI that connects to the local Flask server
- Allows users to upload, modify, and sign APK files directly on Android devices
- Supports FUD (Fully Undetected) obfuscation and custom library signing

## Prerequisites

### For Android APK Build:

1. **Android Studio** (Latest version)
   - Download from: https://developer.android.com/studio

2. **JDK 11 or higher**
   ```bash
   java -version
   ```

3. **Android SDK** with:
   - Android SDK Platform 33
   - Android SDK Build-Tools 33.0.0+
   - Android SDK Platform-Tools

4. **Chaquopy Plugin** (Included in build.gradle)
   - Provides Python support in Android

### For Standalone Python Server:

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **pip** (Python package manager)

## Building the Android APK

### Method 1: Using Android Studio (Recommended)

1. **Open Project**
   ```bash
   cd android-app
   ```
   - Open Android Studio
   - Select "Open an Existing Project"
   - Navigate to the `android-app` directory

2. **Sync Gradle**
   - Android Studio will automatically sync Gradle
   - Wait for dependencies to download (including Chaquopy)

3. **Build APK**
   - Go to: `Build > Build Bundle(s) / APK(s) > Build APK(s)`
   - Or use terminal:
     ```bash
     ./gradlew assembleRelease
     ```

4. **Locate APK**
   - APK will be in: `android-app/app/build/outputs/apk/release/app-release.apk`

5. **Sign APK** (for distribution)
   ```bash
   # Generate keystore (first time only)
   keytool -genkey -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-alias
   
   # Sign APK
   apksigner sign --ks my-release-key.jks --out app-release-signed.apk app-release.apk
   ```

### Method 2: Using Command Line

1. **Navigate to project**
   ```bash
   cd android-app
   ```

2. **Make gradlew executable**
   ```bash
   chmod +x gradlew
   ```

3. **Build APK**
   ```bash
   ./gradlew assembleRelease
   ```

4. **Find APK**
   ```bash
   ls -la app/build/outputs/apk/release/
   ```

## Running Standalone Python Server

If you want to run the server independently (not in Android):

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Run Server**
   ```bash
   python app.py
   ```

4. **Access Interface**
   - Open browser: `http://localhost:5000`

## Installing on Android Device

### Method 1: Direct Install

1. **Enable Unknown Sources**
   - Settings > Security > Unknown Sources (Enable)
   - Or for Android 8+: Settings > Apps > Special Access > Install Unknown Apps

2. **Transfer APK**
   ```bash
   adb install app-release-signed.apk
   ```
   Or copy APK to device and install manually

### Method 2: Using ADB

```bash
# Connect device via USB with USB debugging enabled
adb devices

# Install APK
adb install -r app-release-signed.apk

# Launch app
adb shell am start -n com.apkmodifier/.MainActivity
```

## Project Structure

```
Android-rat/
├── android-app/                    # Android application
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── AndroidManifest.xml
│   │   │   ├── java/com/apkmodifier/
│   │   │   │   ├── MainActivity.java
│   │   │   │   ├── PythonServerService.java
│   │   │   │   ├── BackgroundProcessService.java
│   │   │   │   └── BootReceiver.java
│   │   │   ├── res/
│   │   │   └── assets/            # Python server files
│   │   │       ├── app.py
│   │   │       ├── templates/
│   │   │       ├── static/
│   │   │       └── utils/
│   │   └── build.gradle
│   ├── build.gradle
│   └── settings.gradle
├── app.py                         # Flask server (standalone)
├── templates/                     # HTML templates
├── static/                        # CSS/JS files
├── utils/                         # Python utilities
├── requirements.txt
├── README.md
└── BUILD_INSTRUCTIONS.md
```

## Configuration

### Android App Configuration

Edit `app.py` in `android-app/app/src/main/assets/`:

```python
# Server settings
HOST = '127.0.0.1'  # Localhost for Android
PORT = 5000

# Telegram settings (can be configured via UI)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
```

### Permissions

The app requires these permissions:
- `INTERNET` - For network operations
- `READ/WRITE_EXTERNAL_STORAGE` - For APK file access
- `FOREGROUND_SERVICE` - For background server
- `RECEIVE_BOOT_COMPLETED` - For auto-start on boot

## Features

### 1. APK Upload
- Drag & drop or click to upload
- Maximum 100MB file size
- APK validation

### 2. Injection Options
- **Fully Undetected (FUD)**: Advanced obfuscation
- **Standard**: Basic modification
- Custom library name (e.g., libxx.so)

### 3. Telegram Integration
- Real-time notifications
- Progress updates
- Completion alerts

### 4. Server Upload
- Upload modified APKs to remote servers
- Configurable upload endpoint

### 5. Background Processing
- Long-running tasks (up to 1 hour)
- Progress tracking
- Runs in background service

## Troubleshooting

### Build Errors

1. **Chaquopy not found**
   ```bash
   # Add to build.gradle repositories:
   maven { url "https://chaquo.com/maven" }
   ```

2. **Python packages fail to install**
   - Check internet connection
   - Verify pip package names in build.gradle
   - Check Chaquopy compatibility: https://chaquo.com/chaquopy/doc/current/versions.html

3. **APK signing fails**
   ```bash
   # Ensure keytool and apksigner are in PATH
   export PATH=$PATH:$ANDROID_HOME/build-tools/33.0.0
   ```

### Runtime Issues

1. **Server doesn't start**
   - Check Android logs: `adb logcat | grep Python`
   - Verify Python files in assets directory
   - Check port 5000 is not in use

2. **WebView shows blank**
   - Enable JavaScript in WebView
   - Check network permissions
   - Verify server is running: `http://127.0.0.1:5000`

3. **File upload fails**
   - Grant storage permissions
   - Check file size limit
   - Verify storage path is accessible

## Development

### Testing on Emulator

```bash
# Start emulator
emulator -avd Pixel_6_API_33

# Install APK
adb install app-debug.apk

# View logs
adb logcat | grep -E "APKModifier|Python"
```

### Debugging

1. **Enable USB Debugging** on device
2. **Connect to Chrome DevTools**
   - Chrome: `chrome://inspect`
   - Select WebView instance

## Security Notes

⚠️ **Important Security Considerations:**

1. The app modifies APK files - use only on apps you own or have permission to modify
2. FUD obfuscation is for educational purposes
3. Telegram tokens should be kept secure
4. Server upload endpoints should use HTTPS and authentication
5. This tool is for research and educational purposes only

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/legendhkek/Android-rat/issues
- Documentation: See README.md

## Credits

Built with:
- Flask (Web Framework)
- Chaquopy (Python for Android)
- Android SDK
- Material Design Components
