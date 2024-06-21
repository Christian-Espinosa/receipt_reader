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


# approximate the contour by a more primitive polygon shape
def approximate_contour(contour):
    peri = cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, 0.032 * peri, True)

def get_receipt_contour(contours):    
    for c in contours:
        approx = approximate_contour(c)
        if len(approx) == 4:
            return approx
    print("No rectangular contour found.")
    return None
        
def contour_to_rect(contour, resize_ratio):
    pts = contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect / resize_ratio

def wrap_perspective(img, rect):
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(img, M, (maxWidth, maxHeight))

def bw_scanner(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    T = threshold_local(gray, 21, offset=5, method="gaussian")
    return (gray > T).astype("uint8") * 255


def apply_processing(path_image, save_path):
    
    image = cv2.imread(path_image)

    resize_ratio = 500 / image.shape[0]
    original = image.copy()
    image = opencv_resize(image, resize_ratio)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilated = cv2.dilate(blurred, rectKernel)

    edged = cv2.Canny(dilated, 100, 200, apertureSize=3)

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    image_with_contours = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 3)

    largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    image_with_largest_contours = cv2.drawContours(image.copy(), largest_contours, -1, (0, 255, 0), 3)

    receipt_contour = get_receipt_contour(largest_contours)
    if receipt_contour is None:
        print("No rectangular contour detected.")
    else:
        print("Receipt contour detected correctly :D")

    image_with_receipt_contour = cv2.drawContours(image.copy(), [receipt_contour], -1, (0, 255, 0), 2)

    scanned = wrap_perspective(original.copy(), contour_to_rect(receipt_contour, resize_ratio))

    result = bw_scanner(scanned)

    output = Image.fromarray(result)
    output.save(save_path)

    fig, axs = plt.subplots(3, 3, figsize=(20, 20))
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

    axs[6].set_title('Largest Contours')
    plot_rgb(image_with_largest_contours, axs[6])

    axs[7].set_title('Receipt Contour')
    plot_rgb(image_with_receipt_contour, axs[7])

    axs[8].set_title('Scanned BW Image')
    plot_gray(result, axs[8])

    for ax in axs:
        ax.axis('off')

    plt.tight_layout()
    plt.show()

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(current_directory, 'server', 'test_data')
    save_dir = os.path.join(current_directory, 'server', 'results')

    # Create the results directory if it does not exist
    os.makedirs(save_dir, exist_ok=True)

    # Iterate through all files in the test_data directory
    for file_name in os.listdir(data_dir):
        if file_name.lower().endswith(('.jpeg', '.jpg', '.png')):
            full_file_path = os.path.join(data_dir, file_name)

            save_file_name = f'result_{file_name}'
            save_file_path = os.path.join(save_dir, save_file_name)

            apply_processing(full_file_path, save_file_path)

        


if __name__ == '__main__':
    main()
