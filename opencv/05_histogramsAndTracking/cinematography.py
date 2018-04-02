import os
import json
import math

import cv2
import numpy as np
import importlib

hist_py = importlib.import_module("hist")

def calcFrames():
    temp_dir = os.path.join("temp_dir", "mean.txt")
    fr = open(temp_dir, 'r')

    # these are supposed to np array in (x, 3, 1) shape
    hist = None
    diff = [[0, 0, 0]]
    slope = [[0, 0, 0]]

    line_prev = None
    for l in fr:
        line = json.loads(l)

        
        if line_prev is None:
            slope = np.array([0, 0, 0]).reshape(3, 1, 1)
        else:
            slope_next = np.array([abs(b-a)*5 for a, b in zip(line_prev, line)]).reshape(3, 1, 1)
            print(slope_next[2])
            slope = np.append(slope, slope_next, axis=1)
        # das ist sehr unbeholfen, diese erst init mit len(0)
        
        hist_next = np.array(line).reshape(3, 1, 1)
        if hist is None:
            hist = hist_next
        else:
            hist = np.append(hist, hist_next, axis=1)
        line_prev = line

    fr.close()
    img = hist_py.hist_curve_1d(hist)
    img2 = hist_py.hist_curve_1d(slope)
    dst = (img * 0.1 + img2 * 0.005)
    cv2.namedWindow('wdw', cv2.WINDOW_NORMAL)
    cv2.imshow("wdw", dst)
    cv2.waitKey(0)

if __name__ == "__main__":
    calcFrames()