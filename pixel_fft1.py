#!/usr/bin/python
from ledpattern import *
from ledfunc import *
from alsa_fft import *
from ledUpdateThread import *
import bibliopixel.colors as colors

audio_in  = init_audio_in()
audio_out = init_audio_out()

#numLED = 160 *2
numLED = 10
led = init_led(numLED)

ledUpdate = ledUpdater(led)
ledUpdate.start()
print num_default_bands(), "bands"

try:
   while True:
      l,data = audio_in.read()
      if l:
         splitBands =  split_bands_safe(data)
         output_audio = False
         if len(data) == 1024 and output_audio:      #otherwise we'll crash
            audio_out.write(data)
         
         if not isinstance(splitBands, list):
            continue
         
         ledUpdate.newAudioData(splitBands)
         sleep(.001)
               
         
except KeyboardInterrupt:
#Ctrl+C will exit the animation and turn the LEDs offs
   ledUpdate.stop()
   led.all_off()
   led.update()
   led.waitForUpdate()