import os
import Levenshtein
import numpy as np
import pandas as pd

def read_file(file_path):
    with open(file_path, "r", encoding="latin-1") as file:
        return file.read()

def calculate_metrics(original_text, ocr_text):
    levenshtein_distance = Levenshtein.distance(original_text, ocr_text)
    accuracy = 1 - (levenshtein_distance / max(len(original_text), len(ocr_text)))
    cer = levenshtein_distance / len(original_text)
    return levenshtein_distance, accuracy, cer

def execute(folder1_files, folder2_files):
    results = []
    
    for file1, file2 in zip(folder1_files, folder2_files):
        text1 = read_file(file1)
        text2 = read_file(file2)
        
        levenshtein_distance, accuracy, cer = calculate_metrics(text1, text2)
        file_results = {
            'file1': os.path.basename(file1),
            'file2': os.path.basename(file2),
            'levenshtein_distance': levenshtein_distance,
            'accuracy': accuracy,
            'cer': cer
        }
        
        results.append(file_results)
    
    return results

def save_to_spreadsheet(results, save_path):
    df = pd.DataFrame(results)
    df.to_excel(save_path, index=False)
    print(f"Metrics have been saved to {save_path}")

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    folder1 = os.path.join(current_directory, 'tesseract', 'results_tesseract')
    folder2 = os.path.join(current_directory, 'asprice_api', 'response_txt')
        
    folder1_files = sorted([os.path.join(folder1, file) for file in os.listdir(folder1) if file.endswith('.txt')])
    folder2_files = sorted([os.path.join(folder2, file) for file in os.listdir(folder2) if file.endswith('.txt')])
    
    # Ensure both folders have at least one file
    if not folder1_files or not folder2_files:
        print("One of the folders is empty. Exiting.")
        exit(1)
    
    # Compare files
    results = execute(folder1_files, folder2_files)
    
    save_path = os.path.join(current_directory, 'ocr_metrics.xlsx')
    save_to_spreadsheet(results, save_path)
    
    print("Comparison ended successfully!")
