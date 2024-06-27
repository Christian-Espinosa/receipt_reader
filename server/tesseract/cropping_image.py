import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.filters import threshold_local
from PIL import Image

def opencv_resize(image, ratio):
    width = int(image.shape[1] * ratio)
    height = int(image.shape[0] * ratio)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def plot_rgb(image, ax):
    ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def plot_gray(image, ax):
    ax.imshow(image, cmap='Greys_r')


#CONTOURS
def approximate_contour(contour):
    peri = cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, 0.032 * peri, True)

def get_largest_contour_by_area(contours):
    if not contours:
        return None
    # Find the contour with the largest area
    largest_contour = max(contours, key=cv2.contourArea)
    return largest_contour

def get_largest_contour_by_perimeter(contours):
    if not contours:
        return None
    # Find the contour with the largest perimeter
    largest_contour = max(contours, key=lambda x: cv2.arcLength(x, True))
    return largest_contour

def get_receipt_contour(contours):
    largest_contour = get_largest_contour_by_perimeter(contours)
    if largest_contour is not None:
        print(f'Largest contour length: {len(largest_contour)}')
        return approximate_contour(largest_contour)
    print("No suitable contour found.")
    return None

def contour_to_rect(image, contour, aspect_ratio_threshold=0.5):
    if contour is not None and len(contour) > 0:
        # Find the extreme points of the contour
        x_min = np.min(contour[:, 0, 0])
        x_max = np.max(contour[:, 0, 0])
        y_min = np.min(contour[:, 0, 1])
        y_max = np.max(contour[:, 0, 1])
        
        # Calculate the width and height of the bounding rectangle
        width = x_max - x_min
        height = y_max - y_min
        
        # Get the dimensions and aspect ratio of the original image
        original_height, original_width = image.shape[:2]
        original_aspect_ratio = original_width / original_height
        
        # Calculate the aspect ratio of the bounding rectangle
        bounding_aspect_ratio = width / height
        
        print(f'Original aspect ratio: {original_aspect_ratio}, Bounding aspect ratio: {bounding_aspect_ratio}')
        
        # Check if the aspect ratio difference is within the threshold
        if (abs(bounding_aspect_ratio - original_aspect_ratio) / original_aspect_ratio) > aspect_ratio_threshold:
            print("Bounding rectangle aspect ratio is too different, returning the original image.")
            return None
        
        # Ensure the coordinates are within the image boundaries
        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(original_width, x_max)
        y_max = min(original_height, y_max)
        
        print(f'Adjusted bounding rectangle: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}')
        
        # Create the bounding rectangle contours in the correct format for OpenCV
        bounding_rect_contour = np.array([
            [x_min, y_min],
            [x_max, y_min],
            [x_max, y_max],
            [x_min, y_max]
        ], dtype=np.int32).reshape(-1, 1, 2)
        
        print(f'Bounding rectangle contour: {bounding_rect_contour}')
        
        return bounding_rect_contour
    else:
        print("Invalid contour received.")
        # Return None if the contour is invalid
        return None



def wrap_perspective(img, rect):
    # unpack rectangle points: top left, top right, bottom right, bottom left
    (tl, tr, br, bl) = rect
    # compute the width of the new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    # compute the height of the new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    # take the maximum of the width and height values to reach
    # our final dimensions
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))
    # destination points which will be used to map the screen to a "scanned" view
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    # calculate the perspective transform matrix
    M = cv2.getPerspectiveTransform(rect, dst)
    # warp the perspective to grab the screen
    return cv2.warpPerspective(img, M, (maxWidth, maxHeight))

def bw_scanner(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    T = threshold_local(gray, 21, offset=5, method="gaussian")
    return (gray > T).astype("uint8") * 255

def clean_image(image):
    # Convert to grayscale and apply GaussianBlur
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding to get binary image
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    
    # Invert the binary image
    binary = cv2.bitwise_not(binary)
    
    # Use morphology to clean up the noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # Invert back to original form
    cleaned = cv2.bitwise_not(cleaned)

    return cleaned



def apply_processing(path_image, save_path):
    image = cv2.imread(path_image)

    resize_ratio = 500 / image.shape[0]
    original = image.copy()
    image = opencv_resize(image, resize_ratio)

    image = original
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilated = cv2.dilate(blurred, rectKernel)
    edged = cv2.Canny(dilated, 50, 200, apertureSize=3)
    
    # All contours
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_with_contours = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 4)

    # Get the largest contour
    receipt_contour = get_receipt_contour(contours)
    image_with_contour = cv2.drawContours(image.copy(), [receipt_contour], -1, (0, 255, 0), 4)
    
    # Crop the receipt
    bounding_rect_contour = contour_to_rect(original, receipt_contour)
    if bounding_rect_contour is not None:
        image_with_contour_and_rect = cv2.drawContours(image.copy(), [receipt_contour], -1, (0, 255, 0), 4)
        image_with_contour_and_rect = cv2.drawContours(image_with_contour_and_rect, [bounding_rect_contour], -1, (255, 0, 255), 4)
        # Using cv2.boundingRect to get the correct coordinates
        x, y, w, h = cv2.boundingRect(receipt_contour)
        scanned = image[y:y+h, x:x+w]
    
    else:
        image_with_contour_and_rect = image.copy()
        scanned = image.copy()



    result = bw_scanner(scanned)

    #SAVE
    output = Image.fromarray(result)
    output.save(save_path)
    
    #PLOT================================================================================================
    fig, axs = plt.subplots(2, 5, figsize=(20, 10))  # Changed to 2x5 grid
    figManager = plt.get_current_fig_manager()
    figManager.window.state('zoomed')
    axs = axs.flatten()

    axs[0].set_title('Original Image')
    plot_rgb(original, axs[0])

    axs[1].set_title('Grayscale Image')
    plot_gray(gray, axs[1])

    axs[2].set_title('Blurred Image')
    plot_gray(blurred, axs[2])

    axs[3].set_title('Dilated Image')
    plot_gray(dilated, axs[3])

    axs[4].set_title('Edged Image')
    plot_gray(edged, axs[4])

    axs[5].set_title('All Contours')
    plot_rgb(image_with_contours, axs[5])

    axs[6].set_title('Selected Contour')
    plot_rgb(image_with_contour, axs[6])

    axs[7].set_title('Cropped Image')
    plot_gray(image_with_contour_and_rect, axs[7])

    axs[8].set_title('Cleaned Image')
    plot_gray(result, axs[8])

    for ax in axs:
        ax.axis('off')

    plt.tight_layout()
    plt.show()

    return result

