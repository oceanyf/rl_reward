import cv2
from os import listdir
import imageio
import json
import numpy as np
import h5py
from PIL import Image

files = [f for f in listdir('./top_left/')]
directory_TL = './left/'
directory_TR = './right/'


def get_total_frame(fn):
    cap = cv2.VideoCapture(fn)
    return int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

j = 0
for file in files:
    i = 0
    #fn = directory_TL + file
    #frame_length = get_total_frame(fn)
    video_TL = imageio.get_reader('./top_left/' + file, 'ffmpeg')
    #video_TR = imageio.get_reader(directory_TR + file, 'ffmpeg')
    for im in enumerate(video_TL):
        i += 1
        if i == 1: #int(frame_length/4):
            imageio.imwrite(file.split(".")[0] + ".jpeg", im[1])
            break
    j += 1
    if j > 200:
        break
