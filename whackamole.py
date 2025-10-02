'''
Code by Karla Mejia

This code implements a game of Whack-A-Mole. It uses 4 different LEDs which all correspond
to their own button. The LEDs will light up at random, and if the button is pressed while
the LED is lit, the person's score will go up. Each round lasts 30 seconds.
'''

import RPI.GPIO as GPIO
import time
import smbus
from time import sleep
import random

# defining LED pins
RedLED = 12
YellowLED = 16
GreenLED = 18
BlueLED = 22

# defining button pins
RedBtn = 13
YellowBtn = 15
GreenBtn = 33
BlueBtn = 35

GPIO.setmode(GPIO.BOARD) # numbers #GPIO by physical location

# setting LEDs up as out and low
for pin in [RedLED, YellowLED, GreenLED, BlueLED]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# seting up buttons as input and pull up
for pin in [RedBtn, YellowBtn, GreenBtn, BlueBtn]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def delay(time):
    sleep(time/1000.0)

def delayMicroseconds(time):
    sleep(time/1000000.0)

class Screen():

    enable_mask = 1<<2
    rw_mask = 1<<1
    rs_mask = 1<<0
    backlight_mask = 1<<3

    data_mask = 0x00

    def __init__(self, cols = 16, rows = 2, addr=0x27, bus=1):
        self.cols = cols
        self.rows = rows        
        self.bus_num = bus
        self.bus = smbus.SMBus(self.bus_num)
        self.addr = addr
        self.display_init()
        
    def enable_backlight(self):
        self.data_mask = self.data_mask|self.backlight_mask
        
    def disable_backlight(self):
        self.data_mask = self.data_mask& ~self.backlight_mask
       
    def display_data(self, *args):
        self.clear()
        for line, arg in enumerate(args):
            self.cursorTo(line, 0)
            self.println(arg[:self.cols].ljust(self.cols))
           
    def cursorTo(self, row, col):
        offsets = [0x00, 0x40, 0x14, 0x54]
        self.command(0x80|(offsets[row]+col))
    
    def clear(self):
        self.command(0x10)

    def println(self, line):
        for char in line:
            self.print_char(char)     

    def print_char(self, char):
        char_code = ord(char)
        self.send(char_code, self.rs_mask)

    def display_init(self):
        delay(1.0)
        self.write4bits(0x30)
        delay(4.5)
        self.write4bits(0x30)
        delay(4.5)
        self.write4bits(0x30)
        delay(0.15)
        self.write4bits(0x20)
        self.command(0x20|0x08)
        self.command(0x04|0x08, delay=80.0)
        self.clear()
        self.command(0x04|0x02)
        delay(3)

    def command(self, value, delay = 50.0):
        self.send(value, 0)
        delayMicroseconds(delay)
        
    def send(self, data, mode):
        self.write4bits((data & 0xF0)|mode)
        self.write4bits((data << 4)|mode)

    def write4bits(self, value):
        value = value & ~self.enable_mask
        self.expanderWrite(value)
        self.expanderWrite(value | self.enable_mask)
        self.expanderWrite(value)        

    def expanderWrite(self, data):
        self.bus.write_byte_data(self.addr, 0, data|self.data_mask)
       

'''
tests for each are done below
'''
lcd = Screen()
lcd.enable_backlight()

# pairing LEDs and buttons together
moles = [
    (RedLED, RedBtn, "RED"),
    (YellowLED, YellowBtn, "YELLOW"),
    (GreenLED, GreenBtn, "GREEN"),
    (BlueLED, BlueBtn, "BLUE")
]

def test_whack_a_mole(rounds=10):
    score = 0
    lcd.display_data("Whack-A-LED Test", "Starting in 3...")
    time.sleep(1)
    lcd.display_data("Whack-A-LED Test", "Starting in 2...")
    time.sleep(1)
    lcd.display_data("Whack-A-LED Test", "Starting in 1...")
    time.sleep(1)

    for i in range(rounds):
        led, btn, color = random.choice(moles)

        GPIO.output(led, GPIO.HIGH)
        lcd.display_data(f"ROUND {i+1}", f"Hit {color}!")

        hit = False
        start = time.time()

        while time.time() - start < 2:
            if GPIO.input(btn) == GPIO.LOW:
                hit = True
                break
            time.sleep(0.01)

        GPIO.output(led, GPIO.LOW)

        if hit:
            score += 1
            lcd.display_data("Nice!", f"Score: {score}")
        else:
            lcd.display_data("Too slow!", f"Score: {score}")

        time.sleep(1)

    lcd.display_data("Test Over!", f"Final: {score}/{rounds}")
    time.sleep(5)

try:
    test_whack_a_mole()
finally:
    GPIO.cleanup()