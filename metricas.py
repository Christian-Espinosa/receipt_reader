import os
import Levenshtein
import numpy as np

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def calculate_metrics(original_text, ocr_text):
    levenshtein_distance = Levenshtein.distance(original_text, ocr_text)
    accuracy = 1 - (levenshtein_distance / max(len(original_text), len(ocr_text)))
    cer = levenshtein_distance / len(original_text)
    return levenshtein_distance, accuracy, cer

def main(original_file, ocr_files):
    results = []
    original_text = read_file(original_file)
    
    for ocr_file in ocr_files:
        ocr_text = read_file(ocr_file)
        
        levenshtein_distance, accuracy, cer = calculate_metrics(original_text, ocr_text)
        file_results = {
            'file': ocr_file,
            'levenshtein_distance': levenshtein_distance,
            'accuracy': accuracy,
            'cer': cer
        }
        
        results.append(file_results)
    
    return results

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    original_file = os.path.join(script_dir, 'original_text.txt')
    ocr_files = [
        os.path.join(script_dir, 'text_outputp_image_1_tesseract.txt'),
        os.path.join(script_dir, 'text_output_image_1_tesseract_non_processed.txt'),
        os.path.join(script_dir, 'text_output_image_1_googlecloud.txt'),
        os.path.join(script_dir, 'text_output_image_1_pentoprint.txt')
    ]

    ocr_model_names = ['Tesseract Processed', 'Tesseract non Processed', 'Google Cloud Vision', 'PentoPrint']
    
    results = main(original_file, ocr_files)
    for i, result in enumerate(results):
        print(f"Results for {ocr_model_names[i]}:")
        print(f"Levenshtein Distance: {result['levenshtein_distance']}")
        print(f"Accuracy: {result['accuracy']}")
        print(f"Character Error Rate (CER): {result['cer']}\n")
