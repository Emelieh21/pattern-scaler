from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import fitz  # PyMuPDF
import os
import math
import string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

font_path = os.getcwd()+"/app/assets/arial.ttf"

def is_pdf_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == '.pdf'

def convert_pdf_to_bw_png(input_pdf, output_png, resolution):
    pdf_document = fitz.open(input_pdf)
    page = pdf_document[0]  # Get the first page

    # Convert to grayscale
    pixmap = page.get_pixmap(matrix=fitz.Matrix(resolution/72, resolution/72))
    pixmap.save(output_png)

def add_reference_box(a4_image_copy, dpcm):
    reference_offset = dpcm+15
    rectangle_color = (211, 211, 211)  # RGB value for light grey
    rectangle_coordinates = (reference_offset, reference_offset, reference_offset+dpcm, reference_offset+dpcm)
    draw = ImageDraw.Draw(a4_image_copy)
    draw.rectangle(rectangle_coordinates, fill=rectangle_color)
    return(a4_image_copy)

def add_lines(a4_image_copy, a4_width_px_full, a4_height_px_full, dpcm):
    line_color = (211, 211, 211)  # RGB value for light grey
    draw = ImageDraw.Draw(a4_image_copy)
    draw.line((0,dpcm, a4_width_px_full,dpcm), fill=line_color, width=3)
    draw.line((dpcm,0, dpcm,a4_height_px_full), fill=line_color, width=3)
    draw.line((0,a4_height_px_full-dpcm, a4_width_px_full,a4_height_px_full-dpcm), fill=line_color, width=3)
    draw.line((a4_width_px_full-dpcm,0, a4_width_px_full-dpcm,a4_height_px_full), fill=line_color, width=3)
    return(a4_image_copy)

# TODO: refactor code, these functions are highly repetitive
def add_page_letters_left(a4_image_copy, dpcm, page_count, row, num_sections_x, letters, a4_height_px_full):
    draw = ImageDraw.Draw(a4_image_copy)
    font = ImageFont.truetype(font_path, dpcm/2)
    page_count = page_count - 1
    other_page_count = page_count - 1
    last_page_of_former_row = row*num_sections_x-1
    try:
        result = [letters[page_count], letters[other_page_count]]
    except:
        result = None
    # If the other page count is negative, return nothing
    if (other_page_count < 0):
        result = None
    # if the other page count equals the last page of the last row, return nothing
    if (other_page_count == last_page_of_former_row):
        result = None    
    if (result is not None):
            draw.text((1.15*dpcm, a4_height_px_full/2), result[0], font = font, fill="black")
            draw.text((0.5*dpcm, a4_height_px_full/2), result[1], font = font, fill="black")
    return(a4_image_copy)

def add_page_letters_right(a4_image_copy, dpcm, page_count, row, num_sections_x, letters, a4_height_px_full, a4_width_px_full):
    draw = ImageDraw.Draw(a4_image_copy)
    font = ImageFont.truetype(font_path, dpcm/2)
    page_count = page_count - 1
    other_page_count = page_count + 1
    first_page_of_next_row = (row+1)*num_sections_x
    try:
        result = [letters[page_count], letters[other_page_count]]
    except:
        result = None
    # If the other page count is negative, return nothing
    if (other_page_count < 0):
        result = None
    # if the other page count equals the last page of the last row, return nothing
    if (other_page_count == first_page_of_next_row):
        result = None    
    if (result is not None):
            draw.text((a4_width_px_full - (1.5*dpcm), a4_height_px_full/2), result[0], font = font, fill="black")
            draw.text((a4_width_px_full - (0.85*dpcm), a4_height_px_full/2), result[1], font = font, fill="black")
    return(a4_image_copy)

def add_page_letters_top(a4_image_copy, dpcm, page_count, num_sections_x, letters, a4_width_px_full):
    draw = ImageDraw.Draw(a4_image_copy)
    font = ImageFont.truetype(font_path, dpcm/2)
    page_count = page_count - 1
    other_page_count = page_count - num_sections_x
    try:
        result = [letters[page_count], letters[other_page_count]]
    except:
        result = None
    # If the other page count is negative, return nothing
    if (other_page_count < 0):
        result = None  
    if (result is not None):
            draw.text((a4_width_px_full/2, 1.05*dpcm), result[0], font = font, fill="black")
            draw.text((a4_width_px_full/2, 0.3*dpcm), result[1], font = font, fill="black")
    return(a4_image_copy)

def add_page_letters_bottom(a4_image_copy, dpcm, page_count, num_sections_x, letters, a4_height_px_full, a4_width_px_full):
    draw = ImageDraw.Draw(a4_image_copy)
    font = ImageFont.truetype(font_path, dpcm/2)
    page_count = page_count - 1
    other_page_count = page_count + num_sections_x
    try:
        result = [letters[page_count], letters[other_page_count]]
    except:
        result = None
    # If the other page count is negative, return nothing
    if (other_page_count < 0):
        result = None   
    if (result is not None):
            draw.text((a4_width_px_full/2, a4_height_px_full - (1.65*dpcm)), result[0], font = font, fill="black")
            draw.text((a4_width_px_full/2, a4_height_px_full - (0.90*dpcm), a4_height_px_full/2), result[1], font = font, fill="black")
    return(a4_image_copy)

def set_line_width(resized_image, line_width):
    # Load the image
    image = resized_image
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 150)
    # Find lines in the image using the HoughLinesP function for probabilistic Hough transform
    lines = cv2.HoughLinesP(edges, 3, np.pi / 210, threshold=50, minLineLength=50, maxLineGap=100)
    # Get the original image dimensions
    height, width, _ = resized_image.shape
    # Redraw the detected lines on blank image with whatever width we like
    new_image = Image.new("RGB", (width, height), "white")
    new_image = np.array(new_image)
    # Draw the lines on the original image
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # Draw the line on the image with a specific width (in this case, 2 pixels)
        cv2.line(new_image, (x1, y1), (x2, y2), (0, 0, 0), line_width)
    return(new_image)

def set_scale_factors(height_cm, width_cm, 
                    desired_height, 
                    desired_width, 
                    scale_factor_height, 
                    scale_factor_width):
    if (desired_height):
        # Calculate scale factor
        scale_factor_height = desired_height/height_cm
        print(f"Scale factor height: {scale_factor_height}")

    if (desired_width):
        # Calculate scale factor
        scale_factor_width = desired_width/width_cm
        print(f"Scale factor width: {scale_factor_width}")

    if (not any(x is not None for x in [scale_factor_height, scale_factor_width])):
        raise Exception("scale_factor_height and scale_factor_width can not both be None. Please set at least one of the two.")

    if (scale_factor_height is None):
        scale_factor_height = scale_factor_width

    if (scale_factor_width is None):
        scale_factor_width = scale_factor_height

    return scale_factor_height, scale_factor_width

def scale_pattern(input_file, 
                  desired_height, 
                  desired_width, 
                  scale_factor_height, 
                  scale_factor_width, 
                  pdf_resolution, 
                  line_width):

    # Fine tuning parameters
    inch = 2.54
    file_folder = os.getcwd()+"/app/output-files/"

    # Conversion parameters
    if (is_pdf_file(input_file)):
        ## Convert pdf of scan to png
        print("Converting pdf to png...")
        pdf_input_file = input_file
        input_file = input_file.lower().replace(".pdf", ".png")
        convert_pdf_to_bw_png(pdf_input_file, input_file, pdf_resolution)

    # We need a filename to use later for storing
    file_name = input_file.replace(".png", "")

    # Get the dpi
    image = Image.open(input_file)  # Replace 'your_image.jpg' with the path to your image file
    # Get the image's DPI (Dots Per Inch)
    dpi = image.info.get('dpi')
    if (dpi is None):
        # Use a default
        print("Using default dpi")
        dpi = 72
    else:
        dpi = dpi[0]
    print(dpi)

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

    # Save the PDF file
    pdf.save()
    
    # Custom headers to return the pdf...
    custom_headers = {
        "Content-Disposition": "attachment; filename=result.pdf",
        "X-original-width": f"{width_cm} cm",
        "X-original-height": f"{height_cm} cm",
        "X-new-width": f"{new_width/dpcm} cm",
        "X-new-height": f"{new_height/dpcm} cm"
    }

    return custom_headers