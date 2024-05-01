##################################
#
#   colorstring.py
#
#   functions to color a string
#
##################################

def colorstring(color, msg):
    colors = {
        'blink' : '\033[5m',	    #escape sequence for blink
        'reset' : '\033[0m',	    #escape sequence to RESET text
        'bred' : '\033[1;31m',	    #escape sequence for BOLD RED
        'byellow' : '\033[1;33m',	#escape sequence for BOLD yellow
        'bwhite' : '\033[1;37m',    #escape sequence for BOLD white
        'bgreen' : '\033[1;32m',    #escape sequence for BOLD green
        'bcyan' : '\033[1;36m',     #escape sequence for BOLD cyan
    }     
    
    if color in colors:
        cs = colors[color]
        b = cs + msg + colors['reset']
    else:
        b = msg

    return b    

#############################

if __name__ == '__main__':
    msg="a"
    while msg > "":
        msg = input("Enter message: ")
        if msg == "":
            continue
        color = input("Enter color: ")
        
        b = colorstring(color, msg)
        print(b)



		

