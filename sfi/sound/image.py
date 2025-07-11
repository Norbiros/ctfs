from PIL import Image
import numpy as np

def calculate_brightness(image_path, y_coordinate):
    img = Image.open(image_path)
    pixels = np.array(img)

    # Extract the row at y-coordinate
    row = pixels[y_coordinate]
    row2 = pixels[y_coordinate]

    # Loop over all pixels in the x-direction at y = 1400
    brightness_values = []
    for x in range(len(row)):
        # Convert pixel to grayscale (average of RGB channels)
        grayscale_value = np.mean(row[x][:3])  # Use [:3] to ignore alpha if present
        brightness_values.append(grayscale_value)
        print(f"Brightness at x={x}, y={y_coordinate}: {grayscale_value}")

# Example usage
image_path = 'spectrogram.png'
y_coordinate = 1382
calculate_brightness(image_path, y_coordinate)
