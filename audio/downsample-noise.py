#!/usr/bin/env python
# coding: utf-8

import os
import librosa
import soundfile as sf

target = '../../noise_downsampled'

files = librosa.util.find_files('../../noise', ext='wav')

for file in files:
    basename = os.path.basename(file)
    print(file)
    print(basename)
    y, sr = librosa.load(file, sr=44100, mono = True)
    sf.write((target + "/" + basename), y, sr, subtype = 'PCM_16')

