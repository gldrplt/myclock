# mc_Functions.py
#
#   Functions used by myclock application
import os
def trimlog(logfile, logdays, splitstr):
#   trim log file to specified number of days
#   if splitstr is not left justified, get text from previous split

    leftflag = True    # assume splitstr is not left justified

    try:
        with open(logfile,'r') as f:
            z = f.read()        # read entire logfile

        days = z.split(splitstr)    # split logfile into days
        i = len(days)
        if i <= logdays + 1:     # check if log file exceeds LogDays
            return
    except:
        return

    if days[0] == '':
        leftflag = False    # splitstr is left justified
        
    newlogname = logfile +".old"
    os.renames(logfile,newlogname)	#rename logfile

#   create new logfile
#   rday contains right side of splitstr
#   prefix contains left side of splitstr

    outlog = ''

    # fday is index of first day to be written to new log file
    fday = i - logdays
    for j in range(fday, i):  
        rday = days[j]         # rday contains main part of log day

        #  get left side of splitstr from previous log day
        prefix = ''
        if leftflag:
            pday = days[j-1]       #   pday contains previous log day
            k=pday.rindex('\n')
            prefix = pday[k+1:len(pday)]     #   c is first part of log day

            # remove left side of splitstr from current log day
            if j <= i:        
                l = rday.rindex('\n') + 1
                rday = rday[0:l]      #   e is second part of log day

        logday = prefix + splitstr + rday  #   build log day entry
        outlog = outlog + logday  #   add log day to trimlog
    
    #   write trimmed logfile
    with open(logfile,'w') as f:
        f.write(outlog)

# ######################################
# #
# #   mc_Functions.py
# #
# ######################################

# path = os.path.dirname(os.path.abspath(__file__))
# logfile = path + "/test.log"
# logdays = 4
# split = "Launching"

# trimlog(logfile,logdays,split)

# print(" finished")
