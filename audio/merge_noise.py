import wave
import os
from google.cloud import storage

# adjust as needed
gcp = True

if gcp == False:
    
    noise_dir = "../../noise/"

    infiles = os.listdir(noise_dir)
	outfile = noise_dir + "combined-noise.wav"

	combined_data = []
	for infile in infiles:
    	w = wave.open(noise_dir + infile, 'rb')
    	combined_data.append([w.getparams(), w.readframes(w.getnframes())])
    	w.close()

	output = wave.open(outfile, 'wb')
	output.setparams(combined_data[0][0])
	output.writeframes(combined_data[0][1])
	output.writeframes(combined_data[1][1])
	output.close()
    
else:
    
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
		if ".DS_Store" not in str(infile.name):

			# download blob as string
			file_as_string = infile.download_as_string()
    		w = wave.open(io.BytesIO(file_as_string), 'rb')
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
	blob.upload_from_file("tmp/" + outfile)
	# delete temp file
	os.remove("tmp/" + file_name)












