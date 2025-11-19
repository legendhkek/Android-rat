# Android RAT - Lite Version

## Overview

This is a **simplified/lite version** of the Android RAT that only collects:
- Phone number
- SMS messages

## Differences from Full Version

The full version (in `android-app/`) collects comprehensive data including:
- Device information
- GPS location
- Contacts
- SMS messages
- Call logs
- Installed apps
- Battery status
- Network information
- Screenshots
- And more...

This lite version **only** collects:
- ✅ Phone number (from TelephonyManager)
- ✅ SMS messages (last 50 messages)

## Use Case

This simplified version is designed for:
- Minimal data collection scenarios
- Testing SMS and phone number access
- Lighter footprint applications
- Educational purposes for understanding basic Android permissions

## Permissions Required

### Minimal Permissions:
- `READ_PHONE_STATE` - To read phone number
- `READ_SMS` - To read SMS messages

### Optional:
- `INTERNET` - To send data to server

## Building

Same as the full version:

```bash
cd android-app-lite
./gradlew assembleRelease
```

## Installation

```bash
adb install app/build/outputs/apk/release/app-release.apk
```

## Technical Details

### Modified Files:
- **DataCollectionService.java** - Simplified to only collect phone number and SMS

### Removed Functionality:
- Location tracking
- Contact list collection
- Call log collection
- Installed apps enumeration
- Battery monitoring
- Network info collection
- Screenshot capture
- Camera access
- Audio recording
- File management

## Security Notice

This is for **authorized testing and educational purposes only**. Ensure you have proper permissions before using this application.

## Comparison

| Feature | Full Version | Lite Version |
|---------|-------------|--------------|
| Phone Number | ✅ | ✅ |
| SMS Messages | ✅ | ✅ |
| Location | ✅ | ❌ |
| Contacts | ✅ | ❌ |
| Call Logs | ✅ | ❌ |
| Apps List | ✅ | ❌ |
| Battery Info | ✅ | ❌ |
| Network Info | ✅ | ❌ |
| Screenshots | ✅ | ❌ |
| File Manager | ✅ | ❌ |
| Size | ~391 MB | ~20 MB (estimated) |

## Notes

- This lite version uses the same base structure as the full version
- The main difference is in `DataCollectionService.java` which has been stripped down
- All other services remain the same but the data collection is limited
- Server communication still uses the same Flask backend
