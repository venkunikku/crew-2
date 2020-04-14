import os
import pandas as pd
import librosa 
from google.cloud import storage

gcp = False

x = []
sr = []
audio_class = []

if gcp == False:
    
    meta_data = pd.read_csv('../../training/UrbanSound8K/metadata/metadata.csv')
    folder_name = '../../mixed/'

    for filename in os.listdir(folder_name):

        file = os.path.join(folder_name, filename)

        a, b = librosa.core.load(file,sr=None)
        x.append(a)
        sr.append(b)

        temp_index = meta_data[meta_data['slice_file_name'] == filename].index
        audio_class.append(meta_data['classID'][temp_index[0]])
    
else:
    
    meta_data = pd.read_csv('gs://ad-bucket-15730/training/UrbanSound8K/metadata/metadata.csv')
    folder_name = 'gs://ad-bucket-15730/mixed/'





