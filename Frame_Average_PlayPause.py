from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import urllib.request
import numpy as np


camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=(640, 480))

display_window = cv2.namedWindow("Faces")

time.sleep(1)

last_mean = 0
cnt = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array
    image = cv2.resize(image, (640,480))

    #Detección
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    result = np.abs(np.mean(gray) - last_mean)
   # print(result)
    if result > 2:
        #print("Motion detected!")
        #print("Started recording.")
        #print("\n")
        cnt = 0
        #contents = urllib.request.urlopen("http://localhost:5005/volume/10").read()
        #contents = urllib.request.urlopen("http://localhost:5005/say/vincent%20buy%20your%20condoms%20").read()
        contents = urllib.request.urlopen("http://localhost:5005/play").read()
    elif cnt < 50:
        #print("Waitformotion")
        cnt+=1
    else:
        #print("NoMotoin")
        contents = urllib.request.urlopen("http://localhost:5005/pause").read()

        
    last_mean= np.mean(gray)


    #Muestra ventana
    cv2.imshow("Faces", image)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    
    if key == ord("q"):
        contents = urllib.request.urlopen("http://localhost:5005/pause").read()
        break
    
camera.close()
cv2.destroyAllWindows()
#countdown_timer.stop()