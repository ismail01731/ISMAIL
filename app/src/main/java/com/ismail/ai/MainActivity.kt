package com.ismail.ai

import android.Manifest
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import android.os.Bundle
import android.webkit.PermissionRequest
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : ComponentActivity() {

    private lateinit var webView: WebView

    companion object {
        private const val BACKEND_BASE_URL = "https://ismail-ai-api.onrender.com"
        private const val REQUEST_RECORD_AUDIO = 100
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        if (ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.RECORD_AUDIO
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.RECORD_AUDIO),
                REQUEST_RECORD_AUDIO
            )
        }

        webView = WebView(this)

        WebView.setWebContentsDebuggingEnabled(true)

        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.allowFileAccess = true
        webView.settings.allowContentAccess = true
        webView.settings.databaseEnabled = true
        webView.settings.mediaPlaybackRequiresUserGesture = false

        webView.settings.javaScriptCanOpenWindowsAutomatically = true
        webView.settings.loadsImagesAutomatically = true
        webView.settings.setSupportMultipleWindows(true)

        webView.webViewClient = object : WebViewClient() {

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)

                // পেজ পুরো লোড হলে এখানে কোড চলবে
            }

        }

        webView.webChromeClient = object : WebChromeClient() {
            override fun onPermissionRequest(request: PermissionRequest) {
                runOnUiThread {
                    request.grant(request.resources)
                }
            }
        }

        webView.loadUrl("$BACKEND_BASE_URL/app/")

        setContentView(webView)
    }

    override fun onDestroy() {
        webView.destroy()
        super.onDestroy()
    }
}