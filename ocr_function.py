from pytesseract import image_to_string
from PIL import Image
import os
from shutil import copyfile
import re
_NoneType = type(None)

# Function to crop Image
def format_img(img_loc):
    img = Image.open(img_loc)
    cropped = img.crop((590, 465, 1220, 565))
    return cropped

# Function to read NRP with tesseract
# include a preprocess to keep only digits from words and select the NRP
def read_nrp(img):
    string = image_to_string(img)
    words = string.split()
    get_nrp = [re.sub("\D", "", w) for w in words]
    get_nrp = [w for w in get_nrp if len(w) >= 10]
    nrp = get_nrp[0]
    return nrp

# Main function
def ocr(source_dir, dest_dir):
    if source_dir[:1] != '/':
        source_dir = source_dir + '/'

    if dest_dir[:1] != '/':
        dest_dir = dest_dir + '/'

    for img_file in os.listdir(source_dir):
        location = source_dir + img_file
        cropped = format_img(location)
        nrp = read_nrp(cropped)

        copyfile(location, (dest_dir + nrp + '.jpg'))

    print ('Complete!')

# For single image only
def single_ocr(img):
    img_cropped = format_img(img)
    nrp = read_nrp(img_cropped)
    return nrp