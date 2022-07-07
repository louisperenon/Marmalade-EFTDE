import sys
import os
import numpy as np

require = [
    'sig80_bg',
]

x0_ref    = 0.315
sig80_ref = 0.829  
invcov = np.array([[100991.19714823,-4301.73031119],[-4301.73031119,88058.11673729]])

def get_loglike(Engine_input, Engine): 

    vec = np.array([x0_ref,sig80_ref])  - np.array([Engine_input['x0'],Engine.sig80_bg]) 
    return -0.5 * np.dot(np.dot(vec, invcov), vec)