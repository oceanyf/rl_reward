import h5py
from PIL import Image
import matplotlib.pyplot as plt
from random import randint
import os.path
import numpy as np

rewards = [20]
data_type = ['training', 'validation']
end_effector = dict()
end_effector['TL'] = [2306, 1156]
end_effector['TR'] = [930, 1385]  # [970, 1355]
end_effector['BL'] = [2305, 1184]
end_effector['BR'] = [986, 1206]
width = 800
height = 400

h5_folder = './oct15_2017_LocateTip/training_data/'
for reward in rewards:
    for type in data_type:
        directory = dict()
        directory['TL'] = './oct15_2017_LocateTip/TL/' + type + '/reward' + str(reward) + '/'
        directory['TR'] = './oct15_2017_LocateTip/TR/' + type + '/reward' + str(reward) + '/'
        directory['BL'] = './oct15_2017_LocateTip/BL/' + type + '/reward' + str(reward) + '/'
        directory['BR'] = './oct15_2017_LocateTip/BR/' + type + '/reward' + str(reward) + '/'
        for each in os.listdir(directory['TL']):
            if each.startswith('.'):
                continue
            image = {'TL': [], 'TR': [], 'BL': [], 'BR': []}
            off_center_x = randint(-40, 40)
            off_center_y = randint(-40, 40)
            center = {'TL': [end_effector['TL'][0] + off_center_x, end_effector['TL'][1] + off_center_y],
                      'TR': [end_effector['TR'][0] - off_center_x, end_effector['TR'][1] + off_center_y],
                      'BL': [end_effector['BL'][0] + off_center_x, end_effector['BL'][1] - off_center_y],
                      'BR': [end_effector['BR'][0] - off_center_x, end_effector['BR'][1] - off_center_y]}
            new_end_effector = {'TL': [width - off_center_x, height - off_center_y],
                      'TR': [width + off_center_x, height - off_center_y],
                      'BL': [width - off_center_x, height + off_center_y],
                      'BR': [width + off_center_x, height + off_center_y],}
            f = h5py.File(h5_folder + type + '/' + each.split('.')[0] + '.hdf5')
            for key, value in directory.items():
                new_end_effector[key][:] = [x/2 for x in new_end_effector[key]]
                temp = directory['TL'].replace('TL', key)
                with Image.open(temp + each) as im:
                    image[key] = im.crop((center[key][0] - width, center[key][1] - height,
                                          center[key][0] + width,  center[key][1] + height)).resize([width, height], Image.ANTIALIAS)
                f.create_dataset('image_' + key, data=np.array(image[key], dtype=np.uint8), compression="gzip")
                f.create_dataset('cut_position_' + key, data=np.array(new_end_effector[key], dtype=np.uint16))
            f.create_dataset('reward', data=np.array(reward, dtype=np.uint16))
            f.close()

            # fig = plt.subplot(221)
            # plt.title(str(reward)+temp, fontsize=10)
            # plt.imshow(image['TL'])
            # plt.scatter(x=new_end_effector['TL'][0], y=new_end_effector['TL'][1], c='g', s=8)
            # plt.subplot(222)
            # plt.imshow(image['TR'])
            # plt.scatter(x=new_end_effector['TR'][0], y=new_end_effector['TR'][1], c='g', s=8)
            # plt.subplot(223)
            # plt.imshow(image['BL'])
            # plt.scatter(x=new_end_effector['BL'][0], y=new_end_effector['BL'][1], c='g', s=8)
            # plt.subplot(224)
            # plt.imshow(image['BR'])
            # plt.scatter(x=new_end_effector['BR'][0], y=new_end_effector['BR'][1], c='g', s=8)
            # plt.pause(1)
            # plt.close()
