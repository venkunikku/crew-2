import wave
import os
import gcsfs

gcp = False

if gcp == False:
    noise_dir = "../../noise/"
    
else:
    noise_dir = "gs://ad-bucket-15730/noise/"

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










