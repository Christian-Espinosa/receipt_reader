import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as path;
import 'package:http/http.dart' as http;

class ImageService {
  Future<File> saveImage(File imageFile) async {
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
      return savedImage;
    } catch (e) {
      print('Failed to save image: $e');
      rethrow;
    }
  }

  Future<void> sendImageToServer(File imageFile) async {
    try {
      final uri = Uri.parse('https://your-server.com/upload');
      final request = http.MultipartRequest('POST', uri);
      request.files.add(await http.MultipartFile.fromPath('picture', imageFile.path));

      final response = await request.send();
      if (response.statusCode == 200) {
        print('Upload successful');
      } else {
        print('Upload failed with status code: ${response.statusCode}');
      }
    } catch (e) {
      print('Failed to send image to server: $e');
      rethrow;
    }
  }
}
