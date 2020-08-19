import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import time


def verify():
    import RPi.GPIO as GPIO
    import first
    import hashlib
    from pyfingerprint.pyfingerprint import PyFingerprint
    import time
    import doorlock 
    import serial
    import Triled
    import sqlwg
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    r, g, b = Triled.gpiolightconfig(21,20,16)
    GPIO.setup(r,GPIO.OUT), GPIO.setup(g,GPIO.OUT), GPIO.setup(b,GPIO.OUT)
    Triled.gpiolightout(21, 20, 16)

    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)


    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

## Gets some sensor information
    tempcount= str(f.getTemplateCount())

    try:
        sqlwg.sqwrite("UPDATE gui set page ='fingerprint.html' WHERE id=1")
        print('Waiting for finger...')

    ## Wait that finger is read
        while ( f.readImage() == False ):
            Triled.redon(r)
            data = ser.readline().decode('utf-8')
            if data!= '' and data[0] == 'C':
                first.startpoint()
            elif data!= '' and data[0] == 'D':
                enroll()
            Triled.redoff(r)
            pass

    ## Converts read image to characteristics and stores it in charbuffer 1
        Triled.redoff(r)
        f.convertImage(0x01)

    ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            sqlwg.sqwrite("UPDATE gui set page ='denyaccess.html' WHERE id=1")
            print('No match found!')
            Triled.blueon(b)
            Triled.blueoff(b)
            Triled.redon(r)
            Triled.redoff(r)
            
            return 0
        else:
            sqlwg.sqwrite("UPDATE gui set page ='grantaccess.html' WHERE id=1")
            print('access Granted' )
            print('ID No: ' + str(positionNumber))
            doorlock.unlocklock()
            return 1
        exit(0)

    ## OPTIONAL stuff
    ##

    ## Loads the found template to charbuffer 1
        f.loadTemplate(positionNumber, 0x01)

    ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

    

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(0)








def enroll():
    import RPi.GPIO as GPIO
    import serial
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    import first
    import Triled
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    r, g, b = Triled.gpiolightconfig(21,20,16)
    GPIO.setup(r,GPIO.OUT), GPIO.setup(g,GPIO.OUT), GPIO.setup(b,GPIO.OUT)
    Triled.gpiolightout(21, 20, 16)

    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

## Gets some sensor information
    tempstored= str(f.getTemplateCount()) 
    tempstore = str(f.getStorageCapacity())

## Tries to enroll new finger
    try:
        print("Finger enrollment")
        print (tempstored + "/"+ tempstore +" slots used" )
        Triled.redon(r)
        code = '222444'
        count = 0 
        value =''
        print('Enter secure code')
        while count<6:
            data = ser.readline().decode('utf-8')
            if data!= '' and data[0] != 'A' and data[0] != 'B' and data[0] != 'C' and data[0] != 'D':
                print(data)
                count = count +1
                value = value + str(data[0])
            elif data != '' and data[0] == 'D':
                count = count - 1
                value =  value[0:count]
                if count< 0:
                    count= 0
        
        if code != value:
            print('incorrect code')
            Triled.redoff(r)
            Triled.redon(r)
            Triled.redoff(r)
            Triled.redon(r)
            Triled.redoff(r)
            first.startpoint()
        else:
            Triled.redoff(r)
            print('Waiting for finger...')
            Triled.blueon(b)

    ## Wait that finger is read
        while ( f.readImage() == False ):
            data = ser.readline().decode('utf-8')
            if data!= '' and data[0] == 'C':
                Triled.blueoff(b)
                first.startpoint()
            pass
        Triled.blueoff(b)
    ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

    ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            first.startpoint()

        print('Remove finger...')
        

        print('Waiting for same finger again...')
        Triled.blueon(b)

        ## Wait that finger is read again
        while ( f.readImage() == False ):
            data = ser.readline().decode('utf-8')
            if data!= '' and data[0] == 'C':
                first.startpoint()
            pass
        Triled.blueoff(b)
    ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

    ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            print('Fingers do not match')
            first.startpoint()

    ## Creates a template
        f.createTemplate()

    ## Saves template at new position number
        positionNumber = f.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(0)


