from PIL import ImageDraw, ImageFont

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