import os
from os import listdir
import numpy as np
from PIL import Image

width = 320
height = 160
image_size = [width, height]

files = [f for f in listdir('./training/peduncle/') if "IMGP" in f]
print(len(files))
for file in files:
    with Image.open('./training/peduncle/' + file) as im:
        img = im.resize(image_size, Image.ANTIALIAS)
        img.save(os.getcwd() + "/temp/" + file.split('.')[0] + ".jpeg")



