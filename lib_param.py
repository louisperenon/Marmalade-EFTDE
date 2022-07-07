import numpy as np
from lib_bg import bg

# Parametrisation class

class param(bg):

    def __init__(self, model):

        bg.__init__(self, model)
        fcts_to_load = [
            'cpg',
            'cpgp',
            'intcpg'
        ]
        if 'basis' in model.keys(): 
            for fct in fcts_to_load:
                exec('self.%s = self.%s_%s' % (fct, model['parametrisation'], fct))

    ################################################################################

    # DE0

    def de0_cpg(self, z, n):
        return (1. - self.ztox(z)) / (1. - self.x0) * self.pars['eft_%s_1' % n]

    def de0_cpgp(self, z, n):
        return -self.dxdz_z(z) * self.pars['eft_%s_1' % n] / (1. - self.x0)

    def de0_intcpg(self, z, n):
        return np.exp(
            self.pars['eft_%s_1' % n] * np.log(self.ztox(z) / self.x0)
            / ((1. - self.x0) * -3.)
        )

    ################################################################################

    # DE1

    def de1_cpg(self, z, n):
        x = self.ztox(z)
        return (1. - x)/(1. - self.x0) * (
            self.pars['eft_%s_1' % n] + self.pars['eft_%s_2' % n] * (x - self.x0)
        )

    def de1_cpgp(self, z, n):
        x = self.ztox(z)
        return self.dxdz_z(z) / (1.-self.x0) * (
            (1 - x) * self.pars['eft_%s_2' % n] - self.pars['eft_%s_1' % n]
            - self.pars['eft_%s_2' % n] * (x - self.x0)
        )

    def de1_intcpg(self, z, n):
        x  = self.ztox(z) 
        return np.exp(
            1. / ((1. - self.x0) * -3.) *
            (
                self.pars['eft_%s_2' % n] * (x - self.x0) + (self.pars['eft_%s_1' % n]
                -self.pars['eft_%s_2' % n] * self.x0) * (np.log(x / self.x0))
            )
        )

    ################################################################################

    # SCALINGZ

    def scalingz_cpg(self, z, n):
        return self.pars['eft_%s_1' % n] / (1 + z)**self.pars['eft_%s_2' % n]

    def scalingz_cpgp(self, z, n)   : 
        return -self.pars['eft_%s_1' % n] * (
            self.pars['eft_%s_2' % n] / (1+z)**(self.pars['eft_%s_2' % n]+1)
        )

    def scalingz_intcpg(self, z, n) : 
        return np.exp(
            self.pars['eft_%s_1' % n] / self.pars['eft_%s_2' % n] * 
            ((1 + z)**-self.pars['eft_%s_2' % n] - 1)
        )

    ################################################################################
