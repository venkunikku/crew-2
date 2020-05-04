import numpy as np
import os

from python_speech_features import mfcc

from model_utils import HMM_Model

def hmm_inference(production_models, input_sample): 
    
    scores = []
    
    mfcc_features = mfcc(input_sample, samplerate=44100, nfft=1200, winlen=0.025, winstep=0.01, numcep=13)
    print("mfcc shape: ", mfcc_features.shape)

    for i in range(len(production_models)):
        
        log_prob = production_models[i][0][0].viterbi(mfcc_features)
        scores.append(log_prob)
        #print("log prob for {}: {}".format(str(production_models[i][1]), str(log_prob)))
    
    predicted = scores.index(max(scores))
        
    return predicted
