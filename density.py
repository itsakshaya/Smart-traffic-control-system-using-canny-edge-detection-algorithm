import numpy as np

def calculate_density(edge_image: np.ndarray):
    total_pixels = edge_image.size
    edge_pixels = np.count_nonzero(edge_image)

    density = (edge_pixels / total_pixels) * 100

    # adjust for better realism
    density = density * 2.5
    density = min(density, 100)

    return round(density, 2)