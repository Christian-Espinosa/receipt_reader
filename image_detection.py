import cropping_image as ci
import preprocessing_image as pi
import tesseract_ocr as tocr
import os

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(current_directory, 'server', 'test_data')
    save_dir = os.path.join(current_directory, 'server', 'results')
    
    #More processing
    #save_proc = os.path.join(current_directory, 'server', 'results_processing')
    
    save_tess= os.path.join(current_directory, 'server', 'results_tesseract')

    # Create the results directory if it does not exist
    os.makedirs(save_dir, exist_ok=True)

    # Iterate through all files in the test_data directory
    for file_name in os.listdir(data_dir):
        if file_name.lower().endswith(('.jpeg', '.jpg', '.png')):
            full_file_path = os.path.join(data_dir, file_name)

            save_file_name = f'result_{file_name}'
            save_file_path = os.path.join(save_dir, save_file_name)
            print(f'=============== Processing {file_name} ===============')
            cropped = ci.apply_processing(full_file_path, save_file_path)

            #save_file_path = os.path.join(save_proc, save_file_name)
            #enhanced = pi.enhance_text_regions(cropped, save_file_path)

            save_tesser_path = os.path.join(save_tess, save_file_name + '.txt')
            tocr.tesseract(cropped, save_tesser_path)

if __name__ == '__main__':
    main()