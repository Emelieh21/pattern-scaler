import cv2
from PIL import Image
import math
# TODO: use this code! to make 1*1 cm square and paste image with border!
from PIL import Image
from utils.functions import add_lines, add_reference_box, add_page_letters_left, add_page_letters_right, add_page_letters_top, add_page_letters_bottom, set_line_width, set_scale_factors
import string
# TODO: refactor
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

inch = 2.54
file_folder = "files/"
input_file = "painting.png"
file_name = input_file.replace(".png", "")
desired_height = 38
desired_width = 48
scale_factor_height = None
scale_factor_width = None
line_width = 2

# TODO: this does not work yet, had issues with poppler, but did not feel like messing around with brew
## Convert pdf of scan to png
# from pdf2image import convert_from_path
#print("Converting pdf to png...")
#img_from_pdf = convert_from_path("painting-scan.pdf", poppler_path=r"/usr/local/opt/poppler")
#img_from_pdf.save(input_file, "PNG")

# Get the dpi
image = Image.open(input_file)  # Replace 'your_image.jpg' with the path to your image file
# Get the image's DPI (Dots Per Inch)
dpi = image.info.get('dpi')
if (dpi is None):
    # Use a default
    dpi = 72
else:
    dpi = dpi[0]

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
print(f"Current size of image: {width_cm} by {height_cm} cm")

scale_factor_height, scale_factor_width = set_scale_factors(height_cm, width_cm, 
                                                            desired_height, 
                                                            desired_width, 
                                                            scale_factor_height, 
                                                            scale_factor_width)

# Calculate the new dimensions
new_height = int(height * scale_factor_height)
new_width = int(width * scale_factor_width)
print(f"New size of image: {new_width/dpcm} by {new_height/dpcm} cm")

# Resize the image to the new dimensions
resized_image = cv2.resize(cropped_image, (new_width, new_height))

if (line_width is not None): 
    resized_image = set_line_width(resized_image, line_width)

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

# Parameters for page creation
page_count = 0
total_pages = num_sections_x * num_sections_y
letters = list(string.ascii_uppercase)[0:total_pages]

# TODO: refactor
# Store all resulting images in one pdf
pdf = canvas.Canvas(file_folder+"result.pdf", pagesize=letter)

# Loop to split the large image into A4-sized sections
for row in range(num_sections_y):
    for col in range(num_sections_x):
        page_count += 1
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
        white_background = Image.new("RGB", (round(a4_width_px), round(a4_height_px)), "white")
        white_background.paste(section)
        paste_width, paste_height = white_background.size
        # Calculate the coordinates to paste the image in the center
        x_center = (a4_width_px_full - paste_width) // 2
        y_center = (a4_height_px_full - paste_height) // 2
        a4_image_copy = Image.new("RGB", (a4_width_px_full, a4_height_px_full), "white")
        a4_image_copy.paste(white_background, (x_center, y_center))
        # Add a square centimeter box
        add_reference_box(a4_image_copy, dpcm)
        # Add lines to the sides
        add_lines(a4_image_copy, a4_width_px_full, a4_height_px_full, dpcm)
        # Add letters to the left line
        add_page_letters_left(a4_image_copy, dpcm, page_count, row, num_sections_x, letters, a4_height_px_full)
        add_page_letters_right(a4_image_copy, dpcm, page_count, row, num_sections_x, letters, a4_height_px_full, a4_width_px_full)
        add_page_letters_top(a4_image_copy, dpcm, page_count, num_sections_x, letters, a4_width_px_full)
        add_page_letters_bottom(a4_image_copy, dpcm, page_count, num_sections_x, letters, a4_height_px_full, a4_width_px_full)
        # Save or process the A4-sized section here
        section_file_name = f"{file_folder}{file_name}_section_{row}_{col}.png"
        a4_image_copy.save(section_file_name)
        
        # TODO: refactor, make function to do this
        # Set the size of the PDF page to match the image size
        pdf.setPageSize((a4_image_copy.width, a4_image_copy.height))
        # Draw the PNG image on the PDF
        pdf.drawInlineImage(section_file_name, 0, 0, width=a4_image_copy.width, height=a4_image_copy.height)
        # Add a new page for the next image (optional)
        pdf.showPage()

# TODO: refactor
# Save the PDF file
pdf.save()
