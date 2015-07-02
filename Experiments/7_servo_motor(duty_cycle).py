import RPi.GPIO as GPIO # module to control Pi GPIO channels
import time

GPIO.setmode(GPIO.BOARD) # to use Raspberry Pi board pin numbers
GPIO.setup(11,GPIO.OUT) # set up GPIO output channel i.e. on pin 11 

en = GPIO.PWM(11, 50) # servo motor enable pin , channel=11 frequency=50Hz (software pwm specifications)
en.start(0) # start pwm with duty cycle 0
 
GPIO.setup(i1,GPIO.OUT,initial=GPIO.LOW) # set up GPIO output channel i.e. on pin 11 and initially output is low

# Function name : rotation
# Input : Angle in degrees
# Output : Duty cycle of a pwm pulse is calculated for angle = x degrees 
# Logic : Duty cycle = (Ton/T)*100 ; 
# Example call: rotation(x)
def rotation(x):
    m = (2.2 - 0.6)/(180 - 0) # 0.6ms corresponds to 0 degree and 2.2ms corresponds to 180 degree
    on_time = 0.6 + m*x 
	dc = (on_time/20)*100 # time period of a pwm pulse for a servo motor is 20 ms
	return dc
	
try:
    while 1:  
		angle = 90 # it can range from 0 to 360 degrees
		dc = rotation(angle)
		en.ChangeDutyCycle(dc) # set the appropriate duty cycle to rotate servo by an angle = x degrees
              
except KeyboardInterrupt:
       pass
GPIO.cleanup() # all GPIO pins are cleared
