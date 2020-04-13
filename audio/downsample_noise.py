import os
import librosa
import soundfile as sf
import gcsfs

gcp = False

if gcp == False:
    
    source = '../../noise'
    target = '../../noise_downsampled'
    
else:
    
    source = 'gs://ad-bucket-15730/noise'
    target = 'gs://ad-bucket-15730/noise_downsampled'

files = librosa.util.find_files(source, ext='wav')

for file in files:
    basename = os.path.basename(file)
    print(file)
    print(basename)
    y, sr = librosa.load(file, sr=44100, mono = True)
    sf.write((target + "/" + basename), y, sr, subtype = 'PCM_16')

