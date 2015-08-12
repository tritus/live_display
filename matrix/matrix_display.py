from matrix.driver_ada_matrix import *
from bibliopixel import *
import bibliopixel.colors as colors
import bibliopixel.log as log
from matrix.text_adapter import *
import redis
import time

class MatrixDisplay:

  def __init__(self, _rows, _chain):
    driver = DriverAdaMatrix(rows=32, chain=4)
    driver.SetPWMBits(6) #decrease bit-depth for better performance
    log.setLogLevel(log.DEBUG)
    self.database = redis.StrictRedis(host='localhost', port=6379, db=0)
    #MUST use serpentine=False because rgbmatrix handles the data that way
    self.led_matrix = LEDMatrix(driver, _rows*_chain, _rows, serpentine=False, threadedUpdate = True)

  def display(self, hashtag_string):
    if remaining_space(self.led_matrix, text_width(hashtag_string, 1)) > 0:
      text_size = set_size(self.led_matrix, hashtag_string)
      starting_point = define_starting_point(self.led_matrix, hashtag_string, text_size)
      reset_screen()
      self.led_matrix.drawText(hashtag_string, starting_point['x'], starting_point['y'], colors.White, colors.Off, text_size)
      self.led_matrix.update()
    else:
      scroll_text(self.led_matrix, hashtag_string)

  def reset_screen(self):
    self.led_matrix.all_off()
    self.led_matrix.update()

  def start_display(self):
    previous_hashtag_string = ''
    new_hashtag_string = ''
    while 1:   
      previous_hashtag_string = new_hashtag_string
      new_hashtag_string = self.database.get('display')
      if new_hashtag_string != previous_hashtag_string:
        self.reset_screen()
        self.display(new_hashtag_string)
      time.sleep(5)
