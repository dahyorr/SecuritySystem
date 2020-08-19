

def rfidreturn():
    import os
    import sys
    from evdev import InputDevice, list_devices, ecodes, categorize
    from select import select
    from pathlib import Path
    import locale
    import serial

    LANG = locale.getdefaultlocale()[0].split('_')[0].upper()

    CODE_MAP_CHAR = {
        'DE': {
            'KEY_A': "a",
            'KEY_B': "b",
            'KEY_C': "c",
            'KEY_D': "d",
            'KEY_E': "e",
            'KEY_F': "f",
            'KEY_G': "g",
            'KEY_H': "h",
            'KEY_I': "i",
            'KEY_J': "j",
            'KEY_K': "k",
            'KEY_L': "l",
            'KEY_M': "m",
            'KEY_N': "n",
            'KEY_O': "o",
            'KEY_P': "p",
            'KEY_Q': "q",
            'KEY_R': "r",
            'KEY_S': "s",
            'KEY_T': "t",
            'KEY_U': "u",
            'KEY_V': "v",
            'KEY_W': "w",
            'KEY_X': "x",
            'KEY_Y': "z",
            'KEY_Z': "y",
            'SHIFT_KEY_A': "A",
            'SHIFT_KEY_B': "B",
            'SHIFT_KEY_C': "C",
            'SHIFT_KEY_D': "D",
            'SHIFT_KEY_E': "E",
            'SHIFT_KEY_F': "F",
            'SHIFT_KEY_G': "G",
            'SHIFT_KEY_H': "H",
            'SHIFT_KEY_I': "I",
            'SHIFT_KEY_J': "J",
            'SHIFT_KEY_K': "K",
            'SHIFT_KEY_L': "L",
            'SHIFT_KEY_M': "M",
            'SHIFT_KEY_N': "N",
            'SHIFT_KEY_O': "O",
            'SHIFT_KEY_P': "P",
            'SHIFT_KEY_Q': "Q",
            'SHIFT_KEY_R': "R",
            'SHIFT_KEY_S': "S",
            'SHIFT_KEY_T': "T",
            'SHIFT_KEY_U': "U",
            'SHIFT_KEY_V': "V",
            'SHIFT_KEY_W': "W",
            'SHIFT_KEY_X': "X",
            'SHIFT_KEY_Y': "Z",
            'SHIFT_KEY_Z': "Y",

            'SHIFT_KEY_GRAVE':'°',
            'SHIFT_KEY_1': "!",
            'SHIFT_KEY_2': "\"",
            'SHIFT_KEY_3': "§",
            'SHIFT_KEY_4': "$",
            'SHIFT_KEY_5': "%",
            'SHIFT_KEY_6': "&",
            'SHIFT_KEY_7': "/",
            'SHIFT_KEY_8': "(",
            'SHIFT_KEY_9': ")",
            'SHIFT_KEY_0': "=",
            'SHIFT_KEY_EQUAL': "`",
            'SHIFT_KEY_RIGHTBRACE':'*',
            'SHIFT_KEY_BACKSLASH':'\'',
            'SHIFT_KEY_COMMA':';',
            'SHIFT_KEY_DOT':':',
            'SHIFT_KEY_SLASH':'_',

            'ALTGR_KEY_Q': "@",
            'ALTGR_KEY_MINUS': "\\",
            'ALTGR_KEY_7': "{",
            'ALTGR_KEY_0': "}",
            'ALTGR_KEY_8': "[",
            'ALTGR_KEY_9': "]",
            'ALTGR_KEY_RIGHTBRACE':'~',

            'KEY_NUMERIC_STAR': "*",

            'KEY_GRAVE':'^',
            'KEY_LEFTBRACE':'Ü',
            'KEY_RIGHTBRACE':'+',
            'KEY_SEMICOLON':'Ö',
            'KEY_APOSTROPHE':'Ä',
            'KEY_BACKSLASH':'#',
            'KEY_102ND':'<',
            'KEY_COMMA':',',
            'KEY_DOT':'.',
            'KEY_SLASH':'-',
            'KEY_KPSLASH':'/',
            'KEY_KPASTERISK':'*',
            'KEY_KPMINUS':'-',
            'KEY_KPPLUS':'+',
            'KEY_KPDOT':'.',
            'KEY_SPACE': " ",
            'KEY_EQUAL': "´",
            'KEY_TAB': "\t",

            'KEY_MINUS': "ß",
            'KEY_SPACE': " ",

            'KEY_NUMERIC_1': "1",
            'KEY_NUMERIC_2': "2",
            'KEY_NUMERIC_3': "3",
            'KEY_NUMERIC_4': "4",
            'KEY_NUMERIC_5': "5",
            'KEY_NUMERIC_6': "6",
            'KEY_NUMERIC_7': "7",
            'KEY_NUMERIC_8': "8",
            'KEY_NUMERIC_9': "9",
            'KEY_NUMERIC_0': "0",
            'KEY_KP1': "1",
            'KEY_KP2': "2",
            'KEY_KP3': "3",
            'KEY_KP4': "4",
            'KEY_KP5': "5",
            'KEY_KP6': "6",
            'KEY_KP7': "7",
            'KEY_KP8': "8",
            'KEY_KP9': "9",
            'KEY_KP0': "0",
            'KEY_1': "1",
            'KEY_2': "2",
            'KEY_3': "3",
            'KEY_4': "4",
            'KEY_5': "5",
            'KEY_6': "6",
            'KEY_7': "7",
            'KEY_8': "8",
            'KEY_9': "9",
            'KEY_0': "0"
        },
        'EN': {
            'KEY_A': "A",
            'KEY_B': "B",
            'KEY_C': "C",
            'KEY_D': "D",
            'KEY_E': "E",
            'KEY_F': "F",
            'KEY_G': "G",
            'KEY_H': "H",
            'KEY_I': "I",
            'KEY_J': "J",
            'KEY_K': "K",
            'KEY_L': "L",
            'KEY_M': "M",
            'KEY_N': "N",
            'KEY_O': "O",
            'KEY_P': "P",
            'KEY_Q': "Q",
            'KEY_R': "R",
            'KEY_S': "S",
            'KEY_T': "T",
            'KEY_U': "U",
            'KEY_V': "V",
            'KEY_W': "W",
            'KEY_X': "X",
            'KEY_Y': "Y",
            'KEY_Z': "Z",
            'KEY_GRAVE':'`',
            'KEY_MINUS': "-",
            'KEY_SPACE': " ",  
            'KEY_BACKSLASH': "\\",
            'KEY_GRAVE': "`",
            'KEY_NUMERIC_STAR': "*",
            'KEY_LEFTBRACE': "[",
            'KEY_RIGHTBRACE': "]",    
            'KEY_COMMA': ",",
            'KEY_EQUAL': "=",    
            'KEY_SEMICOLON': ";",
            'KEY_APOSTROPHE': "'",
            'KEY_TAB': "\t",
            'KEY_DOT': ".",
            'KEY_SLASH': "/",
            'KEY_NUMERIC_1': "1",
            'KEY_NUMERIC_2': "2",
            'KEY_NUMERIC_3': "3",
            'KEY_NUMERIC_4': "4",
            'KEY_NUMERIC_5': "5",
            'KEY_NUMERIC_6': "6",
            'KEY_NUMERIC_7': "7",
            'KEY_NUMERIC_8': "8",
            'KEY_NUMERIC_9': "9",
            'KEY_NUMERIC_0': "0",
            'KEY_KP1': "1",
            'KEY_KP2': "2",
            'KEY_KP3': "3",
            'KEY_KP4': "4",
            'KEY_KP5': "5",
            'KEY_KP6': "6",
            'KEY_KP7': "7",
            'KEY_KP8': "8",
            'KEY_KP9': "9",
            'KEY_KP0': "0",
            'KEY_1': "1",
            'KEY_2': "2",
            'KEY_3': "3",
            'KEY_4': "4",
            'KEY_5': "5",
            'KEY_6': "6",
            'KEY_7': "7",
            'KEY_8': "8",
            'KEY_9': "9",
            'KEY_0': "0"
        }
    }

    def parse_key_to_char(val):
        return CODE_MAP_CHAR[LANG][val] if val in CODE_MAP_CHAR[LANG] else ""

    def try_kill_script(script):
        try:
            os.system('pkill -f '+script)
        except OSError:
            return False
        else:
            return True

    founddev = ['/dev/input/event0']

    devices = map(InputDevice, founddev)
    devices = {dev.fd: dev for dev in devices}



    chars = ''
    prefix = ''
    initvalue=""
    returnvalue=""
    while initvalue == "":
        r, w, x = select(devices, [], [])
        for fd in r:
              
            try:
                
                for event in devices[fd].read():
                    if event.type == ecodes.EV_KEY:
                        e = categorize(event)
                        if e.keystate == e.key_down:
                            if e.keycode == 'KEY_LEFTSHIFT' or e.keycode == 'KEY_RIGHTSHIFT':
                                prefix = 'SHIFT_'
                            elif e.keycode == 'KEY_LEFTALT':
                                prefix = 'ALT_'
                            elif e.keycode == 'KEY_RIGHTALT':
                                prefix = 'ALTGR_'
                            
                            elif e.keycode == 'KEY_ESC':
                                chars = ''
                            elif e.keycode == 'KEY_BACKSPACE':
                                chars = chars[:-1]
                            elif e.keycode == 'KEY_ENTER' or e.keycode == 'KEY_KPENTER':
                                initvalue= chars+'\n'
                                returnvalue = initvalue[0:10]
                                sys.stdout.flush()
                                chars = ''
                            else:
                                #print (ecodes.EV_LED) # which outputs 17 forever
                            
                                chars += parse_key_to_char(prefix + e.keycode)
                        elif e.keystate == e.key_up:
                        #sys.stdout.write(parse_key_to_char(e.keycode))
                        #sys.stdout.flush()
                        #print ("'"+e.keycode+"':'"+parse_key_to_char(e.keycode)+"',")
                            if e.keycode == 'KEY_LEFTSHIFT' or e.keycode == 'KEY_RIGHTSHIFT':
                                prefix = ''
                            elif e.keycode == 'KEY_LEFTALT':
                                prefix = ''
                            elif e.keycode == 'KEY_RIGHTALT':
                                prefix = ''
            except:
                try_kill_script('read_hidraw_scanner.py')
    return returnvalue

def rfidauth():
    import sqlwg
    import doorlock
    import RPi.GPIO as GPIO
    import Triled
    import time
    sqlwg.sqwrite("UPDATE gui set page ='keycard.html' WHERE id=1")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    r, g, b = Triled.gpiolightconfig(21,20,16)
    GPIO.setup(r,GPIO.OUT), GPIO.setup(g,GPIO.OUT), GPIO.setup(b,GPIO.OUT)
    Triled.gpiolightout(21, 20, 16)


    print("waiting for card")
    auth=""
    codes= sqlwg.sqget("SELECT code FROM rfid_id")
    Triled.redon(r)

    data =rfidreturn()
    for i in codes:
        if data == i:
            auth = "valid"
        elif data != i and auth != "valid": 
            continue
            
            
    if auth =='valid':
        Triled.redoff(r)
        sqlwg.sqwrite("UPDATE gui set page ='grantaccess.html' WHERE id=1")
        print ("access granted")
        print(data)
        doorlock.unlocklock()
        return 1
    else:
        Triled.redoff(r)
        sqlwg.sqwrite("UPDATE gui set page ='denyaccess.html' WHERE id=1")
        print ("invalid")
        time.sleep(1.5)
        return 0

