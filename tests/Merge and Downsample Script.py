#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import librosa
import soundfile as sf


# In[7]:


target = 'C:\\Users\\ddobrzynski\\Documents\\MScA\\Capstone-Robots\\Data\\UrbanSound8K\\downsampled\\'

files = librosa.util.find_files('C:/Users/ddobrzynski/Documents/MScA/Capstone-Robots/Data/UrbanSound8K/audio', ext='wav')

for file in files:
    basename = os.path.basename(file)
    print(file)
    print(basename)
    y, sr = librosa.load(file, sr=8000, mono = True)
    sf.write((target + basename), y, sr, subtype = 'PCM_16')

