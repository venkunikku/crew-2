import librosa
import soundfile as sf
import wave
import os
from google.cloud import storage
import io

import argparse
parser = argparse.ArgumentParser(description='train parser')
parser.add_argument('--gcp', action='store_true', dest='gcp', help='affects whether to configure to running on the cloud')
parser.add_argument('--local', action='store_false', dest='gcp', help='affects whether to configure to running on the cloud')

parse_results = parser.parse_args()

### SPECIFY WHERE WE'RE RUNNING ###
gcp = parse_results.gcp

if gcp == False:
    
    noise_dir = "../../noise/"

    infiles = os.listdir(noise_dir)
    outfile = noise_dir + "combined-noise.wav"

    combined_data = []
    for infile in infiles:

        # ignore .DS_Store files
        if ".wav" in infile:

            print(infile)
            x,sr = sf.read(noise_dir + infile)
            sf.write('tmp/tmp.wav', x, sr)
            w = wave.open('tmp/tmp.wav', 'r')
            combined_data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()

    output = wave.open(outfile, 'wb')
    output.setparams(combined_data[0][0])
    output.writeframes(combined_data[0][1])
    output.writeframes(combined_data[1][1])
    output.close()
    
else:
    
    bucket_name = "ad-bucket-15730"
    noise_dir = "noise"
    outfile = "combined-noise.wav"
    # open storage client
    storage_client = storage.Client()
    # name bucket from storage client
    bucket = storage_client.get_bucket(bucket_name)
    # get list of all audio files
    infiles = list(bucket.list_blobs(prefix=noise_dir))

    combined_data = []
    for infile in infiles:
        
        # ignore .DS_Store files
        if ".wav" in str(infile.name):
            
            # download blob as string
            file_as_string = infile.download_as_string()
            x,sr = sf.read(io.BytesIO(file_as_string))
            sf.write('tmp/tmp.wav', x, sr)
            w = wave.open('tmp/tmp.wav', 'r')
            combined_data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()

    output = wave.open("tmp/" + outfile, 'wb')
    output.setparams(combined_data[0][0])
    output.writeframes(combined_data[0][1])
    output.writeframes(combined_data[1][1])
    output.close()

    # create new file path/name
    new_file_name = "%s/%s" % (noise_dir, outfile)
    # assign new file name to blog storage object
    blob = bucket.blob(new_file_name)
    # upload temp file to new blog storage object
    blob.upload_from_filename("tmp/" + outfile)
    # delete temp file
    os.remove("tmp/" + outfile)











