package com.ismail.ai
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
class BackendActionClient {
    companion object {
        private const val BASE_URL = "https://ismail-ai-api.onrender.com"
    }
    fun executeCommand(command: String): String? {
        val session = createSession() ?: return null
        val token = session.optString("token")
        if (token.isEmpty()) {
            return null
        }
        val connection = URL("$BASE_URL/api/chat")
            .openConnection() as HttpURLConnection
        connection.requestMethod = "POST"
        connection.setRequestProperty(
            "Content-Type",
            "application/json"
        )
        connection.setRequestProperty(
            "Authorization",
            "Bearer $token"
        )
        connection.doOutput = true
        val body = JSONObject()
            .put("message", command)
            .toString()
        connection.outputStream.use { output ->
            output.write(body.toByteArray(Charsets.UTF_8))
        }
        val responseCode = connection.responseCode
        if (responseCode !in 200..299) {
            connection.disconnect()
            return null
        }
        val response = connection.inputStream
            .bufferedReader()
            .use { it.readText() }
        connection.disconnect()
        return response
    }
    private fun createSession(): JSONObject? {
        val connection = URL("$BASE_URL/api/session")
            .openConnection() as HttpURLConnection
        connection.requestMethod = "POST"
        val responseCode = connection.responseCode
        if (responseCode !in 200..299) {
            connection.disconnect()
            return null
        }
        val response = connection.inputStream
            .bufferedReader()
            .use { it.readText() }
        connection.disconnect()
        return JSONObject(response)
    }
}
