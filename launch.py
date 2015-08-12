from matrix_handler import *

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
