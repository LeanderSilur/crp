import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image


img = mpimg.imread('img_stinkbug.png')
lum_img = img[:, :, 0]

# introduction
# https://matplotlib.org/tutorials/introductory/images.html#sphx-glr-tutorials-introductory-images-py

def showImage():
    plt.imshow(lum_img)
    plt.colorbar()      # show colorbar
    plt.show()

def colormaps():
    value_img = img[:, :, 0]            # pseudocolor image
    plt.imshow(lum_img, cmap="hot")     # set a cmap
    imgplot = plt.imshow(lum_img)       # display image
    imgplot.set_cmap('nipy_spectral')   # change the cmap

    # list of cmaps
    # https://matplotlib.org/tutorials/colors/colormaps.html#classes-of-colormaps

    value_img = img[:, :, 0]      # value

def histogram():
    hist = plt.hist(lum_img.ravel(), bins=256, range=(0.0, 1.0), fc='k', ec='k')
    imgplot = plt.imshow(hist)

def climExample():
    fig = plt.figure()
    a = fig.add_subplot(1, 2, 1)
    imgplot = plt.imshow(lum_img)
    a.set_title('Before')
    plt.colorbar(ticks=[0.1, 0.3, 0.5, 0.7], orientation='horizontal')
    a = fig.add_subplot(1, 2, 2)
    imgplot = plt.imshow(lum_img)
    imgplot.set_clim(0.0, 0.7)
    a.set_title('After')
    plt.colorbar(ticks=[0.1, 0.3, 0.5, 0.7], orientation='horizontal')

def resize():
    img = Image.open('img_stinkbug.png')
    img.thumbnail((64, 64), Image.ANTIALIAS)  # resizes image in-place
    imgplot = plt.imshow(img)

histogram()
plt.show()