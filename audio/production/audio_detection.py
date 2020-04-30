#!/usr/bin/env python
# coding: utf-8

import numpy as np
import os

import librosa
import pyaudio
import noisereduce as nr

from keras.models import model_from_json

from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib

import IPython

import hmm_model_feature_extraction
from model_utils import HMM_Model

# define mic sampling rate
sampling_rate = 44100
# fixed chunk size
chunk_size = 22050 

# initialize portaudio
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sampling_rate, 
    input=True, frames_per_buffer=chunk_size)

# enforce consistent encoding of labels
lb = LabelEncoder()
lb.fit_transform(['air_conditioner', 'car_horn', 'children_playing', 'dog_bark', 
    'drilling', 'engine_idling','gun_shot','jackhammer', 'siren', 'street_music'])

# for hmm inference
hmm = True

if hmm == True:

    production_models = joblib.load("./hmm_models/production_HMM_models.pkl")

    #noise window
    data = stream.read(10000)
    noise_sample = np.frombuffer(data, dtype=np.float32)
    loud_threshold = np.mean(np.abs(noise_sample)) * 10
    print("Loud threshold", loud_threshold)
    audio_buffer = []
    near = 0

    ### STREAMING ###

    while(True):

        # Read chunk and load it into numpy array
        data = stream.read(chunk_size)
        current_window = np.frombuffer(data, dtype=np.float32)
    
        # Reduce noise real-time
        current_window = nr.reduce_noise(audio_clip=current_window, noise_clip=noise_sample, verbose=False)
    
        if audio_buffer==[]:

            audio_buffer = current_window

        else:

            if np.mean(np.abs(current_window))<loud_threshold:
                
                print("Inside silence reign")
                
                if(near<10):

                    audio_buffer = np.concatenate((audio_buffer,current_window))
                    near += 1

                else:

                    predictSound(np.array(audio_buffer))
                    audio_buffer = []
                    near

            else:

                print("Inside loud reign")
                near = 0
                audio_buffer = np.concatenate((audio_buffer,current_window))

# close stream
stream.stop_stream()
stream.close()
p.terminate()

