import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

key = digitalio.DigitalInOut(board.GP21)
key.direction = digitalio.Direction.INPUT
key.pull = digitalio.Pull.DOWN

morseCode={'.-': [Keycode.A], '-...': [Keycode.B], '-.-.': [Keycode.C], '-..': [Keycode.D], '.': [Keycode.E], '..-.': [Keycode.F], '--.': [Keycode.G], '....': [Keycode.H], '..': [Keycode.I], '.---': [Keycode.J], '-.-': [Keycode.K], '.-..': [Keycode.L], '--': [Keycode.M], '-.': [Keycode.N], '---': [Keycode.O], '.--.': [Keycode.P], '--.-': [Keycode.Q], '.-.': [Keycode.R], '...': [Keycode.S], '-': [Keycode.T], '..-': [Keycode.U], '...-': [Keycode.V], '.--': [Keycode.W], '-..-': [Keycode.X], '-.--': [Keycode.Y], '--..': [Keycode.Z], 
           '-----': [Keycode.ZERO], '.----': [Keycode.ONE], '..---': [Keycode.TWO], '...--': [Keycode.THREE], '....-': [Keycode.FOUR], '.....': [Keycode.FIVE], '-....': [Keycode.SIX], '--...': [Keycode.SEVEN], '---..': [Keycode.EIGHT], '----.': [Keycode.NINE],
           '.-...': [Keycode.SHIFT, Keycode.SEVEN], '.----.': [Keycode.QUOTE], '.--.-.': [Keycode.SHIFT, Keycode.TWO], '-.--.-': [Keycode.SHIFT, Keycode.NINE], '-.--.': [Keycode.SHIFT, Keycode.ZERO], '---...': [Keycode.SHIFT, Keycode.SEMICOLON], '--..--': [Keycode.COMMA], '-...-': [Keycode.EQUALS], '-.-.--': [Keycode.SHIFT, Keycode.ONE], '.-.-.-': [Keycode.PERIOD], '-....-': [Keycode.MINUS], '------..-.-----': [Keycode.SHIFT, Keycode.FIVE], '.-.-.': [Keycode.SHIFT, Keycode.EQUALS], '.-..-.': [Keycode.SHIFT, Keycode.QUOTE], '..--..': [Keycode.SHIFT, Keycode.FORWARD_SLASH], '-..-.': [Keycode.FORWARD_SLASH],
           '-.-.-': [Keycode.BACKSLASH], '....-.': [Keycode.SHIFT], '----': [Keycode.BACKSPACE], '.-.-': [Keycode.ENTER], '..--': [Keycode.SPACE]
           }

kbd = Keyboard(usb_hid.devices)

#Config
useLed=True
farns=2 #Farnsworth speed factor (1 = no farnsworth)
noiceDuration=0.01 #signals (dits) less than this are ignored
dahFilePath="/storedDahTiming"

#Helper functions
def send():
    global seq, shift
    if seq not in morseCode:
        print(f"Error: Unknown character ({seq}).")
    elif seq=='....-.':
        shift=not shift
    elif shift:
        kbd.send(*([Keycode.SHIFT]+morseCode[seq]))
        shift=False
    else:
        kbd.send(*morseCode[seq])
    seq=""

def calcDah(duration):
    global dah, dahLog, dahIndex
    if duration>dah*3:
        return() #skip large outliers
    dahLog[dahIndex]=duration
    dahIndex=(dahIndex+1)%10
    dah=sum(dahLog)/len(dahLog)
    if dahIndex==2:
        saveDah()

def saveDah():
    with open(dahFilePath, "w") as dahFile:
        dahFile.write(str(dah))
        dahFile.flush()
    
def loadDah():
    try:
        with open(dahFilePath, "r") as dahFile:
            return float(dahFile.read())
    except:
        return 1.5
    
seq=""
shift=False
dah=loadDah()
dahLog=[dah]*10
dahIndex=0
prevState=key.value
prevTimeStamp=time.monotonic()

while True:
    state=key.value
    if state != prevState:
        duration=time.monotonic()-prevTimeStamp
        if duration<noiceDuration:
            continue
        prevTimeStamp=time.monotonic()
        if useLed:
            led.value=state
        if prevState:
            if duration<(dah/2):
                seq+="."
            else:
                seq+="-"
                calcDah(duration)
        prevState=state
    elif seq and not state and (time.monotonic()-prevTimeStamp)>(dah*farns):
        send()

