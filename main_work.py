# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 15:51:37 2024

@author: Aichi
"""

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
# import threading
from sense_hat import SenseHat
import numpy as np
import urllib
import mediapipe as mp
from pynput import keyboard

import display
import countdown

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
    
if __name__ == "__main_work__":
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

display.show_num_wh(2)

listener.stop()