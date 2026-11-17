##################################
#
#   colorstring.py
#
#   function to color a string
#
##################################

def colorstring(color, msg):
    colors = {
        'blink' : '\033[5m',	    #escape sequence for blink
        'reset' : '\033[0m',	    #escape sequence to RESET text

        'red' : '\033[0;31m',       # escape sequence for red
        'yellow' : '\033[0;33m',    # escape sequence for yellow
        'white' : '\033[0;37m',     # escape sequence for white
        'green' : '\033[0;32m',     # escape sequence for green
        'cyan' : '\033[0;36m',      # escape sequence for cyan

        'bred' : '\033[1;31m',	    #escape sequence for BOLD RED
        'byellow' : '\033[1;33m',	#escape sequence for BOLD yellow
        'bwhite' : '\033[1;37m',    #escape sequence for BOLD white
        'bgreen' : '\033[1;32m',    #escape sequence for BOLD green
        'bcyan' : '\033[1;36m',     #escape sequence for BOLD cyan
    }     
    
    if color in colors:
        lines = msg.split('\n')      #split message into lines
        c =''
        for x in lines:
            c += colors[color] + x + colors['reset'] + '\n'  #add color to each line
        cs = c.rstrip('\n')  #remove trailing newline
    else:
        cs = msg

    return cs    

#############################

if __name__ == '__main__':
    msg="a"
    while msg > "":
        print("Enter message: ", end='')
        lines = []
        while line := input():
            lines.append(line)
    
        msg = "\n".join(lines)
        if msg == "":
            continue
        color = input("Enter color: ")
        
        b = colorstring(color, msg)
        print(b)



		

