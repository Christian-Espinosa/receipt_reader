import 'dart:io';
import 'package:flutter/material.dart';
import '../services/image_service.dart';
import '../services/ocr_service.dart';
import '../services/database_service.dart';

class PictureScreen extends StatelessWidget {
  final File imageFile;
  final VoidCallback onRetake;
  final Function(String) onComplete;

  PictureScreen({required this.imageFile, required this.onRetake, required this.onComplete});

  final ImageService _imageService = ImageService();
  final OcrService _ocrService = OcrService();
  final DatabaseService _databaseService = DatabaseService();

  Future<String> receiveImage() async {
    try {
      final savedImage = await _imageService.saveImage(imageFile);
      await _imageService.sendImageToServer(savedImage);
      final items = await _ocrService.applyOCR(savedImage);

      for (var item in items.entries) {
        await _databaseService.insertExpense(item.key, item.value);
      }

      return items.entries.map((e) => '${e.key}: \$${e.value}').join('\n');
    } catch (e) {
      print('Failed to process image: $e');
      return 'Failed to process image';
    }
  }

  void _showExtractedText(BuildContext context, String text) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Extracted Text'),
          content: SingleChildScrollView(
            child: Text(text),
          ),
          actions: <Widget>[
            TextButton(
              child: Text('OK'),
              onPressed: () {
                Navigator.of(context).pop();
                onComplete(text); // Call onComplete callback
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Review Picture'),
      ),
      body: Image.file(imageFile),
      floatingActionButton: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          FloatingActionButton(
            onPressed: onRetake,
            tooltip: 'Retake Picture',
            child: Icon(Icons.close),
          ),
          FloatingActionButton(
            onPressed: () async {
              String extractedText = await receiveImage();
              _showExtractedText(context, extractedText);
            },
            tooltip: 'Accept Picture',
            child: Icon(Icons.check),
          ),
        ],
      ),
    );
  }
}
