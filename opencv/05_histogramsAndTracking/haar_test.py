import cv2
from math import sin, cos, radians
from collections import OrderedDict



settings = {
    'scaleFactor': 1.2, 
    'minNeighbors': 8, 
    'minSize': (40, 40),
    'flags': cv2.CASCADE_FIND_BIGGEST_OBJECT|cv2.CASCADE_DO_ROUGH_SEARCH
}

def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    if angle == 0: return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*cos(radians(angle)) + y*sin(radians(angle)) + img.shape[1]*0.4
    newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]

def detectOld(img, cascade, drawRect = True, fast = True, color = (255, 0, 0), width = 1):

    missed_counter = 0
    last_angle = 0
    if (fast):
        detected = cascade.detectMultiScale(img, **settings)
    else:
        angles = list(OrderedDict.fromkeys([last_angle, 0, 10, -10, 20, -20]))
        for angle in angles:
            if angle == -1:
                rimg = img
            else:
                rimg = rotate_image(img, angle)

            detected = cascade.detectMultiScale(rimg, **settings)
            if len(detected):
                if angle != last_angle:
                    print("Changed angle to", angle)
                break

    if len(detected) is 0:
        missed_counter += 1
    else:
        for (x, y, w, h) in detected:
            cv2.rectangle(img, (x, y), (x+w, y+h), color, width)
    return detected

def detect(img, cascade, drawRectImg = None, color = (255, 0, 0), width = 1):
    missed_counter = 0
    detected = cascade.detectMultiScale(img, **settings)
    if len(detected) is 0:
        missed_counter += 1
    else:
        if drawRectImg is not None:
            for (x, y, w, h) in detected:
                cv2.rectangle(img, (x, y), (x+w, y+h), color, width)
    return detected

face = cv2.CascadeClassifier("cascades/haarcascade_frontalface_alt.xml")
face2 = cv2.CascadeClassifier("cascades/haarcascade_frontalface_alt2.xml")
mouth_cascade = cv2.CascadeClassifier('cascades/alt/mouth.xml')
nose_cascade = cv2.CascadeClassifier('cascades/alt/nose.xml')
def detectFace(img):
    imgRect = img
    #detect(img, face2, imgRect, color = (200, 170, 170))
    detect(img, nose_cascade, imgRect, color = (100, 255, 170))





camera =  cv2.VideoCapture("bbt.mp4")
ret, img = camera.read()
while True:
    ret, img = camera.read()
    detectFace(img)
    cv2.imshow('facedetect', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
try:
    a = 1
except:
    cv2.destroyWindow("facedetect")