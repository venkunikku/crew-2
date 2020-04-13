import pandas as pd
import numpy as np
import os
import scipy.io.wavfile as wavfile
from python_speech_features import mfcc, logfbank
import gcsfs

class feature_extraction():

	def __init__(self,
		mixed_dir = "../../mixed/",
		processed_dir = "../../training_processed/",
		sampling_freq = 44100,
		gcp=False):

		if gcp = False:        
			self.mixed_dir = mixed_dir
			self.processed_dir = processed_dir

		else:
			self.mixed_dir = "gs://ad-bucket-15730/mixed/"
			self.processed_dir = "gs://ad-bucket-15730/training_processed/"            

		self.sampling_freq = sampling_freq

	def read(self, filename, normalize=True):

		"""
		Read in wav file; Excepts just the filename as arg
		"""

		filepath = self.mixed_dir + filename
		sf, time_signal = wavfile.read(filepath, mmap=True)

		if normalize==True:
			# normalization, assuming 2^15 is the highest possible quantization
			time_signal = time_signal/np.power(2,15)

		return time_signal

	def return_fourier_transform(self, time_signal, normalize=True):

		freq_signal = np.fft.fft(time_signal)

		"""
		We note that several different sample rates could be used that would yield differing numbers and sets of frequencies
		As such, we normalize frequency domain signal by dividing the first half length of the DFT array by sampling frequency 
		(i.e. the number of time steps).
		"""

		if normalize==True:
			# Dividing first half of DFT (freq signal) by sampling freq (len signal)
			len_signal = len(time_signal)
			len_half = np.ceil((len_signal + 1) / 2.0).astype(np.int)
			freq_signal = abs(freq_signal[0:len_half]) / len_signal 

		return freq_signal

	def return_power_spectrum(self, freq_signal, time_signal):

		"""
		Typical analysis is done only with one-sided spectrum, i.e. with half of the power spectrum sequence. 
		To preserve the total amount of energy shown in the half-range double the spectrum with adjustment 
		for cases of even or odd length. Calculation of power spectrum is an important step of extracting feature
		from speech signals. See more on feature extraction in a later section of the document.
		"""

		freq_signal **= 2 
		len_fts = len(freq_signal)
		len_signal = len(signal)

		if len_signal % 2:
			freq_signal[1:len_fts] *= 2

		else:
			freq_signal[1:len_fts-1] *= 2

		return freq_signal

	def return_mfcc(self, time_signal, num_cep=13, nfft=512):

		features_mfcc = mfcc(time_signal, samplerate=self.sampling_freq, nfft=nfft, winlen=0.025, winstep=0.01, numcep=num_cep)
		
		return features_mfcc
















