def parsecode():
    import serial
    import first
    import sqlwg
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    count=0
    value=""
    sqlwg.sqwrite("UPDATE pininput set pin =''")
    while count != 6:
        data = ser.readline().decode('utf-8')
        if data!= '' and data[0] != 'A' and data[0] != 'B' and data[0] != 'C' and data[0] != 'D':
            print (data)
            count = count+1
            value = value + str(data[0])
            sqlwg.sqwrite("UPDATE pininput set pin ='" +value +"'")
            
        elif data != '' and data[0] == 'D':
            count = count - 1
            value =  value[0:count]
            sqlwg.sqwrite("UPDATE pininput set pin ='" +value +"' ")
            if count< 0:
                count= 0
        elif data != '' and data[0] == 'C':
            first.startpoint()
            
    return value

def pininput():
    import RPi.GPIO as GPIO
    import time
    import sys
    import serial
    import Triled
    import doorlock
    import sqlwg
    sqlwg.sqwrite("UPDATE pininput set pin =''")
    sqlwg.sqwrite("UPDATE gui set page ='pininput.html' where id = 1")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    r, g, b = Triled.gpiolightconfig(21,20,16)
    GPIO.setup(r,GPIO.OUT), GPIO.setup(g,GPIO.OUT), GPIO.setup(b,GPIO.OUT)
    Triled.gpiolightout(21, 20, 16)

    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    
    
    code=sqlwg.sqget1("SELECT code FROM pincode where id = 1")
    
    
    print('input your 6 digit pin')
    Triled.redon(r)

    value = parsecode()
    if value==code:
        sqlwg.sqwrite("UPDATE pininput set pin =''")
        sqlwg.sqwrite("UPDATE gui set page ='grantaccess.html' where id = 1")
        print(value)
        print('Correct pin')
        
        Triled.redoff(r)
              #door open fo x seconds
        doorlock.unlocklock()
         #time to close the door
        
        return 1


    else:
        print(value)
        sqlwg.sqwrite("UPDATE pininput set pin =''")
        sqlwg.sqwrite("UPDATE gui set page ='denyaccess.html' where id = 1")
        print('incorrect pin')
        Triled.redoff(r)
        Triled.redon(r)
        Triled.redoff(r)
        Triled.redon(r)
        Triled.redoff(r)
        return 0

 
#def getValues():
 #   data = ser.readline().decode('utf-8')
  #  return data
    
    
    
    
    
    
    
    
    
    
    #if ser.in_waiting > 0:
     #   line = ser.readline().decode('utf-8').rstrip()
      #  print(line)
        



