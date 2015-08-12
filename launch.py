import redis
import time
import math
from rgbmatrix import Adafruit_RGBmatrix
from lib.bibliopixel.drivers.driver_base import *
from lib.bibliopixel import *
import lib.bibliopixel.colors as colors
import lib.bibliopixel.log as log

class DriverAdaMatrix(DriverBase):
    # rows: height of the matrix, same as led-matrix example
    # chain: number of LEDMatrix panels, same as led-matrix example
    def __init__(self, rows = 32, chain = 1):
        super(DriverAdaMatrix, self).__init__(rows*32*chain)
        self._matrix = Adafruit_RGBmatrix(rows, chain)

    #Push new data to strand
    def update(self, data):
        self._matrix.SetBuffer(data)

    #Matrix supports between 2^1 and 2^11 levels of PWM
    #which translates to the total color bit-depth possible
    #A lower value will take up less CPU cycles
    def SetPWMBits(self, bits):
        if bits < 1 or bits > 11:
            raise ValueError("PWM level must be between 1 and 11")
        self._matrix.SetPWMBits(bits)

def displayer(led, hashtag_string):
  text_size = set_size(led, hashtag_string)
  starting_point = define_starting_point(led, hashtag_string, text_size)
  led.all_off()
  led.update()
  led.drawText(hashtag_string, starting_point['x'], starting_point['y'], colors.White, colors.Off, text_size)
  led.update()


def text_width(text, size):
  return (len(text)*6-1)*size

def remaining_space(led_object, text_w):
  return led_object.width-text_w

def set_size(led_object, text):
  size = 1
  while remaining_space(led_object, text_width(text, size)) > (len(text)*6-1) and 8*(size+1) < led_object.height:
    size += 1
  return size

def define_starting_point(led_object, text, text_size):
  starting_point = {}
  starting_point['x']=int(math.floor(remaining_space(led_object, text_width(text, text_size))/2))
  starting_point['y']=int(math.floor((led_object.height-8*text_size)/2))
  return starting_point

try:
  driver = DriverAdaMatrix(rows=32, chain=4)
  driver.SetPWMBits(6) #decrease bit-depth for better performance
  #MUST use serpentine=False because rgbmatrix handles the data that way
  led = LEDMatrix(driver, 128, 32, serpentine=False, threadedUpdate = True)
  log.setLogLevel(log.DEBUG)
  
  previous_hashtag_string = ''
  new_hashtag_string = ''
  database = redis.StrictRedis(host='localhost', port=6379, db=0)
  while 1:   
    previous_hashtag_string = new_hashtag_string
    new_hashtag_string = database.get('display')
    if new_hashtag_string != previous_hashtag_string:
      led.all_off()
      led.update()
      displayer(led, new_hashtag_string)
    time.sleep(5)
except KeyboardInterrupt:
  led.all_off()
  led.update()
