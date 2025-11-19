# Advanced ProGuard Rules for Full Undetectability (FUD)
# Maximum obfuscation and anti-detection for bypassing Play Store and Antivirus

# Aggressive optimization and obfuscation
-optimizationpasses 7
-dontpreverify
-verbose

# Enable all obfuscation techniques
-repackageclasses ''
-allowaccessmodification
-useuniqueclassmembernames
-keepattributes *Annotation*,Signature,Exception,InnerClasses
-dontusemixedcaseclassnames

# Rename source files and line numbers
-renamesourcefileattribute SourceFile
-keepattributes SourceFile,LineNumberTable

# Flatten and obfuscate package hierarchy
-flattenpackagehierarchy 'sys.core.app'
-repackageclasses 'sys.core.app'

# Custom obfuscation dictionary for better stealth
-adaptclassstrings
-obfuscationdictionary dictionary.txt
-classobfuscationdictionary dictionary.txt
-packageobfuscationdictionary dictionary.txt

# Merge classes for stealth
-mergeinterfacesaggressively

# Keep Android components but obfuscate names
-keep public class * extends android.app.Activity {
    public <methods>;
}
-keep public class * extends android.app.Service {
    public <methods>;
}
-keep public class * extends android.content.BroadcastReceiver {
    public <methods>;
}

# Native methods
-keepclasseswithmembernames class * {
    native <methods>;
}

# Keep setters and getters
-keepclassmembers public class * {
    void set*(***);
    *** get*();
}

# Strip all logging for production (FUD)
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
    public static *** w(...);
    public static *** e(...);
    public static *** wtf(...);
}

# Remove printStackTrace calls
-assumenosideeffects class java.lang.Throwable {
    public void printStackTrace();
}

# Advanced optimizations for smaller APK and better stealth
-optimizations !code/simplification/arithmetic,!code/simplification/cast,!field/*,!class/merging/*,!code/allocation/variable

# WebView JavaScript Interface
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# Serialization
-keepnames class * implements java.io.Serializable
-keepclassmembers class * implements java.io.Serializable {
    static final long serialVersionUID;
    private static final java.io.ObjectStreamField[] serialPersistentFields;
    !static !transient <fields>;
    private void writeObject(java.io.ObjectOutputStream);
    private void readObject(java.io.ObjectInputStream);
    java.lang.Object writeReplace();
    java.lang.Object readResolve();
}

# Anti-detection: Hide reflection usage
-keepattributes Signature,InnerClasses,EnclosingMethod

# FUD: Remove metadata that could aid analysis
-keepattributes !SourceFile,!SourceDir

# Optimize and shrink strings
-adaptresourcefilenames
-adaptresourcefilecontents **.properties,META-INF/MANIFEST.MF

# Additional security for native libraries
-keepclasseswithmembernames,includedescriptorclasses class * {
    native <methods>;
}

# Hide all debug information
-keepattributes !LocalVariableTable,!LocalVariableTypeTable

# Optimize method parameters
-optimizations !method/removal/parameter
