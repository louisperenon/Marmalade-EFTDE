import numpy as np

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def parse_ini_file(fname, ignore_errors=False):
    
    ############################
    ### Open the .ini file ###
    ############################
    with open(fname) as f:
        lines = f.readlines()
    out =  {}
    error_ct = 0


    #######################################################
    ### Read all lines and options (==1st word on line) ###
    #######################################################
    slines = []
    options = []
    for line in lines:
        empty_line = line.split() == []
        comment = line[0] == '#'
        if not empty_line and not comment:
            sline = line.split()
            slines.append(sline)
            options.append(sline[0])


    ##############################
    ### Deal with output_fname ###
    ##############################
    ct = options.count('output_fname')
    if ct == 0:
        print('"output_fname" not found.')
        out['output_fname'] = None
        error_ct += 1
    elif ct > 1:
        print('%s instances of "output_fname" found.' % ct)
        out['output_fname'] = None
        error_ct += 1
    else:
        ix = options.index('output_fname')
        if len(slines[ix]) != 2:
            print('Wrong number of arguments for "output_fname".')
            out['output_fname'] = None
            error_ct += 1
        elif is_number(slines[ix][1]):
            print('Wrong argument type for "output_fname".')
            out['output_fname'] = None
            error_ct += 1
        else:
            out['output_fname'] = slines[ix][1]


    #################################
    ### Deal with additional name ###
    #################################

    ct = options.count('add_name')
    if ct == 0:
        print('"add_name" not found.')
        out['add_name'] = None
        error_ct += 1
    elif ct > 1:
        print('%s instances of "add_name" found.' % ct)
        out['add_name'] = None
        error_ct += 1
    else:
        ix = options.index('add_name')
        if len(slines[ix]) != 2:
            print('Wrong number of arguments for "add_name".')
            out['add_name'] = None
            error_ct += 1
        elif is_number(slines[ix][1]):
            print('Wrong argument type for "add_name".')
            out['add_name'] = None
            error_ct += 1
        else:
            out['add_name'] = slines[ix][1]


    #################################
    ### Deal with temps ###
    #################################

    ct = options.count('temps')
    if ct == 0:
        # print('"temps" not found.')
        out['temps'] = None
        # error_ct += 1
    elif ct > 1:
        print('%s instances of "temps" found.' % ct)
        out['temps'] = None
        error_ct += 1
    else:
        ix = options.index('temps')
        if len(slines[ix]) != 2:
            print('Wrong number of arguments for "temps".')
            out['temps'] = None
            error_ct += 1
        elif is_number(slines[ix][1]):
            print('Wrong argument type for "temps".')
            out['temps'] = None
            error_ct += 1
        else:
            out['temps'] = slines[ix][1]


    #########################
    ### Deal with sampler ###
    #########################
    ct = options.count('sampler')
    if ct == 0:
        print('"sampler" not found.')
        out['sampler'] = None
        error_ct += 1
    elif ct > 1:
        print('%s instances of "sampler" found.' % ct)
        out['sampler'] = None
        error_ct += 1
    else:
        ix = options.index('sampler')
        if len(slines[ix]) != 2:
            print('Wrong number of arguments for "sampler".')
            out['sampler'] = None
            error_ct += 1
        elif is_number(slines[ix][1]):
            print('Wrong argument type for "sampler".')
            out['sampler'] = None
            error_ct += 1
        else:
            out['sampler'] = slines[ix][1]


    ###########################
    ### Deal with n_walkers ###
    ###########################
    ct = options.count('n_walkers')
    if ct == 0:
        print('"n_walkers" not found, assuming 2 times the number of parameters.')
        out['n_walkers_type'] = 'prop_to'
        out['n_walkers'] = 2
    elif ct > 1:
        print('%s instances of "n_walkers" found.' % ct)
        error_ct += 1
    else:
        ix = options.index('n_walkers')
        if len(slines[ix]) != 3:
            print('Wrong number of arguments for "n_walkers".')
            error_ct += 1
        elif slines[ix][1] not in ['custom', 'prop_to']:
            print('Unrecognizd argument for "n_walkers" : %s.' % slines[ix][1])
            error_ct += 1
        elif not is_number(slines[ix][2]):
            print('Wrong argument type for "n_walkers".')
            error_ct += 1
        else:
            out['n_walkers_type'] = slines[ix][1]
            out['n_walkers'] = int(slines[ix][2])


    #########################
    ### Deal with n_steps ###
    #########################
    ct = options.count('n_steps')
    if ct == 0:
        print('"n_steps" not found, assuming 10000 steps.')
        out['n_steps'] = 10000
    elif ct > 2:
        print('%s instances of "n_steps" found.' % ct)
        error_ct += 1
    else:
        ix = options.index('n_steps')
        if len(slines[ix]) != 2:
            print('Wrong number of arguments for "n_steps".')
            error_ct += 1
        elif not is_number(slines[ix][1]):
            print('Wrong argument type for "n_steps".')
            error_ct += 1
        else:
            out['n_steps'] = int(slines[ix][1])


    #########################
    ### Deal with thin_by ###
    #########################
    ct = options.count('thin_by')
    if ct == 0:
        print('"thin_by" not found, assuming no thinning.')
        out['thin_by'] = 1
    elif ct > 2:
        print('%s instances of "thin_by" found.' % ct)
        error_ct += 1
    else:
        ix = options.index('thin_by')
        if len(slines[ix]) != 2:
            print('Wrong number of arguments for "thin_by".')
            error_ct += 1
        elif not is_number(slines[ix][1]):
            print('Wrong argument type for "thin_by".')
            error_ct += 1
        else:
            out['thin_by'] = int(slines[ix][1])
            
    ##########################
    ### Deal with parallel ###
    ##########################prior_ctsub
    if 'parallel' not in options:
        print('"parallel" not found, assuming "none".')
        out['parallel'] = 'none'
    else:
        ct = options.count('parallel')
        if ct > 1:
            print('%s instances of "parallel" found.' % ct)
            error_ct += 1
        else:
            ix = options.index('parallel')
            if len(slines[ix]) != 2:
                print('Wrong number of arguments for "parallel".')
                error_ct += 1
            elif slines[ix][1] not in ['none', 'multi', 'MPI']:
                print('Unrecognizd argument for "parallel" : %s.' % slines[ix][1])
                error_ct += 1
            else:
                out['parallel'] = slines[ix][1]


    #######################
    ### Deal with model ###
    #######################
    test_if_basis = options.count('basis')                         #!!!!!!!!!!!!!#
    out['model']= {}
    #------------------#
    # Deal with theory #
    #------------------#
    ct = options.count('theory')
    if ct == 0:
        print('"theory" not found, assuming lcdm.')
        out['model']['theory'] = 'lcdm'
    elif ct > 1:
        print('%s instances of "theory" found.' % ct)
        error_ct += 1
    else:
        ix = options.index('theory')       
        if len(slines[ix]) != 2:
            print('Wrong number of arguments for "theory".')
            error_ct += 1
        elif is_number(slines[ix][1]):
            print('Wrong argument type for "theory".')
            error_ct += 1
        else:
            out['model']['theory'] = slines[ix][1]
    #----------------------#
    # Deal with background #
    #----------------------#
    if test_if_basis != 0:                                         #!!!!!!!!!!!!!#
        ct = options.count('background')
        if ct == 0:
            print('"background" not found, assuming lcdm.')
            out['model']['background'] = 'lcdm'
        elif ct > 1:
            print('%s instances of "background" found.' % ct)
            error_ct += 1
        else:
            ix = options.index('background')
            if len(slines[ix]) != 2:
                print('Wrong number of arguments for "background".')
                error_ct += 1
            elif is_number(slines[ix][1]):
                print('Wrong argument type for "background".')
                error_ct += 1
            else:
                out['model']['background'] = slines[ix][1]
    #-----------------#
    # Deal with basis #
    #-----------------#
    if test_if_basis != 0:                                         #!!!!!!!!!!!!!#
        ct = options.count('basis')
        if ct == 0:
            print('"basis" not found, assuming psm.')
            out['model']['basis'] = 'psm'
        elif ct > 1:
            print('%s instances of "basis" found.' % ct)
            error_ct += 1
        else:
            ix = options.index('basis')
            if len(slines[ix]) != 2:
                print('Wrong number of arguments for "basis".')
                error_ct += 1
            elif is_number(slines[ix][1]):
                print('Wrong argument type for "basis".')
                error_ct += 1
            else:
                out['model']['basis'] = slines[ix][1]
    #---------------------------#
    # Deal with parametrisation #
    #---------------------------#
    if test_if_basis != 0:                                         #!!!!!!!!!!!!!#
        ct = options.count('parametrisation')
        if ct == 0:
            print('"parametrisation" not found, assuming de0.')
            out['model']['parametrisation'] = 'de0'
        elif ct > 1:
            print('%s instances of "parametrisation" found.' % ct)
            error_ct += 1
        else:
            ix = options.index('parametrisation')
            if len(slines[ix]) != 2:
                print('Wrong number of arguments for "parametrisation".')
                error_ct += 1
            elif is_number(slines[ix][1]):
                print('Wrong argument type for "parametrisation".')
                error_ct += 1
            else:
                out['model']['parametrisation'] = slines[ix][1]


    ###############################
    ### Check if any likelihood ###
    ###############################
    ct = options.count('likelihood')
    if ct == 0:
        print('No likelihood specified.')
        error_ct += 1


    ############################
    ### Deal with likelihood ###
    ############################
    out['likelihoods'] = []
    allowed_likelihoods = [
        'Planck_2015_sigom',

        'RSD_2dFGRS',
        'RSD_2MASS',
        'RSD_2MTF',
        'RSD_6dFGS_SNIa',
        'RSD_BOSS_DR12',
        'RSD_FastSound',
        'RSD_GAMA',
        'RSD_IRAS_SNIa',
        'RSD_SDSS',
        'RSD_SDSS_IV',
        'RSD_SDSS_LRG_200',
        'RSD_SDSS_MGS',
        'RSD_Vipers_PDR2',
        'RSD_WiggleZ',

        'RSD_Vipers_PDR2_f',
        'RSD_SDSS_f',
        'RSD_Vipers_PDR2_sigma8',
        'RSD_SDSS_sigma8',

        'SZcluster_fixedSL_fixedPlanck',
        'SZcluster_freeSL_fixedPlanck',
        'SZcluster_freeSL_CCCP',
        'SZcluster_freeSL_CMBlens',
        'SZcluster_freeSL_WtG',
        'SZcluster_sigom',

        'prior_ghost',
        'prior_grad',
        'prior_cs',
        'prior_ctsub',
        'prior_ctsup',
        'prior_gdotg',

        'mock_Planck_2015_sigom',
        'mock_lcdm_fsigma8_R',
        'mock_lcdm_sigma8_R',
        'mock_lcdm_f_R',
        'mock_lcdm_fsigma8_z1',
        'mock_lcdm_sigma8_z1',
        'mock_lcdm_f_z1',
        'mock_lcdm_fsigma8_z15',
        'mock_lcdm_sigma8_z15',
        'mock_lcdm_f_z15',
        'mock_lcdm_fsigma8_z2',
        'mock_lcdm_sigma8_z2',
        'mock_lcdm_f_z2',
        'mock_de0_fsigma8_z1',
        'mock_de0_sigma8_z1',
        'mock_de0_f_z1',
    ]
    for sline in slines:
        if sline[0] == 'likelihood':
            if len(sline) != 2:
                print('Wrong number of arguments for "likelihood".')
                error_ct += 1
            elif sline[1] not in allowed_likelihoods:
                print('Unrecognized "likelihood": "%s". Ignored.' % sline[1])
            elif sline[1] in out['likelihoods']:
                print('Duplicate "likelihood": "%s". Ignored.' % sline[1])
            else:
                out['likelihoods'].append(sline[1])


    #########################################################################
    ### Raise error if any problem detected, else return final dictionary ###
    #########################################################################
    if ignore_errors:
        print('%s problem detected.' % error_ct)
        return out
    elif error_ct == 1:
        raise ValueError('Check your .ini file (1 problem detected).')
    elif error_ct > 1:
        raise ValueError('Check your .ini file (%s problems detected)' % error_ct)
    else:
        return out



def copy_ini_file(fname, params):

    #################################
    ### Write copy of ini file ####
    #################################
    with open(fname) as f:
        lines = f.readlines()
    with open(params['output_fname'] + '.ini', 'w') as f:
        for line in lines:
            empty_line = line.split() == []
            comment = line[0] == '#'
            if not empty_line and not comment:
                f.write(line)
    return None


def autocomplete_ini(ini):

    ###############################
    ### Copy old ini dictionary ###
    ###############################
    new_ini = {}
    for k in ini.keys():
        new_ini[k] = ini[k]


    ############################################
    ### Auto-complete the new ini dictionary ###
    ############################################
    model    = ini['model']
    nsampler = ini['sampler']
    steps    = ini['n_steps']
    walkers  = ini['n_walkers']
    addname  = ini['add_name']
    temps    = ini['temps']

    ### Deal with output filename
    new_ini['output_fname'] += 'xRUN_%s_%s_%s' % (
        addname,
        nsampler,
        model['theory']
    )
    if model['theory'] != 'lcdm':
        new_ini['output_fname'] += '_%s_%s_%s' % (
            model['basis'],
            model['background'],
            model['parametrisation']
        )
    new_ini['output_fname'] += '_steps_%s_walkers_%s' % (
        steps,
        walkers
    )
    if nsampler == 'PT':
        new_ini['output_fname'] += '_temps_%s' % temps

    ### Deal with fixed parameters
    new_ini['fix_par'] = []
    new_ini['fix_par'].append(['zini', 1500.])
    new_ini['fix_par'].append(['zmid', 10.])
    new_ini['fix_par'].append(['z0', 0.])
    new_ini['fix_par'].append(['dz1', 1.])
    new_ini['fix_par'].append(['dz2', 0.01])
    new_ini['fix_par'].append(['method', 'LSODA'])
    new_ini['fix_par'].append(['zstab', np.linspace(0., 1500., 1e4)])
    new_ini['fix_par'].append(['zcmb', 1100.])
    new_ini['fix_par'].append(['D0', 1.])
    new_ini['fix_par'].append(['Dp0', -1. / (1. + 1500.)]) # -D0/(1+zini)
    new_ini['fix_par'].append(['H0', 67.31])
    new_ini['fix_par'].append(['w', -1.])
    new_ini['fix_par'].append(['x0', 0.315])       #!!!!!!!!!!#
    new_ini['fix_par'].append(['sig80', 0.829])     #!!!!!!!!!!#

    ### Deal with parameters
    new_ini['var_par'] = []
    # x0
    new_ini['var_par'].append(['x0', 0.31, 0.1, 0.6, 0.01])
    # sig80
    new_ini['var_par'].append(['sig80', 0.82, 0.3, 1., 0.01])
    # w
    #new_ini['var_par'].append(['w', -1., -2., 0., 0.01])
    # EFT params
    if model['theory'] != 'lcdm':
        if model['parametrisation'] == 'de0' : 
            n_param = 1
        elif model['parametrisation'] == 'de1' : 
            n_param = 2
        elif model['parametrisation'] == 'scalingz' : 
            n_param = 2
        if model['theory'] == 'bd' : 
            n_th = 1 
        elif model['theory'] == 'h3' : 
            n_th = 3
        elif model['theory'] == 'h45' : 
            n_th = 4
        for i in range(n_th):
            for j in range(n_param):
                tmp = ['eft_%s_%s' % (i+1, j+1), 0., -np.inf, np.inf, 1.]
                if model['parametrisation'] == 'de0' : 
                    tmp[2:4] = [-100, 100]
                elif model['parametrisation'] == 'de1' : 
                    # tmp[1] = 0.001
                    tmp[2:4] = [-100, 100]
                    # tmp[4] = 0.001
                elif model['parametrisation'] == 'scalingz' : 
                    if j == 0:
                        tmp[2:4] = [-20., 20.]
                    elif j == 1:
                        tmp[1] = 1.
                        tmp[2:4] = [1., 15.]
                new_ini['var_par'].append(tmp)

    ### Deal with getdist stuff
    # new_ini['gd_pnames']  = []
    # new_ini['gd_plabels'] = []


    # if model['theory'] != 'lcdm':

    #     if model['background'] == 'lcdm':
    #         new_ini['gd_pnames'].append(['Om0','sig80'])
    #         new_ini['gd_plabels'].append([r'\Omega_{m,0}',r'\sigma_{8,0}'])

    #         new_ini['gd_dnames']  = ['muz0','Sigmaz0','gammaz0']
    #         new_ini['gd_dlabels'] = [r'\mu (z=0)-1',r'\Sigma (z=0)-1',r'\gamma (z=0)-1']
    #         new_ini['gd_dranges'] = [[0,None],[None,None],[None,None]]

    #         if model['basis'] == 'alpha':
    #             if model['parametrisation'] == 'de0':
    #                 if model['theory'] == 'h3':
    #                     new_ini['gd_pnames'].np.append(['am0','ak0','ab0'])
    #                     new_ini['gd_plabels'].np.append([r'\alpha_{M,0}',r'\alpha_{K,0}',r'\alpha_{B,0}'])   
    #                 elif model['theory'] == 'h45':
    #                     new_ini['gd_pnames'].np.append(['am0','ak0','ab0','at0'])
    #                     new_ini['gd_plabels'].np.append([r'\alpha_{M,0}',r'\alpha_{K,0}',r'\alpha_{B,0}',r'\alpha_{T,0}'])
    #             elif model['parametrisation'] == 'de1':
    #                 if model['theory'] == 'h3':
    #                     new_ini['gd_pnames'].np.append(['am0','am1','ak0','ak1','ab0','ab1'])
    #                     new_ini['gd_plabels'].np.append([r'\alpha_{M,0}',r'\alpha_{M,1}',r'\alpha_{K,0}',r'\alpha_{K,1}',r'\alpha_{B,0}',r'\alpha_{B,1}'])
    #                 elif model['theory'] == 'h45':
    #                     new_ini['gd_pnames'].np.append(['am0','am1','ak0','ak1','ab0','ab1','at0','at1'])
    #                     new_ini['gd_plabels'].np.append([r'\alpha_{M,0}',r'\alpha_{M,1}',r'\alpha_{K,0}',r'\alpha_{K,1}',r'\alpha_{B,0}',r'\alpha_{B,1}',r'\alpha_{T,0}',r'\alpha_{T,1}'])
    #             elif model['parametrisation'] == 'scalingz':
    #                 if model['theory'] == 'h3':
    #                     new_ini['gd_pnames'].np.append(['am','qm','ak','qk','ab','qb'])
    #                     new_ini['gd_plabels'].np.append([r'a_M',r'q_M',r'a_K',r'q_K',r'a_B',r'q_B'])
    #                 elif model['theory'] == 'h45':
    #                     new_ini['gd_pnames'].np.append(['am','qm','ak','qk','ab','qb','at','qt'])
    #                     new_ini['gd_plabels'].np.append([r'a_M',r'q_M',r'a_K',r'q_K',r'a_B',r'q_B',r'a_T',r'q_T'])

    #         if model['parametrisation'] == 'de0':
    #             if model['theory'] == 'bd':
    #                 self.p_names    = np.append(self.p_names,['mu10'])
    #                 self.p_labels   = np.append(self.p_labels,[r'\mu_{10}'])
    #             elif model['theory'] == 'h3':
    #                 self.p_names    = np.append(self.p_names,['mu10','mu20','mu30'])
    #                 self.p_labels   = np.append(self.p_labels,[r'\mu_{10}',r'\mu_{20}',r'\mu_{30}'])
    #             elif model['theory'] == 'h45':
    #                 self.p_names    = np.append(self.p_names,['mu10','mu20','mu30','mu40'])
    #                 self.p_labels   = np.append(self.p_labels,[r'\mu_{10}',r'\mu_{20}',r'\mu_{30}',r'\mu_{40}'])
    #             else : print  '  /!\  case not found  /!\ ' 

    #         elif model['parametrisation'] == 'de1':
    #             if model['theory'] == 'bd':
    #                 self.p_names    = np.append(self.p_names,['mu10','mu11'])
    #                 self.p_labels   = np.append(self.p_labels,[r'\mu_{10}',r'\mu_{11}'])
    #             elif model['theory'] == 'h3':
    #                 self.p_names    = np.append(self.p_names,['mu10','mu11','mu20','mu21','mu30','mu31'])
    #                 self.p_labels   = np.append(self.p_labels,[r'\mu_{10}',r'\mu_{11}',r'\mu_{20}',r'\mu_{21}',r'\mu_{30}',r'\mu_{31}'])
    #             elif model['theory'] == 'h45':
    #                 self.p_names    = np.append(self.p_names,['mu10','mu11','mu20','mu21','mu30','mu31','mu40','mu41'])
    #                 self.p_labels   = np.append(self.p_labels,[r'\mu_{10}',r'\mu_{11}',r'\mu_{20}',r'\mu_{21}',r'\mu_{30}',r'\mu_{31}',r'\mu_{40}',r'\mu_{41}'])
    #             else : print  '  /!\  case not found  /!\ ' 

    #         elif model['parametrisation'] == 'scalingz':
    #             if model['theory'] == 'bd':
    #                 self.p_names    = np.append(self.p_names,['c1','q1'])
    #                 self.p_labels   = np.append(self.p_labels,[r'c_1',r'q_1'])
    #             elif model['theory'] == 'h3':
    #                 self.p_names    = np.append(self.p_names,['c1','q1','c2','q2','c3','q3'])
    #                 self.p_labels   = np.append(self.p_labels,[r'c_1',r'q_1',r'c_2',r'q_2',r'c_3',r'q_3'])
    #             elif model['theory'] == 'h45':
    #                 self.p_names    = np.append(self.p_names,['c1','q1','c2','q2','c3','q3','c4','q4'])
    #                 self.p_labels   = np.append(self.p_labels,[r'c_1',r'q_1',r'c_2',r'q_2',r'c_3',r'q_3',r'c_4',r'q_4'])




    return new_ini
