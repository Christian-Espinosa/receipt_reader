import json
import os

def extract_receipt_text(json_file_path, txt_save_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        if os.stat(json_file_path).st_size == 0:
            print(f"File is empty: {json_file_path}")
            return
        data = json.load(f)
    
    # Extract OCR text from the JSON data
    receipt_text = data['receipts'][0]['ocr_text']
        
    # Save the extracted text to the text file
    with open(txt_save_path, "w", encoding="utf-8") as f:
        f.write(receipt_text)
    
    print(f"Receipt text has been saved to {txt_save_path}")


def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(current_directory, 'response')
    save_proc = os.path.join(current_directory, 'response_txt')

    print(f"Reading JSON files from {data_dir}")
    # Iterate through all files in the test_data directory
    for file_name in os.listdir(data_dir):
        if file_name.lower().endswith('.json'):
            full_file_path = os.path.join(data_dir, file_name)

            save_file_name = f'resp_txt__{file_name}'.rstrip(".json") + '.txt'
            save_txt_path = os.path.join(save_proc, save_file_name)
            print(f'=============== OCR {file_name} ===============')
            extract_receipt_text(full_file_path, save_txt_path)

if __name__ == '__main__':
    main()