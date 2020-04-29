
import tensorflow as tf
from keras.models import load_model
import glob
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram
import time


% time
def extract_feature(file_name):
    X, sample_rate = librosa.load(file_name)
    stft = np.abs(librosa.stft(X))
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
    return mfccs,chroma,mel,contrast,tonnetz


mfccs, chroma, mel, contrast,tonnetz = extract_feature(file)
ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
#features = np.vstack([features,ext_features])
test_x = np.array(ext_features)


weights_path = ''
model = load_model('weights_path')


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
