#!/usr/bin/env python3
"""
Advanced APK Modifier - Comprehensive APK Manipulation
Supports: Name change, version change, icon replacement, permission injection,
activity injection, service injection, custom payload, resource modification, etc.
"""

import os
import re
import json
import shutil
import subprocess
from PIL import Image
import xml.etree.ElementTree as ET
from datetime import datetime

class AdvancedAPKModifier:
    """
    Advanced APK modification with comprehensive features:
    - Change app name, package name, version
    - Replace icons and images
    - Inject permissions, activities, services
    - Inject custom code (smali)
    - Modify resources (strings, colors, etc.)
    - Add native libraries
    - Sign with custom certificate
    """
    
    def __init__(self, apk_path, output_dir='modified_apk'):
        self.apk_path = apk_path
        self.output_dir = output_dir
        self.decompiled_dir = os.path.join(output_dir, 'decompiled')
        self.manifest_path = None
        self.modifications = []
        
    def decompile(self):
        """Decompile APK using apktool"""
        print("[*] Decompiling APK...")
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        cmd = ['apktool', 'd', '-f', self.apk_path, '-o', self.decompiled_dir]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Decompilation failed: {result.stderr}")
        
        self.manifest_path = os.path.join(self.decompiled_dir, 'AndroidManifest.xml')
        print("[✓] APK decompiled successfully")
        return True
    
    # ==================== APP NAME MODIFICATION ====================
    
    def change_app_name(self, new_name):
        """Change application display name"""
        print(f"[*] Changing app name to: {new_name}")
        
        # Method 1: Update AndroidManifest.xml
        tree = ET.parse(self.manifest_path)
        root = tree.getroot()
        
        # Find application element
        ns = {'android': 'http://schemas.android.com/apk/res/android'}
        app_element = root.find('application')
        
        if app_element is not None:
            app_element.set('{http://schemas.android.com/apk/res/android}label', new_name)
            tree.write(self.manifest_path, encoding='utf-8', xml_declaration=True)
        
        # Method 2: Update strings.xml
        strings_path = os.path.join(self.decompiled_dir, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            strings_tree = ET.parse(strings_path)
            strings_root = strings_tree.getroot()
            
            # Find app_name string
            for string_elem in strings_root.findall('string'):
                if string_elem.get('name') == 'app_name':
                    string_elem.text = new_name
                    break
            else:
                # Create app_name if doesn't exist
                new_string = ET.SubElement(strings_root, 'string', name='app_name')
                new_string.text = new_name
            
            strings_tree.write(strings_path, encoding='utf-8', xml_declaration=True)
        
        self.modifications.append(f"App name changed to: {new_name}")
        print("[✓] App name changed")
        return True
    
    # ==================== VERSION MODIFICATION ====================
    
    def change_version(self, version_name=None, version_code=None):
        """Change app version name and/or code"""
        print(f"[*] Changing version...")
        
        # Parse apktool.yml for version info
        apktool_yml = os.path.join(self.decompiled_dir, 'apktool.yml')
        
        if os.path.exists(apktool_yml):
            with open(apktool_yml, 'r') as f:
                content = f.read()
            
            if version_name:
                content = re.sub(r"versionName: '.*?'", f"versionName: '{version_name}'", content)
                print(f"  Version name: {version_name}")
            
            if version_code:
                content = re.sub(r"versionCode: '.*?'", f"versionCode: '{version_code}'", content)
                print(f"  Version code: {version_code}")
            
            with open(apktool_yml, 'w') as f:
                f.write(content)
        
        # Also update AndroidManifest.xml
        tree = ET.parse(self.manifest_path)
        root = tree.getroot()
        
        if version_name:
            root.set('{http://schemas.android.com/apk/res/android}versionName', version_name)
        
        if version_code:
            root.set('{http://schemas.android.com/apk/res/android}versionCode', str(version_code))
        
        tree.write(self.manifest_path, encoding='utf-8', xml_declaration=True)
        
        self.modifications.append(f"Version changed: {version_name} ({version_code})")
        print("[✓] Version changed")
        return True
    
    # ==================== PACKAGE NAME MODIFICATION ====================
    
    def change_package_name(self, new_package):
        """Change application package name"""
        print(f"[*] Changing package name to: {new_package}")
        
        tree = ET.parse(self.manifest_path)
        root = tree.getroot()
        
        old_package = root.get('package')
        root.set('package', new_package)
        
        tree.write(self.manifest_path, encoding='utf-8', xml_declaration=True)
        
        # Note: Full package rename requires renaming smali files and directories
        # This is a simplified version
        
        self.modifications.append(f"Package changed: {old_package} → {new_package}")
        print("[✓] Package name changed")
        return True
    
    # ==================== ICON/IMAGE MODIFICATION ====================
    
    def replace_icon(self, icon_image_path):
        """Replace app icon with custom image"""
        print(f"[*] Replacing app icon...")
        
        # Generate icons for all densities
        densities = {
            'mdpi': 48,
            'hdpi': 72,
            'xhdpi': 96,
            'xxhdpi': 144,
            'xxxhdpi': 192
        }
        
        source_img = Image.open(icon_image_path)
        
        for density, size in densities.items():
            mipmap_dir = os.path.join(self.decompiled_dir, 'res', f'mipmap-{density}')
            os.makedirs(mipmap_dir, exist_ok=True)
            
            # Resize and save
            resized = source_img.resize((size, size), Image.Resampling.LANCZOS)
            
            # Save as PNG
            icon_path = os.path.join(mipmap_dir, 'ic_launcher.png')
            resized.save(icon_path, 'PNG')
            
            # Also save as round icon
            round_icon_path = os.path.join(mipmap_dir, 'ic_launcher_round.png')
            resized.save(round_icon_path, 'PNG')
        
        self.modifications.append("App icon replaced")
        print("[✓] Icon replaced for all densities")
        return True
    
    def replace_image_resource(self, resource_name, image_path, resource_type='drawable'):
        """Replace any image resource (drawable, mipmap, etc.)"""
        print(f"[*] Replacing image resource: {resource_name}")
        
        source_img = Image.open(image_path)
        
        # Find resource directories
        res_dir = os.path.join(self.decompiled_dir, 'res')
        
        for dirname in os.listdir(res_dir):
            if dirname.startswith(resource_type):
                target_dir = os.path.join(res_dir, dirname)
                target_file = os.path.join(target_dir, f"{resource_name}.png")
                
                if os.path.exists(target_file):
                    # Replace existing
                    source_img.save(target_file, 'PNG')
                    print(f"  Replaced: {dirname}/{resource_name}.png")
        
        self.modifications.append(f"Image resource '{resource_name}' replaced")
        print("[✓] Image resource replaced")
        return True
    
    # ==================== PERMISSION INJECTION ====================
    
    def add_permissions(self, permissions):
        """
        Add permissions to AndroidManifest.xml
        permissions: list of permission strings
        Example: ['android.permission.CAMERA', 'android.permission.RECORD_AUDIO']
        """
        print(f"[*] Adding {len(permissions)} permissions...")
        
        tree = ET.parse(self.manifest_path)
        root = tree.getroot()
        
        # Get existing permissions
        existing = set()
        for perm in root.findall('uses-permission'):
            name = perm.get('{http://schemas.android.com/apk/res/android}name')
            if name:
                existing.add(name)
        
        # Add new permissions
        added = 0
        for perm in permissions:
            if perm not in existing:
                perm_elem = ET.SubElement(root, 'uses-permission')
                perm_elem.set('{http://schemas.android.com/apk/res/android}name', perm)
                added += 1
                print(f"  + {perm}")
        
        tree.write(self.manifest_path, encoding='utf-8', xml_declaration=True)
        
        self.modifications.append(f"Added {added} new permissions")
        print(f"[✓] {added} permissions added")
        return True
    
    # ==================== COMPONENT INJECTION ====================
    
    def add_activity(self, activity_name, exported=False, main_launcher=False):
        """Add new activity to manifest"""
        print(f"[*] Adding activity: {activity_name}")
        
        tree = ET.parse(self.manifest_path)
        root = tree.getroot()
        
        app_element = root.find('application')
        
        activity = ET.SubElement(app_element, 'activity')
        activity.set('{http://schemas.android.com/apk/res/android}name', activity_name)
        activity.set('{http://schemas.android.com/apk/res/android}exported', str(exported).lower())
        
        if main_launcher:
            intent_filter = ET.SubElement(activity, 'intent-filter')
            action = ET.SubElement(intent_filter, 'action')
            action.set('{http://schemas.android.com/apk/res/android}name', 
                      'android.intent.action.MAIN')
            category = ET.SubElement(intent_filter, 'category')
            category.set('{http://schemas.android.com/apk/res/android}name', 
                        'android.intent.category.LAUNCHER')
        
        tree.write(self.manifest_path, encoding='utf-8', xml_declaration=True)
        
        self.modifications.append(f"Activity added: {activity_name}")
        print("[✓] Activity added")
        return True
    
    def add_service(self, service_name, exported=False, enabled=True):
        """Add new service to manifest"""
        print(f"[*] Adding service: {service_name}")
        
        tree = ET.parse(self.manifest_path)
        root = tree.getroot()
        
        app_element = root.find('application')
        
        service = ET.SubElement(app_element, 'service')
        service.set('{http://schemas.android.com/apk/res/android}name', service_name)
        service.set('{http://schemas.android.com/apk/res/android}exported', str(exported).lower())
        service.set('{http://schemas.android.com/apk/res/android}enabled', str(enabled).lower())
        
        tree.write(self.manifest_path, encoding='utf-8', xml_declaration=True)
        
        self.modifications.append(f"Service added: {service_name}")
        print("[✓] Service added")
        return True
    
    def add_receiver(self, receiver_name, actions=None, exported=True):
        """Add broadcast receiver to manifest"""
        print(f"[*] Adding receiver: {receiver_name}")
        
        tree = ET.parse(self.manifest_path)
        root = tree.getroot()
        
        app_element = root.find('application')
        
        receiver = ET.SubElement(app_element, 'receiver')
        receiver.set('{http://schemas.android.com/apk/res/android}name', receiver_name)
        receiver.set('{http://schemas.android.com/apk/res/android}exported', str(exported).lower())
        receiver.set('{http://schemas.android.com/apk/res/android}enabled', 'true')
        
        if actions:
            intent_filter = ET.SubElement(receiver, 'intent-filter')
            for action in actions:
                action_elem = ET.SubElement(intent_filter, 'action')
                action_elem.set('{http://schemas.android.com/apk/res/android}name', action)
        
        tree.write(self.manifest_path, encoding='utf-8', xml_declaration=True)
        
        self.modifications.append(f"Receiver added: {receiver_name}")
        print("[✓] Receiver added")
        return True
    
    # ==================== CODE INJECTION ====================
    
    def inject_smali_code(self, target_class, smali_code, method='onCreate'):
        """Inject smali code into existing class"""
        print(f"[*] Injecting smali code into: {target_class}")
        
        # Convert class name to path
        class_path = target_class.replace('.', '/') + '.smali'
        smali_file = os.path.join(self.decompiled_dir, 'smali', class_path)
        
        if not os.path.exists(smali_file):
            print(f"[!] Class not found: {smali_file}")
            return False
        
        with open(smali_file, 'r') as f:
            content = f.read()
        
        # Find the method
        method_pattern = f'.method.*{method}'
        match = re.search(method_pattern, content)
        
        if match:
            # Find end of method
            insert_pos = content.find('.end method', match.start())
            
            if insert_pos > 0:
                # Insert code before .end method
                modified = content[:insert_pos] + '\n' + smali_code + '\n' + content[insert_pos:]
                
                with open(smali_file, 'w') as f:
                    f.write(modified)
                
                print("[✓] Smali code injected")
                self.modifications.append(f"Code injected into {target_class}.{method}")
                return True
        
        print("[!] Method not found")
        return False
    
    def add_smali_class(self, class_name, smali_code):
        """Add a complete new smali class"""
        print(f"[*] Adding new smali class: {class_name}")
        
        # Convert class name to path
        class_path = class_name.replace('.', '/') + '.smali'
        smali_file = os.path.join(self.decompiled_dir, 'smali', class_path)
        
        # Create directories if needed
        os.makedirs(os.path.dirname(smali_file), exist_ok=True)
        
        with open(smali_file, 'w') as f:
            f.write(smali_code)
        
        self.modifications.append(f"New class added: {class_name}")
        print("[✓] Smali class added")
        return True
    
    # ==================== RESOURCE MODIFICATION ====================
    
    def modify_strings(self, string_replacements):
        """
        Modify string resources
        string_replacements: dict of {string_name: new_value}
        """
        print(f"[*] Modifying {len(string_replacements)} strings...")
        
        strings_path = os.path.join(self.decompiled_dir, 'res', 'values', 'strings.xml')
        
        if not os.path.exists(strings_path):
            print("[!] strings.xml not found")
            return False
        
        tree = ET.parse(strings_path)
        root = tree.getroot()
        
        modified = 0
        for string_elem in root.findall('string'):
            name = string_elem.get('name')
            if name in string_replacements:
                string_elem.text = string_replacements[name]
                modified += 1
                print(f"  {name} = {string_replacements[name]}")
        
        tree.write(strings_path, encoding='utf-8', xml_declaration=True)
        
        self.modifications.append(f"Modified {modified} strings")
        print(f"[✓] {modified} strings modified")
        return True
    
    def modify_colors(self, color_replacements):
        """
        Modify color resources
        color_replacements: dict of {color_name: hex_value}
        """
        print(f"[*] Modifying {len(color_replacements)} colors...")
        
        colors_path = os.path.join(self.decompiled_dir, 'res', 'values', 'colors.xml')
        
        if not os.path.exists(colors_path):
            # Create colors.xml if doesn't exist
            root = ET.Element('resources')
            tree = ET.ElementTree(root)
        else:
            tree = ET.parse(colors_path)
            root = tree.getroot()
        
        for color_name, hex_value in color_replacements.items():
            # Find existing or create new
            found = False
            for color_elem in root.findall('color'):
                if color_elem.get('name') == color_name:
                    color_elem.text = hex_value
                    found = True
                    break
            
            if not found:
                color_elem = ET.SubElement(root, 'color', name=color_name)
                color_elem.text = hex_value
        
        tree.write(colors_path, encoding='utf-8', xml_declaration=True)
        
        self.modifications.append(f"Modified {len(color_replacements)} colors")
        print(f"[✓] Colors modified")
        return True
    
    # ==================== NATIVE LIBRARY INJECTION ====================
    
    def add_native_library(self, lib_name, lib_file_path, architectures=None):
        """
        Add native library (.so file) to APK
        architectures: list of arch (e.g., ['armeabi-v7a', 'arm64-v8a'])
        """
        print(f"[*] Adding native library: {lib_name}")
        
        if architectures is None:
            architectures = ['armeabi-v7a', 'arm64-v8a', 'x86', 'x86_64']
        
        lib_dir = os.path.join(self.decompiled_dir, 'lib')
        
        for arch in architectures:
            arch_dir = os.path.join(lib_dir, arch)
            os.makedirs(arch_dir, exist_ok=True)
            
            target_path = os.path.join(arch_dir, lib_name)
            
            if os.path.exists(lib_file_path):
                shutil.copy(lib_file_path, target_path)
            else:
                # Create dummy library
                with open(target_path, 'wb') as f:
                    f.write(b'\x7fELF')  # ELF header
                    f.write(b'\x00' * 1024)  # Dummy data
            
            print(f"  Added to {arch}")
        
        self.modifications.append(f"Native library added: {lib_name}")
        print("[✓] Native library added")
        return True
    
    # ==================== ASSET/FILE INJECTION ====================
    
    def add_asset_file(self, file_path, asset_name=None):
        """Add file to assets directory"""
        print(f"[*] Adding asset file...")
        
        assets_dir = os.path.join(self.decompiled_dir, 'assets')
        os.makedirs(assets_dir, exist_ok=True)
        
        if asset_name is None:
            asset_name = os.path.basename(file_path)
        
        target_path = os.path.join(assets_dir, asset_name)
        shutil.copy(file_path, target_path)
        
        self.modifications.append(f"Asset added: {asset_name}")
        print(f"[✓] Asset added: {asset_name}")
        return True
    
    def add_raw_resource(self, file_path, resource_name=None):
        """Add file to raw resources"""
        print(f"[*] Adding raw resource...")
        
        raw_dir = os.path.join(self.decompiled_dir, 'res', 'raw')
        os.makedirs(raw_dir, exist_ok=True)
        
        if resource_name is None:
            resource_name = os.path.splitext(os.path.basename(file_path))[0]
        
        target_path = os.path.join(raw_dir, resource_name)
        shutil.copy(file_path, target_path)
        
        self.modifications.append(f"Raw resource added: {resource_name}")
        print(f"[✓] Raw resource added: {resource_name}")
        return True
    
    # ==================== METADATA MODIFICATION ====================
    
    def set_minimum_sdk(self, min_sdk):
        """Set minimum SDK version"""
        print(f"[*] Setting minSdkVersion to: {min_sdk}")
        
        apktool_yml = os.path.join(self.decompiled_dir, 'apktool.yml')
        
        with open(apktool_yml, 'r') as f:
            content = f.read()
        
        content = re.sub(r'minSdkVersion: .*', f'minSdkVersion: {min_sdk}', content)
        
        with open(apktool_yml, 'w') as f:
            f.write(content)
        
        self.modifications.append(f"minSdkVersion set to: {min_sdk}")
        print("[✓] minSdkVersion set")
        return True
    
    def set_target_sdk(self, target_sdk):
        """Set target SDK version"""
        print(f"[*] Setting targetSdkVersion to: {target_sdk}")
        
        apktool_yml = os.path.join(self.decompiled_dir, 'apktool.yml')
        
        with open(apktool_yml, 'r') as f:
            content = f.read()
        
        content = re.sub(r'targetSdkVersion: .*', f'targetSdkVersion: {target_sdk}', content)
        
        with open(apktool_yml, 'w') as f:
            f.write(content)
        
        self.modifications.append(f"targetSdkVersion set to: {target_sdk}")
        print("[✓] targetSdkVersion set")
        return True
    
    # ==================== BUILD & SIGN ====================
    
    def recompile(self, output_apk=None):
        """Recompile APK"""
        print("[*] Recompiling APK...")
        
        if output_apk is None:
            output_apk = os.path.join(self.output_dir, 'modified.apk')
        
        cmd = ['apktool', 'b', self.decompiled_dir, '-o', output_apk]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Recompilation failed: {result.stderr}")
        
        print(f"[✓] APK recompiled: {output_apk}")
        return output_apk
    
    def sign_apk(self, unsigned_apk, signed_apk=None, keystore=None, alias=None):
        """Sign APK with custom keystore"""
        print("[*] Signing APK...")
        
        if signed_apk is None:
            signed_apk = unsigned_apk.replace('.apk', '_signed.apk')
        
        # Simple self-signed certificate for testing
        # In production, use proper keystore
        
        if keystore and alias:
            cmd = [
                'jarsigner', '-verbose',
                '-sigalg', 'SHA256withRSA',
                '-digestalg', 'SHA-256',
                '-keystore', keystore,
                unsigned_apk, alias
            ]
        else:
            # Use apksigner with debug key
            cmd = ['apksigner', 'sign', '--out', signed_apk, unsigned_apk]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"[!] Signing failed: {result.stderr}")
            return unsigned_apk
        
        print(f"[✓] APK signed: {signed_apk}")
        return signed_apk
    
    def zipalign(self, input_apk, output_apk=None):
        """Optimize APK with zipalign"""
        print("[*] Optimizing APK...")
        
        if output_apk is None:
            output_apk = input_apk.replace('.apk', '_aligned.apk')
        
        cmd = ['zipalign', '-v', '4', input_apk, output_apk]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"[!] Zipalign failed: {result.stderr}")
            return input_apk
        
        print(f"[✓] APK optimized: {output_apk}")
        return output_apk
    
    # ==================== REPORT ====================
    
    def generate_report(self):
        """Generate modification report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'original_apk': self.apk_path,
            'modifications': self.modifications,
            'total_changes': len(self.modifications)
        }
        
        report_path = os.path.join(self.output_dir, 'modification_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[✓] Modification report saved: {report_path}")
        print(f"\nTotal modifications: {len(self.modifications)}")
        for mod in self.modifications:
            print(f"  • {mod}")
        
        return report


# ==================== USAGE EXAMPLES ====================

def example_usage():
    """Example of how to use AdvancedAPKModifier"""
    
    # Initialize
    modifier = AdvancedAPKModifier('input.apk', 'output')
    
    # Decompile
    modifier.decompile()
    
    # Change app name
    modifier.change_app_name("My Custom App")
    
    # Change version
    modifier.change_version(version_name="2.0.0", version_code=20)
    
    # Change package name
    modifier.change_package_name("com.custom.package")
    
    # Replace icon
    modifier.replace_icon("custom_icon.png")
    
    # Add permissions
    modifier.add_permissions([
        'android.permission.CAMERA',
        'android.permission.RECORD_AUDIO',
        'android.permission.ACCESS_FINE_LOCATION'
    ])
    
    # Add service
    modifier.add_service(".CustomService", exported=False)
    
    # Add native library
    modifier.add_native_library("libcustom.so", "path/to/lib.so")
    
    # Modify strings
    modifier.modify_strings({
        'welcome_message': 'Welcome to Custom App!',
        'app_description': 'This is a modified app'
    })
    
    # Add asset
    modifier.add_asset_file("config.json")
    
    # Recompile
    output_apk = modifier.recompile()
    
    # Sign
    signed_apk = modifier.sign_apk(output_apk)
    
    # Generate report
    modifier.generate_report()
    
    print(f"\n[✓] Final APK: {signed_apk}")


if __name__ == '__main__':
    print("Advanced APK Modifier - Comprehensive APK Manipulation Tool")
    print("=" * 60)
    example_usage()
