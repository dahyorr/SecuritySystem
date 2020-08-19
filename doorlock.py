import RPi.GPIO as GPIO
def unlock():
    import sqlwg
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    lock = 4
    GPIO.setup(lock,GPIO.OUT)
    GPIO.output(lock,GPIO.LOW)
    sqlwg.sqwrite("UPDATE lockstate set state ='0' WHERE id=1")

def lock():
    import sqlwg
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    lock = 4
    GPIO.setup(lock,GPIO.OUT)
    GPIO.output(lock,GPIO.HIGH)
    sqlwg.sqwrite("UPDATE lockstate set state ='1' WHERE id=1")
    

def unlocklock():
    import sqlwg
    import time
    import Triled
    unlock()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    r, g, b = Triled.gpiolightconfig(21,20,16)
    GPIO.setup(r,GPIO.OUT), GPIO.setup(g,GPIO.OUT), GPIO.setup(b,GPIO.OUT)
    
    Triled.gpiolightout(21, 20, 16)
    Triled.greenon(g)
    Triled.greenoff(g)
    Triled.greenon(g)
    Triled.greenoff(g)
    Triled.greenon(g)
    time.sleep(8)
    Triled.greenoff(g)
    time.sleep(5)
    lock()
