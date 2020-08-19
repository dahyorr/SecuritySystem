
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def gpiolightconfig(r,g,b):
    return r, g, b

def gpiolightout(r,g,b):
    return GPIO.setup(r,GPIO.OUT), GPIO.setup(g,GPIO.OUT), GPIO.setup(b,GPIO.OUT)


def ledreset(r,g,b):
    GPIO.output(r,GPIO.LOW)
    GPIO.output(g,GPIO.LOW)
    GPIO.output(b,GPIO.LOW)

def redon(r):
    GPIO.output(r,GPIO.HIGH)
    time.sleep(0.5)
    
def greenon(g):
    GPIO.output(g,GPIO.HIGH)
    time.sleep(0.5)
    
def blueon(b):
    GPIO.output(b,GPIO.HIGH)
    time.sleep(0.5)
    
def redoff(r):
    GPIO.output(r,GPIO.LOW)
    time.sleep(0.5)
    
def greenoff(g):
    GPIO.output(g,GPIO.LOW)
    time.sleep(0.5)
    
def blueoff(b):
    GPIO.output(b,GPIO.LOW)
    time.sleep(0.5)    
    

    

