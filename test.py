import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
lock = 4
GPIO.setup(lock,GPIO.OUT)
GPIO.output(lock,GPIO.HIGH)
