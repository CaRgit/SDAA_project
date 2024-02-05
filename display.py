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
def show_green():
    sense.set_pixels(FULL_GREEN)
def show_rd():
    sense.set_pixels(FULL_RED)
