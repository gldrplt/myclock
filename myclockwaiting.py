#######################################
#
#   clockwaiting.py
#
#       show blinking segments until
#       time-sync.target is reached
#       and system clock is synced
#
#######################################
from adafruit_ht16k33 import segments
import busio
import board
import time
import signal

def stop(signum, frame):
    
    signame = signal.Signals(signum).name   # python < 3.8
    print("\r  \n", end="")
    print("(signal sent) "+str(signum) + " " + signame +" " + signal.strsignal(signum), 'byellow')
    print("(signal sent) Clearing display ...\n")

    display.fill(0)
    exit()
# Set signal handler for SIGTERM
signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the LED segment class.
# This creates a 7 segment 4 character display:
display = segments.Seg7x4(i2c)
#display = segments(i2c)    # use subclass mysegments

# set brightness
display.brightness = 0

# clear display
display.fill(1)

try:
    while True:
        display.print("00:00")
        time.sleep(1)
        display.colon = False
        time.sleep(1)
except:
    display.fill(0)
