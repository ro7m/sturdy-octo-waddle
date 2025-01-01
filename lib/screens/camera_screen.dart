import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import '../ffi/ocr_bridge.dart';
import 'package:permission_handler/permission_handler.dart';

class CameraScreen extends StatefulWidget {
  final CameraDescription camera;

  const CameraScreen({
    super.key,
    required this.camera,
  });

  @override
  CameraScreenState createState() => CameraScreenState();
}

class CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  Future<void>? _initializeControllerFuture;
  final OCRBridge _ocrBridge = OCRBridge();
  bool _isProcessing = false;
  bool _isCameraPermissionGranted = false;
  String _debugInfo = '';

  void _updateDebugInfo(String info) {
    print(info); // Print to console
    setState(() {
      _debugInfo = info;
    });
  }

  @override
  void initState() {
    super.initState();
    _updateDebugInfo('Initializing camera screen...');
    _requestCameraPermission();
  }

  Future<void> _requestCameraPermission() async {
    _updateDebugInfo('Requesting camera permission...');
    final status = await Permission.camera.request();
    
    if (!mounted) return;
    
    setState(() {
      _isCameraPermissionGranted = status == PermissionStatus.granted;
    });
    
    _updateDebugInfo('Camera permission status: $status');
    
    if (_isCameraPermissionGranted) {
      await _initializeCamera();
    } else {
      _updateDebugInfo('Camera permission denied');
    }
  }

  Future<void> _initializeCamera() async {
    try {
      _updateDebugInfo('Creating camera controller...');
      _controller = CameraController(
        widget.camera,
        ResolutionPreset.medium,
        enableAudio: false,
      );
      
      setState(() {
        _initializeControllerFuture = _controller.initialize();
      });
      
      _updateDebugInfo('Waiting for camera initialization...');
      await _initializeControllerFuture;
      _updateDebugInfo('Camera initialized successfully');
      
      // Check if camera is actually working
      if (!_controller.value.isInitialized) {
        throw CameraException('Failed to initialize', 'Camera controller initialization failed');
      }
      
    } catch (e) {
      _updateDebugInfo('Error initializing camera: $e');
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error initializing camera: $e')),
        );
      }
    }
  }

  @override
  void dispose() {
    _updateDebugInfo('Disposing camera controller...');
    if (_isCameraPermissionGranted && _controller.value.isInitialized) {
      _controller.dispose();
    }
    super.dispose();
  }

  Future<void> _processImage(String imagePath) async {
    try {
      _updateDebugInfo('Processing image: $imagePath');
      
      final result = await _ocrBridge.processImage(imagePath);
      _updateDebugInfo('OCR Result: $result');
      
      if (!mounted) return;

      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('OCR Results'),
          content: SingleChildScrollView(
            child: Text(result.toString()),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('OK'),
            ),
          ],
        ),
      );
    } catch (e) {
      _updateDebugInfo('Error processing image: $e');
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error processing image: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _takePicture() async {
    if (_isProcessing) return;

    try {
      _updateDebugInfo('Taking picture...');
      setState(() {
        _isProcessing = true;
      });

      await _initializeControllerFuture;
      final image = await _controller.takePicture();
      _updateDebugInfo('Picture taken, processing image...');
      await _processImage(image.path);

    } catch (e) {
      _updateDebugInfo('Error taking picture: $e');
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isProcessing = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('OCR Camera'),
      ),
      body: Column(
        children: [
          Expanded(
            child: _buildMainContent(),
          ),
          // Debug info panel
          Container(
            padding: const EdgeInsets.all(8),
            color: Colors.black87,
            width: double.infinity,
            child: Text(
              _debugInfo,
              style: const TextStyle(color: Colors.white, fontSize: 12),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMainContent() {
    if (!_isCameraPermissionGranted) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Camera permission is required to use this app.'),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _requestCameraPermission,
              child: const Text('Request Permission'),
            ),
          ],
        ),
      );
    }

    return FutureBuilder<void>(
      future: _initializeControllerFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.done) {
          if (snapshot.hasError) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text('Error: ${snapshot.error}'),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: _initializeCamera,
                    child: const Text('Retry'),
                  ),
                ],
              ),
            );
          }

          if (!_controller.value.isInitialized) {
            return const Center(
              child: Text('Camera failed to initialize'),
            );
          }

          return Stack(
            children: [
              Positioned.fill(
                child: CameraPreview(_controller),
              ),
              if (_isProcessing)
                const Positioned.fill(
                  child: Center(
                    child: CircularProgressIndicator(
                      valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                    ),
                  ),
                ),
              Positioned(
                bottom: 0,
                left: 0,
                right: 0,
                child: Container(
                  color: Colors.black45,
                  padding: const EdgeInsets.all(16.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      FloatingActionButton(
                        onPressed: _isProcessing ? null : _takePicture,
                        child: Icon(_isProcessing ? Icons.hourglass_empty : Icons.camera_alt),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          );
        }
        return const Center(child: CircularProgressIndicator());
      },
    );
  }
}