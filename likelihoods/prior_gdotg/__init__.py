import numpy as np

require = []

def get_loglike(Engine_input, Engine): 

    test = np.absolute(Engine.gdotg(Engine_input['z0']).min())

    return 0. if test <= 0.002 else -np.inf