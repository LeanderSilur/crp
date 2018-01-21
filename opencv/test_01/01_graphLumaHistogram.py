import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
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
def graphImage(img):
    gray = RGBtoLuminance(img)
    hist = plt.hist(gray.ravel(), bins=8, range=(0.0, 1.0))
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
    histograms_matplot = []
    
    while(cap.isOpened()):
        ret, frame_cv = cap.read()

        # Abort the process, once the frames have all been
        # read and "ret" is no longer true.
        if ret != True:
            cap.release()
            #cv2.destroyAllWindows()
            break

        # p:    temporary path for saving the current frame
        p = os.path.join(tempdir, str(i)+".png")
        cv2.imwrite(p, frame_cv)

        # read the frame back in using the matplotlib.image lib
        frame_matplot = mpimg.imread(p)

        # "frame" and "read_frame" don't produce the same results.
        # Do we need a conversion?
        histograms_cv.append(graphImage(frame_cv))
        histograms_matplot.append(graphImage(frame_matplot))

        i += 1

    # save both lists to files
    WriteData(histograms_cv, "data_opencv2.txt")
    WriteData(histograms_matplot, "data_matplotlib.txt")


graphVideo()