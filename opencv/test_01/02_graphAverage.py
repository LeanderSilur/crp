from skimage.measure import compare_ssim
import imutils
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as mcol
import os
import cv2


# write a two dimensional array to a file with line breaks
def WriteData(data, filename):
    fd = open(filename, "w")
    for d in data:
        fd.write(str(d) + ",\n")
    fd.close()

def graphVideo(input_file = "cubeA.mov"):

    cap = cv2.VideoCapture(input_file)
    hue_mean = []
    sat_mean = []
    lum_mean = []
    i=0
    previous_frame
    while(cap.isOpened()):
        width = int(cap.get(3))
        height = int(cap.get(4))
        ret, frame_cv = cap.read()

        if ret != True:
            cap.release()
            #cv2.destroyAllWindows()
            break
        frame_cv_lum = cv2.cvtColor(frame_cv, cv2.COLOR_RGB2GRAY)
        frame_cv_hsv = cv2.cvtColor(frame_cv, cv2.COLOR_BGR2HSV)

        hue_mean.append(cv2.mean(frame_cv_hsv)[0])
        sat_mean.append(cv2.mean(frame_cv_hsv)[1])
        lum_mean.append(cv2.mean(frame_cv_lum)[0])

        (score, diff) = compare_ssim(previous_frame, frame_cv_lum, full=True)
        diff = (diff * 255).astype("uint8")
        print("SSIM: {}".format(score))

        print("reading", i)
        i += 1
        previous_frame = frame_cv_lum


    plt.plot(hue_mean, '--', color = (1, 0, 0))
    plt.plot(sat_mean, '--', color = (0, 1, 0))
    plt.plot(lum_mean, '--', color = (0, 0, 1))

    plt.show()
    # save both lists to files


graphVideo("bar.mp4")

