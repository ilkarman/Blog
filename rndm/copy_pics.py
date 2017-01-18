""" Python 3 to copy all jpg files into sub-folders
based on day-created """
import os
from datetime import datetime
from shutil import copyfile

# Set these two paths
IMG_SRC = "C:\\Users\\ilkarman\\Pictures"
IMG_DEST = "C:\\Users\\ilkarman\\Documents\\MyTestFolder"

# os.walk() for recursive, otherwise:
for f in os.listdir(IMG_SRC):
    # .. or f.endswith('.png')
    if f.endswith('.jpg'):
        # date created (windows only); daily
        fldr_name = "imgs_" + datetime.fromtimestamp(int(os.path.getctime(IMG_SRC + "\\" + f))).strftime('%Y_%m_%d')
        dst = IMG_DEST + "\\" + fldr_name
        # makedirs can ignore exist warning
        os.makedirs(dst, exist_ok=True)
        copyfile(IMG_SRC + "\\" + f, dst + "\\" + f)
        print("Copied :", f)
