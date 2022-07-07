####################
# 读取文件
####################

name = 'samples_4x512x512x3'

import numpy as np
npz = np.load( name + '.npz' )
print('npz.files =', npz.files)

data = npz['arr_0']
print('data.shape =', data.shape)
print()

####################
# 可视化
####################
'''
import matplotlib.pyplot as plt

for i in range(data.shape[0]):
    
    plt.clf()
    plt.imshow(data[i, ...])
    # plt.show()
    plt.pause(1)
'''
####################
# 保存
####################

import imageio

for i in range(data.shape[0]):

    img_name = name+'_'+str(i)+'.png'
    print(img_name)
    imageio.imwrite( img_name, data[i, ...] )
