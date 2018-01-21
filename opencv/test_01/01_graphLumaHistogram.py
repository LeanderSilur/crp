import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import cv2

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


def graphImage(img):
    gray = RGBtoLuminance(img)
    hist = plt.hist(gray.ravel(), bins=8, range=(0.0, 1.0))
    return np.array(hist[0]).tolist()

def graphVideo(input_file = "cubeA.mov", tempdir = "tempdir"):

    if not os.path.exists(tempdir):
        os.makedirs(tempdir)

    cap = cv2.VideoCapture(input_file)

    width = int(cap.get(3))   # float
    height = int(cap.get(4))  # float
    fps = cap.get(5)
    frames = cap.get(7)
    print(width, height, fps)
    i = 0

    histograms0 = []
    histograms1 = []
    
    while(cap.isOpened()):
        ret, frame_cv = cap.read()

        if ret != True:     # stop, when there is no frame returned
            cap.release()
            cv2.destroyAllWindows()
            break

        p = os.path.join(tempdir, str(i)+".png")
        cv2.imwrite(p, frame_cv)
        frame_matplot = mpimg.imread(p)

        # "frame" and "read_frame" don't produce the same results.
        # Do we need a conversion?
        histograms0.append(graphImage(frame_cv))
        histograms1.append(graphImage(frame_matplot))

        i += 1
    WriteData(histograms0, "data_opencv2.txt")
    WriteData(histograms1, "data_matplotlib.txt")


graphVideo()