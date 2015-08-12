import math

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

def scroll_text(led, text):
  anim = ScrollText(led, text, size=1)
  anim.run()