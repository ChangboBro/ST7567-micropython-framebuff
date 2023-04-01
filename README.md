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
