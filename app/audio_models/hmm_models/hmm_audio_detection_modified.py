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

import scipy.io.wavfile as wavfile

import app.audio_models.hmm_models.hmm_inference
import logging


def start_audio_model():
    mic_logger = logging.getLogger('gpg.mic')
    mic_logger.info('Start')
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
                      'drilling', 'engine_idling', 'gun_shot', 'jackhammer', 'siren', 'street_music'])
    # load in models
    production_models = joblib.load("production_HMM_models.pkl")
    # sort alphabetically per label encoder
    production_models.sort(key=lambda x: x[1])
    ### STREAMING ###
    # start the stream
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sampling_rate,
                    input=True, frames_per_buffer=chunk_size)
    while (True):

        read_time = time.time()
        # read chunk and load it into numpy array
        data = stream.read(chunk_size)
        current_window = np.frombuffer(data, dtype=np.float32)

        # calculate mean signal power
        freq_signal = np.fft.fft(current_window)
        len_signal = len(current_window)
        len_half = np.ceil((len_signal + 1) / 2.0).astype(np.int)
        freq_signal = abs(freq_signal[0:len_half]) / len_signal
        freq_signal **= 2
        len_fts = len(freq_signal)

        if len_signal % 2:
            freq_signal[1:len_fts] *= 2
        else:
            freq_signal[1:len_fts - 1] *= 2

        signal_power = 10 * np.log10(freq_signal)
        # remov any nans and infs
        signal_power = signal_power[~np.isnan(signal_power)]
        signal_power = signal_power[~np.isinf(signal_power)]

        mean_signal_power = np.mean(signal_power)

        print(mean_signal_power)

        if mean_signal_power > -50:

            # make prediction based on current_window
            prediction_index = hmm_inference.hmm_inference(production_models, current_window)
            prediction = list(lb.inverse_transform([prediction_index]))[0]
            print("predicting ", prediction, " at time ", str(read_time - start_time))
            mic_logger.info(prediction)

        # just to be explicit:
        else:
            print("within quiet range")
            pass
