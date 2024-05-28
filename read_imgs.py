import os
import cv2
import paths
from pdf2image import convert_from_path
import numpy as np
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader

import pytesseract
from PIL import Image

def pdfs_to_images(pdf_folder_path, output_folder_path):
    try:
        for filename in os.listdir(pdf_folder_path):
            if filename.endswith(".pdf"):
                pdf_file_path = os.path.join(pdf_folder_path, filename)
                images = convert_from_path(pdf_file_path, dpi=500, poppler_path=paths.poppler_path)

                for i, image in enumerate(images):
                    image_path = f"{output_folder_path}/{filename}_page_{i+1}.png"
                    image.save(image_path, "PNG")

        print("PDFs converted to images successfully.")
    except Exception as e:
        print(f"Error converting PDFs to images: {e}")


def show_images_from_folder(folder_path):
    try:
        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image_path = os.path.join(folder_path, filename)
                image = cv2.imread(image_path)
                images.append(image)

        if len(images) == 0:
            print("No images found in the folder.")
            return

        fig = plt.figure(figsize=(10, 10))
        rows = int(np.ceil(len(images) / 3))
        columns = min(len(images), 3)

        for i, image in enumerate(images):
            ax = fig.add_subplot(rows, columns, i+1)
            ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            ax.axis('off')

        plt.show()

    except Exception as e:
        print(f"Error reading images from folder: {e}")

def load_images_from_folder(folder_path):
    try:
        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image_path = os.path.join(folder_path, filename)
                image = cv2.imread(image_path)
                images.append(image)

        if len(images) == 0:
            print("No images found in the folder.")
            return

        return images

    except Exception as e:
        print(f"Error reading images from folder: {e}")
    
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)

def thin_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

def process_images(images):
    processed_images = []
    for image in images:
        gray_image = grayscale(image)
        thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
        
        d_noised = noise_removal(im_bw)
        thin = thin_font(d_noised)
        thick = thick_font(thin)

        processed_images.append(thick)

    return processed_images

def show_images(images):
    fig = plt.figure(figsize=(10, 10))
    rows = int(np.ceil(len(images) / 3))
    columns = min(len(images), 3)

    for i, image in enumerate(images):
        ax = fig.add_subplot(rows, columns, i+1)
        ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        ax.axis('off')

    plt.show()

def show_one_image(image):
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

def save_images(images, output_folder_path):
    try:
        for i, image in enumerate(images):
            image_path = f"{output_folder_path}\\p_image_{i+1}.png"
            os.makedirs(output_folder_path, exist_ok=True)  # Create the output folder if it doesn't exist
            cv2.imwrite(image_path, np.array(image))

        print("Processed images saved successfully.")
    except Exception as e:
        print(f"Error saving processed images: {e}")
        
def main():
    while True:
        print("Menu:")
        print("1. Convert PDFs to images")
        print("2. Process images")
        print("3. Perform OCR on images")
        print("e. Exit")

        option = input("Select an option: ")

        if option == "1":
            pdfs_to_images(paths.img_path, paths.output_img_path)
            show_images_from_folder(paths.output_img_path)
        elif option == "2":
            # Process images
            images = load_images_from_folder(paths.output_img_path)
            processed_images = process_images(images)
            save_images(processed_images, paths.processed_img_path)
            show_one_image(processed_images[0])
        elif option == "3":
            print(pytesseract.get_tesseract_version())
            image = Image.open(paths.processed_img_path + "\\p_image_1.png")
            text = pytesseract.image_to_string(image)
            print(text)
            with open(paths.text_path + "p_image_1.txt", "w", encoding='utf-8') as file:
                file.write(text)
        elif option == "e":
            break
        else:
            print("Opción Invalida. Intente de nuevo.")

if __name__ == "__main__":
    main()