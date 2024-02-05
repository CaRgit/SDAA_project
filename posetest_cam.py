#!/usr/bin/env python
# coding: utf-8

# In[1]:
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import urllib.request
import numpy as np
import cv2
import mediapipe as mp
# import csv

def write_landmarks_to_csv(landmarks, frame_number, csv_data):
    print(f"Landmark coordinates for frame {frame_number}:")
    for idx, landmark in enumerate(landmarks):
        print(f"{mp_pose.PoseLandmark(idx).name}: (x: {landmark.x}, y: {landmark.y}, z: {landmark.z})")
        csv_data.append([frame_number, mp_pose.PoseLandmark(idx).name, landmark.x, landmark.y, landmark.z])
    print("\n")

#video_path = '/home/pi/Desktop/Pose_Test.mp4'
#output_csv = '/home/pi/Desktop/test.csv'

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

# Open the video file
#cap = cv2.VideoCapture(video_path)

frame_number = 0
csv_data = []

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

        # Add the landmark coordinates to the list and print them
#        write_landmarks_to_csv(result.pose_landmarks.landmark, frame_number, csv_data)

    # Display the frame
    cv2.imshow("Body", image)
    #key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    #cv2.imshow('MediaPipe Pose', image)

    # Exit if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        camera.close()
        break

    frame_number += 1


cv2.destroyAllWindows()

# Save the CSV data to a file
#with open(output_csv, 'w', newline='') as csvfile:
#    csv_writer = csv.writer(csvfile)
#    csv_writer.writerow(['frame_number', 'landmark', 'x', 'y', 'z'])
#    csv_writer.writerows(csv_data)
