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
  
  sense = SenseHat()
  
cont_play = True
ispaused = True
timer_secs = 10
show_secs = 1
count = countdown.CountdownTimer()
# count.start(new_time = timer_secs)
showtimer = countdown.DisplayTimer()
display.show_rd()
contents = urllib.request.urlopen("http://localhost:5005/pause").read()
held_released=True


while not exit:
    if cont_play:
        # display.show_rd()
        if ispaused and showtimer.flag:
                display.show_pause()
                showtimer.flag = False
        if not ispaused and showtimer.flag:
                display.show_play()
                showtimer.flag = False
        events = sense.stick.get_events()
        for event in events:
            # print('Procesando event')
            if event.direction  == "middle" and event.action == "pressed" and ispaused:
                contents = urllib.request.urlopen("http://localhost:5005/play").read()
                ispaused = False
                display.show_play()
                print('Estaba pausado y se ha pulsado el play')
                print('contents: ', contents)
            elif event.direction  == "middle" and event.action == "pressed" and not ispaused:
                contents = urllib.request.urlopen("http://localhost:5005/pause").read()
                ispaused = True
                display.show_pause()
                print('Estaba sonando y se ha pulsado el pause')
                print('contents: ', contents)
            if event.direction  == "middle" and event.action == "held" and held_released:
                cont_play = False
                held_released = False
            if event.direction  == "middle" and event.action == "released":
                held_released = True
            if event.direction  == "right" and event.action == "pressed":
                urllib.request.urlopen("http://localhost:5005/next").read()
                urllib.request.urlopen("http://localhost:5005/play").read()
                ispaused = False
                display.show_next()
                showtimer.start(new_time = show_secs)
                #countdown_timer.start(new_time = timer_secs)
            if event.direction  == "left" and event.action == "pressed":
                urllib.request.urlopen("http://localhost:5005/previous").read()
                urllib.request.urlopen("http://localhost:5005/play").read()
                ispaused = False
                display.show_prev()
                showtimer.start(new_time = show_secs)
                #countdown_timer.start(new_time = timer_secs)
            if event.direction  == "up" and event.action != "released":
                urllib.request.urlopen("http://localhost:5005/volume/+1").read()
                display.show_vol_up()
                showtimer.start(new_time = show_secs)
            if event.direction  == "down" and event.action != "released":
                urllib.request.urlopen("http://localhost:5005/volume/-1").read()
                display.show_vol_dwn()
                showtimer.start(new_time = show_secs)
    else:
        count.start(new_time = timer_secs)
        display.show_green()
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            image = frame.array
            image = cv2.resize(image, (640,480))
          
              # Convert the frame to RGB
            frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
          
              # Process the frame with MediaPipe Pose
            result = pose.process(frame_rgb)
            
            if result.pose_landmarks and not ispaused:
                count.start(new_time = timer_secs)
                if showtimer.flag:
                    showtimer.flag = False
                    display.show_green()
            elif ispaused and showtimer.flag:
                display.show_pause()
                showtimer.flag = False
            elif count.flag and not ispaused:
                display.show_rd()
                contents = urllib.request.urlopen("http://localhost:5005/pause").read()
                count.flag = False
            #    #reset timer
          #  elif #gettimer > 10
            
            
            #display.show_num_wh(2)
            
            events = sense.stick.get_events()
            for event in events:
                if event.direction  == "middle" and event.action == "held" and held_released:
                    cont_play = True
                    display.show_play()
                    held_released = False
                if event.direction  == "middle" and event.action == "released":
                    held_released = True
                if event.direction  == "middle" and event.action == "pressed" and ispaused:
                    contents = urllib.request.urlopen("http://localhost:5005/play").read()
                    ispaused = False
                    display.show_green()
                    #print('Estaba pausado y se ha pulsado el play')
                    #print('contents: ', contents)
                elif event.direction  == "middle" and event.action == "pressed" and not ispaused:
                    contents = urllib.request.urlopen("http://localhost:5005/pause").read()
                    ispaused = True
                    count.stop()
                    display.show_pause()
                    #print('Estaba sonando y se ha pulsado el pause')
                    #print('contents: ', contents)
            rawCapture.truncate(0)
            if exit:
                break

        
listener.stop()
camera.close()