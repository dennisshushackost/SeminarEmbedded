import time
import smbus
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import socket
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# SHT31 measurements function
def read_sht31_data():
    i2c_bus = smbus.SMBus(1)
    i2c_address = 0x44

    i2c_bus.write_i2c_block_data(i2c_address, 0x2C, [0x06])
    time.sleep(0.5)

    data = i2c_bus.read_i2c_block_data(i2c_address, 0x00, 6)

    temp = data[0] * 256 + data[1]
    cTemp = -45 + (175 * temp / 65535.0)
    fTemp = -49 + (315 * temp / 65535.0)
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

    return cTemp, fTemp, humidity

# OLED Display Configuration
room_number = 1
RST = None
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()

UDP_IP = "192.168.46.66"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    cTemp, fTemp, humidity = read_sht31_data()  # Reading data from SHT31
    timestamp = time.time()

    # Clear the display
    draw.rectangle((0,0,width,height), outline=0, fill=0)
            
    # Display Temperature and Humidity Data
    draw.text((x, top),       "Temp(C): " + "%.2f" % cTemp + " C",  font=font, fill=255)
    draw.text((x, top+16),    "Humidity: " + "%.2f" % humidity + " %RH", font=font, fill=255)

    # Update display
    disp.image(image)
    disp.display()
    time.sleep(5)  # Update every 2 seconds
    MESSAGE = f"{cTemp},{humidity},{timestamp},{room_number}".encode()
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
