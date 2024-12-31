import 'dart:ffi' as ffi;
import 'package:ffi/ffi.dart';
import 'dart:convert';
import 'dart:io';

/// FFI signature for the process_image function
typedef ProcessImageFunc = ffi.Pointer<Utf8> Function(
    ffi.Pointer<Utf8>, ffi.Float);
typedef ProcessImage = ffi.Pointer<Utf8> Function(
    ffi.Pointer<Utf8>, double);

/// OCR Bridge class to handle FFI communications with Python
class OCRBridge {
  // Singleton instance
  static final OCRBridge _instance = OCRBridge._internal();
  
  // Library references
  late ffi.DynamicLibrary _lib;
  late ProcessImage _processImage;

  // Factory constructor
  factory OCRBridge() {
    return _instance;
  }

  // Private constructor
  OCRBridge._internal() {
    _lib = _loadLibrary();
    _processImage = _lib
        .lookupFunction<ProcessImageFunc, ProcessImage>('process_image');
  }

  /// Loads the appropriate library based on platform
  ffi.DynamicLibrary _loadLibrary() {
    if (Platform.isAndroid) {
      return ffi.DynamicLibrary.open('libocr_bridge.so');
    } else if (Platform.isIOS) {
      return ffi.DynamicLibrary.process();
    } else {
      throw UnsupportedError('Unsupported platform');
    }
  }

  /// Process an image and return the OCR results
  /// 
  /// Parameters:
  /// - imagePath: Path to the image file
  /// - minConfidence: Minimum confidence threshold (0.0 to 1.0)
  /// 
  /// Returns a Map containing:
  /// - status: 'success' or 'error'
  /// - text: Detected text (if success)
  /// - boxes: Bounding boxes (if success)
  /// - message: Error message (if error)
  Map<String, dynamic> processImage(String imagePath, {double minConfidence = 0.5}) {
    try {
      // Convert path to native string
      final pathPointer = imagePath.toNativeUtf8();
      
      // Call native function
      final resultPointer = _processImage(pathPointer, minConfidence);
      
      // Free the input path pointer
      calloc.free(pathPointer);
      
      // Convert result to Dart map
      final resultString = resultPointer.toDartString();
      return json.decode(resultString);
      
    } catch (e) {
      return {
        'status': 'error',
        'message': 'FFI Error: $e',
      };
    }
  }
}

/// Example usage in a widget:
/// ```dart
/// final bridge = OCRBridge();
/// final result = bridge.processImage(
///   '/path/to/image.jpg',
///   minConfidence: 0.7,
/// );
/// 
/// if (result['status'] == 'success') {
///   print('Detected text: ${result['text']}');
///   print('Bounding boxes: ${result['boxes']}');
/// } else {
///   print('Error: ${result['message']}');
/// }
/// ```