# mc_Functions.py
#
#   Functions used by GarageWeb application
import os
import getopt

def trimlog(logfile, logdays, splitstr):
    try:
        f = open(logfile,'r')
        z = f.read()        # get current log file data
        f.close()
        a = z.split(splitstr)
        i = len(a)
        if i <= logdays + 1:     # check if log file exceeds gwLogDays
            return
    except:
        return
    
    newlogname = logfile +".old"
    os.renames(logfile,newlogname)	#rename logfile

#   create new logfile
    outlog = ''
    for j in range(i - logdays, i-1):  
        b=a[j]              #   b contains first part of log day
        k=b.rindex('\n')
        c=b[k+1:len(b)]     #   c is first part of log day

        e=''
        if j <= i:        
            d=a[j+1]        #   d contains second part of log day
            l = d.rindex('\n') + 1
            e = d[0:l]      #   e is second part of log day
        logday = c + splitstr + e  #   build log day entry
        outlog = outlog + logday  #   add log day to trimlog


    #   write trimmed logfile
    f = open(logfile,'w')	
    f.write(outlog)   
    f.close()


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
