from picamera.array import PiRGBArray
import numpy as np
from picamera import PiCamera
import time
import datetime
from datetime import datetime
import cv2
from imutils.video import VideoStream
import imutils

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

#Define the codec
today = time.strftime("%Y%m%d-%H%M%S")
fps_out = 17
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(today + ".avi", fourcc, fps_out, (640, 480))

#Read image and Convert to HSV
#cap = VideoStream(0)

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 40)
fontScale = 1
fontColor = (255, 0, 0)
lineType = 2

lst = []
lst1 = []
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Capture frame-by-frame
    frame=frame.array
    timer = cv2.getTickCount()

    rawCapture.truncate(0)

    # img=cv2.imread('hw4arrow.JPG')
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # Defining range of Green
    lower_green = np.array([51, 42, 47])
    upper_green = np.array([80, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
   # cv2.imshow('masked',mask)
    mask=cv2.GaussianBlur(mask,(3,3),1)

    # Corner Detection

    # corners=cv2.Canny(mask,100,200)
    corners = cv2.goodFeaturesToTrack(mask,7,0.1,5)
    if corners is None:
        continue
    else:
        corners=np.int0(corners)

    for corner in corners:
        x,y = corner.ravel()
        cv2.circle(frame,(x,y),3,255,-1)
        #cv2.putText(frame, "({},{})".format(x, y), (int(x - 50), int(y - 10) - 20),
        #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        lst.append(x)
        lst1.append(y)
        points_x = np.asarray(lst)
        points_y = np.asarray(lst1)

        arrow_mid_x = int((np.max(points_x) + np.min(points_x)) / 2)
        arrow_dist_x = np.max(points_x) - np.min(points_x)

        arrow_mid_y = int((np.max(points_y) + np.min(points_y)) / 2)
        arrow_dist_y = np.max(points_y) - np.min(points_y)

        if arrow_dist_x > arrow_dist_y:
            west_corners = 0
            east_corners = 0

            for corner in corners:
                x, y = corner.ravel()
                if x < int(arrow_mid_x):
                    west_corners += 1
                else:
                    east_corners += 1

            if west_corners > east_corners:
                orientation = print('West')
                cv2.putText(frame, 'WEST',
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            lineType)
            else:
                orientation = print('East')
                cv2.putText(frame, 'EAST',
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            lineType)
        else:
            north_corners = 0
            south_corners = 0

            for corner in corners:
                x, y = corner.ravel()
                if y < int(arrow_mid_y):
                    north_corners += 1
                else:
                    south_corners += 1

            if north_corners > south_corners:
                orientation = print('North')
                cv2.putText(frame, 'NORTH',
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            lineType)
            else:
                orientation = print('South')
                cv2.putText(frame, 'SOUTH',
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            lineType)
    
    #frame=imutils.resize(frame,(640))
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)   
    cv2.imshow('frame',frame)
   # cv2.waitKey(60)
    key=cv2.waitKey(1) & 0xFF
    out.write(frame)
    #rawCapture.truncate(0)
    #rawCapture.seek(0)
    #print(fps)
    if key==ord('q'):
    	break    

