package com.wuai.text_extractor_app

import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import android.util.Log

class MainActivity: FlutterActivity() {
    private val CHANNEL = "com.wuai.text_extractor_app/ocr"
    private var pythonInitialized = false

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "initializePython" -> {
                    try {
                        // Load the Python library
                        System.loadLibrary("python3.10")
                        // Load the OCR bridge library
                        System.loadLibrary("ocr_bridge")
                        
                        pythonInitialized = true
                        result.success(true)
                        Log.d("MainActivity", "Python runtime initialized successfully")
                    } catch (e: Exception) {
                        Log.e("MainActivity", "Failed to initialize Python: ${e.message}")
                        e.printStackTrace()
                        result.error("INIT_FAILED", "Failed to initialize Python", e.message)
                    }
                }
                else -> result.notImplemented()
            }
        }
    }
}