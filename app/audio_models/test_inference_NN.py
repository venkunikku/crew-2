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
    
    
def extract_feature(file_name):
    #extract all required feaures from a sound wave and stack them into a one row array
    X, sample_rate = librosa.load(file_name)
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
    # Extract features by using extract_feature function
    test_x = extract_feature(audio_input)
    test_x = test_x.reshape((1,193))
    
    # Use standardScaler to transform data
    test_x = scaler.transform(test_x)
    
    predict_y = model.predict(test_x)

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
    
sampling_rate = 44100

# Degfine chunk_size
chunk_size = 100

# Define recording length and total sampled needed
record_seconds = 4
total_samples = sampling_rate * record_seconds

features_array = joblib.load('features_array.sav')
features = np.array(features_array)
sc = StandardScaler()
sc.fit(features)


file_name = 'test_audio.wav'
#test_x = extract_feature(file_name)
#test_x = test_x.reshape(1,193)
production_models = load_model('NN_model/NN_model_weights.h5')

NN_predict(model = production_models,
            audio_input = file_name,
            sample_rate = sampling_rate,
            scaler = sc)

                       
                       