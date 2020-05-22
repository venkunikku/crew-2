
import tensorflow as tf
from keras.models import load_model
import glob
import os
import librosa
import numpy as np
#import matplotlib.pyplot as plt
#from matplotlib.pyplot import specgram
#import time


        
        
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


def NN_predict(audio_input, model):
    #model = load_model(model_file)
    test_x = extract_feature(audio_input)
        
    predit_y = model.predict(test_x)
    pred_y = np.where(predit_y[i] == max(predit_y))

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
    print('Prdeciiton is %s', pred_label)
