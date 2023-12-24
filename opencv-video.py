from __future__ import print_function
import cv2 as cv
import argparse
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

def detectAndDisplay(frame):
  global count_face
  frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
  frame_gray = cv.equalizeHist(frame_gray)
  #-- Detect faces
  faces = face_cascade.detectMultiScale(frame_gray, minNeighbors=5,minSize=(50,50))
  if len(faces) == 0:
    ser.write(b's\n')
    print('stop') 

  #Find a single face and name Target
  target = (320,240,130,130)
  distance = 0
  distance_closest = 0
  for (x,y,w,h) in faces:
    if x < 320:
      distance = x - 320
    elif x > 320:
      distance = 320 - x
    else:
      pass

    if distance < distance_closest:
      target = (x,y,w,h)
      distance_closest = distance
      print(target[0])

    if target[0] < 175:
      ser.write(b'l\n')
      print('left')
    elif target[0] > 370:
      ser.write(b'r\n')
      print('right')
    elif target[2] < 110:
      ser.write(b'f\n')
      print('forward')
    elif target[2] > 160:
      ser.write(b'b\n')
      print('backward')
    else:
      ser.write(b's\n')
      print('stop')    
    
    #print x/y and h/w to monitor
    cv.putText(frame, f'X: {target[0]} Y: {target[1]} Width: {target[2]} Height: {target[3]}', (50, 50), cv.FONT_HERSHEY_SIMPLEX,  1, (0, 255, 255), 2)

    #changes color of circle based on location
    warning_color=()
    if ( target[0] < 370 and target[0] > 175 and target[2] < 160 and target[2] > 110):
      warning_color = [0,255,0]
    else:
      warning_color = (255,0,255)

    center = (target[0] + target[2]//2, target[1] + target[3]//2)
    frame = cv.ellipse(frame, center, (target[2]//2, target[3]//2), 0, 0, 360, warning_color, 4)
  cv.imshow('Capture - Face detection', frame)
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='data/haarcascades/haarcascade_frontalface_alt.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()
face_cascade_name = args.face_cascade
face_cascade = cv.CascadeClassifier()
#-- 1. Load the cascades
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
  print('--(!)Error loading face cascade')
  exit(0)
camera_device = args.camera
#-- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
  print('--(!)Error opening video capture')
  exit(0)
while True:
  ret, frame = cap.read()
  if frame is None:
    print('--(!) No captured frame -- Break!')
    break
  detectAndDisplay(frame)
  if cv.waitKey(10) == 27:
    break