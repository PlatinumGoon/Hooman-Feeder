import cv2
from picamera2 import Picamera2
import RPi.GPIO as GPIO
from time import sleep
import gpiozero
pigpioFactory = gpiozero.pins.pigpio.PiGPIOFactory()
servo = gpiozero.AngularServo(2, min_angle=0, max_angle = 180, pin_factory=pigpioFactory)
vertServo = gpiozero.AngularServo(3, min_angle=0, max_angle = 180)
motor = gpiozero.Motor(forward=4)

angle = 90
middle = 0
inc = 0
difference = 0
face_cascade = cv2.CascadeClassifier("../opencv-4.x/data/haarcascades/haarcascade_frontalface_default.xml")
def SetAngleX(angle,delay = 0):
    if angle >= 0 and angle <= 180:
        servo.angle = angle
def detect_face(img):
    global middle,angle
    coord = face_cascade.detectMultiScale(img)
    print(coord)
    for(x,y,w,h) in coord:
        cv2.rectangle(img,(x,y),(x+w,y+h), (255,255,255), 5)
        middle = x+(w/2)
    if len(coord) > 0:
        print(middle, angle)
        difference = middle - 320
        if middle < 300 or middle > 340:
            angle += difference / 40
        SetAngleX(angle)
    return img
SetAngleX(90,1)
sleep(1)
picam2 = Picamera2()
picam2.preview_configuration.main.size=(640,400)
picam2.preview_configuration.main.format = "RGB888"
picam2.start()

while True:
    im = picam2.capture_array()
    im = detect_face(im)
    cv2.imshow("preview",im)
    if cv2.waitKey(1) == ord('q'):
        break
GPIO.cleanup()
servo.close()
vertServo.close()
picam2.stop()
cv2.destroyAllWindows()
