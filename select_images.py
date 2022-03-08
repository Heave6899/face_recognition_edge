import os
import sys
import shutil
from os import listdir
from os.path import isfile, join
import csv
from PIL import Image

# http://vis-www.cs.umass.edu/lfw/#download

# rename images
# rootdir = "./data/real_images"
# for root, subFolders, files in os.walk(rootdir):
#     print(root, subFolders, files)
#     if root != rootdir:
#         for file_name in os.listdir(root):
#             temp = file_name.split(".")[0]
#             new_name = f"{root}/{temp}.png"
#             os.rename(f"{root}/{file_name}", new_name)
#             print(f"{root}/{file_name}", new_name)

# resize images 
rootdir = "./data/real_images"
for root, subFolders, files in os.walk(rootdir):
    print(root, subFolders, files)
    if root != rootdir:
        for file_name in os.listdir(root):
            file_path = f"{root}/{file_name}"
            print(file_path)
            im = Image.open(file_path)
            im = im.resize((160,160))
            im.save(file_path)
            # sys.exit()

