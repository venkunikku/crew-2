import os
import librosa
import soundfile as sf
import io
from google.cloud import storage

# define sample rate to which you wish to convert
sr = 20000

gcp = True

if gcp == False:
    
    source = '../../noise'
    target = '../../noise_downsampled'

    files = librosa.util.find_files(source, ext='wav')

    for file in files:
        basename = os.path.basename(file)
        y, sr = librosa.load(file, sr=sr, mono = True)
        sf.write((target + "/" + basename), y, sr, subtype = 'PCM_16')
    
else:
    
    bucket_name = "ad-bucket-15730"
    source = 'noise'
    target = 'noise_downsampled'

    # open storage client
    storage_client = storage.Client()
    # name bucket from storage client
    bucket = storage_client.get_bucket(bucket_name)
    # get list of all audio files
    blobs = list(bucket.list_blobs(prefix=source))
    
    for i in range(len(blobs)):
        
        # ignore .DS_Store files
        if ".wav" in str(blobs[i]):
            # extract just file name from str
            file_name = blobs[i].name.split("/")[-1]   
            # download blob as string
            file_as_string = blobs[i].download_as_string()
            # convert string to bytes and then load to librosa, resample at target sample rate 'sr'
            a,b = librosa.core.load(io.BytesIO(file_as_string),sr=sr, mono=True)
            # write temporarily to wav file
            sf.write(("tmp/" + file_name), a, b, subtype = 'PCM_16')
            # create new file path/name
            new_file_name = "%s/%s" % (target, file_name)
            # assign new file name to blog storage object
            blob = bucket.blob(new_file_name)
            # upload temp file to new blog storage object
            blob.upload_from_filename("tmp/" + file_name)
            # delete temp file
            os.remove("tmp/" + file_name)



