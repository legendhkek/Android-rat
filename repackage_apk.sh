#!/bin/bash

# Quick APK Repackaging Script
# Use this after customizing APK_Modifier_Ready

echo "Repackaging APK..."

# Check if apktool is installed
if ! command -v apktool &> /dev/null; then
    echo "Error: apktool not found. Install it first:"
    echo "  sudo apt-get install apktool"
    exit 1
fi

# Repackage
echo "Building APK..."
apktool b APK_Modifier_Ready -o APK_Modifier.apk

if [ $? -eq 0 ]; then
    echo "✓ APK built successfully: APK_Modifier.apk"
    echo ""
    echo "Next steps:"
    echo "1. Sign the APK:"
    echo "   apksigner sign --ks my-key.keystore APK_Modifier.apk"
    echo ""
    echo "2. Install:"
    echo "   adb install APK_Modifier.apk"
else
    echo "✗ Build failed"
    exit 1
fi
