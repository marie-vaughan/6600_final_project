##### Classifying images' nudity using a pre-trained model ####
##### From https://github.com/notAI-tech/NudeNet #####


# all_labels = [
#     "FEMALE_GENITALIA_COVERED",
#     "FACE_FEMALE",
#     "BUTTOCKS_EXPOSED",
#     "FEMALE_BREAST_EXPOSED",
#     "FEMALE_GENITALIA_EXPOSED",
#     "MALE_BREAST_EXPOSED",
#     "ANUS_EXPOSED",
#     "FEET_EXPOSED",
#     "BELLY_COVERED",
#     "FEET_COVERED",
#     "ARMPITS_COVERED",
#     "ARMPITS_EXPOSED",
#     "FACE_MALE",
#     "BELLY_EXPOSED",
#     "MALE_GENITALIA_EXPOSED",
#     "ANUS_COVERED",
#     "FEMALE_BREAST_COVERED",
#     "BUTTOCKS_COVERED",
# ] 



## Example with one image
from nudenet import NudeDetector
detector = NudeDetector()
# the 320n model included with the package will be used

# images with nudity:
# 1433
detections = detector.detect('images/image_811.jpg') # Returns list of detections
print(detections)



## Looping through all the images

import os
import csv
from nudenet import NudeDetector

# Initialize the detector
detector = NudeDetector()

# Path to your images folder
image_folder = "images"
output_csv = "nudity_detection_results.csv"

# Results list
results = []

# Loop through each image
for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(image_folder, filename)
        try:
            detections = detector.detect(image_path)
            
            # If anything is detected
            if detections:
                for det in detections:
                    label = det.get("class", "unknown")
                    score = round(det.get("score", 0.0), 4)
                    box = det.get("box")

                    results.append({
                        "image": filename,
                        "label": label,
                        "confidence": score,
                        "box": box
                    })
                else:
                    results.append({
                        "image": filename,
                        "label": "none_detected",
                        "confidence": 0,
                        "box": None
                    })
        except Exception as e:
            results.append({
                "image": filename,
                "label": "error",
                "confidence": "N/A",
                "box": str(e)
            })

# Write results to CSV
with open(output_csv, "w", newline="") as csvfile:
    fieldnames = ["image", "label", "confidence", "box"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Detection results saved to: {output_csv}")






