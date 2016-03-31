#!/usr/bin/python
import bibliopixel.colors as colors
import random

from ledfunc import *



class LEDpattern:
   def step(self):
      return
      
   def render(self):
      return []

   def step_render(self):
      self.step()
      return self.render()
      
   def render_step(self):
      arr = self.render()
      self.step()
      return arr


      
class combinePattern(LEDpattern):
   def __init__(self,numLED, pattern1, pattern2):
      self.numLED = numLED
      self.pattern1 = pattern1
      self.pattern2 = pattern2
   
   def step(self):
      self.pattern1.step()
      self.pattern2.step()
      
   def render(self):
      arr = [(0,0,0) for i in range(0, self.numLED)]
      arr1 = self.pattern1.render()
      arr2 = self.pattern2.render()
      
      for x in range(0, len(arr)):
         arr[x] = colors.color_blend(arr1[x], arr2[x])
      
      return arr


class rainbowBlocks(LEDpattern):
   def __init__(self, numLED, blockSize, flip = False, offset = 0, stepsize = 1):
      self.numLED = numLED
      self.blockSize = blockSize
      self.flip = flip
      self.offset = offset
      self.stepsize = stepsize
      
      self.curHue = random.randint(0,255)
      
      
   def step(self):
      self.curHue = (self.curHue + self.stepsize) % 255
   
   
   def render(self, bright = 255):
      numLED = self.numLED
      arr = [(0,0,0) for i in range(0, numLED)]
      col = colors.hsv2rgb((self.curHue , 255 ,bright))
      paintBlocks(arr, col, self.blockSize, self.flip, self.offset)
      return arr