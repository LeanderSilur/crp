import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haar/download/cascade_head.xml')
other_cascade = cv2.CascadeClassifier('haar/builtin/haarcascade_fullbody.xml')
#face_cascade = cv2.CascadeClassifier("myhaar.xml")l
cap = cv2.VideoCapture(0)


def drawRoi(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = other_cascade.detectMultiScale(gray, 1.3, 3)
    #img = gray
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255), 1)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
        #eyes = other_cascade.detectMultiScale(roi_gray)
        #for (ex,ey,ew,eh) in eyes:
        #    cv2.rectangle(gray,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    drawRoi(frame)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
