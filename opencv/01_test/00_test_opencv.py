from datetime import datetime
import numpy as np
import cv2





def playVideo():
    #in
    cap = cv2.VideoCapture('cubeA.mov')

    width = int(cap.get(3))   # float
    height = int(cap.get(4)) # float
    fps = cap.get(5)
    frames = cap.get(7)
    print(width, height, fps)
    #out
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, fps, (width,height))

    while(cap.isOpened()):
        ret, frame = cap.read()

        if ret != True:
            cap.release()
            cv2.destroyAllWindows()
            return

        out.write(frame)
        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
playVideo()