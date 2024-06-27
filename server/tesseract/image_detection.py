import cropping_image as ci
import tesseract_ocr as tocr
import os

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.abspath(os.path.join(current_directory, os.pardir))

    data_dir = os.path.join(server_path, 'input_data')
    save_proc = os.path.join(current_directory, 'results')
    save_tess= os.path.join(current_directory, 'results_tesseract')


    # Iterate through all files in the test_data directory
    for file_name in os.listdir(data_dir):
        if file_name.lower().endswith(('.jpeg', '.jpg', '.png')):
            full_file_path = os.path.join(data_dir, file_name)

            save_file_name = f'result_{file_name}'
            save_file_path = os.path.join(save_proc, save_file_name)
            print(f'=============== Processing {file_name} ===============')
            cropped = ci.apply_processing(full_file_path, save_file_path)

            save_file_name = f'result_{file_name}'.rstrip(".jpeg") + '.txt'
            save_file_path = os.path.join(save_tess, save_file_name)
            print(f'=============== OCR {file_name} ===============')
            tocr.tesseract(cropped, save_file_path)

            

if __name__ == '__main__':
    main()