import RPi.GPIO as GPIO
import time
import sqlwg
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
buzzer= 12
switchno = 18
GPIO.setup(switchno,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)
switch=""
while True:
    state = str(sqlwg.sqget1("SELECT state FROM lockstate WHERE id=1"))
    switch= str(GPIO.input(switchno))
    armstate= str(sqlwg.sqget1("SELECT state FROM armstate WHERE id=1"))
    print (state + "      " + switch + '    ' + armstate)
    if state == '1' and switch=='0' and armstate == '1':
        
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)
        time.sleep(0.5)
    elif state == "0":
        time.sleep(1)
        continue
        