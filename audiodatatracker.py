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
      
      self.subscribers = []
      
      for x in range(0, numBands):
         self.buffer.append(RingBuffer(bufferLen))

      self.running = False
      self.delay = delay
      
      self.dataLock = Lock()
      self.subscribeLock = Lock()
   
   def start(self):
      self.running = True
      thread.start_new_thread(self.trackAudioThread,(self.delay,))
      
   def stop(self):
      self.running = False
   
   def newAudioData(self,audioData):
      if not self.running:
         return
      if self.incomingQueue.qsize() > self.bufferLen + 100:
         self.incomingQueue.get()
      
      self.incomingQueue.put_nowait(audioData)
      
      
   
   
   def trackAudioThread(self, delay):
         while self.running:
            sleep(delay)
            if self.incomingQueue.qsize() == 0:
               return
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
            
            output = AudioTrackerScaler(stats)
            
            self.disbatchUpdate(output)
   
   
   def insertAudioData(self, audioData):
      if len(audioData) != self.numBands:
         return
      for x in range(0, self.numBands):
         self.buffer[x].append(audioData[x])
      
   
   def updateSubscribe(self, target):
      self.subscribeLock.acquire()
      self.subscribers.append(target)
      self.subscribeLock.release()
      
      
   def disbatchUpdate(self, data):
      self.subscribeLock.acquire()
      for s in self.subscribers:
         s(data)
      
      self.subscribeLock.release()
   
   
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


      
      
class AudioTrackerScaler:
   def __init__(self, stats):
      self.stats = stats
      
      
      self.audioMin = []
      self.audioMax = []
      self.audioSTD = []
      self.audioAvg = []
      for x in self.stats:
         self.audioMin.append(self.stats[0])
         

      
   def scaleBandToRange(self, band, value, rangeMin, rangeMax):
      s = self.stats[band]

      min = s[0]
      max = s[1]
      range = max - min
      adjValue = float(value) - min
      
      if value < min:
         adjValue = 0
         #self.stats[band][0]= value
      
      if value > max:
         adjValue = float(range)
         #self.stats[band][1]= value


      outputRange = rangeMax - rangeMin
      
      scaledValue = int(adjValue/range * outputRange + rangeMin)
      
      return scaledValue
      
   def printStats(self):
      for x in range(0,len(self.stats)):
         print self.stats[x], self.bandMetric(x)
         
   def mostActiveBand(self):
      stats = self.stats
      minband = 1
      i = minband
      #if type(stats).__name__ == 'list':
      #   return 5
      y = len(stats)
      for x in range(minband,y):
            if self.bandMetric(x) > self.bandMetric(i):
                i =x

      return i

   def bandMetric(self,band):
      range =  abs(self.stats[band][0] - self.stats[band][1])
      return range * self.stats[band][3]


class DummyAudioTrackerScaler(AudioTrackerScaler):
    def __init__(self):
        AudioTrackerScaler([])

    def mostActiveBand(self):
        return 0

    def printStats(self):
        print "lol"

    def scaleBandToRange(self, band, value, rangeMin, rangeMax):
        outputrange = rangeMax - rangeMin
        return int((float(value) - 9) / 30 * outputrange + rangeMin)