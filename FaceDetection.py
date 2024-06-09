import cv2
from picamera2 import Picamera2
import RPi.GPIO as GPIO
from time import sleep
import gpiozero
pigpioFactory = gpiozero.pins.pigpio.PiGPIOFactory()
servo = gpiozero.AngularServo(3, min_angle=0, max_angle = 180, pin_factory=pigpioFactory)
vertServo = gpiozero.AngularServo(2, min_angle=0, max_angle = 180, pin_factory=pigpioFactory)
relServo = gpiozero.AngularServo(27, min_angle=0, max_angle = 180, pin_factory=pigpioFactory)
motor = gpiozero.LED(4)
button = gpiozero.Button(17)
vertpos = 90
angle = 90
middle = 0
midY = 0
inc = 0
difference = 0
face_cascade = cv2.CascadeClassifier("../opencv-4.x/data/haarcascades/haarcascade_frontalface_default.xml")
def SetAngleX(angle,delay = 0):
    if angle >= 0 and angle <= 180:
        servo.angle = angle
def detect_face(img):
    global middle,angle, midY
    coord = face_cascade.detectMultiScale(img)
    for(x,y,w,h) in coord:
        cv2.rectangle(img,(x,y),(x+w,y+h), (255,255,255), 5)
        middle = x+(w/2)
        midY = y + h/2
    if len(coord) > 0:
        print(middle, angle)
        difference = middle - 320
        if middle < 300 or middle > 340:
            angle += (difference / 320 * 4) ** 2 * (difference / abs(difference))
        angle = max(0, min(angle, 180))
        #vertServo.angle = midY / 200 * 15 + 30
        servo.angle = angle
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
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if button.is_pressed:
        print("hi")
        motor.on()
        relServo.angle = 90
        sleep(1)
        relServo.angle = 0
        sleep(2)
        motor.off()
GPIO.cleanup()
servo.close()
vertServo.close()
relServo.close()
picam2.stop()
cv2.destroyAllWindows()
