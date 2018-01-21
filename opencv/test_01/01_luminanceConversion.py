import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#https://stackoverflow.com/a/12201744
def RGBtoLuminance(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114]) # 0.299 > 0.2989 ?

def LumaCheck(filename = 'ocean.png'):
    # we need the cmap, to make up for the missing channel
    img = mpimg.imread(filename)

    fig = plt.figure()

    a = fig.add_subplot(1, 4, 1)
    imgplot = plt.imshow(img)
    a.set_title('Orig')

    lum_img = img[:,:,0]
    a = fig.add_subplot(1, 4, 2)
    imgplot = plt.imshow(lum_img, cmap = plt.get_cmap('gray'))
    a.set_title('without')

    lum_img = RGBtoLuminance(img)
    a = fig.add_subplot(1, 4, 3)
    imgplot = plt.imshow(lum_img, cmap = plt.get_cmap('gray'))
    a.set_title('with luminance * rgb')

    a = fig.add_subplot(1, 4, 4)
    hist = plt.hist(lum_img.ravel(), bins=16, range=(0.0, 1.0))
LumaCheck()
LumaCheck("dark.png")
plt.show()