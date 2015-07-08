import RPi.GPIO as GPIO # module to control Pi GPIO channels
import time

GPIO.setmode(GPIO.BOARD) # to use Raspberry Pi board pin numbers
i1= 11 # servo motor enable
GPIO.setup(i1,GPIO.OUT,initial=GPIO.LOW) # set up GPIO output channel i.e. on pin 11 and initially output is low

# Function name : rotation
# Input : Angle in degrees
# Output : On time and off time of a pwm pulse for angle = x degrees 
# Example call: rotation(x)
def rotation(x):
    m = (2.2 - 0.6)/(180 - 0) # 0.6ms corresponds to 0 degree and 2.2ms corresponds to 180 degree
    on_time = 0.6 + m*x 
	off_time = 20 - on_time # time period of a pwm pulse for a servo motor is 20 ms
	return on_time,off_time
	
try:
    while 1:  
		angle = 90 # it can range from 0 to 360 degrees
		on_time,off_time = rotation(angle)
		GPIO.output(i1,True) 
	    time.sleep(on_time/1000) # time in ms
		GPIO.output(i1,False)
		time.sleep(off_time/1000) 
              

except KeyboardInterrupt:
       pass
GPIO.cleanup() # all GPIO pins are cleared
