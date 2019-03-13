from pytesseract import image_to_string
from PIL import Image
from resizeimage import resizeimage
import os
from shutil import copyfile
from collections import defaultdict
import string
_NoneType = type(None)

def keeper(keep):
    table = defaultdict(_NoneType)
    table.update({ord(c): c for c in keep})
    return table

digit_keeper = keeper(string.digits)

def format_img(img_loc):
    img = Image.open(img_loc)
    resized = resizeimage.resize_height(img, 750)
    cropped = resized.crop((310, 282, 715, 338))
    return cropped

def read_nrp(img):
    string = image_to_string(img)
    words = string.split()
    get_nrp = [w for w in words if len(w) >= 10]
    nrp = get_nrp[0]
    nrp = nrp.translate(digit_keeper)
    return nrp

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

def single_ocr(img):
    img_cropped = format_img(img)
    nrp = read_nrp(img_cropped)
    return nrp