import pandas as pd
import numpy as np
import random
from google.cloud import storage
import os

"""
If training on the cloud, set aside validation set ahead of time for faster validation

"""

bucket_name = "ad-bucket-15730"
mixed_dir = "mixed_20k"
validation_dir = "validation"
validation_set = []
training_prop = 0.8
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)

# read in metadata
metadata = pd.read_csv("gs://" + bucket_name + "/" + mixed_dir + "/mixed_metadata.csv")

# get wav file names as list
file_names = metadata['slice_file_name'].tolist()

# determine how many are for traning
num_to_train = int(np.ceil(len(file_names) * training_prop))

# randomly pull out files to train
train = random.sample(file_names, num_to_train)
print("train length:", len(train))

# derive validation_set from train and convert to list
validation_set = list(set(file_names) - set(train))

for i in range(len(validation_set)):

    print(i)
    source_blob = bucket.blob(mixed_dir + "/" + validation_set[i])
    new_blob = bucket.copy_blob(source_blob, bucket, validation_dir + "/" + validation_set[i])
    source_blob.delete()






