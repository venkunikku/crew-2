import os
import pandas as pd
from pydub import AudioSegment
from random import seed
from random import randint 
import glob
import shutil
from google.cloud import storage
import io

# number of random mixes you want to make for each original smaple
n_iterations = 2

gcp = True

if gcp == False:
    
    noise_downsampled_dir = '../../noise_downsampled/'
    down_sampled_training_dir = '../../training_downsampled/'
    target_dir = '../../mixed/'
    metadata_file = '../../training/UrbanSound8K/metadata/metadata.csv'

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

    # read in original metadata file
    meta_data = pd.read_csv(metadata_file)
    # write original metadata to new directory
    meta_data.to_csv(target_dir+'mixed_metadata.csv', index = False)
    # and read back into pandas
    mixed_meta_data = pd.read_csv(target_dir+'mixed_metadata.csv')

    # create list of noise file names
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
    
else:

    bucket_name = "ad-bucket-15730"
    noise_downsampled_dir = 'noise_downsampled'
    down_sampled_training_dir = 'training_downsampled'
    noise_downsampled_dir = 'noise_downsampled'
    target_dir = 'mixed'
    metadata_file = 'gs://ad-bucket-15730/training/UrbanSound8K/metadata/metadata.csv'

    """
    randomly mixes clean audio files and noise and stores in designated directory
    """

    # move clean downsampled files over
    #os.system("gsutil cp gs://ad-bucket-15730/training_downsampled/* gs://ad-bucket-15730/mixed")

    # read in original metadata file
    mixed_meta_data = pd.read_csv(metadata_file)
    # write original metadata to new directory
    #meta_data.to_csv('tmp/mixed_metadata.csv', index = Fals
    # and read back into pandas
    #mixed_meta_data = pd.read_csv('tmp/mixed_metadata.csv')

    # create list of noise file names
    noise_chunks = []
    # open storage client
    storage_client = storage.Client()
    # name bucket from storage client
    bucket = storage_client.get_bucket(bucket_name)
    # get list of all audio files
    noise_blobs = list(bucket.list_blobs(prefix=noise_downsampled_dir))

    for blob in noise_blobs:

        if 'noise_chunk' in blob.name:

            noise_chunks.append(blob.name)

    # depends on the number of times you want to randomly mix each file
    for i in range(n_iterations):
    
        seed(i)

        # for one iteration, mix each file in the training directory
        # open storage client
        storage_client = storage.Client()
        # name bucket from storage client
        bucket = storage_client.get_bucket(bucket_name)
        # get list of all audio files
        training_blobs = list(bucket.list_blobs(prefix=down_sampled_training_dir))

        for blob in training_blobs:

            # ignore .DS_Store files
            if ".wav" in str(blob.name):
    
                # get the downsampled training clip
                # download blob as string
                file_as_string = blob.download_as_string()
                # convert to bytes and then load into pydub
                sound1 = AudioSegment.from_wav(io.BytesIO(file_as_string))
                # random pick a noise chunk
                random_int = randint(0, (len(noise_chunks)-1))
                noise_file = noise_chunks[random_int]
                # open storage client
                storage_client = storage.Client()
                # name bucket from storage client
                bucket = storage_client.get_bucket(bucket_name)
                # get list of all noise files
                noise_blob = list(bucket.list_blobs(prefix=noise_file))[0]
                # download blob as string
                file_as_string = noise_blob.download_as_string()
                # convert to bytes and then read into pydub
                sound2 = AudioSegment.from_wav(io.BytesIO(file_as_string))
                # combine both sound files
                combined = sound1.overlay(sound2)
                # generate new file name
                # extract just file name from str
                file_name = blob.name.split("/")[-1]
                new_file_name = "mixed_" + str(i) + "_" + file_name
                # export resulting wav to tmp dir
                combined.export("tmp/" + new_file_name, format="wav")
                # create new file path/name
                new_dir_name = "%s/%s" % (target_dir, new_file_name)
                # assign new file name to blog storage object
                new_blob = bucket.blob(new_dir_name)
                # upload temp file to new blog storage object
                new_blob.upload_from_filename("tmp/" + new_file_name)
                # delete temp file
                os.remove("tmp/" + new_file_name)
                print("uploaded {} to bucket and removed from tmp".format(new_file_name))

                # update metadata
                row = mixed_meta_data[mixed_meta_data['slice_file_name'] == file_name]
                mixed_meta_data = mixed_meta_data.append(row)
                updated_row = mixed_meta_data.iloc[len(mixed_meta_data)-1].replace({mixed_meta_data.iloc[len(mixed_meta_data)-1,0]:"%s" % (new_file_name)})
                mixed_meta_data.iloc[len(mixed_meta_data)-1] = updated_row

                print("length:",len(mixed_meta_data)-1)
                newname = "%s" % (new_file_name)
                print("added to metadata; newname:",newname)
            
    
    # write finalized metadata to bucket
    mixed_meta_data.to_csv('gs://ad-bucket-15730/'+target_dir+'/mixed_metadata.csv', index = False)
    

