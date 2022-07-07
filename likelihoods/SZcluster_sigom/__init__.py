import os
import sys
import numpy as np

require = [
    'sig80_bg',
]

path_to_data = os.path.dirname(os.path.realpath(sys.argv[0])) + '/likelihoods/SZcluster_sigom'
data = np.loadtxt(path_to_data+'/mean_model_5.dat')
invcov = np.loadtxt(path_to_data+'/icov_model_5.dat')


def get_loglike(Engine_input, Engine): 

    ### Compute lnlike
    vec = data - np.array([Engine_input['x0'],Engine.sig80_bg]) 
    return -0.5 * np.dot(np.dot(vec, invcov), vec)