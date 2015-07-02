import smbus # python module to access i2c based interfaces
import time

bus = smbus.SMBus(1) # Rev 2 Pi uses 1
DEVICE = 0x20 # Device address (A0-A2)
IODIRA = 0x00 # Pin direction register
IODIRB = 0x01 # Pin direction register
OLATA  = 0x14 # Register for outputs
OLATB  = 0x15 # Register for outputs

# Function name :initialize_mcp
# Input : None
# Output : Initializes MCP23017 IC
# Example call: initialize_mcp()
def initialize_mcp():
    # all bits of IODIRA and IODIRB register are set to 0 meaning GPA 
	# and GPB pins are outputs
    bus.write_byte_data(DEVICE,IODIRA,0x00)
    bus.write_byte_data(DEVICE,IODIRB,0x00)

    # Set all 7 output bits of port A and port B to 0
    bus.write_byte_data(DEVICE,OLATA,0)
    bus.write_byte_data(DEVICE,OLATB,0)

    return
	
# Function name :cmdset4bit
# Input : None
# Output : Sets the 16x2 LCD in 4 bit mode
# Logic : Command 0x30 is sent thrice and command 0x20 is sent
#         once to initialize the LCD 
# Example call: cmdset4bit()
def cmdset4bit():
    time.sleep(1.0/1000)
    bus.write_byte_data(DEVICE,OLATB,0b00000000)
    bus.write_byte_data(DEVICE,OLATA,0b00110000)
    bus.write_byte_data(DEVICE,OLATB,0b00000100)
    time.sleep(5.0/1000)
    bus.write_byte_data(DEVICE,OLATB,0b00000000)

    time.sleep(1.0/1000)
    bus.write_byte_data(DEVICE,OLATA,0b00110000)
    bus.write_byte_data(DEVICE,OLATB,0b00000100)
    time.sleep(5.0/1000)
    bus.write_byte_data(DEVICE,OLATB,0b00000000)

    time.sleep(1.0/1000)
    bus.write_byte_data(DEVICE,OLATA,0b00110000)
    bus.write_byte_data(DEVICE,OLATB,0b00000100)
    time.sleep(5.0/1000)
    bus.write_byte_data(DEVICE,OLATB,0b00000000)

    time.sleep(1.0/1000)
    bus.write_byte_data(DEVICE,OLATA,0b00100000)
    bus.write_byte_data(DEVICE,OLATB,0b00000100)
    time.sleep(5.0/1000)
    bus.write_byte_data(DEVICE,OLATB,0b00000000)

    return

# Function name : convert
# Input : A list of hexadecimal values (commands or data)
# Output : The function returns a list with corresponding decimal 
#          equivalent of the hexadecimal values 
# Logic : A 2 digit hexadecimal value is separated into 1 digit 
#         each and a zero is appended at the end of each digit
#         (eg: '0f' is converted to '00' and 'f0')
# Example call: convert(lst)
def convert(lst):
    fc = []
    l = len(lst)
    for i in range(0,l):
        j = lst[i]
        temp1 = j[0] + '0'
        temp2 = j[1] + '0'
        t = int(temp1,16) # returns the decimal form of a string (temp1)
        u = int(temp2,16)
        fc.append(t)
        fc.append(u)

    return fc # output list

# Function name : stringconvert
# Input : A string i.e. data to be displayed on LCD 
# Output : The function returns a list with corresponding hexadecimal 
#          equivalent of every character in a string 
# Logic : This function converts a character in a string into hex 
#         format and appends the converted hex value into a list for 
#         further processing. (eg: 'A' is converted to '41' i.e. the 
#         hex value of the character )
# Example call: stringconvert(s)
def stringconvert(s):
    s1 = []
    l1 = len(s)
    for i in range(0,l1):
        j = ord(string[i]) # ord() function returns the decimal 
                           # equivalent of an ascii character
        f = hex(j)
        s1.append(f)

    l2 = len(s1)
    newlst = []
    for i in range (0,l2):
        s2 = s1[i]
        s3 = s2[2]
        s4 = s2[3]
        sf = s3 + s4
        newlst.append(sf)

    return newlst # output list 

# Function name : conversion
# Input : 2 lists a data list and a command list 
# Output : The function returns 2 lists 'data' and 'cmd' that 
#         contain data and commands in the form that can be 
#         directly given as a pin output of MCP23017 IC 
# Example call: conversion(com,s)
def conversion(com,s):
    conv_string = stringconvert(s)
    cmd = convert(com)
    data = convert(conv_string)

    return data,cmd # output lists
	
# Function name : lcd_start
# Input : None
# Output : MCP23017 is initialized and lcd is set in 4 bit mode.
# Example call: lcd_start()
def lcd_start():
    initialize_mcp()
    time.sleep(5.0/100)
    cmdset4bit()

# Function name : commandwrt
# Input : A list with commands in converted form (hexadecimal to 
#         decimal format)
# Output : Commands are sent to LCD display one by one 
# Logic : For sending commands RS pin of an LCD is set to 0 and R/W 
#         pin of an LCD is set to 0(for write operation) and a high 
#	  to low enable pulse is applied every time a command is sent
# Example call: commandwrt(cmd)	
def commandwrt(cmd):
    l = len(cmd)
    bus.write_byte_data(DEVICE,OLATB,0b00000000)
    for i in range(0,l):
        time.sleep(1.0/1000)
    	bus.write_byte_data(DEVICE,OLATA,cmd[i])
        bus.write_byte_data(DEVICE,OLATB,0b00000100)
        time.sleep(5.0/1000)
        bus.write_byte_data(DEVICE,OLATB,0b00000000)

    return

# Function name : datawrt
# Input : A list with data in converted form (string to decimal format)
# Output : Data (a string) is sent to LCD display one by one 
# Logic : For sending data RS pin of an LCD is set to 1 and R/W pin 
#         of an LCD is set to 0(for write operation) and a high to 
#         low enable pulse is applied every time data is sent
# Example call: datawrt(data)
def datawrt(data):
    l = len(data)
    for i in range(0,l):
        time.sleep(1.0/1000)
    	bus.write_byte_data(DEVICE,OLATA,data[i])
        bus.write_byte_data(DEVICE,OLATB,0b00000101)
        time.sleep(5.0/1000)
        bus.write_byte_data(DEVICE,OLATB,0b00000001)

    return

# Function name : lcdclear
# Input : None
# Output : LCD screen gets cleared(command = 0x01)
# Example call: lcdclear()
def lcdclear():
    time.sleep(1.0/1000)
    bus.write_byte_data(DEVICE,OLATA,0b00000000)
    bus.write_byte_data(DEVICE,OLATB,0b00000100)
    time.sleep(5.0/1000)
    bus.write_byte_data(DEVICE,OLATB,0b00000000)

    bus.write_byte_data(DEVICE,OLATA,0b00010000)
    bus.write_byte_data(DEVICE,OLATB,0b00000100)
    time.sleep(5.0/1000)
    bus.write_byte_data(DEVICE,OLATB,0b00000000)

try:
  lcd_start()
  com = ['28','01','0f','06'] # a list of commands
  s = "ABCD" # data to be displayed
  
  data,cmd = conversion(com,s)
  commandwrt(cmd)
  datawrt(data)
     

except KeyboardInterrupt:
       pass
       lcdclear()
