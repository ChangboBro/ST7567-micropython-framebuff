#Micro Python ST7567 128*64 lcd driver
#You may need to set elecvolt and regratio to drive your screen properly
#
from micropython import const
import framebuf

SET_BIAS  =const(0xA2)
POWER_CTRL=const(0x28)
SET_BOOST =const(0xF8)
SOFT_RST  =const(0xE2)
SEG_DIR   =const(0xA0)
COM_DIR   =const(0xC0)
REGU_RATIO=const(0x20)
EVSET_MODE=const(0x81)
DISP_ONOFF=const(0xAE)
INV_DISP  =const(0xA6)#0:normal display 1:inverse
ALL_PIX_ON=const(0xA4)
SRTLIN_SET=const(0x40)#40~7F
PAGEAD_SET=const(0xB0)#b0~b8
COLHAD_SET=const(0x10)#0x10~0x1F
COLLAD_SET=const(0x00)#0x00~0x0F

class ST7567(framebuf.FrameBuffer):
    def __init__(self,spi,a0,cs,rst,elecvolt=0x1F,regratio=0x03,invX=0x00,invY=0x00,invdisp=0x00):
        #from machine import Pin 
        #self.a0=Pin(a0,Pin.OUT,value=0)
        #self.cs=Pin(cs,Pin.OUT,value=1)
        #self.rst=Pin(rst,Pin.OUT,value=0)
        a0.init(a0.OUT,value=0)
        cs.init(cs.OUT,value=1)#disable device port
        rst.init(rst.OUT,value=0)#reset device
        self.a0=a0
        self.cs=cs
        self.rst=rst
        self.spi=spi
        
        self.EV=elecvolt
        self.RR=regratio
        self.invX=0x00 if(invX==0) else 0x01#0x00:MX=0 normal dir, 0x01:MX=1 reverse dir
        self.invY=0x00 if(invY==0) else 0x08#0x00:MY=0 0x08:MY=1
        self.invdisp=0x00 if(invdisp==0) else 0x01
        self.buffer=bytearray(128*64//8)
        super().__init__(self.buffer, 128, 64, framebuf.MONO_VLSB)
        
        import time
        time.sleep_ms(1)
        self.rst.value(1)
        time.sleep_ms(1)#reset done
        self.initscreen()
        time.sleep_ms(50)
        self.fill(0)
        self.show()
        self.write_cmd(DISP_ONOFF|0x01)#1:display on normal display mode
        
    def initscreen(self):
        self.write_cmd(SOFT_RST)#optional, I think it's useless
        self.write_cmd(SET_BOOST)#set booster mode
        self.write_cmd(0x00)#boost: 0x00:x4 0x01:x5
        self.write_cmd(SET_BIAS|0x01)# 0:1/9 1:1/7
        self.write_cmd(EVSET_MODE)#put device into EV setting mode
        self.write_cmd(self.EV)#0x00~0x3F set contrast to 0x1f with last command
        self.write_cmd(REGU_RATIO|self.RR)#0x00~0x07 3.0~6.5
        self.write_cmd(POWER_CTRL|0x07)#7:{booster on,regulator on,follower on}
        self.write_cmd(INV_DISP|self.invdisp)#normal display
        self.write_cmd(ALL_PIX_ON|0x00)#0x00:normal display 0x01:all pixel on
        self.write_cmd(SEG_DIR|self.invX)#0:MX=0 normal dir, 1:MX=1 reverse dir
        self.write_cmd(COM_DIR|self.invY)#0x00:MY=0 0x08:MY=1 (may change to reverse y)
        
    def write_cmd(self,cmd):
        self.cs.value(0)#enable device port
        self.a0.value(0)#cmd mode
        self.spi.write(bytearray([cmd]))
        #time.sleep_ms(1)
        self.cs.value(1)#disable device port 
    
    def write_data(self,data):
        self.cs.value(0)#enable device port
        self.a0.value(1)#display data mode
        self.spi.write(data)
        #time.sleep_ms(1)
        self.cs.value(1)#disable device port

    def show(self):
        self.write_cmd(DISP_ONOFF|0x00)
        self.write_cmd(SRTLIN_SET|0x00)
        colcnt=0
        pagcnt=0
        while (pagcnt<9):
            self.write_cmd(PAGEAD_SET|pagcnt)
            self.write_cmd(COLHAD_SET|0x00)
            self.write_cmd(COLLAD_SET|0x00)
            if(pagcnt<8):
                self.write_data(self.buffer[(128*pagcnt):(128*pagcnt+128)])
            else:
                while (colcnt<128):
                    colcnt+=1
                    self.write_data(b"\x00")
            pagcnt+=1
            self.write_cmd(DISP_ONOFF|0x01)
