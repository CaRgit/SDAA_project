
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
from pynput import keyboard

import body_detection

O = [0, 0, 0]
X = [100, 100, 100]
VOLUME_DOWN = [
  O, O, O, O, O, O, O, O,
  O, O, O, O, O, O, O, O,
  O, O, O, O, O, O, O, O,
  O, X, X, X, X, X, X, O,
  O, X, X, X, X, X, X, O,
  O, O, O, O, O, O, O, O,
  O, O, O, O, O, O, O, O,
  O, O, O, O, O, O, O, O
  ]

exit = False

def on_press(key):
    global exit
    try:
        if key.char == 'q':
            #print("La tecla 'q' ha sido presionada. Saliendo del programa.")
            exit = True
    except AttributeError:
        # Ignorar si la tecla no es un carácter (por ejemplo, una tecla especial)
        pass

if __name__ == "__main__":
  print("Bienvenido al proyecto de integración de Raspberry Pi con altavoz SONOS")
  listener = keyboard.Listener(on_press=on_press)
  listener.start()
  camera = PiCamera()
  camera.resolution = (640, 480)
  camera.framerate = 30
  camera.rotation = 180
  rawCapture = PiRGBArray(camera, size=(640, 480))

  #display_window = cv2.namedWindow("Body")

  time.sleep(1)
  
  # Initialize MediaPipe Pose and Drawing utilities
  mp_pose = mp.solutions.pose
  mp_drawing = mp.solutions.drawing_utils
  pose = mp_pose.Pose()

  timer_secs = 10
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
      if not ispaused:
          if countdown_timer.is_running == False:
              urllib.request.urlopen("http://localhost:5005/pause").read()
          if result.pose_landmarks:
              if countdown_timer.is_running == True:
                  countdown_timer.start(new_time = timer_secs)
              else:
                  countdown_timer.start(new_time = timer_secs)
                  urllib.request.urlopen("http://localhost:5005/play").read()
              #mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
              #print ("Human detected")
      events = sense.stick.get_events()
      for event in events:
          print('Procesando event')
          if event.direction  == "middle" and event.action == "pressed" and ispaused:
              contents = urllib.request.urlopen("http://localhost:5005/play").read()
              ispaused = False
              countdown_timer.start(new_time = timer_secs)
              print('Estaba pausado y se ha pulsado el play')
              print('contents: ', contents)
          elif event.direction  == "middle" and event.action == "pressed" and not ispaused:
              contents = urllib.request.urlopen("http://localhost:5005/pause").read()
              ispaused = True
              #countdown_timer.start(new_time = 0)
              countdown_timer.stop()
              print('Estaba sonando y se ha pulsado el pause')
              print('contents: ', contents)
          if event.direction  == "right" and event.action == "pressed":
              urllib.request.urlopen("http://localhost:5005/next").read()
              urllib.request.urlopen("http://localhost:5005/play").read()
              ispaused = False
              countdown_timer.start(new_time = timer_secs)
          if event.direction  == "left" and event.action == "pressed":
              urllib.request.urlopen("http://localhost:5005/previous").read()
              urllib.request.urlopen("http://localhost:5005/play").read()
              ispaused = False
              countdown_timer.start(new_time = timer_secs)
          if event.direction  == "up" and event.action != "released":
              urllib.request.urlopen("http://localhost:5005/volume/+1").read()
              if not ispaused:
                  countdown_timer.start(new_time = timer_secs)
          if event.direction  == "down" and event.action != "released":
              urllib.request.urlopen("http://localhost:5005/volume/-1").read()
              if not ispaused:
                  countdown_timer.start(new_time = timer_secs)
              countdown.update_volume_down()
    
      # Display the frame
      #cv2.imshow("Body", image)
      rawCapture.truncate(0)
  
      # Exit if 'q' key is pressed
      if exit:
          print("Cerrando camara")
          camera.close()
          break

  #cv2.destroyAllWindows()
  countdown_timer.stop()
  listener.stop()
  
