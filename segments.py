from adafruit_ht16k33 import segments
import board
import busio
import time
import random as r

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the LED segment class.
# This creates a 7 segment 4 character display:
display = segments.Seg7x4(i2c)


# clear display
display.fill(0)

display.print(8888)
time.sleep(1)
display.fill(0)

try:
    mask = [1,2,4,8,16,32,64,128]
    for i in mask:
        i = int(i)
        display.set_digit_raw(0,i)
        display.set_digit_raw(1,i)
        display.set_digit_raw(2,i)
        display.set_digit_raw(3,i)
        time.sleep(0.5)
    display.fill(0)
    print("finished pass 1")
    
    while True:
        s0 =  int(r.randint(0,8))
        s1 =  int(r.randint(0,8))
        s2 =  int(r.randint(0,8))
        s3 =  int(r.randint(0,8))

        display.set_digit_raw(0,s0)
        display.set_digit_raw(1,s1)
        display.set_digit_raw(2,s2)
        display.set_digit_raw(3,s3)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\r   \nUser pressed Ctrl-c ...\n")
    display.fill(0)





