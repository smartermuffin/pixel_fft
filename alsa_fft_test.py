#!/usr/bin/python

from alsa_fft import *

data_in =  init_audio_in()
data_out = init_audio_out()


while True:
   l,data = data_in.read()
   if l:    
      process_sample(data)
      if len(data) == 1024:      #otherwise we'll crash
         data_out.write(data)
      
#   data_in.pause(1)
   
   
   #sleep(0.001)

   
#   data_in.pause(0)

