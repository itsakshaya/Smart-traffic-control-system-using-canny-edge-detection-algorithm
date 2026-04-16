import cv2
import numpy as np

def preprocess_image(image: np.ndarray):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    return gray, blurred