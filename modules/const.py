#import required modules
import RPi.GPIO as GPIO

#GPIO pin numbers
PERSON_PIN_NUM = 5
FORKLIST_PIN_NUM = 18
OUP_PIN_NUM = 12

#pin states
OFF = GPIO.HIGH
ON = GPIO.LOW

#yolo configuration
PERSON_CLASS_NUM = 0
FORKLIFT_CLASS_NUM = 2