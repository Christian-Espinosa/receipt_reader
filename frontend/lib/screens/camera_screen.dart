import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'picture_review_screen.dart';
import 'package:camera/camera.dart';
import 'home_screen.dart';

class CameraScreen extends StatefulWidget {
  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  final ImagePicker _picker = ImagePicker();
  XFile? _image;
  CameraController? _controller;
  bool _isTakingPicture = false;
  bool _isPictureTaken = false;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  void _initializeCamera() async {
    final cameras = await availableCameras();
    if (cameras.isNotEmpty) {
      _controller = CameraController(cameras[0], ResolutionPreset.high);
      _controller?.initialize().then((_) {
        if (!mounted) {
          return;
        }
        setState(() {});
      });
    }
  }

  Future<void> _getImageFromGallery() async {
    final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null) {
      setState(() {
        _image = image;
      });
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => PictureScreen(
            imageFile: File(image.path),
            onRetake: () {
              Navigator.pop(context);
              setState(() {
                _isPictureTaken = false;
                _initializeCamera();
              });
            },
            onComplete: (extractedText) {
              _showProcessingSnackbar();
              Navigator.pop(context); // Navigate back to CameraScreen
              Navigator.pop(context); // Navigate back to HomeScreen
              _resetCamera();
            },
          ),
        ),
      );
    }
  }

  void _showProcessingSnackbar() {
    final snackBar = SnackBar(
      content: Text('Processing data...'),
      duration: Duration(seconds: 2),
    );
    ScaffoldMessenger.of(context).showSnackBar(snackBar);
  }

  void _resetCamera() {
    setState(() {
      _isPictureTaken = false;
    });
    _initializeCamera();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          _controller?.value.isInitialized ?? false
              ? CameraPreview(_controller!)
              : Center(child: CircularProgressIndicator()),
          Positioned(
            bottom: 30,
            left: 0,
            right: 0,
            child: Center(
              child: FloatingActionButton(
                backgroundColor: Colors.black.withOpacity(0.5),
                onPressed: _takePicture,
                tooltip: 'Take Picture',
                child: Icon(Icons.camera_alt),
              ),
            ),
          ),
        ],
      ),
      floatingActionButton: _isPictureTaken
          ? null
          : FloatingActionButton(
              onPressed: _getImageFromGallery,
              tooltip: 'Pick Image from gallery',
              child: Icon(Icons.photo_library),
            ),
    );
  }

  Future<void> _takePicture() async {
    if (_controller == null || !_controller!.value.isInitialized || _isTakingPicture) {
      return;
    }
    _isTakingPicture = true;
    try {
      final XFile file = await _controller!.takePicture();
      if (file != null) {
        setState(() {
          _isPictureTaken = true;
        });
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => PictureScreen(
              imageFile: File(file.path),
              onRetake: () {
                Navigator.pop(context);
                setState(() {
                  _isPictureTaken = false;
                  _initializeCamera();
                });
              },
              onComplete: (extractedText) {
                _showProcessingSnackbar();
                Navigator.pop(context); // Navigate back to CameraScreen
                Navigator.pop(context); // Navigate back to HomeScreen
                _resetCamera();
              },
            ),
          ),
        );
      }
    } catch (e) {
      print('Error taking picture: $e');
    } finally {
      _isTakingPicture = false;
    }
  }
}
