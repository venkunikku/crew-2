#!/usr/bin/env python
# coding: utf-8

# start clock from beginning 
import time
start_time = time.time()

import numpy as np
import os

import pyaudio

from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib

import hmm_inference

# define mic sampling rate
sampling_rate = 44100
# fix buffer size
frames_per_buffer = 100
# set chunk size equal to frames_per_buffer
chunk_size = 44100 * 4

# initialize portaudio
p = pyaudio.PyAudio()

# enforce consistent encoding of labels
lb = LabelEncoder()
lb.fit_transform(['air_conditioner', 'car_horn', 'children_playing', 'dog_bark', 
    'drilling', 'engine_idling','gun_shot','jackhammer', 'siren', 'street_music'])

# load in models
production_models = joblib.load("production_HMM_models.pkl")
# sort alphabetically per label encoder
production_models.sort(key=lambda x:x[1])

### STREAMING ###

# start the stream
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sampling_rate, 
    input=True, frames_per_buffer=chunk_size)

while(True):

    read_time = time.time()
    # read chunk and load it into numpy array
    data = stream.read(chunk_size)
    current_window = np.frombuffer(data, dtype=np.float32)
    print("current_window shape: ", current_window.shape)

    # make prediction based on current_window
    prediction_index = hmm_inference.hmm_inference(production_models, current_window) 
    prediction = list(lb.inverse_transform([prediction_index]))[0]
    print("predicting ", prediction, " at time ", str(read_time-start_time))

    # write prediction
    #logs =  open ("logs/audio_logx.txt","a")
    #logs.write("predicting {} at time {}".format(prediction, str(read_time-start_time))
    #logs.close()

