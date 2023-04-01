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
    def __init__(self,spi,a0,cs=None,rst=None,elecvolt=0x1F,regratio=0x03,invX=False,invY=False,invdisp=False):
        a0.init(a0.OUT,value=0)
        self.a0=a0
        if(cs is not None):
            cs.init(cs.OUT,value=1)#disable device port
            self.cs=cs
        if(rst is not None):
            rst.init(rst.OUT,value=0)#reset device
            self.rst=rst
            import time
            time.sleep_ms(1)
            self.rst.value(1)
            time.sleep_ms(1)
        self.spi=spi
        initCMDList=[
            SOFT_RST,#optional, I think it's useless
            SET_BOOST,#set booster mode
            0x00,#boost: 0x00:x4 0x01:x5
            SET_BIAS|0x01,# 0:1/9 1:1/7
            EVSET_MODE,#put device into EV setting mode
            elecvolt,#0x00~0x3F set contrast to 0x1f with last command
            REGU_RATIO|regratio,#0x00~0x07 3.0~6.5
            POWER_CTRL|0x04,#7:{booster on,regulator on,follower on}
            POWER_CTRL|0x06,
            POWER_CTRL|0x07,
            SEG_DIR|(0x01 if invX else 0x00),#0:MX=0 normal dir, 1:MX=1 reverse dir
            COM_DIR|(0x08 if invY else 0x00),#0x00:MY=0 0x08:MY=1 (may change to reverse y)
            INV_DISP|(0x01 if invdisp else 0x00),#normal display
            SRTLIN_SET|0x00,
            DISP_ONOFF|0x01,
            ALL_PIX_ON|0x00]#0x00:normal display 0x01:all pixel on
        self.buffer=bytearray(128*64//8)
        super().__init__(self.buffer, 128, 64, framebuf.MONO_VLSB)
        self.writeCMD(initCMDList)
        self.fill(0)
        self.show()
        
    def writeCMD(self,cmd):
        self.cs.value(0)#enable device port
        self.a0.value(0)#cmd mode
        self.spi.write(bytearray(cmd))
        self.cs.value(1)#disable device port 
    
    def writeData(self,data):
        self.cs.value(0)#enable device port
        self.a0.value(1)#display data mode
        self.spi.write(data)
        self.cs.value(1)#disable device port

    def show(self):
        self.writeCMD([SRTLIN_SET|0x00])
        for pagcnt in range(8):
            self.writeCMD([PAGEAD_SET|pagcnt,COLHAD_SET|0x00,COLLAD_SET|0x00])
            self.writeData(self.buffer[(128*pagcnt):(128*pagcnt+128)])
