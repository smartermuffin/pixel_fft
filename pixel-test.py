#!/usr/bin/python
from time import sleep
import bibliopixel
import random
import thread
import bibliopixel.colors as colors


from ledfunc import *
from ledpattern import *



#causes frame timing information to be output
bibliopixel.log.setLogLevel(bibliopixel.log.DEBUG)
numLED = 161 *2
led = init_led(numLED)

flip = False
width = numLED/16
floater_pos = 0
bright = 255
offset = 0

def flipEvery(threadName, delay):
   while True:
      sleep(delay)
      global flip
      flip = not flip
      
         
def varyOffset(threadName, delay):
   global offset
   while True:
      for x in (1,2,3,0):
         sleep(delay)
         offset = x
         
def varyBright(threadName, delay):
   global bright
   while True:
      for x in range(100,255,5):
         sleep(delay)
         bright = x
         print "Bright",x
      for x in range(255,100,-5):
         sleep(delay)
         bright = x
         print "Bright",x
         
def moveFloater(threadName, delay):
   global floater_pos
   while True:
      for x in range(0, numLED):
         sleep(delay)
         floater_pos = x
      for x in range(numLED,0,-1):
         sleep(delay)
         floater_pos = x
         

         

         
try:
          
   #thread.start_new_thread(flipEvery,("thread-flip",5))
   #thread.start_new_thread(varyOffset,("offset-thread",10))
   #thread.start_new_thread(moveFloater,("floater-thread",.01))
   #thread.start_new_thread(varyBright,("bright-thread",.05))
   
   rain1 = rainbowBlocks(numLED,5)
   rain2 = rainbowBlocks(numLED, 2, stepsize=20)
   combo = combinePattern(numLED, rain1,rain2)
   
   while True:
      #arr = rain2.render_step()
      arr = combo.render_step()
      arrayToLED(arr,led)
      
      sleep(.01)
  
   led.waitForUpdate()
   exit()
  
   tempLED = [(0,0,0) for i in range(0,numLED) ]
   arrayToLED(tempLED, led)
   
   
   
   

   #led.update()
   #led.waitForUpdate()
   #exit()
   
   while True:      
      floater_col = randColor()
      randCoolColor()
      for x in range(0,255):
         
         col = colors.hsv2rgb((x,bright,255))
      
         paintBlocks(tempLED, col,width, flip, offset)
         
         
         
         everyNled(tempLED, 8, floater_col)
         
         #led.set(floater_pos, col)
         arrayToLED(tempLED, led)
         led.waitForUpdate()
         sleep(.008)
      
   
   while True:
      col = randColor()
      for x in range(1,10):
         paintBlocks(col,x, random.randint(1,100) < 90)
         led.update()
         sleep(.15)
      for x in range(10,0,-1):
         paintBlocks(col,x, random.randint(1,100) < 90)
         
         led.update()
         sleep(.15)
      
      col = randColor()
      oldcol = ();
      for x in range(0,numLED):
         if(x != 0):
            led.set(x-1 , oldcol)
         oldcol = led.get(x)
         led.set(x,col)
         led.update()
         sleep(.02)
         
        
except KeyboardInterrupt:
	#Ctrl+C will exit the animation and turn the LEDs offs
    
    led.all_off()
    led.update()
    led.waitForUpdate()