import cv2
from cv2 import resize
import imutils
import numpy as np

bg_subtractor = cv2.createBackgroundSubtractorKNN(detectShadows=True)
erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))

maxima = 0
centers = []
pred = []
n = 0

def slope(x1,x2,y1,y2):
    s = (x1-x2)-(y1-y2)
    return s


cap = cv2.VideoCapture('http://192.168.1.23:8080/video')
success, frame = cap.read()

while success:
    success, frame = cap.read()
    frame = resize(frame,(0,0),None, 0.5,0.5)
    # frame = cv2.flip(frame, 1)
    fg_mask = bg_subtractor.apply(frame)
    _, thresh = cv2.threshold(fg_mask, 35, 255, cv2.THRESH_BINARY)
    cv2.erode(thresh, erode_kernel, thresh, iterations=2)
    cv2.dilate(thresh, dilate_kernel, thresh, iterations=2)
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(contours)
    try:
        c = max(cnts, key=cv2.contourArea)
        (x, y), r = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        centers.append(center)
        cv2.circle(frame, (int(x), int(y)), int(r),(0, 255, 255), 2)
        for i in range(len(centers)-1):
            cv2.circle(frame, centers[i], 3, (0, 0, 255), -1)
            cv2.line(frame, centers[i],centers[i+1], (0, 0, 255), 1)
        if len(centers) > 2:
            x_t = []
            y_t = []
            for cen in range(len(centers)):
                y_t.append(centers[cen][0])
                x_t.append(centers[cen][1])
            s1 = slope(x_t[-1],x_t[-2],y_t[-1],y_t[-2])
            s2 = slope(x_t[-2],x_t[-3],y_t[-2],y_t[-3])
            if x_t[-1] - x_t[-2] > 5:
                if abs(s1 - s2) > 50:
                    del x_t[-1]
                    del y_t[-1]
                    del centers [-1]
                mymodel = np.poly1d(np.polyfit(y_t, x_t, 2))
                for x_p in range(1920):
                    pred.append((x_p,int(mymodel(x_p))))
                for i in range(len(pred)):
                    cv2.circle(frame, pred[i], 1, (0, 255, 0), cv2.FILLED)
            
        pred = []
        # cv2.imshow('mog', fg_mask)
        # cv2.imshow('thresh', thresh)
        cv2.imshow('detection', frame)
        frame = resize(frame,(0,0),None, 2,2)
        cv2.imwrite(f"ball{n}.png",frame)
        n = n + 1

    except:
        centers = []
        pred = []
        # cv2.imshow('mog', fg_mask)
        # cv2.imshow('thresh', thresh)
        cv2.imshow('detection', frame)

    if cv2.waitKey(1) == ord('q'): # Escape
        break

cap.release()
cv2.destroyAllWindows()