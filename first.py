## complete looging in all other files
import serial
import RPi.GPIO as GPIO
import time
import Triled
import subprocess
import serialexdef
import finger
import rfidchecker
import logging
import sqlwg
import subprocess
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
r, g, b = Triled.gpiolightconfig(21,20,16)
GPIO.setup(r,GPIO.OUT), GPIO.setup(g,GPIO.OUT), GPIO.setup(b,GPIO.OUT)
Triled.gpiolightout(21, 20, 16)


def waitforinput():
    Triled.ledreset(r,g,b)
    time.sleep(1)
    data=''
    while data == '':
        data = ser.readline().decode('utf-8')

def startpoint():
    logging.info('Waiting for auth type')
    sqlwg.sqwrite("UPDATE gui set page ='index.html' where id = 1")
    Triled.ledreset(r,g,b)
    idlecount=0
    alarmen= 0
    commandcount=0
    command=""

    while True:
    
        print("How to you want to verify")
        Triled.blueon(b)
        Triled.blueoff(b)
        data = ser.readline().decode('utf-8')
        if data!= '' and data[0]== 'A' :
            print (data[0] + "- Fingerprint selected")
            logging.info('Fingerprint Selected')
            sqlwg.sqwrite("UPDATE gui set page ='fingerprint.html' where id = 1")
            Triled.blueoff(b)
            tries = 0
            while tries < 3:
                feedback= finger.verify()
                if feedback == 0:
                    tries = tries + 1
                    feedinfo = "auth failed attempt " + str(tries)
                    logging.info(feedinfo)
                elif feedback == 1:
                    tries = 3
            sqlwg.sqwrite("UPDATE gui set page ='index.html' where id = 1")
        
        elif data!= '' and data[0]== 'B' :
            print (data[0] + "- pin selected")
            logging.info('PIN selected')
            sqlwg.sqwrite("UPDATE gui set page ='pininput.html' where id = 1")
            tries = 0
            Triled.blueoff(b)
            while tries < 3:
                feedback= serialexdef.pininput()
                if feedback == 0:
                    tries = tries + 1
                    feedinfo = "auth failed attempt " + str(tries)
                    logging.info(feedinfo)
                elif feedback == 1:
                    tries = 3
            sqlwg.sqwrite("UPDATE gui set page ='index.html' where id = 1")
    
 #       
        
        elif data!= '' and data[0]== 'C' :
            print (data[0] + "- Card Reader selected")
            logging.info('Card reader selected')
            sqlwg.sqwrite("UPDATE gui set page ='keycard.html' where id = 1")
            tries= 0
            Triled.blueoff(b)
            while tries < 3:
                feedback= rfidchecker.rfidauth()
                if feedback == 0:
                    tries = tries + 1
                    feedinfo = "auth failed attempt " + str(tries)
                    logging.info(feedinfo)
                elif feedback == 1:
                    tries = 3
            sqlwg.sqwrite("UPDATE gui set page ='index.html' where id = 1")

        elif data!= '' and data[0]== 'D' :
            alarmen = alarmen +1
            print(alarmen)
            if alarmen > 4:
                alarmen = 0
                if str(sqlwg.sqget1("SELECT state FROM armstate where id = 1")) == "0":
                    sqlwg.sqwrite("UPDATE armstate set state ='1' where id = 1")
                    sqlwg.sqwrite("UPDATE gui set page ='arm.html' where id = 1")
                    print("alarm system has been armed")
                    logging.info('Alarm system enabled')
                    Triled.redon(r)
                    Triled.redoff(r)
                    Triled.redon(r)
                    Triled.redoff(r)
                    time.sleep(2)
                    
                elif str(sqlwg.sqget1("SELECT state FROM armstate where id = 1")) == "1":
                    sqlwg.sqwrite("UPDATE armstate set state ='0' where id = 1")
                    sqlwg.sqwrite("UPDATE gui set page ='disarm.html' where id = 1")
                    print("alarm system has been disarmed")
                    logging.info('alarm system disabled')
                    Triled.greenon(g)
                    Triled.greenoff(g)
                    Triled.greenon(g)
                    Triled.greenoff(g)
                    time.sleep(2)
            sqlwg.sqwrite("UPDATE gui set page ='index.html' where id = 1")
                    

                
        elif data!= '' and data[0]== '*' :
            commandcount = commandcount + 1
            print("commandcount = " + str(commandcount))
            if commandcount > 2:
                sqlwg.sqwrite("UPDATE gui set page ='commandmode.html' where id = 1")
                commandcount=0
                print("Enter the command code")
                logging.info('entering command')
                while len(command) < 4:
                    GPIO.output(g,GPIO.HIGH)
                    time.sleep(0.2)
                    GPIO.output(g,GPIO.LOW)
                    time.sleep(0.2)
                    GPIO.output(r,GPIO.HIGH)
                    time.sleep(0.2)
                    GPIO.output(r,GPIO.LOW)
                    
                    data = ser.readline().decode('utf-8')
                    if data!= '' and data[0] != 'A' and data[0] != 'B' and data[0] != 'C' and data[0] != 'D' and data[0] != '#' and data[0] != '*':
                        print(data)
                        command = command + str(data[0])
                print(command)
                if command == "5*2#":
                    print("reboot")
                    logging.info('rebooting system')
                    command=""
                    subprocess.call(["sudo", "reboot"])
                else:
                    print("no command code matched")
                    logging.info('invalid command')
                    sqlwg.sqwrite("UPDATE gui set page ='index.html' where id = 1")
                    command=""

                    
                
                   
        
        
        
        
        
        
        elif data!= '' and data[0]== '#' :
            print (data[0] + "- Enroll fingerprint")
            logging.info('enrollinig fingerprint')
            finger.enroll()
        elif data == '':
            idlecount= idlecount + 1
            if idlecount > 20:
                logging.info('Entering sleep mode')
                print('Entering sleep mode')
                sqlwg.sqwrite("UPDATE gui set page ='sleep.html' where id = 1")
                waitforinput()
                idlecount=0
                logging.info('Returned from sleep mode')
                print("awake")
                sqlwg.sqwrite("UPDATE gui set page ='index.html' where id = 1")
        elif data != '':
            idlecount=0
    




        





#Triled usage
