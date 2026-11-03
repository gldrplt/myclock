#######################################
#
#   myclockwaiting.py
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

class Timer:
# count up timer
    def __init__(self):
        self.start = time.perf_counter()

    def elapsed(self):
        return time.perf_counter() - self.start

    def elapsed_hms(self):
        s = int(self.elapsed())
        h, s = divmod(s, 3600)
        m, s = divmod(s, 60)
        return f"{h:02}:{m:02}:{s:02}"

def stop(signum, frame):
    
    signame = signal.Signals(signum).name   # python < 3.8
    msg = "(signal sent) "+str(signum) + " " + signame +" " + signal.strsignal(signum)
    printmsg(msg, 'byellow')
    dur = int(timer.elapsed())
    msg = "Wait Time : " + str(int(timer.elapsed())) + " seconds"
    printmsg(msg, 'bwhite')
    display.fill(0)
    exit()

def printmsg(msg, color = None):
    ts = date + timer.elapsed_hms()+ " "
    if msg != "":
        msg = cs.colorstring(color, ts + msg)

    print(msg)      # print msg to stdout
    # write msg to log file
    with open("myclockwaiting.log", "a") as file:
        file.write(msg+'\n')

####################################
#
# Program start
#
####################################
datedto = datetime.now() # get date
date = datedto.strftime("%Y %b %d ")

timer = Timer()     # start timer
# open new log file
with open("myclockwaiting.log", "w"):
          pass
          
printmsg("Waiting for time sync...", 'bwhite')

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
time.sleep(1.5)

segments = [1,2,64,16,8,4,32]   # segment bits for 7-segment display
colon = True
# cycle through each segment
for segment in segments:
    display.set_digit_raw(0,segment)
    display.set_digit_raw(1,segment)
    display.set_digit_raw(2,segment)
    display.set_digit_raw(3,segment)
    display.colon = colon
    colon = not colon
    time.sleep(0.5)

display.fill(0) # clear display
try:
    while True:
        now = timer.elapsed()
        t = int(now)
        colon = (t % 2 == 0)
        t = f"{t:04d}"
        display.colon = colon
        print (t)
        display.print(t)
        time.sleep(1)
except:
    display.fill(0)
