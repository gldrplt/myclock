############################
#
#   myclock.py
#
#	options	-s blank clock display
#			+s show clock
#			-b <0-1> set display brightness
#			-k kill clock
#			+m show military time (24 hr)
#			-m show 12 hr time
#			-f fill display - all segments on
#			+d show time and date
#			-d show time only
#
############################

def showclock(msgevent, display):

    print("\nDisplay time on 4 digit 7 segment display ...\n")
    
    while True:
        msgevent.clear()

        # build month/year for display of date
        date = datetime.now().strftime("%m%d")
        colontime = time.time() - 0.5

        try:
            while showflag:
                # loop 3 times to show time
                for i in range(3):
                    
                    # test showflag
                    if not showflag:
                        display.fill(0)
                        break

                    # get system time
                    now = datetime.now()
                    hour = now.hour
                    if hour >12 and milflag == False:    # convert to 12hr time
                        hour = hour - 12
                    minute = now.minute
                    second = now.second
                    # setup HH:MM for display and print it
                    clock = '%2d%02d' % (hour,minute)   # concat hour + minute
                                                        # add leading zero to minute

                    # display               
                    display.print(clock)
                            
                    # Toggle colon when displaying time
                    t = time.time()
                    dur = t - colontime
                    if dur >= .8:
                        display.print(":")      # show colon
                        colontime = time.time() # reset colon time
                    else:
                        display.print(";")  # blank colon
    
                    time.sleep(0.7)

                if dateflag:
                    display.print(";")
                    display.print(date)
                    time.sleep(0.7)
    
        except KeyboardInterrupt:
            print("\rUser pressed Ctrl-c\n")
        finally:
            pass
        
        print("waiting for message event...")
        msgevent.wait() # wait for msg to be sent

def stop(signum, frame):
    global showflag

    signame = signal.Signals(signum).name   # python < 3.8
    
    print("\n", signum, signame)
    print("\nTerminate signal sent ...\n")
    print("Clearing display ...\n")

    showflag = False
    display.fill(0)

    exit()
    
###################################    
#   Start of Program
###################################
import os
import sys
import signal
import time
from threading import Thread
from threading import Event
from datetime import datetime
from adafruit_ht16k33 import segments
import board
import busio

dateflag = False     # show clock and date flag

# Set signal handler for SIGTERM
signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the LED segment class.
# This creates a 7 segment 4 character display:
display = segments.Seg7x4(i2c)

# clear display
display.fill(0)

#   start clock thread
milflag = False
showflag = True
runflag = True
msgevent = Event()
t1 = Thread(target = showclock, args = (msgevent, display), daemon=True)
t1.start()
time.sleep(.5)

# get command line parameters if passed
clparm = ""
if len(sys.argv) > 1:
    n = len(sys.argv)
    z = ""
    for i in range(1,n):
        z = z + sys.argv[i] + " "
    clparm = z.rstrip()  # set command line parm entered flag

# get path of this program
path = os.path.dirname(os.path.abspath(__file__))
pipefile = path + "/clockpipe"

while runflag:
    try:
        while True:
            if clparm == "":
                print("waiting for message\n")            
                f = open(pipefile, "r")      # read from clockpipe
                                                # system will block until other end
                                                # is connected
                parm = f.readline()
                f.close()
            else:
                parm = clparm
                clparm = ""

            if parm.endswith("\n"):         # strip new line char
                parm = parm[:len(parm)-1]
                
            print("message = "+parm+":", "length =",len(parm))        # echo parm
            z = parm.split(" ")
            print ("z = ",z)
            if len(z) == 2:
                z = parm.split(" ")           
                print(z[0])
                print(z[1])

            if z[0] == "-b":
                br=float(z[1])
                print("display.brightness = ",br)
                display.brightness = br

            if parm == "+m" :
                print("... milflag = true...")
                milflag = True
            elif parm == "-m":
                print("... milflag = false...")
                milflag = False

            if parm == "-k":
                print("... kill display ...\n")
                showflag = False
                raise KeyboardInterrupt("User pressed Ctrl-C ...")

            if parm == "-s":
                print("... blanking display ...")
                display.fill(0)
                showflag = False

            if parm == "+s":
                print("... show clock ...")
                showflag = True

            if parm =="-f":
                print("... fill display ...")
                display.fill(1)
                showflag = False

            if parm =="+d":
                print("... show time and date ...")
                dateflag = True
                showflag = True
            
            if parm =="-d":
                print("... show time only ...")
                dateflag = False
                showflag = True

            time.sleep(.5)
            msgevent.set()                  # raise message sent event
    
    except KeyboardInterrupt:
        runflag = False
        print("\rUser raised exception Ctrl-C ...")
        print("Cleaning up ...\n")
        # clear display
        display.fill(0)

    finally:
        pass
        
print("... myclock.py ended ...\n")




