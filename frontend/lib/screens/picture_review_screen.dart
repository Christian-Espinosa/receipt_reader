// lib/screens/picture_review_screen.dart

import 'dart:io';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as path;
import '../services/ocr_service.dart';
import '../services/database_service.dart';

class PictureScreen extends StatelessWidget {
  final File imageFile;
  final VoidCallback onRetake;
  final Function(String) onComplete;

  PictureScreen({required this.imageFile, required this.onRetake, required this.onComplete});

  final OcrService _ocrService = OcrService();
  final DatabaseService _databaseService = DatabaseService();

  Future<void> receiveImage(BuildContext context) async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final String newPath = path.join(directory.path, 'img_receipts');
      final newDirectory = Directory(newPath);

      if (!await newDirectory.exists()) {
        await newDirectory.create();
        print('Directory created at $newPath');
      }

      final String newImagePath = path.join(newPath, path.basename(imageFile.path));
      final savedImage = await imageFile.copy(newImagePath);

      print('Image saved to $newImagePath');

      // Apply OCR in the background and save to database
      /*final Map<String, double> items = await _ocrService.applyOCR(savedImage);
      for (var item in items.entries) {
        await _databaseService.insertExpense(item.key, item.value);
      }

      final extractedText = items.entries.map((e) => '${e.key}: \$${e.value}').join('\n');
      onComplete(extractedText);*/
      final Map<String, dynamic> json = await _ocrService.applyOCR(savedImage);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Processing data...'),
          duration: Duration(seconds: 2),
        ),
      );

      // Ensure sequential navigation
      await Navigator.maybePop(context);
      await Navigator.maybePop(context);
    } catch (e) {
      print('Failed to save image: $e');
    }
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
              await receiveImage(context);
            },
            tooltip: 'Accept Picture',
            child: Icon(Icons.check),
          ),
        ],
      ),
    );
  }
}
