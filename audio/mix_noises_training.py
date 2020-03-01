import os
import pandas as pd
from pydub import AudioSegment
from random import seed
from random import randint 


noise_downsampled_dir = '../noise_downsampled/'
## I used just one folder above
noise_chunks = []

for i in os.listdir(noise_downsampled_dir):
    if os.path.isfile(os.path.join(noise_downsampled_dir,i)) and 'noise_chunk' in i:
        noise_chunks.append(i)

seed(31)

down_sampled_training_dir = '../downsampled/'
noise_downsampled_dir = '../noise_downsampled/'
target_dir = '../training_downsampled/'


for filename in os.listdir(down_sampled_training_dir):
    # get the downsampled training clip
    base_name = filename
    file_path1 = os.path.join(down_sampled_training_dir, filename)
    #print(file_path1)
    sound1 = AudioSegment.from_file(file_path1)

    # random pick a noise chunk
    random_int = randint(0, (len(noise_chunks)-1))
    noise_file = noise_chunks[random_int]
    file_path2 = os.path.join(noise_downsampled_dir, noise_file)
    sound2 = AudioSegment.from_file(file_path2)
    
    
    combined = sound1.overlay(sound2)
    combined.export(target_dir + "mixed_" + base_name, format="wav")


## Gneratin new metadata
mixed_meta_data = pd.read_csv('../training/UrbanSound8K/metadata/metadata.csv')
name_list = mixed_meta_data['slice_file_name']
temp = ['mixed_' + s for s in name_list]
mixed_meta_data['slice_file_name'] = temp
mixed_meta_data.to_csv(target_dir+'mixed_metadata.csv', index = False)