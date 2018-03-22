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

def graphVideo(input_file = "cubeA.mov", tempdir = "tempdir"):

    if not os.path.exists(tempdir):
        os.makedirs(tempdir)

    cap = cv2.VideoCapture(input_file)

    i = 0
    histograms_cv = []
    while(cap.isOpened()):
        ret, frame_cv = cap.read()

        if ret != True:
            cap.release()
            #cv2.destroyAllWindows()
            break
        frame_cv_lum = cv2.cvtColor(frame_cv, cv2.COLOR_RGB2GRAY)
        frame_cv_hsv = cv2.cvtColor(frame_cv, cv2.COLOR_BGR2HLS)
        lum = cv2.calcHist([frame_cv_lum],[0],None,[256],[0,256])
        hsv = cv2.calcHist([frame_cv_hsv],[1],None,[256],[0,256])
        plt.plot(lum, color = 'r')
        plt.plot(hsv, color = 'g')
        plt.show()

        #frame_cv_norm = cv2.normalize(frame_cv_rgb, None, alpha=0, beta=1,
        #    norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        #hist = plt.hist(frame_cv_lum.ravel(), bins=8, range=(0,255))
        #opencv2 is 40x faster
        hist = cv2.calcHist([frame_cv_lum],[0],None,[256],[0,256])
        histograms_cv.append(hist)
        
        print("reading", i)
        i += 1
    plt.xlim([0,256])
    for idx, h in enumerate(histograms_cv):
        if (idx%20 == 0):
            print("plotting", idx)
            c = mcol.hsv_to_rgb((idx/len(histograms_cv) * 0.8, 1, 1))
            plt.plot(h, color = c, linewidth=0.4)
    plt.show()
    # save both lists to files
    WriteData(histograms_cv, "data_opencv2.txt")


graphVideo("jp.mov", "tempdir")


"""
        frame_cv_lum = cv2.cvtColor(frame_cv, cv2.COLOR_RGB2GRAY)
        frame_cv_hsv = cv2.cvtColor(frame_cv, cv2.COLOR_BGR2HLS)
        lum = cv2.calcHist([frame_cv_lum],[0],None,[256],[0,256])
        hsv = cv2.calcHist([frame_cv_hsv],[1],None,[256],[0,256])
        plt.plot(lum, color = 'r')
        plt.plot(hsv, color = 'g')
        plt.show()

        # how to kill hsv
"""