import os
import librosa
import soundfile as sf
import gcsfs

sr = 44100
audio_class = []

gcp = False

if gcp == False:

    current_dir = '../../training/UrbanSound8K/audio'
    target_dir = "../../training_downsampled"
    
else:
    
    current_dir = 'gs://ad-bucket-15730/training/UrbanSound8K/audio'
    target_dir = "gs://ad-bucket-15730/training_downsampled"
    

for folder in os.listdir(current_dir):
	
	if folder != '.DS_Store':
 
		path = os.path.join(current_dir, folder)
		for filename in os.listdir(path):
			if filename != '.DS_Store':	
				a,b = librosa.core.load(os.path.join(path, filename),sr=sr, mono=True)
				sf.write((target_dir + "/" + filename), a, b, subtype = 'PCM_16')

