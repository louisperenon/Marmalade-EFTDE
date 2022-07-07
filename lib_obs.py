from lib_basis import basis

# observable class

class obs(basis):

    def __init__(self, model):

        basis.__init__(self, model)

    ################################################################################

    # EFT misc functions

    def egc(self, z):
        return self.egc_sc(z) * (1. + self.egc_ff(z))

    def gsp_ff(self, z):
        return self.gsp(z) / self.gsp_sc(z) - 1

    def ldp_sc(self, z):
        return 0.5 * self.egc_sc(z) * (1. + self.gsp_sc(z))

    def ldp_ff(self, z):
        return self.ldp(z) / self.ldp_sc(z) - 1

    def ldp(self, z):
        return 0.5 * self.egc(z) * (1. + self.gsp(z))

    ################################################################################

    # EFT tests functions

    def cs2(self, z):
        return self.gradient(z) / self.ghost(z)

    def ct2(self, z):
        return self.ct2(z)

    def gdotg(self, z):
        return self.gdotg(z)

    def addE(self, z):
        return False

    ################################################################################

    # EFT growth functions

    def diff_f(self, z, f):
        return f**2./(1+z)+(2./(1+z)-self.HpH2_z(z))*f-1.5*self.ztox(z)*self.egc(z)/(1+z)

    def diff_D(self, z, init):
        D0, Dp0 = init
        return [
            Dp0,
            (1. / (1 + z) - self.HpH2_z(z)) * Dp0 + 1.5 * self.ztox(z) * self.egc(z) / (1+z)**2 * D0
        ]
