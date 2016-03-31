#!/usr/bin/python
from alsa_fft import *

audio_in  = init_audio_in()
audio_out = init_audio_out()

while True:
   l,data = audio_in.read()
   if l:   
      output_audio = True
      if len(data) == 1024 and output_audio:      #otherwise we'll crash
         audio_out.write(data)
