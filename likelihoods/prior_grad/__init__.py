import numpy as np
from scipy.optimize import minimize

require = []

def get_loglike(Engine_input, Engine): 

    # Step 1
    scalar = Engine.gradient(Engine_input['zstab'])
    tensor = Engine.ct2(Engine_input['zstab'])
    if scalar.min()<=0. or tensor.min()<=0.:
        return -np.inf

    # Step 2a
    tmp = Engine_input['zstab'][np.argsort(scalar)[:3]]
    szmin = tmp.min()
    szmax = tmp.max()
    def to_min_scal(z):
        if z<szmin or z>szmax:
            return np.inf
        else:
            return Engine.gradient(z)
    scalar_mini = minimize(
        to_min_scal,
        0.5*(szmin+szmax),
        method='Nelder-Mead',
    )
    if scalar_mini['fun']<0:
        return -np.inf

    # Step 2b
    tmp = Engine_input['zstab'][np.argsort(tensor)[:3]]
    tzmin = tmp.min()
    tzmax = tmp.max()
    def to_min_tens(z):
        if z<tzmin or z>tzmax:
            return np.inf
        else:
            return Engine.ct2(z)
    tensor_mini = minimize(
        to_min_tens,
        0.5*(tzmin+tzmax),
        method='Nelder-Mead',
    )
    if tensor_mini['fun']<0:
        return -np.inf

    return 0.