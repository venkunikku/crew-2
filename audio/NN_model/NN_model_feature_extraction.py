import glob
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram
import pandas as pd
from sklearn.externals import joblib



## feature extract functions for all 193 features
def extract_feature(file_name):
    X, sample_rate = librosa.load(file_name)

    # Short-time Fourier transform
    stft = np.abs(librosa.stft(X))

    # Mel-frequency cepsetrum coefficient and use 40 coefficient
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)

    # Chroma freatures represent 12 different pitch classes
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)

    # Mel-scaled sepectrogram
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)

    # spectral contrast
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)

    # Tonal centroid features
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)

    return mfccs, chroma, mel, contrast, tonnetz

'''
There are two more possibel feaures, and havn't used in the current model
# spectral centroid is a measure used in digital signal processing to characterise a spectrum.
cent = librosa.feature.spectral_centroid(y=y, sr=sr)

# Spectral Rolloff This measure is useful in distinguishing voiced speech from unvoiced
rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
'''


## one_hot_encoede function for 10 labels 
def one_hot_encode(labels):
    n_labels = len(labels)
    n_unique_labels = len(np.unique(labels))
    one_hot_encode = np.zeros((n_labels,n_unique_labels))
    one_hot_encode[np.arange(n_labels), labels] = 1
    return one_hot_encode



## meta data dir
meta_data = pd.read_csv('../mixed/mixed_metadata.csv')

## read all mixed noisy audio data and extract all features described above
audio_class = []
folder_name = '../mixed/'
features, labels = np.empty((0,193)), np.empty(0)

for filename in os.listdir(folder_name):
    if filename != "mixed_metadata.csv":
        file = os.path.join(folder_name, filename)

        
        mfccs, chroma, mel, contrast,tonnetz = extract_feature(file)

        # stack all feaures into one row
        ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
        features = np.vstack([features,ext_features])

        # build correcponding label
        temp_index = meta_data[meta_data['slice_file_name'] == filename].index
        audio_class.append(meta_data['classID'][temp_index[0]])


## save features and labels

filename = 'audio_class_min_max.sav'
joblib.dump(audio_class, filename)  

filename = 'features_array_minmax.sav'
joblib.dump(features, filename)  