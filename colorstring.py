##################################
#
#   colorstring.py
#
#   functions to color a string
#
##################################

class colors:
	blink='\033[5m'		#escape sequence for blink
	reset='\033[0m'		#escape sequence to RESET text
	bred='\033[1;31m'	#escape sequence for BOLD RED
	byellow='\033[1;33m'	#escape sequence for BOLD yellow
	bwhite='\033[1;37m'	#escape sequence for BOLD white
	bgreen='\033[1;32m'	#escape sequence for BOLD green
	
def colorstring(color, msg):
	
    cs = ''
    match color:
        case 'bred':
            cs = colors.bred
        case 'bwhite':
            cs = colors.bwhite
        case 'byellow':
            cs = colors.byellow
        case 'bgreen':
            cs = colors.bgreen
        case _:
            return msg
    
    x = cs + msg +colors.reset
    return x

#############################

if __name__ == '__main__':
    a = "this is test"
    b = colorstring('byellow', a)
    print(b)



		

