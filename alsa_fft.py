#!/usr/bin/python
sample_rate = 44100
no_channels =1 
chunk = 512 # Use a multiple of 8
default_bands = [20,200,400,750,800,900,1000,1250,2500,3200,5000,8000,10000,15000,20000]
band_max = [0] * len(default_bands)
band_min = [100] * len(default_bands)
last_split_band = [0] * len(default_bands)

import warnings
warnings.filterwarnings('error')

def num_default_bands():
   return len(default_bands) -1

def init_audio_in():
   data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL, cardindex=1)
   data_in.setchannels(no_channels)
   data_in.setrate(sample_rate)
   data_in.setformat(aa.PCM_FORMAT_S16_LE)
   data_in.setperiodsize(chunk)
   return data_in

def init_audio_out():
   data_out = aa.PCM(type=aa.PCM_PLAYBACK, mode=aa.PCM_NORMAL, cardindex=0)
   data_out.setchannels(no_channels)
   data_out.setrate(sample_rate)
   data_out.setformat(aa.PCM_FORMAT_S16_LE)
   data_out.setperiodsize(chunk)
   return data_out

def fidx(val):
    return int(chunk*val/sample_rate)
    
import alsaaudio as aa
from time import sleep
from struct import unpack
import numpy as np

global f_pow

def calculate_levels(data, chunk,sample_rate):
   # Convert raw data to numpy array
   data = unpack("%dh"%(len(data)/2),data)
   data = np.array(data, dtype='h')
   # Apply FFT - real data so rfft used
   fourier=np.fft.rfft(data)
   # Remove last element in array to make it the same size as chunk
   fourier=np.delete(fourier,len(fourier)-1)
   # Find amplitude
   power = np.log10(np.abs(fourier))**2
   # Araange array into 8 rows for the 8 bars on LED matrix
   #power = np.reshape(power,(8,chunk/8))
   #matrix= np.int_(np.average(power,axis=1)/4)
   return power


def band_split(data, bands = []):
   if bands == []:
      bands = default_bands
   #print "Data",len(data)
   split_bands = []
   for f1, f2 in zip(bands[:-1],bands[1:]):
      #print "freq",f1,f2
      #print "index",fidx(f1), fidx(f2)
      #print data[fidx(f1)    :fidx(f2)]
      slice_power = int(np.mean(data[fidx(f1)    :fidx(f2)]))
      #print slice_power
      split_bands.append(slice_power) 
   return split_bands


#def scale_freqs(split_freqs):   
   
   
def track_levels(split_freqs):
   for idx in range(0,len(split_freqs)):
      if split_freqs[idx] > band_max[idx]:
         band_max[idx] = split_freqs[idx]
      
      if split_freqs[idx] < band_min[idx]:
          band_min[idx] = split_freqs[idx]
      
      #print band_min[idx], band_max[idx]
      if True:
         return
         #print split_freqs[5]

def process_sample(data):
   #print "Raw data len",len(data)
   if len(data) != chunk *2:
      return
   try:
      power = calculate_levels(data,chunk,sample_rate)
   except:
      return
   split_bands = band_split(power)
   track_levels(split_bands)
   #print split_bands
   

def split_bands_safe(data):
   global last_split_band
   if len(data) != chunk *2:
      return
   try:
      power = calculate_levels(data,chunk,sample_rate)
   except:
      print "hurf durf"
      return last_split_band
   split_bands = band_split(power)
   last_split_band = split_bands
   return split_bands
   



