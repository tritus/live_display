from bibliopixel.drivers.driver_base import *
from bibliopixel import *
import bibliopixel.colors as colors
import bibliopixel.log as log

class MatrixDisplay:

  def __init__(self, led_matrix_object):
    self.led_matrix = led_matrix_object

  def display(hashtag_string):
    if remaining_space(led_matrix, text_width(hashtag_string, 1)) > 0:
      text_size = set_size(led_matrix, hashtag_string)
      starting_point = define_starting_point(led_matrix, hashtag_string, text_size)
      reset_screen()
      led_matrix.drawText(hashtag_string, starting_point['x'], starting_point['y'], colors.White, colors.Off, text_size)
      led_matrix.update()
    else:
      scroll_text(led_matrix, hashtag_string)

  def reset_screen():
    led_matrix.all_off()
    led_matrix.update()
