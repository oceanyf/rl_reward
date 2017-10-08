import cv2
from os import listdir
import imageio
import json
import numpy as np
import h5py
from PIL import Image
import matplotlib.pyplot as plt
from random import randint
import pymsgbox
from matplotlib.widgets import Button
import time
import os.path

next_one = False
save = False
save_flag = '4clear'
movie_folder = './sep10_2017_LocateTip/'


def on_button_clicked(event):
    print('Next............')
    global next_one
    next_one = True


def on_button_save4_clicked(event):
    print('Choose to save 4 clear.......')
    global save
    save = True
    global next_one
    next_one = True
    global save_flag
    save_flag = '4clear'


def on_button_save3_clicked(event):
    print('Choose to save 3 clear.......')
    global save
    save = True
    global next_one
    next_one = True
    global save_flag
    save_flag = '3clear'


def on_button_save2_clicked(event):
    print('Choose to save 2 clear.......')
    global save
    save = True
    global next_one
    next_one = True
    global save_flag
    save_flag = '2clear'


def on_button_save1_clicked(event):
    print('Choose to save 1 clear.......')
    global save
    save = True
    global next_one
    next_one = True
    global save_flag
    save_flag = '1clear'


def get_total_frame(fn):
    cap = cv2.VideoCapture(fn)
    return int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


if os.path.isfile(movie_folder + 'sep10_2017_LocateTip_checklist.txt'):
    with open(movie_folder + 'sep10_2017_LocateTip_checklist.txt') as json_data:
        training_list = json.load(json_data)
else:
    training_list = {'4clear':[], '3clear':[], '2clear':[], '1clear':[]}

# with h5py.File(movie_folder + 'training_data/3clear/GOPR0002.hdf5', 'r') as f:
#     print(f['cut_position_TL'][0], f['cut_position_TR'][0])
#     for i in range(0, len(f['reward']), 5):
#         fig = plt.subplot(221)
#         plt.title(f['reward'][i], fontsize=20)
#         plt.imshow(f['image_TL'][i])
#         plt.scatter(x=f['cut_position_TL'][0], y=f['cut_position_TL'][1], c='r', s=8)
#         plt.subplot(222)
#         plt.imshow(f['image_TR'][i])
#         plt.scatter(x=f['cut_position_TR'][0], y=f['cut_position_TR'][1], c='r', s=8)
#         plt.subplot(223)
#         plt.imshow(f['image_BL'][i])
#         plt.scatter(x=f['cut_position_BL'][0], y=f['cut_position_BL'][1], c='r', s=8)
#         plt.subplot(224)
#         plt.imshow(f['image_BR'][i])
#         plt.scatter(x=f['cut_position_BR'][0], y=f['cut_position_BR'][1], c='r', s=8)
#         plt.pause(0.01)

files = [f for f in listdir(movie_folder + 'top_left/')]
directory = dict()
directory['TL'] = movie_folder + 'top_left/'
directory['TR'] = movie_folder + 'top_right/'
directory['BL'] = movie_folder + 'bottom_left/'
directory['BR'] = movie_folder + 'bottom_right/'
end_effector = dict()
end_effector['TL'] = [1350, 589]
end_effector['TR'] = [550, 610]
end_effector['BL'] = [1340, 500]
end_effector['BR'] = [565, 528]
score = 85
for file in files:
    if file in [each for value in training_list.values() for each in value]:
        continue
    image = {'TL': [], 'TR': [], 'BL': [], 'BR': []}
    off_center_x = randint(-40, 40)
    off_center_y = randint(-40, 40)
    center = {'TL': [end_effector['TL'][0] + off_center_x, end_effector['TL'][1] + off_center_y],
              'TR': [end_effector['TR'][0] - off_center_x, end_effector['TR'][1] + off_center_y],
              'BL': [end_effector['BL'][0] + off_center_x, end_effector['BL'][1] - off_center_y],
              'BR': [end_effector['BR'][0] - off_center_x, end_effector['BR'][1] - off_center_y]}
    frame_length = dict()
    for key, value in directory.items():
        fn = value + file
        frame_length[key] = get_total_frame(fn)
    max_step = frame_length[min(frame_length, key=frame_length.get)]
    for key, value in directory.items():
        fn = value + file
        #frame_length = get_total_frame(fn)
        video = imageio.get_reader(fn, 'ffmpeg')
        steps = 0
        for im in enumerate(video):
            if steps >= max_step:
                break
            if steps < score:
                image[key].append(im[1][center[key][1]-200:center[key][1]+200, center[key][0]-400:center[key][0]+400])
                steps += 1
            else:
                break
    reward = [(i+1)*100.0/steps for i in range(steps)]
    new_end_effector = {'TL': [400 - off_center_x, 200 - off_center_y],
              'TR': [400 + off_center_x, 200 - off_center_y],
              'BL': [400 - off_center_x, 200 + off_center_y],
              'BR': [400 + off_center_x, 200 + off_center_y],}
    for i in range(0, len(reward), 5):
        fig = plt.subplot(221)
        plt.title(file, fontsize=20)
        plt.imshow(image['TL'][i])
        plt.scatter(x=new_end_effector['TL'][0], y=new_end_effector['TL'][1], c='r', s=8)
        plt.subplot(222)
        plt.imshow(image['TR'][i])
        plt.scatter(x=new_end_effector['TR'][0], y=new_end_effector['TR'][1], c='r', s=8)
        plt.subplot(223)
        plt.imshow(image['BL'][i])
        plt.scatter(x=new_end_effector['BL'][0], y=new_end_effector['BL'][1], c='r', s=8)
        plt.subplot(224)
        plt.imshow(image['BR'][i])
        plt.scatter(x=new_end_effector['BR'][0], y=new_end_effector['BR'][1], c='r', s=8)
        plt.pause(0.01)

    button_next = Button(plt.axes([0.81, 0.01, 0.1, 0.075]), 'Next')
    plt.pause(0.01)
    button_save4 = Button(plt.axes([0.61, 0.01, 0.1, 0.075]), 'Save 4clear')
    plt.pause(0.01)
    button_save3 = Button(plt.axes([0.41, 0.01, 0.1, 0.075]), 'Save 3clear')
    plt.pause(0.01)
    button_save2 = Button(plt.axes([0.21, 0.01, 0.1, 0.075]), 'Save 2clear')
    plt.pause(0.01)
    button_save1 = Button(plt.axes([0.01, 0.01, 0.1, 0.075]), 'Save 1clear')
    plt.pause(0.01)

    save = False
    next_one = False
    button_next.on_clicked(on_button_clicked)
    button_save4.on_clicked(on_button_save4_clicked)
    button_save3.on_clicked(on_button_save3_clicked)
    button_save2.on_clicked(on_button_save2_clicked)
    button_save1.on_clicked(on_button_save1_clicked)

    while not next_one:
        plt.pause(0.1)

    if save:  # show a Continue/Cancel dialog
        f = h5py.File(movie_folder + 'training_data/' + save_flag + '/' + file.split('.')[0] + '.hdf5')
        for key, value in directory.items():
            f.create_dataset('image_'+key, data=np.array(image[key], dtype=np.uint8), compression="gzip")
            f.create_dataset('cut_position_'+key, data=np.array(new_end_effector[key], dtype=np.uint16))
        #f.create_dataset('image' + key, data=np.array(image[key]).astype("float"), compression="gzip")
        f.create_dataset('reward', data=np.array(reward, dtype=np.uint16))
        f.close()
        training_list[save_flag].append(file)
        with open(movie_folder + 'sep10_2017_LocateTip_checklist.txt', 'w') as outfile:
            json.dump(training_list, outfile)

    plt.close()