#!/usr/bin/env python
# coding: utf-8

# start clock from beginning 
import time
start_time = time.time()

import numpy as np
import os

import librosa
import pyaudio
import noisereduce as nr

import tensorflow as tf
from keras.models import load_model
import glob
import os
import librosa
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib

import IPython
from sklearn.externals import joblib

#from NN_model.inference_NN import extract_feature, NN_predict
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
    

def extract_feature(X, sample_rate):
    #X, sample_rate = librosa.load(audio_input)
    stft = np.abs(librosa.stft(X))
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
    # return mfccs,chroma,mel,contrast,tonnetz
    ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
    test_x = np.array(ext_features)
    return(test_x)


def NN_predict(audio_input, model, sample_rate, scaler):
    #model = load_model(model_file)
    test_x = extract_feature(audio_input, sample_rate)
    #test_x = np.transpose(test_x)
    test_x = test_x.reshape((1,193))
    
    test_x = scaler.transform(test_x)
    
    predict_y = model.predict(test_x)
    print(predict_y)
    pred_y = np.where(predict_y == np.max(predict_y))[1][0]
    print(pred_y)
    class_name = (  [0, 'air_conditioner'],
                        [1, 'car_horn'],
                        [2, 'children_playing'],
                        [3, 'dog_bark'],
                        [4, 'drilling'],
                        [5, 'engine_idling'],
                        [6, 'gun_shot'],
                        [7, 'jackhammer'],
                        [8, 'siren'],
                        [9, 'street_music'])
     
    pred_label = class_name[pred_y]
    print('Prdiction is ', pred_label)

# define mic sampling rate
sampling_rate = 44100

# fix buffer size
#frames_per_buffer = 100
# chunk_size is same as frames per buffer

# set chunk size equal to frames_per_buffer
chunk_size = 1024
record_seconds = 4

total_samples = sampling_rate * record_seconds

features_array = joblib.load('features_array.sav')
features = np.array(features_array)
sc = StandardScaler()
sc.fit(features)

# initialize portaudio
p = pyaudio.PyAudio()


# for NN inference
#hmm = True
NN = True

if NN == True:

    # load in models
    production_models = load_model('NN_model/NN_model_weights.h5')#("./hmm_models/production_HMM_models.pkl")
    # sort alphabetically per label encoder
    #production_models.sort(key=lambda x:x[1])

    ### STREAMING ###

    # start the stream
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sampling_rate, 
    input=True, frames_per_buffer=chunk_size)
    print('start streaming')
    
    #stream = librosa.stream(filename,block_length=256,frame_length=4096,hop_length=1024)
    #print('start streaming')
    current_window = np.arrary([])
    
    while(True):

        read_time = time.time()
        # read chunk and load it into numpy array
        data = stream.read(total_samples)
        current_window = np.frombuffer(data, dtype=np.float32)
        
        #if total_samples  >= len(current_window) or time.time() - read_time >= 4  :
        # make prediction based on current_window
        #prediction_index = inference_NN.inference_NN.NN_predict(production_models, current_window) 
        print('start to predicting')
          
        NN_predict(model = production_models,
                 audio_input = current_window,
                sample_rate = sampling_rate)
            
        break
            
        #prediction = list(lb.inverse_transform([prediction_index]))[0]
        # write prediction
        #with open ("logs/audio_logx.txt","a") as logs:
        #    logs.write("predicting {} at time {}".format(prediction, str(read_time-start_time)))

        
        #if (time.time() - read_time >= 10):
         #   print('break')
          #  break

# close stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    print('stop streaming')
                               

