#!/usr/bin/python
from PIL import Image
import os, sys
import cv2

import os
import os.path

lss = []
for dirpath, dirnames, filenames in os.walk("./data"):
    for filename in [f for f in filenames if (f.endswith(".jpeg") or f.endswith(".jpg"))]:
        lss.append(filename)
        print(os.path.split(filename)[1], filename, dirpath)
        im = cv2.imread(dirpath + '/' + filename)
        image = cv2.cvtColor(im, cv2.COLOR_RGBA2RGB)
        cv2.imshow('image', image)
        cv2.imwrite('ddd/' + os.path.split(filename)[1], image)
# def resize():
#     for item in dirs:
#         if os.path.isfile(path+item):
#             

# resize()