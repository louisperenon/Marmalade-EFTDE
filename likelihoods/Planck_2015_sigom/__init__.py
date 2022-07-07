import os
import sys
import numpy as np

require = [
    'sig80_bg',
]

x0_ref    = 0.315
sig80_ref = 0.829  
invcov    = np.array([[5645.19381733, -240.45760465],[ -240.45760465,  4922.26204073]]) 

def get_loglike(Engine_input, Engine): 

    vec = np.array([x0_ref,sig80_ref])  - np.array([Engine_input['x0'],Engine.sig80_bg]) 
    return -0.5 * np.dot(np.dot(vec, invcov), vec)