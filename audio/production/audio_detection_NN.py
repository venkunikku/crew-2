#!/usr/bin/env python
# coding: utf-8

# start clock from beginning 
import time
start_time = time.time()

import numpy as np
import librosa
import pyaudio
import wave
import tensorflow as tf
from keras.models import load_model
import os

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.externals import joblib

#from NN_model.inference_NN import extract_feature, NN_predict
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
    

def extract_feature(audio_input):
    X, sample_rate = librosa.load(file_name)

    # Short-time Fourier transform
    stft = np.abs(librosa.stft(X))

    # Mel-frequency cepsetrum coefficient and use 40 coefficient
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=12).T,axis=0)

    # Chroma freatures represent 12 different pitch classes
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)

    # Mel-scaled sepectrogram
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)

    # spectral contrast
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)

    # Tonal centroid features
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)

    # spectral centroid is a measure used in digital signal processing to characterise a spectrum.
    cent = np.mean(librosa.feature.spectral_centroid(y=X, sr=sample_rate).T,axis=0)

    # Spectral Rolloff This measure is useful in distinguishing voiced speech from unvoiced
    rolloff = np.mean(librosa.feature.spectral_rolloff(y=X, sr=sample_rate).T,axis=0)

    # return mfccs,chroma,mel,contrast,tonnetz
    ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
    test_x = np.array(ext_features)
    return(test_x)

def NN_predict(audio_input, model, sample_rate, scaler):
    # Extract features by using extract_feature function
    test_x = extract_feature(audio_input, sample_rate)
    test_x = test_x.reshape((1,193))
    
    # Use standardScaler to transform data
    test_x = scaler.transform(test_x)
    
    predict_y = model.predict(test_x)
    print(predict_y)
    
    # Show the predicted class
    pred_y = np.where(predict_y == np.max(predict_y))[1][0]
    #print(pred_y)
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

# Degfine chunk_size
chunk_size = 8192

# Define recording length and total sampled needed
record_seconds = 4
total_samples = sampling_rate * record_seconds



# initialize portaudio
p = pyaudio.PyAudio()

audio_format = pyaudio.paFloat32

# for NN inference
#hmm = True
NN = True

weight_path = 'NN_model/NN_model_weights.h5'
feature_path = 'features_array.sav'
if NN == True:

    # load in model
    production_models = load_model(weight_path)

    # Load the standard scaler from training data
    features_array = joblib.load(feature_path)
    features = np.array(features_array)
    sc = StandardScaler()
    sc.fit(features)

    ### STREAMING ###
    
    # start the stream
    stream = p.open(format=audio_format, channels=1, rate=sampling_rate, 
                    input=True, frames_per_buffer=chunk_size,
                    output = True, input_device_index = 2)
    
    

    current_window = np.array([])
    read_time = time.time()
    
    print('start streaming')
    stream.start_stream()
    
    while(True):

        if time.time() - read_time >= 4:
            #total_samples  >= len(current_window) and 
            # read chunk and load it into numpy array
            
            print('start to predicting')
            data = stream.read(total_samples)
            current_window = np.fromstring(data, dtype=np.float32)
            #current_window = np.float(current_window)
            
            NN_predict(model = production_models,
                        audio_input = current_window,
                        sample_rate = sampling_rate,
                        scaler = sc)

            # make prediction based on current_window 
            
            
            
            end_time = time.time()
            print('Time from hearing sound to finish prediction" ', end_time - read_time)

            break
        #prediction = list(lb.inverse_transform([prediction_index]))[0]
        # write prediction
        #with open ("logs/audio_logx.txt","a") as logs:
        #    logs.write("predicting {} at time {}".format(prediction, str(read_time-start_time)))

        
        #if (time.time() - read_time >= 10):
         #   print('break')
          #  break
    stream.write(current_window)
    stream.stop_stream()
    stream.close()
    p.terminate()
    print('stop streaming')

waveFile = wave.open('test_audio.wav', 'wb')
waveFile.setnchannels(1)
waveFile.setsampwidth(2)
waveFile.setframerate(sampling_rate)
waveFile.writeframes(b''.join(current_window))
waveFile.close()

file_name = 'test_audio.wav'
## the whole process takes 12.75s