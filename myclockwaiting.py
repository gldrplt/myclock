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
import colorstring as cs
from datetime import datetime

def stop(signum, frame):
    end = datetime.now()
    signame = signal.Signals(signum).name   # python < 3.8
    printmsg(end, "(signal sent) "+str(signum) + " " + signame +" " + signal.strsignal(signum), 'byellow')
    dur = end - start
    printmsg(end, "Wait Time : " + str(dur.total_seconds()) +  " seconds", 'bwhite')
    display.fill(0)
    exit()

def fmtts(time):
    z = time
    hms = z.strftime("%H:%M:%S")    # hours:min:sec
    ms = z.strftime(".%f")          # microseconds 6 digits
    ms = ms[0:3]                    # 2 digits
    ts = hms + ms
    return ts

def printmsg(dto, msg, color = None):
    
    ts = dto.strftime("%Y %b %d %H:%M:%S ")   # show date    
    if msg != "":
        msg = cs.colorstring(color, ts + msg)

    print(msg)                                      # print msg to stdout
    
####################################
#
# Program start
#
####################################
start = datetime.now()
printmsg(start, "Waiting for time sync...", 'bwhite')

# Set signal handler for SIGTERM
signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGUSR1, stop)

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
