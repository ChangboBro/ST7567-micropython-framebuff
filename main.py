from machine import Pin,SPI
from ST7567 import ST7567
import time

"""
__:sck is low, --:sck is high, |:sample data, x:data change, =:data hold

pha=0 pol=0 __|--__|--     pha=1 pol=0 __--|__--|__
           _x====x====                 __x====x====
pha=0 pol=1 --|__--|__     pha=1 pol=1 --__|--__|--
           _x====x====                 __x====x====

pol=0:idle state(before communication start and after communication finish) is 0
pol=1:idle state is 1

pha=0: sample at edge of first sck voltage switching
pha=1: sample at edge of second sck voltage switching
"""
spi = SPI(0,baudrate=200_000, polarity=1, phase=1, sck=Pin(2), mosi=Pin(3),miso=Pin(16))#under 20Mhz is OK
lcd=ST7567(spi,a0=Pin(1),cs=Pin(5),rst=Pin(4),elecvolt=0x32,regratio=0x05,invX=False,invY=True,invdisp=0)

while True:
    time.sleep(1)
    lcd.fill(0)
    lcd.text("Sitronix st7567 demo",0,0,1)
    lcd.text("st7567 demo",0,8,1)
    lcd.text("Using",0,20,1)
    lcd.text("Micro Python",0,28,1)
    lcd.text("and framebuffer",0,36,1)
    lcd.text("Code by:",0,44,1)
    lcd.text("ChangboBro",0,52,1)
    lcd.show()
    time.sleep(2)
    lcd.fill(0)
    lcd.text("now running on:",0,0,1)
    lcd.text("RaspberryPi pico",0,10,1)
    lcd.show()
    time.sleep(1)
