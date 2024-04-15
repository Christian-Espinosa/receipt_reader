import cv2
import pytesseract

#create a hello word
    # Load the image
    image = cv2.imread('path/to/your/image.jpg')

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