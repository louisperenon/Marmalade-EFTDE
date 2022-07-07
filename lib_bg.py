# Background class

class bg:

    def __init__(self, model):

        self.x0 = 0.1 # arbitrary
        self.pars = {} # arbitrary
        fcts_to_load = [
            'xtoz',
            'ztox',
            'H2H02',
            'HdH2_z',
            'HpH2_z',
            'dzdt_z',
            'dxdz_z',
            'bg_diff_f',
            'bg_diff_D'
        ]
        if model['theory'] == 'lcdm' : model['background'] = 'lcdm'
        for fct in fcts_to_load:
            exec('self.%s = self.%s_%s' % (fct, model['background'], fct))

    ################################################################################

    # LCDM

    #--> z(x)
    def lcdm_xtoz(self, x):
        return (self.x0*(1.-x)/(x*(1.-self.x0)))**(-1./3)-1. 

    #--> x(z)
    def lcdm_ztox(self, z):
        return self.x0/(self.x0+(1.-self.x0)*(1.+z)**-3)

    #-->(H^2/H^2(z=0))(z)
    def lcdm_H2H02(self, z):
        return self.x0*(1.+z)**3+1-self.x0

    #--> (dH/dt/H^2)(z)
    def lcdm_HdH2_z(self, z):
        return -1.5*self.x0/(self.x0+(1.-self.x0)*(1.+z)**-3) 

    #--> (dH/dz/H)(z)
    def lcdm_HpH2_z(self, z):
        return 1.5*self.x0*(1.+z)**2/(self.x0*(1.+z)**3+1-self.x0) 

    #--> (dz/dt/H)(z)
    def lcdm_dzdt_z(self, z):
        return -(1.+z)

    #--> (dx/dz)(z)
    def lcdm_dxdz_z(self, z):
        return -3*self.x0*(self.x0-1)*(1+z)**2/(self.x0*(z**3+3*z**2+3*z)+1)**2

    def lcdm_bg_diff_f(self, z, f):
        return f**2/(1+z)+(-1.5*(self.x0*(1.+z)**2)/(self.x0*(1.+z)**3+1-self.x0)+2./(1+z))*f-1.5*self.ztox(z)/(1+z)

    def lcdm_bg_diff_D(self, z, init):
        D0, Dp0 = init
        dzdt    = -(1+z)
        d2zdtdz = -1-1.5*self.x0/(self.x0+(1-self.x0)/(1+z)**3)
        A       = (d2zdtdz+2)/dzdt
        B       = -1.5*self.ztox(z)/dzdt**2
        return [Dp0, -A*Dp0-B*D0]

    ################################################################################

    # WCDM (copy-pasted from LCDM for now)

    #--> z(x)
    def wcdm_xtoz(self, x):
        return (self.x0*(1.-x)/(x*(1.-self.x0)))**(-1./3)-1. 

    #--> x(z)
    def wcdm_ztox(self, z):
        return self.x0/(self.x0+(1.-self.x0)*(1.+z)**-3)

    #-->(H^2/H^2(z=0))(z)
    def wcdm_H2H02(self, z):
        return self.x0*(1.+z)**3+1-self.x0

    #--> (dH/dt/H^2)(z)
    def wcdm_HdH2_z(self, z):
        return -1.5*self.x0/(self.x0+(1.-self.x0)*(1.+z)**-3) 

    #--> (dH/dz/H)(z)
    def wcdm_HpH2_z(self, z):
        return 1.5*self.x0*(1.+z)**2/(self.x0*(1.+z)**3+1-self.x0) 

    #--> (dz/dt/H)(z)
    def wcdm_dzdt_z(self, z):
        return -(1.+z)

    #--> (dx/dz)(z)
    def wcdm_dxdz_z(self, z):
        return -3*self.x0*(self.x0-1)*(1+z)**2/(self.x0*(z**3+3*z**2+3*z)+1)**2

    def wcdm_bg_diff_f(self, z, f):
        return f**2/(1+z)+(-1.5*(self.x0*(1.+z)**2)/(self.x0*(1.+z)**3+1-self.x0)+2./(1+z))*f-1.5*self.ztox(z)/(1+z)

    def wcdm_bg_diff_D(self, z, init):
        D0, Dp0 = init
        dzdt    = -(1+z)
        d2zdtdz = -1-1.5*self.x0/(self.x0+(1-self.x0)/(1+z)**3)
        A       = (d2zdtdz+2)/dzdt
        B       = -1.5*self.ztox(z)/dzdt**2
        return [Dp0, -A*Dp0-B*D0]

    ################################################################################
