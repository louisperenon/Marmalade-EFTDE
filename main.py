import os
import sys
import numpy as np
import time

import engine
import parser
import emcee




### Parse the input ini file
ini_fname = sys.argv[1]
base_ini = parser.parse_ini_file(ini_fname)


### Automatically add stuff to ini dictionnary and save it
ini = parser.autocomplete_ini(base_ini)
parser.copy_ini_file(ini_fname,ini)


### MCMC settings
model    = ini['model']
nsampler = ini['sampler']
steps    = ini['n_steps']
walkers  = ini['n_walkers']
addname  = ini['add_name']


### Import requested likelihoods (including priors-type likelihoods)
path_to_likes = os.path.dirname(os.path.realpath(sys.argv[0])) + '/likelihoods'
sys.path.insert(0, path_to_likes)
likes = []
require = []
for like_name in ini['likelihoods']:
    exec('import %s' % like_name)
    exec('likes.append(%s.get_loglike)' % like_name)
    ## Lists the requirements of the likelihood (bg, sig8, f...)
    exec('tmp_require = %s.require' % like_name)
    for r in tmp_require:
        if r not in require:
            require.append(r)


### Actual loglike function
def lnlike(p):

    lnp, lnls = 0., []
    bad_res = tuple([-np.inf] * (1 + 1 + len(likes) + 3))

    ### Test range priors
    for i, par in enumerate(ini['var_par']):
        # Uniform
        if not par[2] <= p[i] <= par[3]:
            return bad_res

    ### Create parameters dictionnary for EFT engine
    Engine_input = {}
    for par in ini['fix_par']:
        Engine_input[par[0]] = par[1]
    for i, par in enumerate(ini['var_par']):
        Engine_input[par[0]] = p[i]

    ### Initialize
    Engine = engine.EFT_engine(model, require, Engine_input)

    ### Compute the priors
    lnls = np.zeros(len(likes))
    for i, like in enumerate(likes):
        if 'prior' in ini['likelihoods'][i]:
            lnp = like(Engine_input, Engine)
            if not np.isfinite(lnp):
               return bad_res
            else:
                lnls[i] = lnp

    ###  Compute of EFT engine
    Engine.compute()

    ### Compute likelihoods
    for i, like in enumerate(likes):
        if not 'prior' in ini['likelihoods'][i]:
            lnls[i] = like(Engine_input, Engine)

    ### Compute derived parameters
    derivs = []
    if model['theory'] != 'lcdm':
        derivs.append(Engine.egc(0.) - 1.)
        derivs.append(Engine.ldp(0.) - 1.)
        derivs.append(Engine.gsp(0.) - 1.)

    ### Return lnlike + lnprior, lnprior, all partial lnlike, and derived params
    res = [lnls.sum() + lnp, lnp] +  list(lnls) + derivs
    return tuple(res)


### Set up walkers
n_dim     = len(ini['var_par'])
p0_start  = [par[1] for par in ini['var_par']]
std_start = [par[4] for par in ini['var_par']]

p_start = []
while len(p_start)<walkers:
    p_test = np.random.normal(p0_start, std_start, n_dim)
    if np.isfinite(lnlike(p_test)[0]):
        p_start.append(p_test)


### Prepare some inputs for the MCMC
blobs_dtype = [("log_prior", float)]
blobs_dtype += [("lnl_%s" % name, float) for name in ini['likelihoods']]
blobs_dtype += [("egc(z=0)-1", float)]
blobs_dtype += [("ldp(z=0)-1", float)]
blobs_dtype += [("gsp(z=0)-1", float)]
# names = '  '.join([par[1] for par in ini['var_par']])


### Do the MCMC (with MPI)
if (__name__ == '__main__') & (ini['parallel'] == 'MPI'):
    from schwimmbad import MPIPool
    with MPIPool() as pool:
        if not pool.is_master():
            pool.wait()
            sys.exit(0)

        if pool.is_master():
            print 'Starting MCMC :' + ini['output_fname']
            print ' '
        #     print p_start



        backend = emcee.backends.HDFBackend(ini['output_fname'] + '.h5')
        if nsampler == 'AI':
            sampler = emcee.EnsembleSampler(
                walkers,
                n_dim,
                lnlike,
                pool=pool,
                backend=backend,
                blobs_dtype=blobs_dtype,
            )

        time0 = time.time()
        sampler.run_mcmc(p_start, steps, thin_by=ini['thin_by'], progress=True)
        # sample = np.column_stack((-sampler.get_log_prob(flat=True),sampler.get_chain(flat=True)))
        # np.savetxt(ini['output_fname']+'_chain.txt', sample, fmt='%1.4e') #, fmt=run.fmt
        m_chain, s_chain = divmod((time.time()-time0), 60)
        h_chain, m_chain = divmod(m_chain, 60)
        print('   t_chain  = %d:%02d:%02d'% (h_chain, m_chain, s_chain))
        print ' '

elif ini['parallel'] == 'multi':
    from multiprocessing import Pool
    # with Pool() as pool:
    pool = Pool()
    backend = emcee.backends.HDFBackend(ini['output_fname'] + '.h5')
    if nsampler == 'AI':
        sampler = emcee.EnsembleSampler(
            walkers,
            n_dim,
            lnlike,
            pool=pool,
            backend=backend,
            blobs_dtype=blobs_dtype,
        )

        sampler.run_mcmc(p_start, steps, thin_by=ini['thin_by'], progress=True)

    # sample = np.column_stack((-sampler.get_log_prob(discard=int(0.3*steps),flat=True),sampler.get_chain(discard=int(0.3*steps),flat=True)))
    sample = np.column_stack((-sampler.get_log_prob(flat=True),sampler.get_chain(flat=True)))

    np.savetxt(ini['output_fname']+'_chain.txt', sample, fmt='%1.4e') #, fmt=run.fmt
    pool.close()

else :
    backend = emcee.backends.HDFBackend(ini['output_fname'] + '.h5')
    if nsampler == 'AI':
        sampler = emcee.EnsembleSampler(
            walkers,
            n_dim,
            lnlike,
            backend=backend,
            blobs_dtype=blobs_dtype,
        )
    # if nsampler == 'PT':
    #     sampler = PTSampler(
    #         ntemps=temps,
    #         nwalkers=walkers,
    #         dim=n_dim,
    #         logl=lnlike,
    #         logp=lnprior,
    #         loglargs=(model, data, comb, prior, likelihood),
    #         logpargs=(model, likelihood),
    #         threads=threads,
    #         pool=pool
    #     )

    sampler.run_mcmc(p_start, steps, thin_by=ini['thin_by'], progress=True)
