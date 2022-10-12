import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)


led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

key = digitalio.DigitalInOut(board.GP16)
key.direction = digitalio.Direction.INPUT
key.pull = digitalio.Pull.DOWN

morseCode={'.-': Keycode.A, '-...': Keycode.B, '-.-.': Keycode.C, '-..': Keycode.D, '.': Keycode.E, '..-.': Keycode.F, '--.': Keycode.G, '....': Keycode.H, '..': Keycode.I, '.---': Keycode.J, '-.-': Keycode.K, '.-..': Keycode.L, '--': Keycode.M, '-.': Keycode.N, '---': Keycode.O, '.--.': Keycode.P, '--.-': Keycode.Q, '.-.': Keycode.R, '...': Keycode.S, '-': Keycode.T, '..-': Keycode.U, '...-': Keycode.V, '.--': Keycode.W, '-..-': Keycode.X, '-.--': Keycode.Y, '--..': Keycode.Z
           '-----': Keycode.ZERO, '.----': Keycode.ONE, '..---': Keycode.TWO, '...--': Keycode.THREE, '....-': Keycode.FOUR, '.....': Keycode.FIVE, '-....': Keycode.SIX, '--...': Keycode.SEVEN, '---..': Keycode.EIGHT, '----.': Keycode.NINE,
           '.-...': (Keycode.SHIFT, Keycode.SEVEN), '.----.': Keycode.QUOTE, '.--.-.': (Keycode.SHIFT, Keycode.TWO), '-.--.-': (Keycode.SHIFT, Keycode.NINE), '-.--.': (Keycode.SHIFT, Keycode.ZERO), '---...': (Keycode.SHIFT, Keycode.SEMICOLON), '--..--': Keycode.COMMA, '-...-': Keycode.EQUALS, '-.-.--': (Keycode.SHIFT, Keycode.ONE), '.-.-.-': Keycode.PERIOD, '-....-': Keycode.MINUS, '------..-.-----': (Keycode.SHIFT, Keycode.FIVE), '.-.-.': (Keycode.SHIFT, Keycode.EQUALS), '.-..-.': (Keycode.SHIFT, Keycode.QUOTE), '..--..': (Keycode.SHIFT, Keycode.FORWARD_SLASH), '-..-.': Keycode.FORWARD_SLASH,
           '-.-.-': Keycode.BACKSLASH, '....-.': Keycode.SHIFT, '----': Keycode.BACKSPACE, '.-.-': Keycode.ENTER, '..--': Keycode.SPACE
           }

useLed=True
dah=1.5
#dit=dah/3
#wordGap=dit*7

seq=""

def send(seq):
    print(seq)
    kbd.send(morseCode[seq])

prevState=key.value
prevTimeStamp=time.monotonic()
unsent=False

while True:
    if key.value != prevState:
        duration=time.monotonic()-prevTimeStamp
        prevTimeStamp=time.monotonic()
        if useLed:
            led.value=key.value
        if prevState:
            if duration<(dah/2):
                seq+="."
            else:
                seq+="-"
        prevState=key.value
    elif seq and not key.value and (time.monotonic()-prevTimeStamp)>dah:
        send(seq)
        seq=""
        unsent=False
        

        
