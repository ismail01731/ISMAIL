package com.ismail.ai

import android.Manifest
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import android.util.Log

class MainActivity : ComponentActivity() {

    
    private lateinit var webView: WebView

    private companion object {
        const val BACKEND_BASE_URL = "https://ismail-ai-api.onrender.com"
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        

        

        webView = WebView(this)

        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.allowFileAccess = true
        webView.settings.allowContentAccess = true
        webView.settings.databaseEnabled = true
        webView.settings.setSupportZoom(false)

        

        webView.webViewClient = WebViewClient()
        webView.loadUrl("$BACKEND_BASE_URL/app/")


        



        setContentView(webView)
    }

    override fun onDestroy() {
        
        webView.destroy()
        super.onDestroy()
    }

    
}

