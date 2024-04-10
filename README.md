# ST7567-micropython-framebuff
a simple micropython lib (class) to drive Sitronix ST7567 128*64 dot matrix LCD display, using framebuffer (a MicroPython-specific librarie)

the main.py is to show you how to initialize it and call method in the ST7567 file.

main.py用来让你知道怎样实例化和调用内部方法

the ST7567.py is the lib file you can use in your project.

你可以将ST7567.py作为库文件用在你的工程内

I just tested it with my RaspberryPi Pico, didn't test with other MCU...

我只试过树莓派pico，别的MCU做没测试

Hope it helps...

希望能帮到你咯

![running effect](https://github.com/ChangboBro/ST7567-micropython-framebuff/blob/main/1665837163204.jpg?raw=true)

Update 2023.4.1: the ST7567_obsolete.py is the old version of ST7567.py. The new version is simpler and faster.

2023.4.1更新：ST7567_obsolete.py是原始的版本，现在的ST7567.py相比之前的更简单，运行的更快速

2024.4.10：
In the demo file, the spi and lcd object is defined as:
``` python3
spi = SPI(0,baudrate=200_000, polarity=1, phase=1, sck=Pin(2), mosi=Pin(3),miso=Pin(16))#under 20Mhz is OK
lcd=ST7567(spi,a0=Pin(1),cs=Pin(5),rst=Pin(4),elecvolt=0x32,regratio=0x05,invX=False,invY=True,invdisp=0)
``` 
So, you should connect them as this if you test your screen with the demo file:
pins of Ras-Pi-pico|pins of your screen
|---|---|
2   |sck(scl)
3   |mosi(sda)
16(optional)  |miso(out?)
1   |a0(dc)
5   |cs
4   |rst
You have many options to connect your screen and your Ras-Pi-pico, its not fixed.
This program did't implement functions that need miso, so actually you don't need to connect that.
BL pin controls the backlight of your screen.
VCC/GND are power pins, this screen uses 3.3v for power.
You can change the pin arrangement of your circuit, as long as you change your code too. 
Note the SPI pins should conform to the constrain of Raspberry Pi Pico Pinout.
