import cv2
import pytesseract
import paths
from pdf2image import convert_from_path
import numpy as np
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileReader

def read_pdf_files(path):
    pdf_files = []

    with open(path, 'rb') as file:
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

def main():

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