#!/usr/bin/python
from threading import Thread
from threading import Lock
from random import randint
import time
import Queue

from ledpattern import *
from ledfunc import *
from alsa_fft import *
from audiodatatracker import *
import bibliopixel.colors as colors


class ledUpdater(Thread):
 
   def __init__(self, led):
      Thread.__init__(self)
      self.led = led
      self.running = True
      self.incomingAudioData = Queue.Queue()
      self.last_normLevel = 0
      self.audioUpdates = 0
      
      self.dataTracker = AudioDataTracker(500,num_default_bands(),15)
      
      self.dataTracker.updateSubscribe(self.newAudioTrackerData)
      self.dataTracker.start()
      
      self.runCount = 0
      self.updateCount = 0
      
      
      
   def stop(self):
      self.running = False
      self.dataTracker.stop()
      
   def newAudioData(self, audioData):
      if self.incomingAudioData.qsize() > 10:
         #print self.incomingAudioData.qsize() 
         self.incomingAudioData.get()
      self.incomingAudioData.put(audioData)
      self.dataTracker.newAudioData(audioData)
      
      #self.audioUpdates +=1
      #print self.audioUpdates
       
   
   def newAudioTrackerData(self,trackerScaler):
      trackerScaler.printStats()
   
   
   
   def run(self):
      while self.running:
         self.runCount += 1
         #if self.runCount % 10000 == 0:
         #  print self.runCount,self.updateCount, self.incomingAudioData.qsize()
         if self.incomingAudioData.empty():
            continue
         
         curAudioData = self.incomingAudioData.get()
         #print self.incomingAudioData.qsize()
               
         if len(curAudioData) >0:
            self.updateLED(curAudioData)
            self.updateCount +=1
         
         
         
         
         
   def updateLED(self,splitBands):      
         #init fifo of hist_normLevel
         
         cutoff=34.0
         band = 7

         
         if splitBands[band] > cutoff:
            normLevel = 255
            print splitBands[band]
         else:
            normLevel = int(splitBands[band]/cutoff * 220 + 30)
            
         if normLevel < self.last_normLevel:
            col = colors.hsv2rgb((self.last_normLevel - 10,200,255))
            self.last_normLevel = self.last_normLevel - 10
            self.led.fill(col)
            self.led.update()
            sleep(.02)
            return
         
         
         if abs(normLevel - self.last_normLevel) > 50:
            col = colors.hsv2rgb((normLevel,200,255))
            self.last_normLevel = normLevel
            self.led.fill(col)
            self.led.update()
            sleep(.02)
            
            
