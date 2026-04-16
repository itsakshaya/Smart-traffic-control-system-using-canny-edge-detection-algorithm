import cv2
import numpy as np

def detect_edges(blurred_image: np.ndarray, low: int, high: int):
    edges = cv2.Canny(blurred_image, low, high)
    return edges