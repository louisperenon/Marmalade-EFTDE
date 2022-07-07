import numpy as np
from lib_param import param

# Basis class

class basis(param):

    def __init__(self, model):

        param.__init__(self, model)
        if model['theory'] == 'lcdm':
            fcts_to_load = []
        else:
            fcts_to_load = [
                'M2',
                'egc_sc',
                'egc_ff',
                'gsp_sc',
                'gsp',
                'gradient',
                'ghost',
                'ct2',
                'gdotg',
            ]
        if 'basis' in model.keys(): 
            if model['basis'] == 'psm':
                fcts_to_load += ['calC']
            for fct in fcts_to_load:
                exec('self.%s = self.%s_%s_%s' % (fct, model['basis'], model['theory'], fct))

    ################################################################################
    ################################################################################
    ################################################################################

    # PSM couplings

    def mu1(self, z):
        return self.cpg(z, 1)

    def mu22(self, z):
        return self.cpg(z, 2)    

    def mu3(self, z):
        return self.cpg(z, 3)

    def eps4(self, z):
        return self.cpg(z, 4)

    def mu1dot(self, z):
        return (self.HdH2_z(z) * self.cpg(z, 1) + self.dzdt_z(z) * self.cpgp(z, 1))

    def mu3dot(self, z):
        return (self.HdH2_z(z) * self.cpg(z, 3) + self.dzdt_z(z) * self.cpgp(z, 3))

    def eps4dot(self, z):
        return self.dzdt_z(z) * self.cpgp(z, 4)

    def mu3circ(self, z):
        return self.mu3(z) * (1 + self.mu1(z)) + self.mu3dot(z)

    def eps4circ(self, z):
        return self.eps4(z) * (1 + self.mu1(z)) + self.eps4dot(z)

    ################################################################################

    # BD

    def psm_bd_M2(self, z):
        return self.intcpg(z, 1)

    def psm_bd_calC(self, z):
        vmu1 = self.cpg(z, 1)  
        return 0.5 * (vmu1 - self.mu1dot(z) - vmu1**2.) - self.HdH2_z(z) - 1.5 * self.ztox(z) / self.psm_bd_M2(z)

    def psm_bd_egc_sc(self, z):
        return 1. / self.psm_bd_M2(z)

    def psm_bd_egc_ff(self, z):
        return self.mu1(z)**2 / self.psm_bd_gradient(z) / 4.

    def psm_bd_gsp_sc(self, z):
        return np.ones(np.size(z))

    def psm_bd_gsp(self, z):
        x1 = self.mu1(z) / self.psm_bd_calC(z)
        return (1 + 0.5 * x1) / (1 + x1)

    def psm_bd_gradient(self, z):
        return self.psm_bd_calC(z) + 0.75 * self.mu1(z)**2

    def psm_bd_ghost(self, z):
        return self.psm_bd_gradient(z)

    def psm_bd_ct2(self, z):
        return np.ones(np.size(z))

    def psm_bd_gdotg(self, z):
        return -self.mu1(z)


    ################################################################################

    # H3

    def psm_h3_M2(self, z):
        return self.intcpg(z, 1)

    def psm_h3_calC(self, z):
        vmu1 = self.cpg(z, 1)  
        return 0.5*(vmu1 - self.mu1dot(z) - vmu1**2.) - self.HdH2_z(z) - 1.5 * self.ztox(z) / self.psm_h3_M2(z)

    def psm_h3_egc_sc(self, z):
        return 1. / self.psm_h3_M2(z)

    def psm_h3_egc_ff(self, z):
        return (self.mu1(z) + self.mu3(z))**2 / self.psm_h3_gradient(z) / 4.

    def psm_h3_gsp_sc(self, z):
        return np.ones(np.size(z))

    def psm_h3_gsp(self, z):
        vmu1 = self.mu1(z)
        x2 = 2 * self.psm_h3_calC(z) + self.mu3circ(z)
        return ((vmu1 - self.mu3(z)) * vmu1 + x2) / (2 * vmu1**2 + x2)

    def psm_h3_gradient(self, z):
        vmu1 = self.mu1(z)
        vmu3 = self.mu3(z)
        return self.psm_h3_calC(z) + 0.5 * self.mu3circ(z) + 0.25 * (vmu1 - vmu3) * (3 * vmu1 + vmu3)

    def psm_h3_ghost(self, z):
        return (self.psm_h3_calC(z) + 2. * self.mu22(z)) + 0.75 * (self.mu1(z) - self.mu3(z))**2.

    def psm_h3_ct2(self, z):
        return np.ones(np.size(z))

    def psm_h3_gdotg(self, z):
        return -self.mu1(z)

    ################################################################################

    # H45

    def psm_h45_M2(self, z):
        return self.intcpg(z, 1) / (1 + self.eps4(0.))**2

    def psm_h45_calC(self, z):
        vmu1 = self.cpg(z, 1)  
        return 0.5 * (vmu1 - self.mu1dot(z) - vmu1**2.) - self.HdH2_z(z) - 1.5 * self.ztox(z) / self.psm_h45_M2(z)

    def psm_h45_egc_sc(self, z):
        return 1. / self.psm_h45_M2(z) / (1 + self.eps4(z))**2

    def psm_h45_egc_ff(self, z):
        vmu1   = self.mu1(z)
        veps4  = self.eps4(z)
        veps4c = self.eps4circ(z)
        return (1. + veps4) / self.psm_h45_gradient(z) * (
            (vmu1 - self.mu3(z)) / (2. * (1. + veps4)) - vmu1 - veps4c
        )**2

    def psm_h45_gsp_sc(self, z):
        return 1 + self.eps4(z)

    def psm_h45_gsp(self, z):
        vmu1   = self.mu1(z)
        veps4  = self.eps4(z)
        veps4c = self.eps4circ(z)
        x1     = vmu1 + veps4c
        x2     = 2 * self.psm_h45_calC(z) + self.mu3circ(z) - 2 * self.HdH2_z(z) * veps4 + 2 * veps4c
        return ((vmu1 - self.mu3(z)) * x1 + (1 + veps4) * x2) / (2 * x1**2 + x2)

    def psm_h45_gradient(self, z):
        vmu1   = self.mu1(z)
        vmu3   = self.mu3(z)
        veps4  = self.eps4(z)
        veps4c = self.eps4circ(z)
        return (
            (self.psm_h45_calC(z) + 0.5 * self.mu3circ(z) - self.HdH2_z(z) * veps4 + veps4c) 
            * (vmu1 - vmu3) * ((vmu1 - vmu3) / (4 * (1 + veps4)) - vmu1 - veps4c)
        )

    def psm_h45_ghost(self, z):
        return (
            (self.psm_h45_calC(z) + 2. * self.mu22(z))
            * (1. + self.eps4(z)) + 0.75 * (self.mu1(z) - self.mu3(z))**2.
        )

    def psm_h45_ct2(self, z):
        return 1. / (1. + self.eps4(z))

    def psm_h45_gdotg(self, z):
        return -self.mu1(z) - 2 * self.eps4dot(z)

    ################################################################################
    ################################################################################
    ################################################################################

    # ALPHA couplings

    def alpha_m(self, z):
        return self.cpg(z, 1)

    def alpha_k(self, z):
        return self.cpg(z, 2)

    def alpha_b(self, z):
        return self.cpg(z, 3)

    def alpha_t(self, z):
        return self.cpg(z, 4)

    def alpha_mdot(self, z):
        return self.dzdt_z(z) * self.cpgp(z, 1)

    def alpha_bdot(self, z):
        return self.dzdt_z(z) * self.cpgp(z, 3)

    def alpha_tdot(self, z):
        return self.dzdt_z(z) * self.cpgp(z, 4)

    ################################################################################

    # H3

    def alpha_h3_M2(self, z):
        return self.intcpg(z, 1)

    def alpha_h3_egc_sc(self, z):
        return 1. / self.alpha_h3_M2(z)

    def alpha_h3_egc_ff(self, z):
        return 2. / self.alpha_h3_gradient(z) * (0.5 * self.alpha_b(z) + self.alpha_m(z))**2

    def alpha_h3_gsp_sc(self, z):
        return np.ones(np.size(z))

    def alpha_h3_gsp(self, z):
        ab = self.alpha_b(z)
        xi = 0.5 * ab + self.alpha_m(z)
        B = self.alpha_h3_gradient(z)
        return (1 + ab * xi / B) / (1 + 2 * xi**2 / B)

    def alpha_h3_gradient(self, z):
        ab = self.alpha_b(z)
        return 2. * (
            (1 - 0.5 * ab) * (self.alpha_m(z) + 0.5 * ab - self.HdH2_z(z))
            + 0.5 * self.alpha_bdot(z) - 1.5 * self.ztox(z) / self.alpha_h3_M2(z)
        )

    def alpha_h3_ghost(self, z):
        return self.alpha_k(z) + 1.5 * self.alpha_b(z)**2

    def alpha_h3_ct2(self, z):
        return np.ones(np.size(z))

    def alpha_h3_gdotg(self, z): 
        return -self.alpha_m(z)

    ################################################################################

    # H45

    def alpha_h45_M2(self, z):
        return self.intcpg(z, 1) * (1 + self.alpha_t(0.))

    def alpha_h45_egc_sc(self, z):
        return (1 + self.alpha_t(z)) / self.alpha_h45_M2(z)

    def alpha_h45_egc_ff(self, z):
        at = self.alpha_t(z)
        return (
            2. / (self.alpha_h45_gradient(z) * (1 + at))
            * (0.5 * self.alpha_b(z) * (1. + at) + self.alpha_m(z) - at)**2.
        )

    def alpha_h45_gsp_sc(self, z):
        return 1. / (1 + self.alpha_t(z))

    def alpha_h45_gsp(self, z):
        ab = self.alpha_b(z)
        at = self.alpha_t(z)
        xi = 0.5 * ab * (1. + at) + self.alpha_m(z) - at
        B  = self.alpha_h45_gradient(z)
        return (1 + ab * xi / B) / (1 + at + 2 * xi**2 / B)

    def alpha_h45_gradient(self, z):
        ab = self.alpha_b(z)
        at = self.alpha_t(z)
        return 2. * (
            (1 - 0.5 * ab) * (self.alpha_m(z) - at + 0.5 * ab * (1 + at) - self.HdH2_z(z))
            + 0.5 * self.alpha_bdot(z) - 1.5 * self.ztox(z) / self.alpha_h45_M2(z)
        )

    def alpha_h45_ghost(self, z):
        return self.alpha_k(z) + 1.5 * self.alpha_b(z)**2

    def alpha_h45_ct2(self, z):
        return 1 + self.alpha_t(z)

    def alpha_h45_gdotg(self, z): 
        return self.alpha_tdot(z)/(1.+self.alpha_t(z))-self.alpha_m(z)

    ################################################################################

