import 'package:flutter/services.dart';
import 'package:flutter/foundation.dart';

class PythonBridge {
  static const platform = MethodChannel('com.wuai.text_extractor_app/ocr');
  static bool _initialized = false;

  static Future<bool> initialize() async {
    if (_initialized) return true;

    try {
      final bool result = await platform.invokeMethod('initializePython');
      _initialized = result;
      debugPrint('Python initialization ${result ? 'successful' : 'failed'}');
      return result;
    } on PlatformException catch (e) {
      debugPrint('Failed to initialize Python: ${e.message}');
      return false;
    }
  }
}