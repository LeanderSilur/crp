import sys
print(sys.version)

import cv2
import cv2.cv as cv


print "cv2 version:    ", cv2.__version__

import sklearn
print sklearn.__version__
from action.suite import *

file_path = "D:/180105_crp/crp/actionvideotoolkit/01_testing/Movies/action/SHINING/SHINING.mov"



cflab = ColorFeaturesLAB("SHINING")
cflab.analyze_movie_with_display()