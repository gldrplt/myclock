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

# define user-defined exception
class myKillException(Exception):
    pass

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
            printmsg("(thread) Keyboard Interrupt thrown ...")
            threadflag = False

        except Exception as error:
            printmsg("(thread) Exception thrown ...")
            printmsg("(thread) Exception name = "+type(error).__name__)
            signal.raise_signal(signal.SIGTERM)
            threadflag = False
            raise

        finally:
            pass
    
    printmsg("(thread) Clearing display ...")
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
    printmsg("(signal sent) "+str(signum) + " " + signame +" " + signal.strsignal(signum))
    printmsg("(signal sent) Clearing display ...\n")

    showflag = False
    display.fill(0)

    threadflag = False
    runflag = False
    raise SystemExit     # Raise exception to exit main program

def fmtts(time):
    z = time
    hms = z.strftime("%H:%M:%S")    # hours:min:sec
    ms = z.strftime(".%f")          # microseconds 6 digits
    ms = ms[0:3]                    # 2 digits
    ts = hms + ms
    return ts

def printmsg(msg):
    z = datetime.now()                          # get current time
    if "Launching" in msg:
        ts = z.strftime("%Y %b %d %H:%M:%S ")   # format time stamp for Launch msg
    else:
        if logdateflag:                             # format time stamp for all other msg
            ts = z.strftime("%Y %b %d %H:%M:%S ")   # show date
        else:
            ts = z.strftime("\t    %H:%M:%S ")       # don't show date
    
    print(ts + msg)                             # print msg to stdout
    
    x = ts + msg + "\n"                         # add new line symbol to msg
    f = open(logfile, "a")                      # write msg to log file
    f.write(x)
    f.close()

def printstderr(msg):   # print to stderr
    z=datetime.now()
    ts = z.strftime("%Y %b %d %H:%M:%S ")
    x = ts + msg + "\n"
    print(x, file=sys.stderr)

def procparmstr(parmstr):
    global clparm
    global logdateflag
    try:
        options, remainder = getopt.getopt(parmstr, "", ['date',
                                                        'nodate'])
        for opt, arg in options:
            if opt in ('--date'):
                logdateflag = True
            elif opt in ('--nodate'):
                logdateflag = False
        tparm = remainder      # set clparm to remaing parms

    except:
        tparm = parmstr

    if len(tparm) == 0:
        clparm = ""
    elif len(tparm) == 1:
        clparm = tparm[0]
    elif len(tparm) > 1:
        n = len(tparm)
        z = ""
        for i in range(0,n):
            z = z + tparm[i] + " "
        clparm = z

def sendmail():
    z=datetime.now()
    ts = z.strftime("%Y %b %d %H:%M:%S ")
    hn = os.uname()[1]  # get hostname

    sender = "myclock.py"
    receiver = "gldrplt@gmail.com"
    subject = ts + "Program Exception Occurred"
    msg = ts + "Program myclock.py on server "+hn+" raised Program exception \
          \n\nrun cat myclock.stderr.log to see details \
          \n\nmessage sent from myclock.py"
    
    newmsg = f"""\
    
    From: <myclock.py@{hn}>
    To: {receiver}
    Subject: {subject}

    Program: myclock.py
    On server: {hn}

    raised OS Exception

    use cat myclock.stderr.log to see details
    
    message sent from myclock.py"""

    msg = newmsg

    sendemail.sendmail(sender, receiver, subject, msg)    
    printmsg("(main) Program exception email sent ...\n")
    pass

###################################    
#   Start of Program
###################################
import os
import sys
import getopt
import signal
import time
from threading import Thread
from threading import Event
from datetime import datetime
from adafruit_ht16k33 import segments
import board
import busio
import mc_Functions as mcf
import sendemail

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

# process command line parameters if passed
# look for --date or --nodate
logdateflag = False
clparm = sys.argv[1:]
procparmstr(clparm)

# get path of this program
path = os.path.dirname(os.path.abspath(__file__))
pipefile = path + "/clockpipe"
logfile = path + "/myclock.log"

# trim log file to 4 days
logdays = 5
splitstr = "Launching"
mcf.trimlog(logfile, logdays, splitstr)

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
                args = parm.split()
                procparmstr(args)           # process parmstr
                                            # look for --date or --nodate
                clparm = ""
            else:
                parm = clparm
                clparm = ""

            parm = parm.rstrip()        # remove \n if present                
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

            if parm == "--nodate":
                logdateflag = False
                printmsg("(main) ... do not show full date yyyy/mm/dd in log file ...")

            if parm == "--date":
                logdateflag = True
                printmsg("(main) ... show full date yyyy/mm/dd in log file ...")

    except KeyboardInterrupt:
        runflag = False
        threadflag = False
        print("\r  ", end="")
        printmsg("(main) User raised exception Ctrl-C ...")
        printstderr("(main) User pressed Ctrl-c ...")
        
    except SystemExit:
        runflag = False
        threadflag = False
        printmsg("(main) SIGINT or SIGTERM raised ...")
    
    except myKillException:
        runflag = False
        printmsg("(main) thread sent myKillException ...")
        # raise # stops program

    except Exception as error:
        runflag = False
        threadflag = False
        printmsg("(main) Exception thrown ...")
        printmsg("(main) Exception Name = " + type(error).__name__)
        sendmail()      # send email
        raise

    finally:
        pass

printmsg("(main) Clearing display ...\n")
# clear display
display.fill(0)
sendmail()
printmsg("(main) Exiting myclock.py ...\n")
