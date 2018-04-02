from __future__ import print_function

import cv2
import numpy as np

bins = np.arange(256).reshape(256,1)

def hist_curve_1d(im, w = None):
    #print(im.shape)
    #print(im)
    if w is None:
        w = im.shape[1]
    # length of 1d matrix
    l = im.shape[1]
    h = np.zeros((300,w,3))
    tmp_bins = np.arange(l).reshape(l,1)
    if im.shape[0] == 1:
        color = [(255,255,255)]
    else:
        color = [ (255,0,0),(0,255,0),(0,0,255) ]
    for i, col in enumerate(color):
        # why would i want to normalize this
        #cv2.normalize(im[i], im[i], 0, 255, cv2.NORM_MINMAX)
        hist = np.int32(np.around(im[i]))
        pts = np.int32(np.column_stack((tmp_bins, hist)))
        cv2.polylines(h,[pts],False,col, 1)
    y=np.flipud(h)
    return y
def hist_curve(im, thickness = 1):
    h = np.zeros((300,256,3))
    if len(im.shape) == 2:
        color = [(255,255,255)]
    elif im.shape[2] == 3:
        color = [ (255,0,0),(0,255,0),(0,0,255) ]
    for ch, col in enumerate(color):
        hist_item = cv2.calcHist([im],[ch],None,[256],[0,256])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        pts = np.int32(np.column_stack((bins,hist)))
        cv2.polylines(h,[pts],False,col, thickness)
    # calculate the mean values and draw horizontal lines
    mean_values = cv2.mean(im)
    for col, m in zip(color, mean_values):
        m = int(m)
        cv2.line(h, (0, m), (256, m), col, thickness)
    y=cv2.flip(h, 0)
    for idx, col in enumerate(color):
        cv2.putText(y, "ch" + str(idx), (10, idx * 30 + 10), cv2.FONT_HERSHEY_PLAIN, 1, col)
    return y

def hist_lines(im):
    h = np.zeros((300,256,3))
    if len(im.shape)!=2:
        print("hist_lines applicable only for grayscale images")
        #print("so converting image to grayscale for representation"
        im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    hist_item = cv2.calcHist([im],[0],None,[256],[0,256])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    for x,y in enumerate(hist):
        cv2.line(h,(x,0),(x,y),(255,255,255))
    y = np.flipud(h)
    return y

