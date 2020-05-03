import pyaudio
import numpy as np
import numpy.fft as fft
import time

CHUNK = 4096 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)
STREAM_SECONDS = 30

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

frequencies = []


while True: 
# create a numpy array holding a single read of audio data
    for i in range(0, int(RATE / CHUNK * STREAM_SECONDS)):#to it a few times just to see
        data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        spectrum = fft.fft(data)
        freqs = fft.fftfreq(len(spectrum))
        l = len(data)
        
        #imax = index of first peak in spectrum
        imax = np.argmax(np.abs(spectrum))
        fs = freqs[imax]
        
        freq = (imax*fs/l)*1000000
        #frequencies.append(freq)
        print(freq)
        if freq > 1500:
            import record_noise.py
            stream.stop_stream()
            stream.close()
            p.terminate()
    break
    
# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()

#print(frequencies)
