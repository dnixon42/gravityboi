from machine import Pin, SPI, PWM
import time
import framebuf

# These are the default pins and whatnot on the Waveshare RP2040 1.28 w/built in w/ IMU
# 
# spi = SPI(1, baudrate=40000000, sck=Pin(10), mosi=Pin(11))
# lcd = GC9A01A(spi, cs=9, dc=8, rst=12, bl=25)
#

class GC9A01A:
    def __init__(self, spi, cs, dc, rst, bl, width=240, height=240):
        self.spi = spi
        self.cs = Pin(cs, Pin.OUT)
        self.dc = Pin(dc, Pin.OUT)
        self.rst = Pin(rst, Pin.OUT)
        self.bl = Pin(bl, Pin.OUT)
        self.width = width
        self.height = height
        self.bl_pin = PWM(Pin(bl))  # Change this to your actual backlight pin
        self.bl_pin.freq(1000)      # 1 kHz PWM frequency (works well for brightness)

        self.buffer = bytearray(self.width * self.height * 2)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.RGB565)

        self.reset()
        self.init_display()
        self.bl.on()

    def reset(self):
        self.rst.off()
        time.sleep_ms(100)
        self.rst.on()
        time.sleep_ms(100)

    def write_cmd(self, cmd):
        self.cs.off()
        self.dc.off()
        self.spi.write(bytearray([cmd]))
        self.cs.on()

    def write_data(self, data):
        self.cs.off()
        self.dc.on()
        self.spi.write(bytearray([data]) if isinstance(data, int) else data)
        self.cs.on()

    def init_display(self):
        self.write_cmd(0xEF)
        self.write_cmd(0xEB); self.write_data(0x14)
        self.write_cmd(0xFE); self.write_cmd(0xEF)
        self.write_cmd(0xEB); self.write_data(0x14)
        self.write_cmd(0x84); self.write_data(0x40)
        self.write_cmd(0x85); self.write_data(0xFF)
        self.write_cmd(0x86); self.write_data(0xFF)
        self.write_cmd(0x87); self.write_data(0xFF)
        self.write_cmd(0x88); self.write_data(0x0A)
        self.write_cmd(0x89); self.write_data(0x21)
        self.write_cmd(0x8A); self.write_data(0x00)
        self.write_cmd(0x8B); self.write_data(0x80)
        self.write_cmd(0x8C); self.write_data(0x01)
        self.write_cmd(0x8D); self.write_data(0x01)
        self.write_cmd(0x8E); self.write_data(0xFF)
        self.write_cmd(0x8F); self.write_data(0xFF)
        self.write_cmd(0xB6); self.write_data(0x00); self.write_data(0x00)
        self.write_cmd(0x36); self.write_data(0x48)
        self.write_cmd(0x3A); self.write_data(0x05)
        self.write_cmd(0x90); self.write_data(0x08); self.write_data(0x08); self.write_data(0x08); self.write_data(0x08)
        self.write_cmd(0xBD); self.write_data(0x06)
        self.write_cmd(0xBC); self.write_data(0x00)
        self.write_cmd(0xFF); self.write_data(0x60); self.write_data(0x01); self.write_data(0x04)
        self.write_cmd(0xC3); self.write_data(0x13)
        self.write_cmd(0xC4); self.write_data(0x13)
        self.write_cmd(0xC9); self.write_data(0x22)
        self.write_cmd(0xBE); self.write_data(0x11)
        self.write_cmd(0xE1); self.write_data(0x10); self.write_data(0x0E)
        self.write_cmd(0xDF); self.write_data(0x21); self.write_data(0x0c); self.write_data(0x02)
        self.write_cmd(0xF0); self.write_data(0x45); self.write_data(0x09); self.write_data(0x08); self.write_data(0x08); self.write_data(0x26); self.write_data(0x2A)
        self.write_cmd(0xF1); self.write_data(0x43); self.write_data(0x70); self.write_data(0x72); self.write_data(0x36); self.write_data(0x37); self.write_data(0x6F)
        self.write_cmd(0xF2); self.write_data(0x45); self.write_data(0x09); self.write_data(0x08); self.write_data(0x08); self.write_data(0x26); self.write_data(0x2A)
        self.write_cmd(0xF3); self.write_data(0x43); self.write_data(0x70); self.write_data(0x72); self.write_data(0x36); self.write_data(0x37); self.write_data(0x6F)
        self.write_cmd(0xED); self.write_data(0x1B); self.write_data(0x0B)
        self.write_cmd(0xAE); self.write_data(0x77)
        self.write_cmd(0xCD); self.write_data(0x63)
        self.write_cmd(0x70); self.write_data(0x07); self.write_data(0x07); self.write_data(0x04); self.write_data(0x0E); self.write_data(0x0F); self.write_data(0x09); self.write_data(0x07); self.write_data(0x08); self.write_data(0x03)
        self.write_cmd(0xE8); self.write_data(0x34)
        self.write_cmd(0x62); self.write_data(0x18); self.write_data(0x0D); self.write_data(0x71); self.write_data(0xED); self.write_data(0x70); self.write_data(0x70); self.write_data(0x18); self.write_data(0x0F); self.write_data(0x71); self.write_data(0xEF); self.write_data(0x70); self.write_data(0x70)
        self.write_cmd(0x63); self.write_data(0x18); self.write_data(0x11); self.write_data(0x71); self.write_data(0xF1); self.write_data(0x70); self.write_data(0x70); self.write_data(0x18); self.write_data(0x13); self.write_data(0x71); self.write_data(0xF3); self.write_data(0x70); self.write_data(0x70)
        self.write_cmd(0x64); self.write_data(0x28); self.write_data(0x29); self.write_data(0xF1); self.write_data(0x01); self.write_data(0xF1); self.write_data(0x00); self.write_data(0x07)
        self.write_cmd(0x66); self.write_data(0x3C); self.write_data(0x00); self.write_data(0xCD); self.write_data(0x67); self.write_data(0x45); self.write_data(0x45); self.write_data(0x10); self.write_data(0x00); self.write_data(0x00); self.write_data(0x00)
        self.write_cmd(0x67); self.write_data(0x00); self.write_data(0x3C); self.write_data(0x00); self.write_data(0x00); self.write_data(0x00); self.write_data(0x01); self.write_data(0x54); self.write_data(0x10); self.write_data(0x32); self.write_data(0x98)
        self.write_cmd(0x74); self.write_data(0x10); self.write_data(0x85); self.write_data(0x80); self.write_data(0x00); self.write_data(0x00); self.write_data(0x4E); self.write_data(0x00)
        self.write_cmd(0x98); self.write_data(0x3e); self.write_data(0x07)
        self.write_cmd(0x35)
        self.write_cmd(0x21)
        self.write_cmd(0x11)
        time.sleep_ms(120)
        self.write_cmd(0x29)

    def set_window(self, x0, y0, x1, y1):
        self.write_cmd(0x2A)
        self.write_data(bytearray([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF]))
        self.write_cmd(0x2B)
        self.write_data(bytearray([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF]))
        self.write_cmd(0x2C)

    def show(self):
        self.set_window(0, 0, self.width - 1, self.height - 1)
        self.cs.off()
        self.dc.on()
        self.spi.write(self.buffer)
        self.cs.on()
        
    def set_brightness(self, level):
        level = max(1, min(255, level))
        duty = int((level / 255) * 65535)
        self.bl_pin.duty_u16(duty)
        
    def draw_text(self, text, x, y, color=0xFFFF, bg=0x0000):
            w = len(text) * 8  # 8 pixels per char width
            h = 8              # 8 pixels high font
            buf = bytearray(w * h * 2)
            fb = framebuf.FrameBuffer(buf, w, h, framebuf.RGB565)            
            fb.fill(bg)
            fb.text(text, 0, 0, color)
            # Set window and draw buffer to screen
            self.set_window(x, y, x + w - 1, y + h - 1)
            self.cs.off()
            self.dc.on()
            self.spi.write(buf)
            self.cs.on()

