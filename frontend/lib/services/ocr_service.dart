import 'dart:io';
import 'package:google_mlkit_text_recognition/google_mlkit_text_recognition.dart';

class OcrService {
  Future<Map<String, double>> applyOCR(File imageFile) async {
    final inputImage = InputImage.fromFile(imageFile);
    final textRecognizer = TextRecognizer(script: TextRecognitionScript.latin);
    final recognizedText = await textRecognizer.processImage(inputImage);

    Map<String, double> items = {};

    for (TextBlock block in recognizedText.blocks) {
      for (TextLine line in block.lines) {
        // Simple regex to match item and price patterns
        final regex = RegExp(r'([A-Za-z\s]+)\s+(\d+\.\d{2})');
        final match = regex.firstMatch(line.text);
        if (match != null) {
          final itemName = match.group(1)!.trim();
          final itemPrice = double.parse(match.group(2)!);
          items[itemName] = itemPrice;
        }
      }
    }

    textRecognizer.close();
    return items;
  }
}
