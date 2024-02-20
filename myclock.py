#########################################################
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
#########################################################

def showclock(display):
    global threadflag
    global runflag

    while threadflag:
        
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
                    if hour == 0:                       # if hour = 0 change to 12
                        hour = 12
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
            signum = 2  # stop signal
            stop(signum, frame)
            threadflag = False

        except Exception as error:
            printmsg("(thread) Exception thrown ...")
            printmsg("(thread) Exception name = "+type(error).__name__)
            threadflag = False
            
        finally:
            pass

    printmsg("(thread) Clearing display ...\n")
    display.fill(0)
    printmsg("(thread) Exiting showclock thread ...\n")
    runflag = False
    sys.exit()

def stop(signum, frame):
    global showflag
    global threadflag
    global runflag
    
    signame = signal.Signals(signum).name   # python < 3.8
    print("\r  \n", end="")
    printmsg(str(signum) + " " + signame)
    printmsg("Terminate signal sent ...\n")
    printmsg("Clearing display ...\n")

    showflag = False
    display.fill(0)

    threadflag = False
    runflag = False
    raise SystemExit    # Raise exception to exit main program

def fmtts(time):
    z = time
    hms = z.strftime("%H:%M:%S")    # hours:min:sec
    ms = z.strftime(".%f")          # microseconds 6 digits
    ms = ms[0:3]                    # 2 digits
    ts = hms + ms
    return ts

def printmsg(msg):
    z = datetime.now()
    ts = z.strftime("%Y %b %d %H:%M:%S ")
    print(ts + msg)
    x = ts + msg + "\n"
    
    f = open("myclock.log", "a")
    f.write(x)
    f.close()

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
threadflag = True   # thread flag
milflag = False     # show 12 hour time
showflag = True     # tell thread to show display
runflag = True      # main program run flag

t1 = Thread(target = showclock, args = (display,), daemon=True)
t1.start()

#time.sleep(.5)

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

# print start message to stdout
msg = "Launching 4 digit 7 segment display\n"
printmsg(msg)

# main loop
while runflag:
    try:
        while True:
            if clparm == "":
                printmsg("(main) waiting for message event\n")
                f = open(pipefile, "r")     # read from clockpipe
                                            # system will block until other end
                                            # is connected
                parm = f.readline()
                f.close()
            else:
                parm = clparm
                clparm = ""

            if parm.endswith("\n"):         # strip new line char
                parm = parm[:len(parm)-1]
                
            z = parm.split(" ")
            if len(z) == 2:
                z = parm.split(" ")           

            if z[0] == "-b":
                br=float(z[1])
                printmsg("(main) ... setting display brightness " + z[1])
                display.brightness = br

            if parm == "+m" :
                printmsg("(main) ... display military time ...")
                milflag = True
            elif parm == "-m":
                printmsg("(main) ... display standard 12hr time ...")
                milflag = False

            if parm == "-k":
                printmsg("(main) ... kill display ...")
                showflag = False
                raise KeyboardInterrupt("User sent kill display ...")

            if parm == "-s":
                printmsg("(main) ... blanking display ...")
                display.fill(0)
                showflag = False

            if parm == "+s":
                printmsg("(main) ... show clock ...")
                showflag = True

            if parm =="-f":
                printmsg("(main) ... fill display ...")
                display.fill(1)
                showflag = False

            if parm =="+d":
                printmsg("(main) ... show time and date ...")
                dateflag = True
                showflag = True
            
            if parm =="-d":
                printmsg("(main) ... show time only ...")
                dateflag = False
                showflag = True

            time.sleep(.5)
    
    except KeyboardInterrupt:
        runflag = False
        threadflag = False
    #    print("\r  ", end="")
        printmsg("(main) User raised exception Ctrl-C ...")

    except SystemExit:
        runflag = False
        threadflag = False
    
        printmsg("(main) User raised SystemExit ...")
    
    except Exception as error:
        runflag = False
        threadflag = False
        printmsg("(main) Exception thrown ...")
        printmsg("(main) Exception Name = " + type(error).__name__)

    finally:
        pass

printmsg("(main) Cleaning up ...\n")
# clear display
display.fill(0)

printmsg("(main) ... myclock.py ended ...\n")
