package com.tiwari.aiagent

import android.app.Activity
import android.os.Bundle
import android.graphics.Color
import android.view.Gravity
import android.widget.*
import java.net.HttpURLConnection
import java.net.URL
import java.io.OutputStreamWriter
import java.util.concurrent.Executors

class MainActivity : Activity() {
    private val executor = Executors.newSingleThreadExecutor()
    private lateinit var serverInput: EditText
    private lateinit var messageInput: EditText
    private lateinit var status: TextView
    private lateinit var reply: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val prefs = getSharedPreferences("tiwari_settings", MODE_PRIVATE)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(28, 32, 28, 32)
            setBackgroundColor(Color.rgb(12, 18, 35))
        }
        fun label(value: String, size: Float) = TextView(this).apply {
            text = value; textSize = size; setTextColor(Color.WHITE); gravity = Gravity.CENTER
        }
        root.addView(label("TIWARI AI", 32f))
        root.addView(label("Your Universal AI Personal Agent", 15f))
        serverInput = EditText(this).apply {
            hint = "https://your-service.onrender.com"; setSingleLine(true)
            setTextColor(Color.WHITE); setHintTextColor(Color.LTGRAY)
            setText(prefs.getString("server_url", ""))
        }
        root.addView(serverInput)
        root.addView(Button(this).apply {
            text = "CONNECT TO RENDER"
            setOnClickListener {
                val base = serverInput.text.toString().trim().trimEnd('/')
                if (!base.startsWith("https://")) showStatus("Valid HTTPS Render URL enter karein")
                else { prefs.edit().putString("server_url", base).apply(); checkBackend(base) }
            }
        })
        status = label("Backend: Not connected", 15f); root.addView(status)
        messageInput = EditText(this).apply {
            hint = "Tiwari, kya karna hai?"; setTextColor(Color.WHITE); setHintTextColor(Color.LTGRAY)
        }
        root.addView(messageInput)
        root.addView(Button(this).apply {
            text = "SEND"
            setOnClickListener {
                val base = prefs.getString("server_url", "") ?: ""
                val msg = messageInput.text.toString().trim()
                if (base.isBlank()) showStatus("Pehle Render connect karein")
                else if (msg.isBlank()) showStatus("Message likhein")
                else sendMessage(base, msg)
            }
        })
        reply = label("Hey Tiwari! Main taiyar ho raha hoon.", 16f); root.addView(reply)
        setContentView(root)
    }

    private fun checkBackend(base: String) {
        executor.execute {
            try {
                val conn = URL("$base/api/health").openConnection() as HttpURLConnection
                conn.connectTimeout = 15000; conn.readTimeout = 15000
                val result = conn.inputStream.bufferedReader().readText(); conn.disconnect()
                runOnUiThread { showStatus("Connected: $result") }
            } catch (e: Exception) { runOnUiThread { showStatus("Connection failed: ${e.message}") } }
        }
    }

    private fun sendMessage(base: String, message: String) {
        executor.execute {
            try {
                val conn = URL("$base/api/chat").openConnection() as HttpURLConnection
                conn.requestMethod = "POST"; conn.connectTimeout = 20000; conn.readTimeout = 20000
                conn.doOutput = true; conn.setRequestProperty("Content-Type", "application/json")
                val safe = message.replace("\\", "\\\\").replace("\"", "\\\"")
                OutputStreamWriter(conn.outputStream).use { it.write("""{"message":"$safe","language":"hinglish"}""") }
                val response = conn.inputStream.bufferedReader().readText(); conn.disconnect()
                runOnUiThread { reply.text = response }
            } catch (e: Exception) { runOnUiThread { showStatus("Message failed: ${e.message}") } }
        }
    }
    private fun showStatus(value: String) { if (::status.isInitialized) status.text = value }
    override fun onDestroy() { executor.shutdown(); super.onDestroy() }
}
