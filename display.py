# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 15:51:00 2024

@author: Aichi
"""

import numpy as np
from sense_hat import SenseHat


#define all the colors:

O = [0, 0, 0]       # black
X = [100, 100, 100] # white
G = [0, 100, 0]     # green
R = [100, 0, 0]     # red

# define symbols

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

VOLUME_UP = [
  O, O, O, O, O, O, O, O,
  O, O, O, X, X, O, O, O,
  O, O, O, X, X, O, O, O,
  O, X, X, X, X, X, X, O,
  O, X, X, X, X, X, X, O,
  O, O, O, X, X, O, O, O,
  O, O, O, X, X, O, O, O,
  O, O, O, O, O, O, O, O,
  ]

NEXT = [
  O, O, O, O, O, O, O, O,
  O, O, X, O, O, X, O, O,
  O, O, X, X, O, X, O, O,
  O, O, X, X, X, X, O, O,
  O, O, X, X, X, X, O, O,
  O, O, X, X, O, X, O, O,
  O, O, X, O, O, X, O, O,
  O, O, O, O, O, O, O, O,
  ]

PREV = [
  O, O, O, O, O, O, O, O,
  O, O, X, O, O, X, O, O,
  O, O, X, O, X, X, O, O,
  O, O, X, X, X, X, O, O,
  O, O, X, X, X, X, O, O,
  O, O, X, O, X, X, O, O,
  O, O, X, O, O, X, O, O,
  O, O, O, O, O, O, O, O,
  ]

PLAY = [
  O, O, X, O, O, O, O, O,
  O, O, X, X, O, O, O, O,
  O, O, X, O, X, O, O, O,
  O, O, X, O, O, X, O, O,
  O, O, X, O, O, X, O, O,
  O, O, X, O, X, O, O, O,
  O, O, X, X, O, O, O, O,
  O, O, X, O, O, O, O, O,
  ]

PAUSE = [
  O, O, O, O, O, O, O, O,
  O, X, X, O, O, X, X, O,
  O, X, X, O, O, X, X, O,
  O, X, X, O, O, X, X, O,
  O, X, X, O, O, X, X, O,
  O, X, X, O, O, X, X, O,
  O, X, X, O, O, X, X, O,
  O, O, O, O, O, O, O, O,
  ]

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

# define numbers

def define_numbers(O,X):
  numbers = []
  
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
  return numbers

#create number arrays
num_wh = define_numbers(O, X)
num_rd = define_numbers(O, R)
sense = SenseHat()

def show_num_wh(number):
    sense.set_pixels(num_wh[number])
def show_num_rd(number):
    sense.set_pixels(num_rd[number])
def show_vol_dwn():
    sense.set_pixels(VOLUME_DOWN)
def show_vol_up():
    sense.set_pixels(VOLUME_UP)
def show_next():
    sense.set_pixels(NEXT)
def show_prev():
    sense.set_pixels(PREV)
def show_play():
    sense.set_pixels(PLAY)
def show_pause():
    sense.set_pixels(PAUSE)
def show_green():
    sense.set_pixels(FULL_GREEN)
def show_rd():
    sense.set_pixels(FULL_RED)
def get_pixels():
    return sense.get_pixels()
def show_clear():
    sense.clear()