import os
import sys
import numpy as np

require = [
    'sig8',
    'sig80_bg',
]

path_to_data = os.path.dirname(os.path.realpath(sys.argv[0])) + '/likelihoods/SZcluster_freeSL_fixedPlanck'
data = np.loadtxt(path_to_data+'/mean_model_1.dat')
invcov = np.loadtxt(path_to_data+'/icov_model_1.dat')

n_clus   = 8
dz_integ = 0.01
n_integ  = np.round(((data[2:, 2] - data[2:, 1])) / dz_integ).astype('int') + 1

def get_loglike(Engine_input, Engine): 

    ### Create theory vector
    theo = np.zeros(data.shape[0])
    # Omega_m
    theo[0] = Engine_input['x0']
    # sigma8 in LCDM
    theo[1] = Engine.sig80_bg
    # sigma8 in each z bin
    for i in range(n_clus):
        z_tmp = np.linspace(data[i+2, 1], data[i+2, 2], n_integ[i])
        sig8_tmp = Engine.sigma8(z_tmp)
        theo[i+2] = np.trapz(sig8_tmp, z_tmp) / (data[i+2, 2] - data[i+2, 1])

    ### Compute lnlike
    vec = data[:, 0] - theo
    return -0.5 * np.dot(np.dot(vec, invcov), vec)
