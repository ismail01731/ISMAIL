package com.ismail.ai
import android.os.Build
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
class BackendActionClient {
    private val cloudBackendUrl =
        "https://ismail-ai-api.onrender.com"
    private val localBackendUrl =
        "http://10.0.2.2:8000"
    private fun isAndroidEmulator(): Boolean {
        return Build.FINGERPRINT.contains("generic") ||
                Build.FINGERPRINT.contains("emulator") ||
                Build.MODEL.contains("Emulator") ||
                Build.MODEL.contains("Android SDK")
    }
    fun sendAction(
        text: String,
        callback: (Boolean, String) -> Unit
    ) {
        Thread {
            val backends =
                if (isAndroidEmulator()) {
                    listOf(localBackendUrl, cloudBackendUrl)
                } else {
                    listOf(cloudBackendUrl)
                }
            var lastError = "Backend unavailable"
            for (backendUrl in backends) {
                var connection: HttpURLConnection? = null
                try {
                    val url = URL("$backendUrl/api/action")
                    connection =
                        url.openConnection() as HttpURLConnection
                    connection.requestMethod = "POST"
                    connection.connectTimeout = 5000
                    connection.readTimeout = 15000
                    connection.doOutput = true
                    connection.setRequestProperty(
                        "Content-Type",
                        "application/json"
                    )
                    val json = JSONObject()
                    json.put("text", text)
                    connection.outputStream.use { output ->
                        output.write(
                            json.toString()
                                .toByteArray(Charsets.UTF_8)
                        )
                    }
                    val responseCode =
                        connection.responseCode
                    val stream =
                        if (responseCode in 200..299) {
                            connection.inputStream
                        } else {
                            connection.errorStream
                        }
                    val responseText =
                        stream
                            ?.bufferedReader()
                            ?.use { it.readText() }
                            ?: ""
                    if (responseCode in 200..299) {
                        callback(true, responseText)
                        return@Thread
                    }
                    lastError =
                        "HTTP $responseCode: $responseText"
                } catch (e: Exception) {
                    lastError =
                        e.message ?: "Backend connection failed"
                } finally {
                    connection?.disconnect()
                }
            }
            callback(false, lastError)
        }.start()
    }
}
