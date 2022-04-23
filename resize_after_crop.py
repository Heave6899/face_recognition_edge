#!/usr/bin/python
from PIL import Image
import os, sys

path = "dd/"
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((160,160), Image.ANTIALIAS)
            imResize.save('ddd/' + f + '-160.jpg', 'JPEG', quality=90)

resize()