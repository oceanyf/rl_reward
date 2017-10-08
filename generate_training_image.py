import os
from os import listdir
import csv
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from tkinter import messagebox

width = 320
height = 160

bad_list = ['0063', '0042', '0187', '0103', '0165', '0167', '0039', '0060', '0041', '0083', '0104', '0125', '0017',
            '0079', '0119', '0076', '0117', '0198', '0010', '0038', '0100', '0078', '0118', '0180', '0178', '0011',
            '0059', '0121', '0120', '0014', '0013', '0032', '0053', '0122', '0184', '0037', '0098', '0034', '0200',
            '0054', '0185', '0184', '0044', '0065', '0086', '0128', '0108', '0129', '0171', '0004', '0046', '0130',
            '0147', '0151', '0026', '0089', '0090', '0112', '0154', '0147', '0021', '0168', '0152', '0069', '0132',
            '0175', '0196', '0029', '0113', '0134', '0155', '0176', '0030', '0072']


def centerCrop(im, x, y):
    left = np.ceil(x - width / 2.)
    top = np.ceil(y - height / 2.)
    right = np.floor(x + width / 2.)
    bottom = np.floor(y + height / 2.)
    sample = im.crop((left, top, right, bottom))
    return sample

files = [f for f in listdir('./images2/label/peduncle/')]
for file in files:
    if file == '.DS_Store':
        continue
    #if file.split('.')[0].split('R')[1] in bad_list:
    #    print(file)
    #    continue
    readCSV = csv.reader(open('./images2/label/peduncle/' + file, 'r'))
    for line in readCSV:
        with Image.open('./images2/' + file.split('.')[0] + '.jpeg') as im:
            sample = centerCrop(im, int(line[1])/4*1.55, int(line[2])/4*1.55)
            #plt.imshow(sample)
            #plt.pause(1)
            sample.save(os.getcwd() + "/training2/" + file.split('.')[0] + ".jpeg")

