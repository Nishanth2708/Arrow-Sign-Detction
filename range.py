import RPi.GPIO as gpio
import time
import numpy as np
import cv2
import imutils
import os



#Define pin allocation

trig=16
echo=18
img=cv2.imread('cam.jpg')
img=cv2.resize(img,(640,480))

def distance():
	gpio.setmode(gpio.BOARD)
	gpio.setup(trig,gpio.OUT)
	gpio.setup(echo,gpio.IN)	
	
	# Ensure output has no value
	gpio.output(trig,False)
	time.sleep(0.01)
	
	#Generate the trigger pulse

	gpio.output(trig,True)
	time.sleep(0.00001)
	gpio.output(trig,False)
	#Generate echo time signal
	while gpio.input(echo)==0:
		pulse_start=time.time()

	while gpio.input(echo)==1:

		pulse_end=time.time()
	pulse_duration=pulse_end-pulse_start
	
	#Convert time to Distance
	distance=pulse_duration*17150
	distance=round(distance,2)
	
	return distance


if __name__=='__main__':
	try:
		n=1
		lst=[]
		while n<11:
			dist=distance()
			print('Distance:',distance(),'cm')
			n +=1
			time.sleep(1)
			lst.append(dist)
		avg=round(sum(lst)/len(lst),2)
		print('mean',avg)
	except KeyboardInterrupt:
		gpio.cleanup()
cv2.putText(img,'Distance: {}'.format(avg),(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
cv2.imshow('k',img)
cv2.waitKey(0)
