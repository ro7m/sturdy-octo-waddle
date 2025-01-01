import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'screens/camera_screen.dart';

void main() async {
  try {
    // Ensure plugin services are initialized
    WidgetsFlutterBinding.ensureInitialized();
    
    debugPrint("Getting available cameras...");
    // Get available cameras
    final cameras = await availableCameras();
    
    if (cameras.isEmpty) {
      debugPrint("No cameras found!");
      throw CameraException('No cameras available', 'No cameras were found on the device');
    }
    
    debugPrint("Found ${cameras.length} cameras");
    // Get the first (usually back) camera
    final firstCamera = cameras.first;
    debugPrint("Using camera: ${firstCamera.name}");

    runApp(
      MaterialApp(
        theme: ThemeData(
          primarySwatch: Colors.blue,
          useMaterial3: true,
        ),
        home: CameraScreen(camera: firstCamera),
      ),
    );
  } catch (e) {
    debugPrint("Error in main: $e");
    runApp(
      MaterialApp(
        home: Scaffold(
          body: Center(
            child: Text('Failed to initialize camera: $e'),
          ),
        ),
      ),
    );
  }
}