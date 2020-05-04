import numpy as np

import pomegranate
from hmmlearn import hmm

### Define a class to train the HMM ###

# Parameters of `hmm.GaussianHMM()`:
# `n_components`: number of states of HMM
# `covariance_type`: type of covariance matrix for each state. 
# Each state is a random vector. 
# This parameter is a string defining the type of covariance matrix of this vector. Defaults to `"diagonal"`


class HMM_Model(object):
    
    def __init__(self, num_components=12, 
                 num_iter=100,
                use_pomegranate=True,
                distribution=pomegranate.distributions.NormalDistribution,
                gpu=False):
        
        self.n_components = num_components
        self.n_iter = num_iter
        self.use_pomegranate = use_pomegranate
        self.distribution = distribution
        
        # define the covariance type and the type of HMM:
        self.cov_type = 'diag'
        self.model_name = 'GaussianHMM'
        
        # initialize the variable in which we will store the models for each word:
        self.models = []
        
        # define the model using the specified parameters:
        if not self.use_pomegranate:

            self.model = hmm.GaussianHMM(n_components=self.n_components,
                                     covariance_type=self.cov_type,
                                     n_iter=self.n_iter, verbose=True)
        
        # we anble pomegranate's gpu utility if gpu is set to true 
        self.gpu = gpu
        if self.gpu==True:
            
            pomegranate.utils.enable_gpu()
            print("pomegranate_gpu is enabled: ", pomegranate.utils.is_gpu_enabled())
            
        else:
            
            pomegranate.utils.disable_gpu()
            print("pomegranate_gpu is enabled: ", pomegranate.utils.is_gpu_enabled())
            

    def train(self, training_data, multidimensional_input, n_threads, batches_per_epoch, lr_decay):
        
        """
        Defines a method to train the model
        'training_data' is a 2D numpy array where each row has the 
        length of number of mfcc coefficients
        """
        # for default case using pomegranate package        
        if self.use_pomegranate:
            
            # training on multidimensional input (i.e. n_samples x n_windows x n_cepstral_coefs)
            if multidimensional_input:
                
                print("training on multidimensional input using pomegranate, {} states, {} iterations, sample shape {}, and {} threads".format(self.n_components,self.n_iter,training_data.shape, n_threads))
                self.model = pomegranate.HiddenMarkovModel.from_samples(self.distribution, 
                                                                    self.n_components,
                                                                    training_data, 
                                                                    max_iterations=self.n_iter,
                                                                    stop_threshold = 1e-3,
                                                                    algorithm="baum-welch",
                                                                    batches_per_epoch=batches_per_epoch,
                                                                    lr_decay=lr_decay,
                                                                    n_jobs=n_threads, 
                                                                    verbose=True)
            
            # training on unidimensional input (i.e. one cepstral grid per track)
            else:
                
                print("training on unidimensional input using pomegranate, {} states, {} iterations, sample shape {}, and {} threads".format(self.n_components,self.n_iter,training_data.shape, n_threads))
                self.model = pomegranate.HiddenMarkovModel.from_samples(self.distribution, 
                                                                    self.n_components,
                                                                    training_data, 
                                                                    max_iterations=self.n_iter, 
                                                                    stop_threshold = 1e-3,    
                                                                    algorithm="baum-welch",
                                                                    batches_per_epoch=batches_per_epoch,
                                                                    lr_decay=lr_decay,
                                                                    n_jobs=n_threads, 
                                                                    verbose=True)
                
                
            self.models.append(self.model)
        
        # for alternative case using hmmlearn
        else:
            
            print("training on unidimensional input using pomegranate, {} states, {} iterations, and sample shape {}".format(self.n_components,self.n_iter,training_data.shape))
            np.seterr(all='ignore')
            cur_model = self.model.fit(training_data)
            self.models.append(cur_model)

    
    def compute_score(self, input_data):
        
        """
        Define a method to compute log likelihood score for input features
        Returns: Log likelihood of sample input_data
        """
        if 'use_pomegranate' in self.__dict__.keys():
            
            print("scoring input of shape ", input_data.shape, "pomegranate")

            return self.model.log_probability(input_data)
            
        else:
            
            print("scoring input of shape ", input_data.shape, " hmmlearn")
            
            return self.model.score(input_data)

    def viterbi(self, input_data):

        """
        Returns log probability of most likely state sequence per viterbi algorith
        """
        
        if 'use_pomegranate' in self.__dict__.keys():

            print("using pomegranate")

            return self.model.viterbi(input_data)

        else:

            print("using hmm_learn")

            return self.model.decode(input_data, algorithm='viterbi')











