import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:http/http.dart' as http;

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: TakePictureScreen(),
    );
  }
}

class TakePictureScreen extends StatefulWidget {
  @override
  _TakePictureScreenState createState() => _TakePictureScreenState();
}

class _TakePictureScreenState extends State<TakePictureScreen> {
  CameraController? controller;
  List<CameraDescription>? cameras;
  String? imagePath;

  @override
  void initState() {
    super.initState();
    availableCameras().then((availableCameras) {
      cameras = availableCameras;
      if (cameras!.isNotEmpty) {
        controller = CameraController(cameras![0], ResolutionPreset.medium);
        controller!.initialize().then((_) {
          if (!mounted) {
            return;
          }
          setState(() {});
        });
      }
    });
  }

  @override
  void dispose() {
    controller?.dispose();
    super.dispose();
  }

  Future<void> takePicture() async {
    if (!controller!.value.isInitialized) {
      print('Error: select a camera first.');
      return;
    }
    final Directory extDir = await getApplicationDocumentsDirectory();
    final String dirPath = '${extDir.path}/Pictures/flutter_test';
    await Directory(dirPath).create(recursive: true);
    final String filePath = '$dirPath/${DateTime.now().millisecondsSinceEpoch}.jpg';

    if (controller!.value.isTakingPicture) {
      // A capture is already pending, do nothing.
      return;
    }

    try {
      await controller!.takePicture(filePath);
      setState(() {
        imagePath = filePath;
      });
      uploadImage(filePath);
    } catch (e) {
      print(e);
      return;
    }
  }

  Future<void> uploadImage(String filePath) async {
    var request = http.MultipartRequest('POST', Uri.parse('YOUR_SERVER_URL'));
    request.files.add(await http.MultipartFile.fromPath('picture', filePath));
    var res = await request.send();
    if (res.statusCode == 200) print('Upload successful');
    else print('Upload failed');
  }

  @override
  Widget build(BuildContext context) {
    if (controller == null || !controller!.value.isInitialized) {
      return const Center(child: CircularProgressIndicator());
    }
    return Scaffold(
      appBar: AppBar(title: Text('Take a Picture')),
      body: Column(
        children: <Widget>[
          Expanded(
            child: CameraPreview(controller!),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: FloatingActionButton(
              onPressed: takePicture,
              child: Icon(Icons.camera),
            ),
          )
        ],
      ),
    );
  }
}
