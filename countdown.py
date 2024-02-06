# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 15:50:38 2024

@author: Aichi
"""
import threading
import time
import urllib

import display

class CountdownTimer:
    def __init__(self):
        self.timer_thread = None
        self.is_running = False
        self.lock = threading.Lock()
        self.flag = False
        #self.sense=SenseHat()
        #self.volume_down = False
      
    #def update_volume_down(self):
    #    self.volume_down = True

    def start(self, new_time):
        with self.lock:
            #self.sense.clear()
            #self.sense.set_pixels(FULL_GREEN)
            self.time_remaining = new_time + 3
            self.new_time = new_time
            self.flag = False
            #time.sleep(3)
            if not self.is_running:
                self.is_running = True
                self.timer_thread = threading.Thread(target=self._run_timer)
                self.timer_thread.start()
            
    def stop(self):
        with self.lock:
            self.is_running = False
      #      time.sleep(1)
      #      self.sense.clear()
      #      self.sense.set_pixels(FULL_RED)

    def _run_timer(self):
        while self.is_running and self.time_remaining > 0:
            with self.lock:
      #          self.sense.clear()
                if self.time_remaining < self.new_time:
       #             if self.volume_down:
        #                self.sense.set_pixels(VOLUME_DOWN)
       #             else:
        #              self.sense.set_pixels(FULL_GREEN)
        #        else:
         #           self.volume_down = False
                    if self.time_remaining > 5:
                        display.show_num_wh(self.time_remaining)
        #              self.sense.set_pixels(numbers[self.time_remaining])
                    else:
                        display.show_num_rd(self.time_remaining)
        #                for index,rgb in enumerate(number_red):
        #                    number_red[index][1] *= 0
        #                    number_red[index][2] *= 0
        #                self.sense.set_pixels(number_red)
                self.time_remaining -= 1
                #print(f"Time remaining: {self.time_remaining} seconds")
            time.sleep(1)
        self.is_running = False
        self.flag = True
                
class DisplayTimer:
    def __init__(self):
        self.timer_thread = None
        self.is_running = False
        self.lock = threading.Lock()
        self.flag = False
        #self.sense=SenseHat()
        #self.volume_down = False
      
    #def update_volume_down(self):
    #    self.volume_down = True

    def start(self, new_time):
        with self.lock:
            #self.sense.clear()
            #self.sense.set_pixels(FULL_GREEN)
            self.time_remaining = new_time
            self.flag = False
            #self.new_time = new_time
            #time.sleep(3)
            if not self.is_running:
                self.is_running = True
                self.timer_thread = threading.Thread(target=self._run_timer)
                self.timer_thread.start()
            
    def stop(self):
        with self.lock:
            self.is_running = False
      #      time.sleep(1)
      #      self.sense.clear()
      #      self.sense.set_pixels(FULL_RED)

    def _run_timer(self):
        while self.is_running and self.time_remaining > 0:
            with self.lock:
      #          self.sense.clear()
       #         if self.time_remaining < self.new_time:
       #             if self.volume_down:
        #                self.sense.set_pixels(VOLUME_DOWN)
       #             else:
        #              self.sense.set_pixels(FULL_GREEN)
        #        else:
         #           self.volume_down = False
        #            if self.time_remaining > 5:
         #               display.show_num_wh(self.time_remaining)
        #              self.sense.set_pixels(numbers[self.time_remaining])
          #          else:
           #             display.show_num_rd(self.time_remaining)
        #                for index,rgb in enumerate(number_red):
        #                    number_red[index][1] *= 0
        #                    number_red[index][2] *= 0
        #                self.sense.set_pixels(number_red)
                self.time_remaining -= 1
                #print(f"Time remaining: {self.time_remaining} seconds")
            time.sleep(1)
        self.is_running = False
        self.flag = True
        #display.show_rd()

       # self.sense.clear()
      # self.sense.set_pixels(FULL_RED)