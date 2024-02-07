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
#import numpy as np
import urllib
import mediapipe as mp
from pynput import keyboard
import os
import subprocess
import sys

import display
import countdown

stop = False
debug = False

def on_press(key):
    global stop
    try:
        if key.char == 'q':
            #print("La tecla 'q' ha sido presionada. Saliendo del programa.")
            stop = True
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
  os.chdir('./SonosAPI')
  subprocess.Popen('npm start', shell = True)
  
  time.sleep(2)
  
cont_play = True
ispaused = True
timer_secs = 10
show_secs = 1
count = countdown.CountdownTimer()
# count.start(new_time = timer_secs)
showtimer = countdown.DisplayTimer()
display.show_pause()
try:
    urllib.request.urlopen("http://localhost:5005/pause").read()
except:
    print("API Error")
    camera.close()
    listener.stop()
    display.show_clear()    
    sys.exit()
held_released=True


while not stop:
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
                try:
                    urllib.request.urlopen("http://localhost:5005/play").read()
                except:
                    print("API Error")
                ispaused = False
                display.show_play()
                #print('Estaba pausado y se ha pulsado el play')
                #print('contents: ', contents)
            elif event.direction  == "middle" and event.action == "pressed" and not ispaused:
                try:
                    urllib.request.urlopen("http://localhost:5005/pause").read()
                except:
                    print("API Error")
                ispaused = True
                display.show_pause()
                #print('Estaba sonando y se ha pulsado el pause')
                #print('contents: ', contents)
            if event.direction  == "middle" and event.action == "held" and held_released:
                cont_play = False
                held_released = False
            if event.direction  == "middle" and event.action == "released":
                held_released = True
            if event.direction  == "right" and event.action == "pressed":
                try:
                    urllib.request.urlopen("http://localhost:5005/next").read()
                    urllib.request.urlopen("http://localhost:5005/play").read()
                except:
                    print("API Error")
                ispaused = False
                display.show_next()
                showtimer.start(new_time = show_secs)
                #countdown_timer.start(new_time = timer_secs)
            if event.direction  == "left" and event.action == "pressed":
                try:
                    urllib.request.urlopen("http://localhost:5005/previous").read()
                    urllib.request.urlopen("http://localhost:5005/play").read()
                except:
                    print("API Error")
                ispaused = False
                display.show_prev()
                showtimer.start(new_time = show_secs)
                #countdown_timer.start(new_time = timer_secs)
            if event.direction  == "up" and event.action != "released":
                try:
                    urllib.request.urlopen("http://localhost:5005/volume/+1").read()
                except:
                    print("API Error")
                display.show_vol_up()
                showtimer.start(new_time = show_secs)
            if event.direction  == "down" and event.action != "released":
                try:
                    urllib.request.urlopen("http://localhost:5005/volume/-1").read()
                except:
                    print("API Error")
                display.show_vol_dwn()
                showtimer.start(new_time = show_secs)
    else:
        switch_mode = False
        if debug:
            cv2.startWindowThread()
            cv2.namedWindow("detection")
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            image = frame.array
            image = cv2.resize(image, (640,480))
              # Convert the frame to RGB
            frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
          
              # Process the frame with MediaPipe Pose
            result = pose.process(frame_rgb)
            
            if result.pose_landmarks and not ispaused:
                if debug:
                    mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    
                if not showtimer.is_running:
                    display.show_green()
                if not count.is_running:
                    try:
                       contents = urllib.request.urlopen("http://localhost:5005/play").read()
                    except:
                       print("API Error")
                    display.show_green()
                count.start(new_time = timer_secs)
                if showtimer.flag:
                    showtimer.flag = False
                    display.show_green()
            elif ispaused and showtimer.flag:
                display.show_pause()
                showtimer.flag = False
            elif count.flag and not ispaused:
                display.show_rd()
                try:
                    urllib.request.urlopen("http://localhost:5005/pause").read()
                except:
                    print("API Error")
                count.flag = False
            #    #reset timer
          #  elif #gettimer > 10
            
            
            #display.show_num_wh(2)
            
            events = sense.stick.get_events()
            for event in events:
                if event.direction  == "middle" and event.action == "held" and held_released:
                    cont_play = True
                    held_released = False
                    switch_mode = True
                if event.direction  == "middle" and event.action == "released":
                    held_released = True
                if event.direction  == "middle" and event.action == "pressed" and ispaused:
                    try:
                        urllib.request.urlopen("http://localhost:5005/play").read()
                    except:
                        print("API Error")
                    ispaused = False
                    count.start(new_time = timer_secs)
                    display.show_green()
                    #print('Estaba pausado y se ha pulsado el play')
                    #print('contents: ', contents)
                elif event.direction  == "middle" and event.action == "pressed" and not ispaused:
                    try:
                        urllib.request.urlopen("http://localhost:5005/pause").read()
                    except:
                        print("API Error")
                    ispaused = True
                    count.stop()
                    display.show_pause()
                    #print('Estaba sonando y se ha pulsado el pause')
                if event.direction  == "right" and event.action == "pressed":
                    try:
                        urllib.request.urlopen("http://localhost:5005/next").read()
                        urllib.request.urlopen("http://localhost:5005/play").read()
                    except:
                        print("API Error")
                    ispaused = False
                    display.show_next()
                    showtimer.start(new_time = show_secs)
                    #countdown_timer.start(new_time = timer_secs)
                if event.direction  == "left" and event.action == "pressed":
                    try:
                        urllib.request.urlopen("http://localhost:5005/previous").read()
                        urllib.request.urlopen("http://localhost:5005/play").read()
                    except:
                        print("API Error")
                    ispaused = False
                    display.show_prev()
                    showtimer.start(new_time = show_secs)
                    #countdown_timer.start(new_time = timer_secs)
                if event.direction  == "up" and event.action != "released":
                    try:
                        urllib.request.urlopen("http://localhost:5005/volume/+1").read()
                    except:
                        print("API Error")
                    display.show_vol_up()
                    showtimer.start(new_time = show_secs)
                if event.direction  == "down" and event.action != "released":
                    try:
                        urllib.request.urlopen("http://localhost:5005/volume/-1").read()
                    except:
                        print("API Error")
                    display.show_vol_dwn()
                    showtimer.start(new_time = show_secs)
            #print('contents: ', contents)
            if debug:
                cv2.imshow("detection", image)
            rawCapture.truncate(0)
            if stop or switch_mode:
                break
try:
    urllib.request.urlopen("http://localhost:5005/pause").read()
except:
    print("API Error")
showtimer.stop()
count.stop()        
listener.stop()
cv2.destroyAllWindows()
display.show_clear()
camera.close()