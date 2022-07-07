import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate   import solve_ivp
from lib_obs import obs

class EFT_engine(obs): 

    ###################################################################################

    ### Initialisation phase : done before the chain begins
    def __init__(self, model, require, pars):

        obs.__init__(self, model)
        self.require = require
        self.pars    = pars
        self.x0      = pars['x0']

        if model['theory'] == 'lcdm':
            # from lib_bg import bg
            # self.diff_f = bg(model).lcdm_bg_diff_f
            # self.diff_D = bg(model).lcdm_bg_diff_D
            self.diff_f = self.lcdm_bg_diff_f
            self.diff_D = self.lcdm_bg_diff_D

    ###################################################################################

    ### Cosmo phase : done at each chain step
    def compute(self):

        zvec = np.append(
            np.linspace(
                self.pars['zini'], 
                self.pars['zmid'],
                (self.pars['zini']-self.pars['zmid']+self.pars['dz1'])/self.pars['dz1']
            ),
            np.linspace(
                self.pars['zmid']-self.pars['dz2'],
                self.pars['z0'],
                (self.pars['zmid']-self.pars['z0'])/self.pars['dz2']
            )
        )

        # >> f(z) in EFT
        if ('f' in self.require) | ('fsig8' in self.require):
            sol = solve_ivp(
                self.diff_f,
                [self.pars['zini'], self.pars['z0']],
                [1.],
                t_eval = zvec,
                method = self.pars['method']
            )
            f_zvec = sol.y[0, :]
            self.f = interp1d(zvec, f_zvec)

        # >> sigma_8(z) in EFT
        if ('sig8' in self.require) | ('fsig8' in self.require) | ('sig80_bg' in self.require):
            sol = solve_ivp(
                self.diff_D,
                [self.pars['zini'], self.pars['z0']],
                [self.pars['D0'], self.pars['Dp0']],
                t_eval = zvec,
                method = self.pars['method']
            )
            sig8_zvec = sol.y[0, :] / sol.y[0, -1] * self.pars['sig80']
            self.sigma8 = interp1d(zvec, sig8_zvec)

        # >> sigma_8(z=0) in BG, starting with same sigma8 as EFT in the past 
        if 'sig80_bg' in self.require:
            sol = solve_ivp(
                self.bg_diff_D,
                [self.pars['zini'], self.pars['z0']],
                [self.pars['D0'], self.pars['Dp0']],
                t_eval = zvec,
                method = self.pars['method']
            )
            # sig8_bg_zvec = sol.y[0, :] / sol.y[0, 0] * sig8_zvec[0]
            self.sig80_bg = sol.y[0, -1] / sol.y[0, 0] * sig8_zvec[0]

        # >> f*sigma_8(z) in EFT
        if 'fsig8' in self.require:
            self.fsigma8 = interp1d(zvec, f_zvec * sig8_zvec)
