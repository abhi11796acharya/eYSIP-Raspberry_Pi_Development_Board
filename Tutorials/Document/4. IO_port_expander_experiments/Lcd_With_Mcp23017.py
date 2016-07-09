# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

#import

import smbus
import time

#define I2C connections
bus = smbus.SMBus(1)
DEVICE = 0x20
IODIRA = 0x00
IODIRB = 0x01
OLATA = 0x14
OLATB = 0x15



# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def set_high_command(value):
  data_r = bus.read_byte_data(DEVICE,OLATB)
  data_w = data_r | value
  bus.write_byte_data(DEVICE,OLATB, data_w) 

def set_low_command(value):
  data_r = bus.read_byte_data(DEVICE,OLATB)
  data_w = data_r & value
  bus.write_byte_data(DEVICE,OLATB, data_w) 

def set_high_char(value):
  data_r = bus.read_byte_data(DEVICE,OLATA)
  data_w = data_r | value
  bus.write_byte_data(DEVICE,OLATA, data_w)

def set_low_char(value):
  data_r = bus.read_byte_data(DEVICE,OLATA)
  data_w = data_r & value
  bus.write_byte_data(DEVICE,OLATA, data_w)
  
def main():
  # Main program block
  bus.write_byte_data(DEVICE,IODIRA,0x00)
  bus.write_byte_data(DEVICE,IODIRB,0x00)
  bus.write_byte_data(DEVICE,OLATA,0x00)
  bus.write_byte_data(DEVICE,OLATB,0x00)
  

  # Initialise display
  lcd_init()

  while True:

    # Send some test
    lcd_string("Rasbperry Pi",LCD_LINE_1)
    lcd_string("16x2 LCD Test",LCD_LINE_2)

    time.sleep(3) # 3 second delay

    # Send some text
    lcd_string("1234567890123456",LCD_LINE_1)
    lcd_string("abcdefghijklmnop",LCD_LINE_2)

    time.sleep(3) # 3 second delay

    # Send some text
    lcd_string("RaspberryPi-spy",LCD_LINE_1)
    lcd_string(".co.uk",LCD_LINE_2)

    time.sleep(3)

    # Send some text
    lcd_string("Follow me on",LCD_LINE_1)
    lcd_string("Twitter @RPiSpy",LCD_LINE_2)

    time.sleep(3)

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte_char(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
  set_high_command(0x01)
  

  # High bits
  set_low_char(0x0F) 
  
  if bits&0x10==0x10:    
    set_high_char(0x10) 
  if bits&0x20==0x20:    
    set_high_char(0x20) 
  if bits&0x40==0x40:    
    set_high_char(0x40)
  if bits&0x80==0x80:    
    set_high_char(0x80)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  set_low_char(0x0F)
  
  if bits&0x01==0x01:
    set_high_char(0x10) 
  if bits&0x02==0x02:
    set_high_char(0x20) 
  if bits&0x04==0x04:
    set_high_char(0x40) 
  if bits&0x08==0x08:
    set_high_char(0x80) 

  # Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
  set_low_command(0x0FE)
  

  # High bits
  set_low_char(0x0F) 
  
  if bits&0x10==0x10:    
    set_high_char(0x10)  
  if bits&0x20==0x20:    
    set_high_char(0x20) 
  if bits&0x40==0x40:    
    set_high_char(0x40) 
  if bits&0x80==0x80:    
    set_high_char(0x80) 

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  set_low_char(0x0F)
  
  if bits&0x01==0x01:
    set_high_char(0x10) 
  if bits&0x02==0x02:
    set_high_char(0x20) 
  if bits&0x04==0x04:
    set_high_char(0x40) 
  if bits&0x08==0x08:
    set_high_char(0x80) 

  # Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  set_high_command(0x02)
  time.sleep(E_PULSE)
  set_low_command(0xFD)
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte_char(ord(message[i]),LCD_CHR)

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    
