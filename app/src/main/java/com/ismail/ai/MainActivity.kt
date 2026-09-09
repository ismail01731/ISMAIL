package com.ismail.ai

import android.Manifest
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import android.os.Bundle
import android.webkit.PermissionRequest
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import android.webkit.WebSettings
import android.view.ViewGroup
import android.view.View
import android.os.Message
import androidx.activity.ComponentActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

import android.content.Intent
import android.speech.RecognizerIntent
import android.webkit.JavascriptInterface
import androidx.activity.result.contract.ActivityResultContracts

class MainActivity : ComponentActivity() {

    private lateinit var webView: WebView

    private val speechLauncher =
        registerForActivityResult(
            ActivityResultContracts.StartActivityForResult()
        ) { result ->

            if (result.resultCode == RESULT_OK) {

                val text =
                    result.data
                        ?.getStringArrayListExtra(
                            RecognizerIntent.EXTRA_RESULTS
                        )
                        ?.firstOrNull()

                if (text != null) {
                    webView.evaluateJavascript(
                        """
                        window.receiveNativeVoice(
                            ${org.json.JSONObject.quote(text)}
                        );
                        """.trimIndent(),
                        null
                    )
                }
            }
        }

    companion object {
        private const val BACKEND_BASE_URL =
            "https://ismail-ai-api.onrender.com"

        private const val REQUEST_RECORD_AUDIO = 100
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        if (
            ContextCompat.checkSelfPermission(
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

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            allowFileAccess = true
            allowContentAccess = true
            databaseEnabled = true
            mediaPlaybackRequiresUserGesture = false

            javaScriptCanOpenWindowsAutomatically = true
            loadsImagesAutomatically = true
            setSupportMultipleWindows(true)

            userAgentString =
                userAgentString + " ISMAILAIAndroid"

            mixedContentMode =
                WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE
        }

        webView.webViewClient =
            object : WebViewClient() {

                override fun shouldOverrideUrlLoading(
                    view: WebView?,
                    url: String?
                ): Boolean {

                    if (url == null) return false

                    view?.loadUrl(url)
                    return true
                }
            }

        webView.webChromeClient =
            object : WebChromeClient() {

                override fun onPermissionRequest(
                    request: PermissionRequest
                ) {
                    runOnUiThread {
                        request.grant(request.resources)
                    }
                }

                override fun onCreateWindow(
                    view: WebView?,
                    isDialog: Boolean,
                    isUserGesture: Boolean,
                    resultMsg: Message?
                ): Boolean {

                    val popupWebView =
                        WebView(this@MainActivity)

                    popupWebView.settings.apply {
                        javaScriptEnabled = true
                        domStorageEnabled = true
                        javaScriptCanOpenWindowsAutomatically = true
                        setSupportMultipleWindows(true)
                        loadsImagesAutomatically = true
                    }

                    popupWebView.webViewClient =
                        object : WebViewClient() {

                            override fun shouldOverrideUrlLoading(
                                view: WebView?,
                                url: String?
                            ): Boolean {

                                if (url == null) return false

                                view?.loadUrl(url)
                                return true
                            }
                        }

                    popupWebView.webChromeClient =
                        object : WebChromeClient() {

                            override fun onCloseWindow(
                                window: WebView?
                            ) {
                                if (window != null) {
                                    (window.parent as? ViewGroup)
                                        ?.removeView(window)

                                    window.destroy()
                                }
                            }

                            override fun onPermissionRequest(
                                request: PermissionRequest
                            ) {
                                runOnUiThread {
                                    request.grant(request.resources)
                                }
                            }
                        }

                    popupWebView.layoutParams =
                        ViewGroup.LayoutParams(
                            ViewGroup.LayoutParams.MATCH_PARENT,
                            ViewGroup.LayoutParams.MATCH_PARENT
                        )

                    popupWebView.visibility = View.VISIBLE

                    addContentView(
                        popupWebView,
                        popupWebView.layoutParams
                    )

                    val transport =
                        resultMsg?.obj
                            as? WebView.WebViewTransport

                    transport?.webView = popupWebView

                    resultMsg?.sendToTarget()

                    return true
                }
            }

        webView.addJavascriptInterface(

            object {

                @JavascriptInterface
                fun startVoiceRecognition() {

                    runOnUiThread {

                        val intent =
                            Intent(
                                RecognizerIntent.ACTION_RECOGNIZE_SPEECH
                            )

                        intent.putExtra(
                            RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                            RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
                        )

                        intent.putExtra(
                            RecognizerIntent.EXTRA_LANGUAGE,
                            "bn-BD"
                        )

                        intent.putExtra(
                            RecognizerIntent.EXTRA_PROMPT,
                            "কথা বলুন..."
                        )

                        speechLauncher.launch(intent)
                    }
                }

            },

            "AndroidVoice"
        )

        webView.loadUrl(
            "$BACKEND_BASE_URL/app/"
        )

        setContentView(webView)
    }

    override fun onDestroy() {
        webView.destroy()
        super.onDestroy()
    }
}