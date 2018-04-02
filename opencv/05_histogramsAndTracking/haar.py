import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('cascades/alt/mouth.xml')
nose_cascade = cv2.CascadeClassifier('cascades/alt/nose.xml')

settings = {
    'scaleFactor': 1.2, 
    'minNeighbors': 8, 
    'minSize': (40, 40),
    'flags': cv2.CASCADE_FIND_BIGGEST_OBJECT|cv2.CASCADE_DO_ROUGH_SEARCH
}
def countDownNeighbours(roi_gray, roi_color, cascade, max_amount, color, start = 12, end = 3, step = 1, drawRect = True):
    step = int((abs(start-end)/(start-end))*abs(step))

    settings['minNeighbors'] = start
    casc = cascade.detectMultiScale(roi_gray, **settings)
    while len(casc) > max_amount and settings['minNeighbors'] > end:
        settings['minNeighbors'] += step
        casc = cascade.detectMultiScale(roi_gray, **settings)
    if (drawRect):
        for (ex,ey,ew,eh) in casc:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh), color,1)
    return casc


def getFaces(img, drawRect = True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    settings['minNeighbors'] = 4
    settings['minSize'] = (40, 40)

    faces = face_cascade.detectMultiScale(gray, **settings)

    face_list = []
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        settings['minSize'] = (12, 12)

        ev = [y + int(h*1/5), y + int(h*4/5), x, x+w]
        eyes = countDownNeighbours(gray[ev[0]:ev[1], ev[2]:ev[3]], img[ev[0]:ev[1], ev[2]:ev[3]], eye_cascade, 2, (255, 255, 128), start = 10, end = 4, step = 1, drawRect = drawRect)

        nv = [y + int(h*2/5), y + int(h*4/5), x + int(w*1/4), x + int(w*3/4)]
        nose = countDownNeighbours(gray[nv[0]:nv[1], nv[2]:nv[3]], img[nv[0]:nv[1], nv[2]:nv[3]], nose_cascade, 1, (255, 128, 255), start = 6, end = 2, step = 2, drawRect = drawRect)

        mv = [y + int(h*3/5), y + int(h*5/5), x + int(w*1/5), x + int(w*4/5)]
        mouth = countDownNeighbours(gray[mv[0]:mv[1], mv[2]:mv[3]], img[mv[0]:mv[1], mv[2]:mv[3]], mouth_cascade, 1, (128, 255, 255), start = 6, end = 2, step = 2, drawRect = drawRect)

        if drawRect:
            img = cv2.rectangle(img,(x,y),(x+w,y+h), (255,0,0), 1)

        if (len(eyes)):
            ice = []
            for eye in eyes:
                ice.append(list(eye))
            eyes = ice
        if (len(nose)):
            nose = nose[0]
        if (len(mouth)):
            mouth = mouth[0]
        face_list.append([[x, y, w, h], list(eyes), list(nose), list(mouth)])
    return face_list


if __name__ == "__main__":
    cap = cv2.VideoCapture("bbt.mp4")

    while(cap.isOpened()):
        #cap.set(1, 100)
        ret, frame = cap.read()

        if ret != True:
            cap.release()
            cv2.destroyAllWindows()
            break
        getFaces(frame)
        cv2.imshow('img', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            