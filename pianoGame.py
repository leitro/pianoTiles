import cv2
import numpy as np
import os
import pyscreenshot as ss
import time

def onMouse(event, x, y, flags, param):
    global flag, pLeftTop, pRightBottom
    if event == cv2.EVENT_LBUTTONDOWN:
        if flag:
            pLeftTop = (x,y)
        else:
            pRightBottom = (x,y)
        flag = False

flag = True
pLeftTop = None
pRightBottom = None

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', onMouse)

img = ss.grab(bbox=(0,0,1300,768))
img = np.array(img)
cv2.imshow('frame', img)
if cv2.waitKey(0) & 0xff == ord(' '):
    cv2.destroyAllWindows()
count = 0 #Avoid running endlessly.
while True:
    t0 = time.time()
    img = ss.grab(bbox=(pLeftTop[0],pLeftTop[1],pRightBottom[0],pRightBottom[1]), childprocess=False, backend='imagemagick') #'imagemagick' runs fastest acording my test.
    t1 = time.time()
    print(round(t1-t0, 2))
    target = np.array(img)
    print(target.shape)
    if target.shape[-1] != 3:
        gray = target.reshape((target.shape[0],target.shape[1],1))
    else:
        gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    if gray[1,1] < 150 and gray[1,1] > 130: #The Grayscale value of green background in the finishing page is 140
        break
    ret, thresh = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY_INV)
    thresh = cv2.erode(thresh, None, iterations=5)
    im, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    num = 0
    for c in contours:
        topMost = tuple(c[c[:,:,1].argmin()][0])
        bottomMost = tuple(c[c[:,:,1].argmax()][0])
        if bottomMost[1]-topMost[1] < 50:
            continue
        pointX = int(bottomMost[0])
        pointY = int(bottomMost[1])
        cv2.circle(thresh, (pointX, pointY), 2, 125, 2)
        realX = pointX + pLeftTop[0]
        realY = pointY + pLeftTop[1]
        os.system('xdotool mousemove '+ str(realX)+' '+str(realY))
        os.system('xdotool click 1')
        print(realX, realY)
        count += 1
    if count >= 12345:
        break
    #cv2.imwrite(str(count)+'.png', thresh)
    #cv2.imwrite(str(count)+'.1.png',target)
    time.sleep(0.1)
