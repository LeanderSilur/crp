import numpy as np
import cv2
from matplotlib import pyplot as plt


# Initiate STAR detector
orb = cv2.ORB_create()


def drawKeyPoints(img):
    pass
def detectKeyPoints(img):
    # find the keypoints with ORB
    kp = orb.detect(img, None)
    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)

    print(len(kp), " > ", end ='')
    i = 0
    while i < len(kp):
        #print(k.angle, k.class_id, k.octave, k.pt, k.response, k.size)
        if (kp[i].size < 100) or (kp[i].angle < 2) or (kp[i].angle > 2.5):
            del kp[i]
        else:
            i += 1
    print(len(kp))
    kp = kp[-10:]
    # draw only keypoints location,not size and orientation
    return cv2.drawKeypoints(img, kp, None, color=(0,255,0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

def drawMatches(img1, img2):
    # find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1,des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
    # Draw first 10 matches.
    img3 = img1
    #cv2.drawMatches(img1,kp1,img2,kp2,matches[:10], img3, flags=4)
    img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, img3, flags=2)
    return img3


if __name__ == "__main__":
    path = 'jp.mp4'
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL )
    #in
    cap = cv2.VideoCapture(path)
    print(dir(cap))
    ret, frame_A = cap.read()
    frame_B = frame_A


    while(cap.isOpened()):
        ret, frame_B = cap.read()

        if ret != True:
            cap.release()
            cv2.destroyAllWindows()
            exit()
        frame = drawKeyPoints(frame_B)
        frame = drawMatches(frame_A, frame_B)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_A = frame_B


