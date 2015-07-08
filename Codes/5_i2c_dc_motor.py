import smbus  # module to access i2c based interfaces
import time
import RPi.GPIO as GPIO  # module to control Pi GPIO channels

GPIO.setmode(GPIO.BOARD) # to use Raspberry Pi board pin numbers
GPIO.setup(12,GPIO.OUT) # set up GPIO output channel i.e. on pin 11 

bus = smbus.SMBus(1) # Rev 2 Pi uses 1

DEVICE = 0x20 # Device address (A0-A2)
IODIRB = 0x01 # Pin direction register
OLATB  = 0x15 # Register for outputs

en = GPIO.PWM(12, 50) #dc motor enable pin , channel=12 frequency=50Hz (software pwm specifications)
en.start(0) # start pwm with duty cycle 0

# all bits of IODIRB register are set to 0 meaning GPA pins are outputs
bus.write_byte_data(DEVICE,IODIRB,0x00)

# Set output all 7 output bits of GPB to 0
bus.write_byte_data(DEVICE,OLATB,0)

# Function name :forward
# Input : None
# Output : Motor moves in clockwise direction i.e. forward
# Example call: forward() 
def forward():
     bus.write_byte_data(DEVICE,OLATB,0b00000001 # one input to the motor is set to logic high and the 
                                                 # other input is set to logic low resulting in clockwise motion	 
     time.sleep(1)

# Function name :backward
# Input : None
# Output : Motor moves in anticlockwise direction i.e. backward
# Example call: backward() 	 
def backward():
     bus.write_byte_data(DEVICE,OLATB,0b00000010)# one input to the motor is set to logic low and the 
                                                 # other input is set to logic high resulting in anticlockwise motion
     time.sleep(1)
   

try:
    while 1:
	     forward()
         for dc in range(0,100,10):
	              en.ChangeDutyCycle(dc) # duty cycle keeps changing by 10% starting from 0
	              time.sleep(0.5)
		
         en.ChangeDutyCycle(0)		
	     backward()
         for dc in range(0,100,10):
	              en.ChangeDutyCycle(dc) # duty cycle keeps changing by 10% starting from 0
	              time.sleep(0.5)
                      
        
              
except KeyboardInterrupt:
       pass
       GPIO.cleanup() # all GPIO pins are cleared
