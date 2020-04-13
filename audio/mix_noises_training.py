import os
import pandas as pd
from pydub import AudioSegment
from random import seed
from random import randint 
import glob
import shutil
import gcsfs

n_iterations = 2

gcp = False

if gcp == False:
    noise_downsampled_dir = '../../noise_downsampled/'
    down_sampled_training_dir = '../../training_downsampled/'
    noise_downsampled_dir = '../../noise_downsampled/'
    target_dir = '../../mixed/'
    metadata_file = '../../training/UrbanSound8K/metadata/metadata.csv'
    
else:
    noise_downsampled_dir = 'gs://ad-bucket-15730/noise_downsampled/'
    down_sampled_training_dir = 'gs://ad-bucket-15730/training_downsampled/'
    noise_downsampled_dir = 'gs://ad-bucket-15730/noise_downsampled/'
    target_dir = 'gs://ad-bucket-15730/mixed/'
    metadata_file = 'gs://ad-bucket-15730/training/UrbanSound8K/metadata/metadata.csv'
    

"""
randomly mixes clean audio files and noise and stores in designated directory
"""

# delete all existing contents
files = glob.glob(target_dir + '*')
for f in files:
    os.remove(f)

# move clean downsampled files over
for filename in glob.glob(os.path.join(down_sampled_training_dir, '*.*')):
    shutil.copy(filename, target_dir)

mixed_meta_data = pd.read_csv(metadata_file)

# read in noise files
noise_chunks = []
for i in os.listdir(noise_downsampled_dir):
    if os.path.isfile(os.path.join(noise_downsampled_dir,i)) and 'noise_chunk' in i:
        noise_chunks.append(i)

# depends on the number of times you want to randomly mix each file
for i in range(n_iterations):
    
    seed(i)

    # for one iteration, fix each file in the training directory
    for filename in os.listdir(down_sampled_training_dir):

        if filename != ".DS_Store":
    
            # get the downsampled training clip
            file_path1 = os.path.join(down_sampled_training_dir, filename)
            sound1 = AudioSegment.from_file(file_path1)

            # random pick a noise chunk
            random_int = randint(0, (len(noise_chunks)-1))
            noise_file = noise_chunks[random_int]
            file_path2 = os.path.join(noise_downsampled_dir, noise_file)
            sound2 = AudioSegment.from_file(file_path2)
        
            # combine both sound files
            combined = sound1.overlay(sound2)
        
            # export resulting wav to target dir
            combined.export(target_dir + "mixed_" + str(i) + "_" + filename, format="wav")

            # update metadata
            row = mixed_meta_data[mixed_meta_data['slice_file_name'] == filename]
            mixed_meta_data = mixed_meta_data.append(row)
            updated_row = mixed_meta_data.iloc[len(mixed_meta_data)-1].replace({mixed_meta_data.iloc[len(mixed_meta_data)-1,0]:"mixed_%s_%s" % (str(i),filename)})
            mixed_meta_data.iloc[len(mixed_meta_data)-1] = updated_row

            print("length:",len(mixed_meta_data)-1)
            newname = "mixed_%s_%s" % (str(i), filename)
            print("newname:",newname)
            
mixed_meta_data.to_csv(target_dir+'mixed_metadata.csv', index = False)
