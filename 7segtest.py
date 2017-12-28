# code modified, tweaked and tailored from code by bertwert 
# on RPi forum thread topic 91796
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

n = 10
 
# GPIO ports for the 7seg pins - leaving out DP and using 25 instead of 18 for center-center
segments =  (11,4,23,8,7,10,25)
# 7seg_segment_pins (7,8,3,2,1,10,4) +  100R inline
 
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
 
# GPIO ports for the digit 0-1 pins 
digits = (22,27)
# 7seg_digit_pins (9,6) digits 0-1 respectively
 
for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)
 
num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}
 
try:
    while True:
        n = time.ctime()[14:16]
#        s = str(n).rjust(2)
        s = '88'
        for digit in range(2):
            for loop in range(0,7):
                GPIO.output(segments[loop], num[s[digit]][loop])
#			Blink clock cursor
#                if (int(time.ctime()[18:19])%2 == 0) and (digit == 1):
#                    GPIO.output(25, 1)
#                else:
#                    GPIO.output(25, 0)
            GPIO.output(digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(digits[digit], 1)
finally:
    GPIO.cleanup()
