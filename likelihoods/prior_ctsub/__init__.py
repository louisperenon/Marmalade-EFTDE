import numpy as np
from scipy.optimize import minimize

require = []

def get_loglike(Engine_input, Engine): 

    # Step 1
    test = Engine.ct2(Engine_input['zstab'])
    if test.max()>1.:
        return -np.inf

    # Step 2a
    tmp = Engine_input['zstab'][np.argsort(test)[:-3]]
    zmin = tmp.min()
    zmax = tmp.max()
    def to_min_test(z):
        if z<zmin or z>zmax:
            return np.inf
        else:
            return -Engine.ct2(z)
    test_mini = minimize(
        to_min_test,
        0.5*(zmin+zmax),
        method='Nelder-Mead',
    )
    if (-test_mini['fun'])>1.:
        return -np.inf

    return 0.
