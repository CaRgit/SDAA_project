
#!/usr/bin/env python
# coding: utf-8

# In[1]:
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import threading
from sense_hat import SenseHat
import numpy as np
import urllib
import mediapipe as mp

import body_detection

if __name__ == "__main__":
  camera = PiCamera()
  camera.resolution = (640, 480)
  camera.framerate = 30
  camera.rotation = 180
  rawCapture = PiRGBArray(camera, size=(640, 480))

  display_window = cv2.namedWindow("Body")

  time.sleep(1)
  
  # Initialize MediaPipe Pose and Drawing utilities
  mp_pose = mp.solutions.pose
  mp_drawing = mp.solutions.drawing_utils
  pose = mp_pose.Pose()

  timer_secs = 110
  countdown_timer = body_detection.CountdownTimer()
  
  ispaused = False

  sense = SenseHat()

  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

      image = frame.array
      image = cv2.resize(image, (640,480))
  
      # Convert the frame to RGB
      frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  
      # Process the frame with MediaPipe Pose
      result = pose.process(frame_rgb)
  
      # Draw the pose landmarks on the frame
      if result.pose_landmarks:
          mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
          print ("Human detected")
          countdown_timer.start(new_time = timer_secs)
      events = sense.stick.get_events()
      for event in events:
          print('Procesando event')
          if event.direction  == "middle" and event.action == "pressed" and ispaused:
              contents = urllib.request.urlopen("http://localhost:5005/play").read()
              ispaused = False
              print('Estaba pausado y se ha pulsado el play')
              print('contents: ', contents)
          elif event.direction  == "middle" and event.action == "pressed" and not ispaused:
              contents = urllib.request.urlopen("http://localhost:5005/pause").read()
              ispaused = True
              print('Estaba sonando y se ha pulsado el pause')
              print('contents: ', contents)
          if event.direction  == "right" and event.action != "released":
              urllib.request.urlopen("http://localhost:5005/next").read()
          if event.direction  == "left" and event.action != "released":
              urllib.request.urlopen("http://localhost:5005/previous").read()
          if event.direction  == "up" and event.action != "released":
              urllib.request.urlopen("http://localhost:5005/volume/+5").read()
          if event.direction  == "down" and event.action != "released":
              urllib.request.urlopen("http://localhost:5005/volume/-5").read()
    
      # Display the frame
      cv2.imshow("Body", image)
      rawCapture.truncate(0)
  
      # Exit if 'q' key is pressed
      if cv2.waitKey(1) & 0xFF == ord('q'):
          camera.close()
          break

  cv2.destroyAllWindows()
  countdown_timer.stop()
  
