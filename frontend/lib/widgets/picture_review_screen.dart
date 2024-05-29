import 'dart:io';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as path;

class PictureScreen extends StatelessWidget {
  final File imageFile;
  final VoidCallback onRetake;

  PictureScreen({required this.imageFile, required this.onRetake});

  Future<void> _saveImage() async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final String newPath = path.join(directory.path, 'storage');
      final newDirectory = Directory(newPath);

      if (!await newDirectory.exists()) {
        await newDirectory.create();
      }

      final String newImagePath = path.join(newPath, path.basename(imageFile.path));
      await imageFile.copy(newImagePath);
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
            onPressed: _saveImage,
            tooltip: 'Accept Picture',
            child: Icon(Icons.check),
          ),
        ],
      ),
    );
  }
}