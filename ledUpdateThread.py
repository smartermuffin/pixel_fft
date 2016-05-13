#!/usr/bin/python
from threading import Thread
from threading import Lock
from random import randint
import time
import Queue
import copy

from ledpattern import *
from ledfunc import *
from alsa_fft import *
from audiodatatracker import *
from fileParams import *
import bibliopixel.colors as colors


class ledUpdater(Thread):
    def __init__(self, led):
        Thread.__init__(self)
        self.led = led
        self.running = True
        self.incomingAudioData = Queue.Queue()
        self.last_normLevel = 0
        self.audioUpdates = 0

        self.params = fileParams()



        self.dataTracker = AudioDataTracker(500, num_default_bands(), 5)

        self.dataTracker.updateSubscribe(self.newAudioScaler)
        self.dataTracker.start()

        self.runCount = 0
        self.updateCount = 0

        self.scaler = DummyAudioTrackerScaler()
        self.scalerLock = Lock()

        self.colorOffset = 0
        self.colorOffsetCount = 0

    def stop(self):
        self.running = False
        self.dataTracker.stop()

    def newAudioData(self, audioData):
        if self.incomingAudioData.qsize() > 10:
            # print self.incomingAudioData.qsize()
            self.incomingAudioData.get()
        self.incomingAudioData.put_nowait(audioData)
        self.dataTracker.newAudioData(audioData)

        # self.audioUpdates +=1
        # print self.audioUpdates

    def newAudioScaler(self, trackerScaler):
        print "Band: ",trackerScaler.mostActiveBand()
        trackerScaler.printStats()

        self.scalerLock.acquire()
        self.scaler = trackerScaler
        self.scalerLock.release()

    def getAudioScaler(self):
        self.scalerLock.acquire()
        scaler = copy.deepcopy(self.scaler)
        self.scalerLock.release()
        return scaler

    def run(self):
        while self.running:
            self.runCount += 1
            params = self.params.getParams()

            if params["onoff"] == 0:
                self.led.all_off()
                self.led.update()
                continue

            if self.incomingAudioData.empty():
                continue

            curAudioData = self.incomingAudioData.get()
            # print self.incomingAudioData.qsize()

            if len(curAudioData) > 0:


                self.updateLED(curAudioData, params)
                self.updateCount += 1

    def updateLED(self, splitBands, params):
        sleepval = params["update_delay"] * .01

        scaler = self.getAudioScaler()

        band = 7
        if True:
        #if isinstance(scaler, AudioTrackerScaler):
            band = scaler.mostActiveBand()
            #print band, splitBands[band], scaler.scaleBandToRange(band,splitBands[band],0,1000)
        else:
            return





        normLevel = scaler.scaleBandToRange(band,splitBands[band],0,100)
        brightlevel = scaler.scaleBandToRange(0,splitBands[0],0,100)

        if normLevel < self.last_normLevel:
            col = colors.hsv2rgb(((self.last_normLevel - 10 + self.colorOffset) % 255, 200, 255))
            #col = colors.hsv2rgb(((self.last_normLevel - 10 + self.colorOffset ) % 255, 200, 150+brightlevel))
            self.last_normLevel = self.last_normLevel - 10
            self.drawBlocks(col)
            #self.led.fill(col)
            #self.led.update()
            sleep(sleepval)


        if abs(normLevel - self.last_normLevel) > 50:
            leveldiff = normLevel - self.last_normLevel
            col = colors.hsv2rgb(((normLevel + self.colorOffset + 10) % 255, 200, 255))
            #col = colors.hsv2rgb(((normLevel + self.colorOffset +10)  % 255, 200, 150 + brightlevel))
            self.last_normLevel = normLevel +10
            self.drawBlocks(col)
            #self.led.fill(col)
            #self.led.update()
            sleep(sleepval)



        self.updateOffset()

    def updateOffset(self):
        self.colorOffsetCount += 1
        if self.colorOffsetCount % 5 == 0:
            self.colorOffset  = (self.colorOffset + 5) % 240


    def drawBlocks(self, col):
        a = [0] *(self.led.numLEDs)
        #paintBlocks(a, col, 10)
        #arrayToLED(a, self.led)
        self.led.fill(col)
        self.led.update()