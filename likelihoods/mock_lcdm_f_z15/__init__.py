#!/usr/bin/python
import sys
import os
import numpy as np

require = [
	'f',
]

path_to_data = os.path.dirname(os.path.realpath(sys.argv[0])) + '/likelihoods/mock_f_z15'
x, y, erry = np.loadtxt(path_to_data+'/data.txt', comments='#', unpack=True)

def get_loglike(Engine_input, Engine):
	return -0.5*np.sum(((y-Engine.f(x))/erry)**2.)
