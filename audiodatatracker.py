from ringbuffer import *
from threading import *

class AudioDataTracker:
   def __init__(self, bufferLen, numBands):
      self.buffer = []
      self.numBands = numBands
      
      self.bandMin = [] * numBands
      self.bandMax = [] * numBands
      
      self.incomingLock = Lock()
      
      for x in range(0, numBands):
         self.buffer.append(RingBuffer(bufferLen))

   def newAudioData(self, audioData):
      if len(audioData) != self.numBands:
         return
      for x in range(0, self.numBands):
         self.buffer[x].append(audioData[x])
      
   def getData(self):
      return self.buffer[7].get()

