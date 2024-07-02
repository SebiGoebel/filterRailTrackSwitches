from PIL import Image
import os

# Define the folder containing the .png files
folder_path = 'tempData_Austria_Salzburg_Villach'

# Create a new folder for .jpg files
jpg_folder = os.path.join(folder_path, 'jpg_files')
os.makedirs(jpg_folder, exist_ok=True)

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.png'):
        # Open the .png image
        img_path = os.path.join(folder_path, filename)
        img = Image.open(img_path)

        # Convert the image to RGB (required for .jpg)
        img = img.convert('RGB')

        # Save the image as .jpg in the new folder
        new_filename = os.path.splitext(filename)[0] + '.jpg'
        new_img_path = os.path.join(jpg_folder, new_filename)
        img.save(new_img_path, 'JPEG')

print("Conversion completed and files copied to the new folder!")
