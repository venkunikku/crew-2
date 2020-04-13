from pydub import AudioSegment
import numpy as np
from google.cloud import storage

gcp = False

if gcp == False:
    
    noise_downsampled_dir = "../../noise_downsampled/"

    audio_file = noise_downsampled_dir + "combined-noise.wav"
    audio = AudioSegment.from_wav(audio_file)
    list_of_timestamps = list(np.arange(4,120,4))  #and so on in *seconds*

    start = 0
    for  idx,t in enumerate(list_of_timestamps):
        #break loop if at last element of list
        if idx == len(list_of_timestamps):
            break

        end = t * 1000 #pydub works in millisec
        print("split at [{}:{}] s".format(start/1000, end/1000))
        audio_chunk = audio[start:end]
        audio_chunk.export(noise_downsampled_dir + "noise_chunk_{}.wav".format(end/1000), format="wav")

        start = end  #pydub works in millisec
    
else:
    
    merged_noise_downsampled_file = "noise/combined-noise.wav"
    noise_downsampled_dir = "noise_downsampled"
    # open storage client
    storage_client = storage.Client()
    # name bucket from storage client
    bucket = storage_client.get_bucket(bucket_name)
    # get list of all audio files
    blobs = list(bucket.list_blobs(prefix=merged_noise_downsampled_file))

    for i in range(len(blobs)):
        
        # ignore .DS_Store files
        if ".DS_Store" not in str(blobs[i].name):

            # download blob as string
            file_as_string = blobs[i].download_as_string()

            audio = AudioSegment.from_wav(io.BytesIO(file_as_string))
            list_of_timestamps = list(np.arange(4,120,4))  #and so on in *seconds*

            start = 0
            for  idx,t in enumerate(list_of_timestamps):
                #break loop if at last element of list
                if idx == len(list_of_timestamps):
                    break

                end = t * 1000 #pydub works in millisec
                print("split at [{}:{}] s".format(start/1000, end/1000))
                audio_chunk = audio[start:end]
                file_name = "noise_chunk_{}.wav".format(end/1000)
                audio_chunk.export("tmp/" + file_name, format="wav")
                # create new file path/name
                new_file_name = "%s/%s" % (noise_downsampled_dir, file_name)
                # assign new file name to blog storage object
                blob = bucket.blob(new_file_name)
                # upload temp file to new blog storage object
                blob.upload_from_file("tmp/" + file_name)
                # delete temp file
                os.remove("tmp/" + file_name)

                start = end  #pydub works in millisec








