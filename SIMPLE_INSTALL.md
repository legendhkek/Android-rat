# Simple Installation Guide

## What You Have

You now have `APK_Modifier_Ready/` - a modified APK directory ready to be packaged.

## What You Need

### Option 1: Use Existing Tools (Recommended)

**Requirements:**
- `apktool` - For repackaging APK
- `apksigner` or `jarsigner` - For signing APK
- `zipalign` - For optimizing APK (optional)

**Install on Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install apktool android-sdk-platform-tools-common
```

**Install on macOS:**
```bash
brew install apktool
```

**Install on Windows:**
- Download apktool from: https://ibotpeaches.github.io/Apktool/
- Download Android SDK tools

### Option 2: Manual Method

If you don't have apktool, you can manually create the APK:

1. **ZIP the directory:**
   ```bash
   cd APK_Modifier_Ready
   zip -r ../APK_Modifier.zip *
   mv ../APK_Modifier.zip ../APK_Modifier.apk
   ```

2. **Sign with jarsigner:**
   ```bash
   keytool -genkey -v -keystore my-key.keystore -alias my-alias -keyalg RSA -keysize 2048 -validity 10000
   jarsigner -verbose -keystore my-key.keystore APK_Modifier.apk my-alias
   ```

## Quick Start

### Using the Script (Easiest)

```bash
# 1. Repackage
./repackage_apk.sh

# 2. Sign (first time - create keystore)
keytool -genkey -v -keystore my-key.keystore -alias my-alias -keyalg RSA -keysize 2048 -validity 10000

# 3. Sign APK
apksigner sign --ks my-key.keystore APK_Modifier.apk

# 4. Install
adb install APK_Modifier.apk
```

### Manual Steps

```bash
# 1. Build APK from directory
apktool b APK_Modifier_Ready -o APK_Modifier.apk

# 2. Create keystore (once)
keytool -genkey -v -keystore my-key.keystore -alias my-alias -keyalg RSA -keysize 2048 -validity 10000

# 3. Sign
apksigner sign --ks my-key.keystore --out APK_Modifier_signed.apk APK_Modifier.apk

# 4. Optimize (optional)
zipalign -v 4 APK_Modifier_signed.apk APK_Modifier_final.apk

# 5. Install
adb install APK_Modifier_final.apk
```

## Customization Before Packaging

### Configure Settings

Edit `APK_Modifier_Ready/assets/config/app_config.json`:

```json
{
  "telegram": {
    "bot_token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
  },
  "monitoring": {
    "interval_seconds": 300
  }
}
```

### Customize Web Interface

Edit files in `APK_Modifier_Ready/assets/web/`:
- `index.html` - Main interface
- `css/style.css` - Styling
- `js/app.js` - JavaScript functionality

### Change App Name/Icon

- Icon: Replace files in `APK_Modifier_Ready/res/mipmap-*/`
- Name: Edit `APK_Modifier_Ready/AndroidManifest.xml`

## Important Notes

### About Java/Python Conversion

The current structure includes:
- ✓ All web interface assets (HTML, CSS, JS)
- ✓ Configuration files
- ✓ AndroidManifest with permissions
- ✓ Native libraries (libxx.so)
- ✗ Java classes (not included - use full build)

**For full functionality, you have two options:**

1. **Use the full Android build** (android-app/)
   - Includes all Java services
   - Includes Python server (via Chaquopy)
   - Complete integration
   - Run: `cd android-app && ./gradlew assembleRelease`

2. **Add Java classes manually** (advanced)
   - Compile Java to .class files
   - Convert to DEX using dx tool
   - Add to classes.dex

### Converting Python to Java

Python code (app.py, utils/) cannot be directly added to DEX files. You need:

1. **Use Chaquopy** (in android-app/ build) - Embeds Python runtime
2. **Rewrite in Java/Kotlin** - Port Flask server to Java HTTP server
3. **Use WebView + External Server** - Keep Python separate

## Troubleshooting

**"apktool not found"**
- Install: `sudo apt-get install apktool`

**"Signature verification failed"**
- Create new keystore
- Use same key for signing

**"Installation failed"**
- Enable "Install from Unknown Sources"
- Check Android version compatibility

**"App crashes on launch"**
- Java classes are missing
- Use full build from android-app/

## Next Steps

For production use, you should:

1. **Use the full Android build** for complete functionality
2. Add proper Java service implementations
3. Include Python runtime (Chaquopy) if using Python
4. Add proper error handling
5. Test on real devices

See BUILD_INSTRUCTIONS.md for full build process.
