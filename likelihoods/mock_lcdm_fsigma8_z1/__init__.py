import sys
import os
import numpy as np

require = [
	'fsig8',
]

path_to_data = os.path.dirname(os.path.realpath(sys.argv[0])) + '/likelihoods/mock_fsigma8_z1'
x, y, erry = np.loadtxt(path_to_data+'/data.txt', comments='#', unpack=True)

def get_loglike(Engine_input, Engine):
	return -0.5*np.sum(((y-Engine.fsigma8(x))/erry)**2.)