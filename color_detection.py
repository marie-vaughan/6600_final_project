import os
import csv
from colorthief import ColorThief

##### Find top 5 colors in images and save into image_colors.csv #####

# Folder with images
image_folder = 'images'
output_csv = 'image_colors.csv'

# Store data for CSV
data = []

# Loop through all JPGs
for filename in os.listdir(image_folder):
    if filename.lower().endswith('.jpg'):
        image_path = os.path.join(image_folder, filename)
        try:
            ct = ColorThief(image_path)
            palette = ct.get_palette(color_count=5)
            data.append({
                'image': filename,
                'colors': palette
            })
        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")

# Save to CSV
with open(output_csv, mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['image', 'colors'])
    writer.writeheader()
    for row in data:
        # Convert RGB tuples to string for CSV
        row['colors'] = str(row['colors'])
        writer.writerow(row)

print(f"✅ Saved color data to {output_csv}")



##### Save RGB into major color categories #####

from colorsys import rgb_to_hsv
import pandas as pd
import ast

# Read the CSV and safely parse the string of RGB tuples
df = pd.read_csv("image_colors.csv")
df['colors'] = df['colors'].apply(ast.literal_eval)

def rgb_to_color_category(r, g, b):
    r_, g_, b_ = r / 255.0, g / 255.0, b / 255.0
    h, s, v = rgb_to_hsv(r_, g_, b_)
    h_deg = h * 360

    if s < 0.2:
        if v < 0.2:
            return 'black'
        elif v > 0.8:
            return 'white'
        else:
            return 'gray'

    if h_deg < 15 or h_deg >= 345:
        return 'red'
    elif h_deg < 45:
        return 'orange'
    elif h_deg < 65:
        return 'yellow'
    elif h_deg < 170:
        return 'green'
    elif h_deg < 260:
        return 'blue'
    elif h_deg < 290:
        return 'purple'
    elif h_deg < 330:
        return 'pink'
    else:
        return 'red'


# Apply to each row of RGB palettes
df['color_categories'] = df['colors'].apply(
    lambda palette: [rgb_to_color_category(*rgb) for rgb in palette]
)

# Get list of unique color categories across all rows
all_colors = sorted({color for row in df['color_categories'] for color in row})

# One-hot encode for each row
for color in all_colors:
    df[color] = df['color_categories'].apply(lambda cats: int(color in cats))

# df.to_csv("image_colors.csv", index=False)
# print("Saved updated CSV with one-hot encoded color columns.")

df.drop(columns=['color_categories', 'colors'], inplace=True)  
df.to_csv("image_colors_onehot.csv", index=False)
print("✅ Saved updated CSV with one-hot encoded color columns.")