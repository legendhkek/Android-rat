# APK Modifier - Advanced ProGuard Rules for FUD
# Maximum obfuscation and anti-detection

# Obfuscation settings
-dontoptimize
-dontpreverify
-verbose

# Enable aggressive obfuscation
-repackageclasses ''
-allowaccessmodification
-useuniqueclassmembernames
-keepattributes *Annotation*,Signature,Exception,InnerClasses

# Rename classes, methods, and fields
-renamesourcefileattribute SourceFile
-keepattributes SourceFile,LineNumberTable

# Obfuscate package names
-flattenpackagehierarchy 'a.b.c'
-repackageclasses 'a.b.c'

# String encryption
-adaptclassstrings
-obfuscationdictionary dictionary.txt
-classobfuscationdictionary dictionary.txt
-packageobfuscationdictionary dictionary.txt

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

# Remove logging
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
    public static *** w(...);
    public static *** e(...);
    public static *** wtf(...);
}

# Optimization
-optimizations !code/simplification/arithmetic,!code/simplification/cast,!field/*,!class/merging/*
-optimizationpasses 5

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
