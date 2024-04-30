import cv2
import pytesseract
import paths
from pdf2image import convert_from_path
import numpy as np
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileReader


def read_pdf(pdf_file_path):
    try:
        with open(pdf_file_path, "rb") as file:
            reader = PdfFileReader(file)
            num_pages = reader.numPages
            print(f"Number of pages: {num_pages}")

            for page_num in range(num_pages):
                page = reader.getPage(page_num)
                text = page.extractText()
                print(f"Page {page_num + 1}:")
                print(text)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        
def read_pdf_files(path):
    pdf_files = []

    with open(path, 'w') as file:
        for line in file:
            pdf_files.append(line.strip())


    return pdf_files

def read_pdf_pages(pdf_file):
    pdf_images = []
    pages = convert_from_path(pdf_file)
    for page in pages:
        image = np.array(page)
        pdf_images.append(image)
    return pdf_images
from pdf2image import convert_from_path

def pdf_to_image(pdf_file_path, output_folder_path):
    try:
        # Convert PDF to list of PIL.Image objects
        images = convert_from_path(pdf_file_path)

        # Save each image as a PNG file in the output folder
        for i, image in enumerate(images):
            image_path = f"{output_folder_path}/page_{i+1}.png"
            image.save(image_path, "PNG")
        print("PDF converted to images successfully.")
    except Exception as e:
        print(f"Error converting PDF to images: {e}")


def main():

    read_pdf(paths.img_path)
    l_pdfs = read_pdf_files(paths.img_path)
    l_imgs = read_pdf_pages(l_pdfs)

    # Create a figure to display the images
    fig, axes = plt.subplots(nrows=len(l_imgs), ncols=1)

    # Iterate over the images and display them in the figure
    for i, img in enumerate(l_imgs):
        axes[i].imshow(img)
        axes[i].axis('off')

    # Show the figure
    plt.show()
    

    # Crop the image (replace the values with your desired coordinates)
    cropped_image = image[y_start:y_end, x_start:x_end]

    # Convert the cropped image to grayscale
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # Apply Otsu's thresholding to binarize the image
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Apply OCR using pytesseract
    text = pytesseract.image_to_string(binary_image)

    # Print the extracted text
    print(text)
    
if __name__ == "__main__":
    main()