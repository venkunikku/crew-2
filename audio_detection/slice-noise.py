from pydub import AudioSegment
import numpy as np

noise_downsampled_dir = "../../noise_downsampled/"

audio_file = noise_downsampled_dir + "combined-noise.wav"
audio = AudioSegment.from_wav(audio_file)
list_of_timestamps = list(np.arange(5,120,5))  #and so on in *seconds*

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
