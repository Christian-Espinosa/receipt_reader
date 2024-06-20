import 'dart:io';
import 'dart:convert';
import 'package:path/path.dart' as p; // Add this import
import 'package:http/http.dart' as http;

class OcrService {
  Future<Map<String, dynamic>> applyOCR(File imageFile) async {
    final String receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt';

    final request = http.MultipartRequest('POST', Uri.parse(receiptOcrEndpoint))
      ..fields['client_id'] = 'TEST' // Use 'TEST' for testing purpose
      ..fields['recognizer'] = 'auto' // can be 'US', 'CA', 'JP', 'SG' or 'auto'
      ..fields['ref_no'] = 'ocr_flutter_123' // optional caller provided ref code
      ..files.add(await http.MultipartFile.fromPath('file', imageFile.path));

    try {
      final response = await request.send();
      if (response.statusCode == 200) {
        final responseBody = await response.stream.bytesToString();
        final Map<String, dynamic> jsonResponse = json.decode(responseBody);

        print(jsonResponse); // Print the JSON response

        // Store the JSON response locally in the project directory
        await _storeJsonResponse(jsonResponse);

        return jsonResponse; // Return the JSON response
      } else {
        print('Failed to process receipt. Status code: ${response.statusCode}');
        return {};
      }
    } catch (e) {
      print('Error occurred: $e');
      return {};
    }
  }

  Future<void> _storeJsonResponse(Map<String, dynamic> jsonResponse) async {
    // Get the current directory of the script
    final directory = Directory.current;
    final String filePath = p.join(directory.path, 'data', 'receipt_response.json');
    final File file = File(filePath);

    await file.writeAsString(json.encode(jsonResponse), mode: FileMode.write);
    print('JSON response stored at: $filePath');
  }
}


