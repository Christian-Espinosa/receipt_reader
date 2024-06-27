import numpy as np
import cv2
import matplotlib.pyplot as plt
import pytesseract
import re
import json

from pytesseract import Output

def plot_gray(image):
    plt.figure(figsize=(16,10))
    return plt.imshow(image, cmap='Greys_r')

def plot_rgb(image):
    plt.figure(figsize=(16,10))
    return plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def tesseract(image, save_path=None, feedback_path=None):
    d = pytesseract.image_to_data(image, output_type=Output.DICT)
    n_boxes = len(d['level'])
    boxes = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])    
        boxes = cv2.rectangle(boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    plot_rgb(boxes)

    extracted_text = pytesseract.image_to_string(image)

    if save_path:
        with open(save_path, 'w') as text_file:
            text_file.write(extracted_text)

    if feedback_path:
        with open(feedback_path, 'r') as file:
            feedback = json.load(file)
        
        feedback.append({
            'image': image_path,  # Path or identifier of the image
            'extracted_text': extracted_text,
            'correct_text_': ''  
        })
        
        with open(feedback_path, 'w') as file:
            json.dump(feedback, file)
