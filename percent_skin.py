### This function converts an image to HSV color space and detects skin pixels using a predefined skincolor range. ####

import os
import csv
import cv2
import numpy as np

def detect_skin_percentage(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define skin color range in HSV
    lower_skin = np.array([0, 48, 80], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # Create a mask for skin pixels
    skin_mask = cv2.inRange(hsv_image, lower_skin, upper_skin)
    
    # Calculate the number of skin pixels
    num_skin_pixels = np.sum(skin_mask > 0)
    
    # Calculate the total number of pixels
    total_pixels = image.shape[0] * image.shape[1]
    
    # Calculate the percentage of skin pixels
    skin_percentage = (num_skin_pixels / total_pixels) * 100
    
    return skin_percentage

# Example for one image:
# image_path = 'images/image_833.jpg'
# percentage = detect_skin_percentage(image_path)
# print(f"Percentage of skin in the image: {percentage:.2f}%")

# Folder path
image_folder = "images"
output_csv = "skin_percentages.csv"

# Collect results
results = []

# Loop over all image files
for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(image_folder, filename)
        try:
            percent = detect_skin_percentage(image_path)
            if percent is not None:
                results.append({
                    "image": filename,
                    "skin_percentage": round(percent, 2)
                })
            else:
                results.append({
                    "image": filename,
                    "skin_percentage": "unreadable"
                })
        except Exception as e:
            results.append({
                "image": filename,
                "skin_percentage": f"error: {e}"
            })

# Write to CSV
with open(output_csv, "w", newline="") as csvfile:
    fieldnames = ["image", "skin_percentage"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"Skin percentage results saved to {output_csv}")

### Does not do well detecting skin with greyscale images 
