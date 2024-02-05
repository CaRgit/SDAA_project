from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import threading
from sense_hat import SenseHat
import numpy as np
import urllib

G = [0, 100, 0]
FULL_GREEN = [
  G, G, G, G, G, G, G, G,
  G, G, G, G, G, G, G, G,
  G, G, G, G, G, G, G, G,
  G, G, G, G, G, G, G, G,
  G, G, G, G, G, G, G, G,
  G, G, G, G, G, G, G, G,
  G, G, G, G, G, G, G, G,
  G, G, G, G, G, G, G, G
  ]

R = [100, 0, 0]
FULL_RED = [
  R, R, R, R, R, R, R, R,
  R, R, R, R, R, R, R, R,
  R, R, R, R, R, R, R, R,
  R, R, R, R, R, R, R, R,
  R, R, R, R, R, R, R, R,
  R, R, R, R, R, R, R, R,
  R, R, R, R, R, R, R, R,
  R, R, R, R, R, R, R, R
  ]

def define_numbers(O,X):
  global numbers
  
  B=[0,0,100]
  
  VOID = np.array([
  [O],
  [O],
  [O],
  [O],
  [O],
  [O],
  [O],
  [O],
  ])

  OVER99 = np.array([
  [B],
  [O],
  [O],
  [O],
  [O],
  [O],
  [O],
  [O],
  ])
  
  DIGITS = [
  np.array([
  [O, O, O],
  [X, X, X],
  [X, O, X],
  [X, O, X],
  [X, O, X],
  [X, O, X],
  [X, O, X],
  [X, X, X],
  ]),
    
  np.array([
  [O, O, O],
  [O, O, X],
  [O, O, X],
  [O, O, X],
  [O, O, X],
  [O, O, X],
  [O, O, X],
  [O, O, X],
  ]),
    
  np.array([
  [O, O, O],
  [X, X, X],
  [O, O, X],
  [O, O, X],
  [X, X, X],
  [X, O, O],
  [X, O, O],
  [X, X, X],
  ]),
    
  np.array([
  [O, O, O],
  [X, X, X],
  [O, O, X],
  [O, O, X],
  [X, X, X],
  [O, O, X],
  [O, O, X],
  [X, X, X],
  ]),
    
  np.array([
  [O, O, O],
  [X, O, X],
  [X, O, X],
  [X, O, X],
  [X, X, X],
  [O, O, X],
  [O, O, X],
  [O, O, X],
  ]),

  np.array([
  [O, O, O],
  [X, X, X],
  [X, O, O],
  [X, O, O],
  [X, X, X],
  [O, O, X],
  [O, O, X],
  [X, X, X],
  ]),
    
  np.array([
  [O, O, O],
  [X, X, X],
  [X, O, O],
  [X, O, O],
  [X, X, X],
  [X, O, X],
  [X, O, X],
  [X, X, X],
  ]),
    
  np.array([
  [O, O, O],
  [X, X, X],
  [O, O, X],
  [O, O, X],
  [O, O, X],
  [O, O, X],
  [O, O, X],
  [O, O, X],
  ]),
    
  np.array([
  [O, O, O],
  [X, X, X],
  [X, O, X],
  [X, O, X],
  [X, X, X],
  [X, O, X],
  [X, O, X],
  [X, X, X],
  ]),
    
  np.array([
  [O, O, O],
  [X, X, X],
  [X, O, X],
  [X, O, X],
  [X, X, X],
  [O, O, X],
  [O, O, X],
  [X, X, X],
  ]),
  ]
  
  numbers = []
  
  for num in range(10000):
      if num < 10:
          numbers_aux = np.concatenate((VOID, VOID, VOID, VOID, VOID, DIGITS[num]),1)
          numbers_aux = numbers_aux.reshape(64,3)
          numbers.append(numbers_aux.tolist())
      elif num <100:
          numbers_aux = np.concatenate((VOID,DIGITS[int((num%100)/10)],VOID,DIGITS[(num%100)%10]),1)
          numbers_aux = numbers_aux.reshape(64,3)
          numbers.append(numbers_aux.tolist())
      else:
          numbers_aux = np.concatenate((OVER99,DIGITS[int((num%100)/10)],VOID,DIGITS[(num%100)%10]),1)
          numbers_aux = numbers_aux.reshape(64,3)
          numbers.append(numbers_aux.tolist())

define_numbers([0, 0, 0], [100, 100, 100])

class CountdownTimer:
    def __init__(self):
        self.timer_thread = None
        self.is_running = False
        self.lock = threading.Lock()
        self.sense=SenseHat()

    def start(self, new_time):
        with self.lock:
            #self.sense.clear()
            #self.sense.set_pixels(FULL_GREEN)
            self.time_remaining = new_time+3
            self.new_time = new_time
            #time.sleep(3)
            if not self.is_running:
                self.is_running = True
                self.timer_thread = threading.Thread(target=self._run_timer)
                self.timer_thread.start()
            
    def stop(self):
        with self.lock:
            self.is_running = False
            time.sleep(1)
            self.sense.clear()
            self.sense.set_pixels(FULL_RED)

    def _run_timer(self):
        while self.is_running and self.time_remaining > 0:
            with self.lock:
                self.sense.clear()
                if self.time_remaining > self.new_time:
                    self.sense.set_pixels(FULL_GREEN)
                elif self.time_remaining > 5:
                    self.sense.set_pixels(numbers[self.time_remaining])
                else:
                    number_red = numbers[self.time_remaining]
                    for index,rgb in enumerate(number_red):
                        number_red[index][1] *= 0
                        number_red[index][2] *= 0
                    self.sense.set_pixels(number_red)
                self.time_remaining -= 1
                #print(f"Time remaining: {self.time_remaining} seconds")
            time.sleep(1)
        self.is_running = False
        self.sense.clear()
        self.sense.set_pixels(FULL_RED)
        #print("Countdown complete!")

#camera = PiCamera()
#camera.resolution = (640, 480)
#camera.framerate = 30
#camera.rotation = 180
#rawCapture = PiRGBArray(camera, size=(640, 480))

#display_window = cv2.namedWindow("Faces")

#hog = cv2.HOGDescriptor()
#hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#time.sleep(1)

#timer_secs = 110
#countdown_timer = CountdownTimer()

#ispaused = False
#mode = "spotify"

#for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

#    image = frame.array
#    image = cv2.resize(image, (640,480))

    #Detección
#    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#    boxes, weights = hog.detectMultiScale(image, winStride=(8,8) )
#    for (x,y,w,h) in boxes:
#        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

    #Muestra ventana
#    cv2.imshow("Faces", image)
#    key = cv2.waitKey(1) & 0xFF
#    rawCapture.truncate(0)
    
#    if len(boxes) > 0:
#        print ("Human detected")
#        countdown_timer.start(new_time = timer_secs)
      
#    events = sense.stick.get_events()
#    if events:
#        if mode == "spotify":
#            for event in events:
#                if event.direction  == "middle" and event.action != "released" and ispaused:
#                    urllib.request.urlopen('localhost:5005/play')
#                    ispaused = False
#                if event.direction  == "middle" and event.action != "released" and !ispaused:
#                    urllib.request.urlopen('localhost:5005/pause')
#                    ispaused = True
#                if event.direction  == "right" and event.action != "released":
#                    urllib.request.urlopen('localhost:5005/next')
#                if event.direction  == "left" and event.action != "released":
#                    urllib.request.urlopen('localhost:5005/previous')
#                if event.direction  == "up" and event.action != "released":
#                    urllib.request.urlopen('localhost:5005/volume/+5')
#                if event.direction  == "down" and event.action != "released":
#                    urllib.request.urlopen('localhost:5005/volume/-5')
#        elif mode == "modify_timer":
#                if event.direction  == "up" and event.action != "released":
#                    timer_secs += 1
#                if event.direction  == "down" and event.action != "released":
#                    if timer_secs > 0:
#                        timer_secs -= 1
#        countdown_timer.start(new_time = timer_secs)

#    if key == ord("q"):
#        break
    
#camera.close()
#cv2.destroyAllWindows()
#countdown_timer.stop()
