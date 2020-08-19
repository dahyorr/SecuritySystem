import time
time.sleep(2)
import serialexdef
import subprocess
import logging
import os
import doorlock
os.chdir('/home/pi/SecuritySystem/media')
LOG_FILENAME = 'log.txt'
logging.basicConfig(filename=LOG_FILENAME,format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
logging.info('System Start')
doorlock.lock()
logging.info('Door locked')

#from tkinter import *
#window= Tk()
#window.title("first gui")
#window.mainloop()

x = os.path.exists('/dev/ttyACM0')
y = os.path.exists('/dev/ttyUSB0')
if x == False :
    time.sleep(20)
    subprocess.call(["sudo", "reboot"])
else:
    import first

    first.startpoint()