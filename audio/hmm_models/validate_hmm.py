"""
LOAD NECESSARY MODULES
"""

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import pandas as pd
import numpy as np
import os
import warnings
from scipy.io import wavfile
from hmmlearn import hmm  
import pomegranate
from python_speech_features import mfcc
from sklearn.externals import joblib
import hmm_model_feature_extraction
from model_utils import HMM_Model
import random
from tqdm import tqdm
from ast import literal_eval
from google.cloud import storage

"""
MODEL CONFIGURATIONS
"""

import argparse
parser = argparse.ArgumentParser(description='train parser')
parser.add_argument('--gcp', action='store_true', dest='gcp', help='affects whether to configure to running on the cloud')
parser.add_argument('--local', action='store_false', dest='gcp', help='affects whether to configure to running on the cloud')
parser.add_argument('--trial_name', action='store', dest='trial_name', help='indicate name of trial')
parser.add_argument('--num_cep_coefs', action='store', dest='num_cep_coefs', type=int, \
                    help='indicate number of cepstral coefficients to use')

parse_results = parser.parse_args()

### SPECIFY WHERE WE'RE RUNNING ###
gcp = parse_results.gcp
### name this particular trial ###
trial_name = parse_results.trial_name
print("trial_name: ", trial_name)
### number of cepstral coefficients to return from mfcc (13 is typical) ###
num_cep_coefs = parse_results.num_cep_coefs
print("num_cep_coefs: ", num_cep_coefs)


"""
ADDITIONAL CONFIGURATIONS BASED ON COMPUTE LOCATION
"""

if gcp == True:
    
    import gcsfs
    import pickle
    import cupy
    
    # specify gcs bucket
    bucket_name = "ad-bucket-15730"
    # set cloud based mixed dir
    gcs_mixed_dir = "gs://{}/mixed_20k".format(bucket_name)
    # set cloud based hmm model dir
    gcs_hmm_model_dir = "gs://{}/hmm_models".format(bucket_name)
    # set cloud based validation dir
    gcs_validation_dir = "gs://{}/validation".format(bucket_name)
    # set local, vm-based mixed dir
    local_mixed_dir = "mixed_local"
    # set local, vm-based validation dir
    local_validation_dir = "validation_local"
    # initialize gcsfs object
    fs = gcsfs.GCSFileSystem(project = 'audio-detection-1')
    metadata = pd.read_csv(gcs_mixed_dir + "/mixed_metadata.csv")
	
    # enable gpus for pomegranate
    pomegranate.utils.enable_gpu()
    print("communicating with GPU: ", pomegranate.utils.is_gpu_enabled())
    
    ### moving pre-populated validation and training set ###
    ### for faster model validation ###
    
    # need to create folder on vm instance for validation set
    if "validation_local" not in os.listdir():
        
        os.mkdir("validation_local")
        
    # need to create folder on vm instance for training (mixed) set 
    if "mixed_local" not in os.listdir():
        
        os.mkdir("mixed_local")
        
    # if fewer then ten (arbitrary) files, copy all in from gcs   
    if len(os.listdir("validation_local")) < 10:
        
        os.system("gsutil -m cp {}/* ./{}".format(gcs_validation_dir, local_validation_dir))
        
    # if fewer then ten (arbitrary) files, copy all in from gcs    
    if len(os.listdir("mixed_local")) < 10:
        
        os.system("gsutil -m cp {}/* ./{}".format(gcs_mixed_dir, local_mixed_dir))

    
else:
    
    # configuration when not running on the cloud
    local_mixed_dir = "../../../mixed"
    local_hmm_model_dir = "../../../hmm_models"
    metadata = pd.read_csv(local_mixed_dir + "/mixed_metadata.csv")

### initialize feature extraction class ###
# mixed_dir will depend on whether we are pulling from gcs or locally
# sampling_freq will depend on how we initially processed our audio files
# gcs will depend on whether we want to pull from gcs during training or from local directory
fe = hmm_model_feature_extraction.feature_extraction(mixed_dir=local_mixed_dir, sampling_freq = 20000, gcs = False)

### choose hidden states per self-organizing maps

label_states = pd.Series({"air_conditioner":20, "car_horn":18, "children_playing":11,
             "dog_bark":17, "drilling":20, "engine_idling":20,
             "gun_shot":9, "jackhammer":18, "siren":17,
             "street_music":17})

"""
DEFINE SCORING FUNCTION
"""

def score_one_sample(trained_models, test_file_name):
    
    """
    trained_model: ModelHMM object with trained model
    test_file_path: path to wav file
    """
    # empty list to hold all of the scores
    scores = []
    
    # load in file from validation set and convert to mfcc features
    loaded = fe.read(test_file_name)
    mfcc_features = fe.return_mfcc(loaded, nfft=1200)
    
    # iterate through each of the trained models
    for i in trained_models:
        
        # compute log likelihood score for using each of the trained models
        sample_score = i[0][0][0].compute_score(mfcc_features)
        scores.append(sample_score)
        
    predicted = scores.index(max(scores))
    print("max score is:", max(scores), "at index:", predicted)
    predicted = trained_models[predicted][0][1]
   
    return predicted

"""
LOAD MODEL FROM PKL
"""

if gcp == True:
    
    with fs.open(gcs_hmm_model_dir + '/model_{}.pkl'.format(trial_name), 'rb') as file:
        asdf = pickle.load(file)
        
else:

    trained_models = joblib.load(local_hmm_model_dir + '/model_{}.pkl'.format(trial_name))

"""
LOAD IN VALIDATION SAMPLES
"""

if gcp == True:

    f = fs.open(gcs_hmm_model_dir + '/validation_samples_{}.txt'.format(trial_name),'r')
    validation_samples = f.readlines()
    f.close()
    validation_samples = [literal_eval(validation_samples[i]) for i in range(len(validation_samples))]   

else:

    f = open(local_hmm_model_dir + '/validation_samples_{}.txt'.format(trial_name),'r')
    validation_samples = f.readlines()
    f.close()
    validation_samples = [literal_eval(validation_samples[i]) for i in range(len(validation_samples))]  

"""
ITERATE THROUGH VALIDATION SAMPLE USING VALIDATION FUNCTION
"""

points = 0
validation_list = []

for i in tqdm(range(len(validation_samples))):
    
    print("validation sample size: ", len(validation_samples))
    actual = validation_samples[i][1]
    print("actual: ", actual)
    predicted = score_one_sample(trained_models, validation_samples[i][0])
    print("predicted:", predicted)
    validation_list.append((actual,predicted))
    if actual == predicted:
        
        points += 1
        print("scored a point!")
        print(points, "points")

"""
PRINT OVERALL ACCURACY
"""

overall_accuracy = points/len(validation_samples)
print("overall accuracy: ", overall_accuracy)

"""
CREATE DF OUT OF VALIDATION LIST
"""

validation_performance_df = pd.DataFrame(validation_list, columns = ['actual', 'predicted']) 

"""
SAVE RESULTING VALIDATION PERFORMANCE DF TO HMM_MODEL DIR
"""

if gcp == True:
    
    validation_performance_df.to_csv(gcs_hmm_model_dir + '/validation_performance_{}.csv'.format(trial_name))
    label_states.to_csv(gcs_hmm_model_dir + '/label_states_{}.csv'.format(trial_name))
    
else:
    
    validation_performance_df.to_csv(local_hmm_model_dir + '/validation_performance_{}.csv'.format(trial_name))
    label_states.to_csv(local_hmm_model_dir + '/label_states_{}.csv'.format(trial_name))

    
       




