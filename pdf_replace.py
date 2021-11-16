''' We have used pymupdf module for the pdf munpulation, you can install it using
    this link https://pymupdf.readthedocs.io/en/latest/installation.html
'''
import fitz
import pathlib
import os

from fitz.fitz import TEXT_ALIGN_CENTER, TEXT_ALIGN_RIGHT
from fitz.utils import getColor

# Get current file path
current_path = pathlib.Path(__file__).parent.absolute()

# Create input and output folders if doesn't exist
input_folder = os.path.join(current_path, 'input')
output_folder = os.path.join(current_path, 'output')
if not os.path.exists(input_folder):
    os.makedirs(input_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

REPLACEMENT_DICT = {
    '{FULL NAME}': 'JOHN TURNE',
    '{number1}': '1234567890000000000000',
    '{number2}': 'AA123456',
    '{date11111}': '17/12/2021'
}

# DEFINE COLORS
white = getColor("whitesmoke")
blue = (0, 0,.6)

def process_pdf(doc, image_filename=None):
    output_filename = 'result.pdf'
    output_file_path = os.path.join(current_path, 'output', output_filename)
    replace_image_path = os.path.join(current_path, 'assets', 'QR.jpg')
    # now read the page
    page = doc.loadPage(0)
    # Text align value
    text_align = TEXT_ALIGN_CENTER
    #TEXT REPLACEMENT
    for rep_key, rep_value in REPLACEMENT_DICT.items():
        text_instances = page.searchFor(rep_key)
        for inst in text_instances:
                    #Customization ACC to KEY
                    if rep_key == '{number1}':
                        rect = fitz.Rect(inst.x0-400, inst.y0+2, inst.x1, inst.y1+2)
                        text_align = TEXT_ALIGN_RIGHT
                    elif rep_key == '{FULL NAME}' :
                        rect = fitz.Rect(inst.x0-170, inst.y0+2, inst.x1+170, inst.y1+2)
                    else:
                        rect = fitz.Rect(inst.x0-18, inst.y0+2, inst.x1+18, inst.y1+2)
                        text_align = TEXT_ALIGN_CENTER

                    #Delete text
                    annot = page.addRedactAnnot(rect)
                    # if you want to make sure to keep overlapping images:
                    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
                    page.insert_textbox(rect,rep_value, fontsize=12,
                    border_width=1, color=blue,align=text_align)

    # add QR image on top center
    qr_image_filename = 'centerqr.png'
    qr_insert_image_path = os.path.join(current_path, 'assets', qr_image_filename)

    # define the position (upper-center)
    qr_image_rectangle = fitz.Rect(270, 10,340,70)
    page.insertImage(qr_image_rectangle, filename=qr_insert_image_path)

   # insert background image to the pull page
    full_page_image_path = os.path.join(current_path, 'assets', 'background.png')
    full_img_rect = fitz.Rect(0,0,612,792)
    page.insertImage(full_img_rect, filename=full_page_image_path, overlay=False)

    # Check for Image
    if image_filename:
        # Insert Image:
        replace_image_path = os.path.join(current_path, 'assets', image_filename)
        # Get the rect dynamically here
        img_list = doc.getPageImageList(0, full=True)  # important: use 'full' parameter
        item = img_list[0] #fetch first image rect in the page
        img_rect = page.getImageBbox(item)
        shape = page.newShape()  # create Shape
        shape.draw_rect(img_rect)
        shape.finish(color = white, fill = white)
        shape.commit()
        page.insertImage(img_rect, filename=replace_image_path)

    # save final doc here
    doc.save(output_file_path, garbage=4, deflate=True, clean=True)

if __name__ == "__main__":
    # Get the pdf file
    #define your input path here
    # input_filename = 'TEST PDF INPUT TEMPLATE.pdf'
    input_filename =   input('\nInput the PDF file name: ')
    ask_for_image = input('\n Do you want to replace the image ? \n Enter yes or no: ')
    if (ask_for_image == 'yes'):
        image_filename = input('\nInput the Image file name: ')
    else:
        image_filename = None
    input_file = os.path.join(current_path, 'input', input_filename)

    doc = fitz.open(input_file)  # open document
    process_pdf(doc, image_filename = image_filename)
