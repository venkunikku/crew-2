import numpy as np
import os

from hmm_models.model_utils import HMM_Model


def hmm_inference(production_models, input_sample): 

	scores = []

	mfcc_features = mfcc(input_sample, samplerate=self.sampling_freq, nfft=1200, winlen=0.025, winstep=0.01, numcep=13)

	for i in range(len(production_models)):

		log_prob = production_models[i][0][0].viterbi(input_sample)
		scores.append(log_prob)

	predicted = scores.index(max(scores))

	return predicted


    	









