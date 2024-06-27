import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_local
from PIL import Image

def enhance_text_regions(image, save_path=None):
    orig = image.copy()
    
    # Convert to grayscale
    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding to create a binary image
    T = threshold_local(blurred, 21, offset=10, method="gaussian")
    bw_image = (blurred > T).astype("uint8") * 255
    
    # Apply morphological transformations to remove small noise
    kernel = np.ones((2, 2), np.uint8)
    bw_image = cv2.morphologyEx(bw_image, cv2.MORPH_OPEN, kernel)
    bw_image = cv2.morphologyEx(bw_image, cv2.MORPH_CLOSE, kernel)
    
    # Further noise reduction using median blur
    bw_image = cv2.medianBlur(bw_image, 3)
    
    # Convert back to BGR to save as an image
    cleaned_image = cv2.cvtColor(bw_image, cv2.COLOR_GRAY2BGR)
    
    # Save the cleaned image
    output = Image.fromarray(cleaned_image)
    if save_path:
        output.save(save_path)
    
    # Display the cleaned image
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(cleaned_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
    
    return cleaned_image

