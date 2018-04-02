import numpy as np
import cv2
from matplotlib import pyplot as plt
import importlib
import os

hist_py = importlib.import_module("hist")
haar_py = importlib.import_module("haar")

# compare frame of a video cap
def compare_frame_change(path, do_faces = True):
    temp_dir = "temp_dir"

    orb = cv2.ORB_create()
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    fd_diff = open(os.path.join(temp_dir, "diff.txt"), "w")
    fd_mean = open(os.path.join(temp_dir, "mean.txt"), "w")
    fd_face = open(os.path.join(temp_dir, "face.txt"), "w")
    fd_motion = open(os.path.join(temp_dir, "motion.txt"), "w")

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.namedWindow('active_frame', cv2.WINDOW_NORMAL)
    cv2.namedWindow('all_frames', cv2.WINDOW_NORMAL)

    cap = cv2.VideoCapture(path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    _, frame_A_bgr = cap.read()
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    live_histogram = np.array([])
    hsv_histograms = np.array([[[[]]]])

    while(cap.isOpened()):
        ret, frame_B_bgr = cap.read()

        if ret != True:
            cap.release()
            cv2.destroyAllWindows()
            np.save(os.path.join(temp_dir, "hsv_histograms"), hsv_histograms)
            fd_diff.close()
            fd_mean.close()
            fd_face.close()
            fd_motion.close()
            return

        frame_B_hsv = cv2.cvtColor(frame_B_bgr, cv2.COLOR_BGR2HSV)
        hist = np.array([cv2.calcHist([frame_B_hsv],[i], None, [256], [0, 256]) for i in range(0, 3)]).astype(int).reshape(3, 1, 256)
        hsv_histograms = np.append(hsv_histograms, [hist])

        frame_C_bgr = cv2.absdiff(frame_B_bgr, frame_A_bgr)
        #frame_C_bgr = cv2.blur(frame_C_bgr,(100, 100))

        frame_C_hsv = cv2.cvtColor(frame_C_bgr, cv2.COLOR_BGR2HSV)
        m_c = list(cv2.mean(frame_C_hsv))[:3]
        m_c = [float(x) for x in m_c]
        m_b = list(cv2.mean(frame_B_hsv))[:3]
        m_b = [float(x) for x in m_b]
        fd_diff.write(str(m_c) + "\n")
        fd_mean.write(str(m_b) + "\n")

        next_mean_step = np.array(m_b).reshape(3, 1, 1)
        if len(live_histogram) is 0:
            live_histogram = next_mean_step
        else:
            live_histogram = np.append(live_histogram, next_mean_step, axis=1)
        
        if (do_faces):
            faces = haar_py.getFaces(frame_B_bgr)
            fd_face.write(str(faces) + "\n")
        cv2.imshow('frame', frame_B_bgr)
        cv2.imshow('active_frame', hist_py.hist_curve(frame_B_hsv))
        cv2.imshow('all_frames', hist_py.hist_curve_1d(live_histogram, total_frames))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_A_bgr = frame_B_bgr

path = 'bbt.mp4'

#li = [[x for x in range(0, 100)]]
#ar = np.array(li, dtype=np.uint8)

compare_frame_change(path, False)
