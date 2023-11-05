import cv2
from PIL import Image
import math
# TODO: use this code! to make 1*1 cm square and paste image with border!
from PIL import Image, ImageDraw

inch = 2.54
reference_offset = 100 # pixels of offset to add the little square centimeter
file_folder = "files/"
input_file = "sweater-top.png"
desired_height = None
scale_factor = 2.17 #2.2497142857142856

# Get the dpi
image = Image.open(input_file)  # Replace 'your_image.jpg' with the path to your image file
# Get the image's DPI (Dots Per Inch)
dpi = image.info.get('dpi')[0]
# Get dots per cm
dpcm = dpi/inch

# Load the scanned A4 image
image = cv2.imread(input_file)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter the detected contours based on size or other criteria
# For example, you can keep the largest contour
largest_contour = max(contours, key=cv2.contourArea)

# Get the bounding box of the largest contour
x, y, w, h = cv2.boundingRect(largest_contour)

# Crop the original image to the detected region
cropped_image = image[y:y+h, x:x+w]

# Save the cropped image
cv2.imwrite(file_folder+"cropped_image.png", cropped_image)

# Get the original image dimensions
height, width, _ = cropped_image.shape

# Get current sizes in cm
height_cm = height/dpcm
width_cm = width/dpcm

if (desired_height):
    # Calculate scale factor
    scale_factor = desired_height/height_cm
    print(f"Scale factor: {scale_factor}")

# Calculate the new dimensions
new_height = int(height * scale_factor)
new_width = int(width * scale_factor)

# Resize the image to the new dimensions
resized_image = cv2.resize(cropped_image, (new_width, new_height))

# Save or display the resized image
cv2.imwrite(file_folder+"resized_image.png", resized_image)

# Load the large image
large_image = Image.open(file_folder+"resized_image.png")

# A4 paper dimensions in millimeters
a4_width_cm = 21
a4_height_cm = 29.7

# Calculate the size of one A4 section in pixels
a4_width_px_full = int((a4_width_cm / inch) * dpi)  
a4_height_px_full = int((a4_height_cm / inch) * dpi)  
a4_width_px = a4_width_px_full - 2*dpcm # take out 1 cm for the border
a4_height_px = a4_height_px_full - 2*dpcm # take out 1 cm for the border

# Calculate the number of A4-sized sections needed
num_sections_x = math.ceil(large_image.width / a4_width_px)
num_sections_y = math.ceil(large_image.height / a4_height_px)

# Create a new image with a white background
background_color = (255, 255, 255)  # RGB value for white
a4_image = Image.new("RGB", (a4_width_px_full, a4_height_px_full), background_color)

# Get the dimensions of the base image and the image to be pasted
base_width, base_height = a4_image.size

# Loop to split the large image into A4-sized sections
for row in range(num_sections_y):
    for col in range(num_sections_x):
        x1 = col * a4_width_px
        y1 = row * a4_height_px
        x2 = x1 + a4_width_px
        y2 = y1 + a4_height_px
        if (x2 > new_width):
            x2 = new_width
        if (y2 > new_height):
            y2 = new_height
        section = large_image.crop((x1, y1, x2, y2))
        # Paste this section on an intermediate white background
        white_background = Image.new("RGB", (round(a4_width_px), round(a4_height_px)), background_color)
        white_background.paste(section)
        paste_width, paste_height = white_background.size
        # Calculate the coordinates to paste the image in the center
        x_center = (base_width - paste_width) // 2
        y_center = (base_height - paste_height) // 2
        a4_image_copy = a4_image
        a4_image_copy.paste(white_background, (x_center, y_center))
        # Add a square centimeter box
        # Create a drawing context
        draw = ImageDraw.Draw(a4_image_copy)
        rectangle_color = (211, 211, 211)  # RGB value for light grey
        rectangle_coordinates = (reference_offset, reference_offset, reference_offset+dpcm, reference_offset+dpcm)
        draw.rectangle(rectangle_coordinates, fill=rectangle_color)
        # Save or process the A4-sized section here
        a4_image_copy.save(f"{file_folder}section_{row}_{col}.png")
