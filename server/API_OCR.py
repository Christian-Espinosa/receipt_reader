from flask import Flask, request, jsonify
from datetime import datetime
from PIL import Image
import os
import subprocess
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file:
        # Save the file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # Call the separate script to process the image
        result = subprocess.run(
            ['python', 'process_image.py', file_path], 
            capture_output=True, 
            text=True
        )

        if result.returncode != 0:
            return jsonify({'error': 'Error processing the image'}), 500
        
        response = json.loads(result.stdout)
        return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
