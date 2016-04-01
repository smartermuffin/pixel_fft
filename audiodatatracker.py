import Queue
from time import sleep
from math import sqrt

from ringbuffer import *
from threading import *
import thread

def slow_stats(data, sleepVal):
   max = data[0]
   min = data[0]
   sum = 0.0
   for x in data:
      sum += x
      if x > max:
         max = x
      if x < min:
         min = x
      sleep(sleepVal)
   
   average = sum/len(data)
   
   sumDevSq = 0.0
   for x in data:
      dev = average - x
      sumDevSq += dev*dev
      sleep(sleepVal)
   stdDev =  sqrt(sumDevSq/(len(data)-1))
   
   
   return min, max, average, stdDev



class AudioDataTracker:
   def __init__(self, bufferLen, numBands, delay):
      self.buffer = []
      self.numBands = numBands
      self.bufferLen = bufferLen
      
      self.bandMin = [] * numBands
      self.bandMax = [] * numBands
      
      self.incomingQueue = Queue.Queue()
      
      for x in range(0, numBands):
         self.buffer.append(RingBuffer(bufferLen))

      self.running = False
      self.delay = delay
      
      self.dataLock = Lock()
   
   def start(self):
      self.running = True
      thread.start_new_thread(self.trackAudioThread,(self.delay,))
      
   def stop(self):
      self.running = False
   
   def newAudioData(self,audioData):
      if self.incomingQueue.qsize() > self.bufferLen:
         self.incomingQueue.get()
      
      self.incomingQueue.put(audioData)
      
      
   
   
   def trackAudioThread(self, delay):
         while self.running:
            sleep(delay)
            self.dataLock.acquire()
            queueSize = self.incomingQueue.qsize()
            print queueSize
            for x in range(0,queueSize):
               audioData = self.incomingQueue.get()
               self.insertAudioData(audioData)
               data = self._getData()
               sleep(.003)
            self.dataLock.release()
            
            stats = []
            for d in data:
               stats.append(slow_stats(d,0))
            
            for line in stats:
               print line
   
   
   def insertAudioData(self, audioData):
      if len(audioData) != self.numBands:
         return
      for x in range(0, self.numBands):
         self.buffer[x].append(audioData[x])
      
   
   
   
   def _getData(self):
      x = []
      for buf in self.buffer:
         x.append(buf.get())
      return x
      
   def getData(self):
      self.dataLock.acquire()
      x=self._getData()
      self.dataLock.release()
      return x

