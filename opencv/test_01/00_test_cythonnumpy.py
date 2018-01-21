import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#import time
#from PIL import Image
import os, sys


img = mpimg.imread('stinkbug.png')
fd = open("data.txt", "w")
lum_img = img[:, :, 0]

hist = plt.hist(lum_img.ravel(), bins=16, range=(0.0, 1.0), fc='k', ec='k')
his = np.array(hist[0]).tolist()

print(his)
for h in his:
    fd.write(str(h))
    pass

fd.close()
#plt.show()
