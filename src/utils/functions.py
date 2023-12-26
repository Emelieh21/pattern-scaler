from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

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
    font = ImageFont.truetype("./assets/arial.ttf", dpcm/2)
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
    font = ImageFont.truetype("./assets/arial.ttf", dpcm/2)
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
    font = ImageFont.truetype("./assets/arial.ttf", dpcm/2)
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
    font = ImageFont.truetype("./assets/arial.ttf", dpcm/2)
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
