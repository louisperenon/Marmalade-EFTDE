import sys
import os
import numpy as np

require = [
	'fsig8',
]

path_to_data = os.path.dirname(os.path.realpath(sys.argv[0])) + '/likelihoods/RSD_SDSS_IV'
x, y, erry = np.loadtxt(path_to_data+'/data.txt', comments='#', unpack=True)
invcov     = np.linalg.inv(np.loadtxt(path_to_data+'/cov_mat.txt', comments='#', unpack=True))

def get_loglike(Engine_input, Engine): 
    vec_dat = y-Engine.fsigma8(x)
    return -0.5*np.dot(np.dot(vec_dat,invcov),vec_dat)



