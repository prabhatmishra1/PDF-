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

# This list is just for example and defines the input according to pdf
REPLACEMENT_LIST = [
    #input for TEST PDF INPUT TEMPLATE.pdf
     {'{FULL NAME}': 'Prabahat','{number1}': '1234567890','{number2}': 'AA123456','{date11111}': '17/12/2021'},
    #input for 4_giberish template.pdf
     {'FULLNAME}': 'JLKSD', '{PASSPORT}': 'JFDSKLFHSDLK', '{GENDER}': 'Male', '{DATE3}': '20.09.2021', '{DATE4}': '20.09.2020'},
    #input for 3_giberish template.pdf
     {'{str1}': 'XXX', '{str2}': 'xxx', '{str3}': 'xxx', '{str4}': 'xxx', '{str5}': 'xxx', '{DATE2}': '12.04.1197'},
    #input for string and tables.pdf
     {'{28698}': '289023', '{06092021}': '2692121', '{01SSS}': '01CCC','{2345890}': '23456890', '{759478229}': '759478221'}

]

# This is just for example to pass images accroding to pdf

REPLACEMENT_IMG_LIST = [
    # input for TEST PDF INPUT TEMPLATE.pdf
    {'Im1': 'mainqr.png'},
    #img for 4_giberish template.pdf
    {'Im1': 'qr.png', 'Im2': 'mainqr.png'},
    #input for 3_giberish template.pdf
    {'Im1': '1.png', 'Im2': '3.png', 'Im3': 'bar.png','Im4': 'mainqr.png', 'Im0': '5.png'},
    #input for strings and tables.pdf
    {'Im1': 'mainqr.png'},
]

# DEFINE COLORS
white = (1, 1, 1)
black = (0, 0, 0)
blue = (0, 0, 0.6)


def process_pdf(doc, images_filename=None, bg_image_filename=None,REPLACEMENT_DICT=None):
    output_filename = 'result.pdf'
    output_file_path = os.path.join(current_path, 'output', output_filename)
    # now read the page
    # page = doc.loadPage(0)
    for page in doc:
        #TEXT REPLACEMENT
        for rep_key, rep_value in REPLACEMENT_DICT.items():
            text_instances = page.searchFor(rep_key)
            for inst in text_instances:
                # Get text color, font and size here
                text_info = page.get_text('dict', clip=inst)['blocks'][0]['lines'][0]['spans'][0]
                text_info_dict = {
                    'fontsize': text_info.get('size',12),
                    'border_width':1,
                    'color':fitz.sRGB_to_pdf(text_info.get('color', black)),
                    # 'align': TEXT_ALIGN_CENTER

                }
                # Customzing rect value
                rect = fitz.Rect(inst.x0-fitz.getTextlength(rep_value) /
                                2, inst.y0+2, inst.x1, inst.y1+2)
                #Delete text
                annot = page.addRedactAnnot(rect)
                # if you want to make sure to keep overlapping images:
                page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)
                # Insert text here
                page.insert_textbox(rect,rep_value, **text_info_dict)

        # Check for the top layer Images
        if images_filename:
            # Insert Image:
            ImageList = sorted(page.get_images(full=True))
            for img in ImageList:
                img_rect = page.getImageBbox(img)
                # Lets check rep image in images dict first:
                if img[7] in images_filename:
                    page.addRedactAnnot(rect, text=" ")
                    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)
                    replace_image_path = os.path.join(
                    current_path, 'assets', images_filename[img[7]])
                    page.insertImage(img_rect, filename=replace_image_path)
        if bg_image_filename:
            # insert background image to the full page
            full_page_image_path = os.path.join(
                current_path, 'assets', bg_image_filename)
            page.insertImage(page.rect,
                            filename=full_page_image_path, overlay=False
                            )


    # save final doc here
    doc.save(output_file_path, garbage=4, deflate=True, clean=True)

if __name__ == "__main__":
    # Get the pdf file
    #define your input path here
    '''input_filename = TEST PDF INPUT TEMPLATE.pdf, 3_giberish template.pdf,
    4_giberish template.pdf '''

    input_filename =   input('\nInput the PDF file name: ')
    REPLACEMENT_DICT = eval(input('\nEnter the replacement dict: '))
    # For e.g {'FX462582': 'FX462581','4327974399': '4327974398'},

    #  Take the top layer images
    ask_for_image = input('\n Do you want to replace the images ? \n Enter yes or no: ').strip().lower()
    images_filename = eval(input('\nInput the dict of images: ').strip()) if ask_for_image == "yes" else None

    # Take the background image here
    ask_for_bg_image = input('\n Do you want to add the background image ? \n Enter yes or no: ')
    bg_image_filename = input('\nInput the background image file name: ') if ask_for_bg_image == 'yes' else None
    input_file = os.path.join(current_path, 'input', input_filename)

    doc = fitz.open(input_file)  # open document
    process_pdf(doc, images_filename=images_filename,
    REPLACEMENT_DICT=REPLACEMENT_DICT,
    bg_image_filename = bg_image_filename
    )
    print("=======================================\n")
    print("PDF Updated Successfully................")
