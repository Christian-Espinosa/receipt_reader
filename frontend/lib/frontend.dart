import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:google_ml_kit/google_ml_kit.dart';
import 'package:http/http.dart' as http;
import 'dart:io';

//void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: CameraScreen(),
    );
  }
}

class CameraScreen extends StatefulWidget {
  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  late CameraController controller;
  String recognizedText = "";

  @override
  void initState() {
    super.initState();
    initializeCamera();
  }

  Future<void> initializeCamera() async {
    final cameras = await availableCameras();
    final firstCamera = cameras.first;

    controller = CameraController(
      firstCamera,
      ResolutionPreset.medium,
    );

    controller.initialize().then((_) {
      if (!mounted) {
        return;
      }
      setState(() {});
    });
  }

  Future<void> recognizeTextFromImage(CameraImage image) async {
    final inputImage = InputImage.fromBytes(
      bytes: image.planes[0].bytes,
      inputImageData: InputImageData(
        imageRotation: InputImageRotation.rotation0,
      ),
        size: Size(image.width.toDouble(), image.height.toDouble()),
      ),
        inputImageFormat: InputImageFormat.unknown,
      ),
        size: Size(image.width.toDouble(), image.height.toDouble()),
        imageRotation: ImageRotation.Rotation0,
      ),
    );

    final textDetector = GoogleMlKit.vision.textDetector();
    final RecognisedText recognisedText = await textDetector.processImage(inputImage);

    setState(() {
      recognizedText = recognisedText.text;
    });
  }

  Future<void> sendToServer(String text, File image) async {
    var request = http.MultipartRequest('POST', Uri.parse('http://your-server.com/upload'));
    request.fields['text'] = text;
    request.files.add(await http.MultipartFile.fromPath('image', image.path));
    var response = await request.send();
    if (response.statusCode == 200) print('Uploaded!');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('OCR App')),
      body: Column(
        children: <Widget>[
          Text('Recognized Text: $recognizedText'),
          ElevatedButton(
            onPressed: () async {
              await controller.stopImageStream();
              // sendToServer(recognizedText, capturedImage);
            },
            child: Text('Stop OCR'),
          ),
            onPressed: () async {
              await controller.startImageStream((image) => recognizeTextFromImage(image));
            },
            child: Text('Start OCR'),
          ),
          RaisedButton(
            onPressed: () async {
              await controller.stopImageStream();
              // sendToServer(recognizedText, capturedImage);
            },
            child: Text('Stop OCR'),
          ),
        ],
      ),
    );
  }
}