import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as mcol
import os
import cv2


# print the specs of a cv2 capture object
def GrabSpecs(cv_cap):
    width = int(cv_cap.get(3))
    height = int(cv_cap.get(4))
    fps = cv_cap.get(5)
    frames = cv_cap.get(7)
    print(width, height, fps)

# write a two dimensional array to a file with line breaks
def WriteData(data, filename):
    fd = open(filename, "w")
    for d in data:
        fd.write(str(d) + ",\n")
    fd.close()


# convert a 3 channel numpy image to a single channel
# grayscale image by perceived luminance
#
# https://stackoverflow.com/a/12201744
def RGBtoLuminance(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114]) # 0.299 > 0.2989 ?


# returns a histogram list from a numpy image
def graphGrayImage(img, steps = 8, prange = (0.0, 1.0)):
    hist = plt.hist(img.ravel(), bins=steps, range=prange)
    return np.array(hist[0]).tolist()


# saves histogram data to a file
def graphVideo(input_file = "cubeA.mov", tempdir = "tempdir"):

    # Temporarily saving the files in a subdirectory and
    # reading them back in, changes the output.
    # Create a temporary directory for this purpose.
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
        #frame_cv_rgb = cv2.cvtColor(frame_cv, cv2.COLOR_BGR2RGB)
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
