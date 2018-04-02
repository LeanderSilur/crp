import numpy as np
import cv2
from matplotlib import pyplot as plt

print(cv2.__version__)


# Initiate SIFT detector
orb = cv2.ORB_create()
def drawMatches(img1, img2):

    # find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])

    # cv2.drawMatchesKnn expects list of lists as matches.
    out_img = img1
    img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,out_img, flags=2)
    return img3


img1 = cv2.imread('box.png',0)          # queryImage
img2 = cv2.imread('box_in_scene.png',0) # trainImage

cv2.imshow('frame', img3)
cv2.waitKey(0)