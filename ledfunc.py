#!/usr/bin/python
import random
import bibliopixel
import bibliopixel.colors as colors
from bibliopixel.drivers.LPD8806 import *
from bibliopixel.led import *

def init_led(numLED):
   #set number of pixels & LED type here 
   
   driver = bibliopixel.drivers.LPD8806.DriverLPD8806(num = numLED,use_py_spi=False, dev="/dev/spidev0.0",SPISpeed=64 ,c_order = ChannelOrder.BRG)

   #load the LEDStrip class
   led = LEDStrip(driver, threadedUpdate = False)
   return led


def arrayToLED(arr, led):
   if len(arr) != led.numLEDs:
      print "Dimensions do not match"
      return
   else:
      for x in range(0,len(arr)):
         led.set(x,arr[x])
      led.update()

def randColor():
   r= random.randint(0,255)
   g= random.randint(0,255)
   b= random.randint(0,255)
   return (r,g,b)
   
   
def randCoolColor():
   hue = random.randint(0,255)
   col = colors.hsv2rgb((hue,255,255))
   return col
   
def compColor(color):
   r,g,b = color
   r = 255 - r
   g = 255 - g
   b = 255 - b
   return (r,g,b)
   
   
def everyNled(arr, n, color, offset=0):
   for x in range(0,len(arr)):
      if (x + offset ) % n == 0:
         arr[x -1] = color
   

   
def paintBlocks(arr,color, width = 4, flip= False, offset = 0):

   
   if flip:
      otherColor = color
      color = compColor(otherColor)
   else:
      otherColor = compColor(color)
   
   #otherColor = color
   for x in range(0, width +1):
      everyNled(arr,width*2, color, x + offset)
   for x in range(width, width*2):
      everyNled(arr, width*2, otherColor, x + offset)  

      
