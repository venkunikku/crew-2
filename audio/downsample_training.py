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
    
	for folder in os.listdir(current_dir):
	
		if folder != '.DS_Store':
 
			path = os.path.join(current_dir, folder)
			for filename in os.listdir(path):
				if filename != '.DS_Store':	
					a,b = librosa.core.load(os.path.join(path, filename),sr=sr, mono=True)
					sf.write((target_dir + "/" + filename), a, b, subtype = 'PCM_16')
    
else:
    
	bucket_name = "ad-bucket-15730"
	current_dir = 'training/UrbanSound8K/audio'
	target_dir = "training_downsampled"
    
    # open storage client
	storage_client = storage.Client()
    # name bucket from storage client
	bucket = storage_client.get_bucket(bucket_name)
    # get list of all audio files
	blobs = list(bucket.list_blobs(prefix=current_dir))
    
	for i in range(len(blobs)):
        
        # ignore .DS_Store files
		if ".DS_Store" not in str(blobs[i]):
            
			# extract just file name from str
			file_name = blobs[i].name.split("/")[-1]   
            # download blob as string
			file_as_string = blobs[i].download_as_string()
            # convert string to bytes and then load to librosa
			a,b = librosa.core.load(io.BytesIO(file_as_string),sr=sr, mono=True)
            # write temporarily to wav file
			sf.write(("tmp/" + file_name), a, b, subtype = 'PCM_16')
            # create new file path/name
			new_file_name = "%s/%s" % (target_dir, file_name)
            # assign new file name to blog storage object
			blob = bucket.blob(new_file_name)
            # upload temp file to new blog storage object
			blob.upload_from_file("tmp/" + file_name)
			# delete temp file
			os.remove("tmp/" + file_name)
            
            
            
        
        
    


    
