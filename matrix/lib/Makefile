# Creating RGB matrix library
# When you link this library with your binary, you need to add -lrt -lm -lpthread
# So
#   -lrgbmatrix
##
OBJECTS=gpio.o framebuffer.o thread.o bdf-font.o graphics.o
TARGET=librgbmatrix.a

# If you see that your display is inverse, you might have a matrix variant
# has uses inverse logic for the RGB bits. Attempt this
#DEFINES+=-DINVERSE_RGB_DISPLAY_COLORS


# Running on the Raspberry Pi 2 seems to require slowing down the GPIO
# bit setting, or we get glitches in the display.  Uncomment this line
# if you get glitching.

DEFINES+=-DRGB_SLOWDOWN_GPIO

DEFINES+=-DADAFRUIT_RGBMATRIX_HAT

INCDIR=../include
CXXFLAGS=-Wall -O3 -g $(DEFINES)

$(TARGET) : $(OBJECTS)
	ar rcs $@ $^

%.o : %.cc
	$(CXX) -I$(INCDIR) $(CXXFLAGS) -c -o $@ $<

clean:
	rm -f $(OBJECTS) $(TARGET)
