# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_GMDB_DCA.m

    ##################################################################
### ASIAN OPTION PRICER  (RUN SCRIPT)
##################################################################
# Descritpion: Script to Price Gauranteed Minimum Death Benefits (GMDB) in Levy Models using the PROJ method
#               This version is based on a dollar cost average style investment account (see reference paper below)
    
    # Terminal Payoff:  Payoff(tau) = L*exp(g*tau) + (Gam(tau) - L*exp(g*tau))^+
#                      Gam(tau) = S_M * sum_{m=0}^M(alpha*gamma / S_m)
#                          tau  = time of death (discrete periods)
#                            M  = number of periods until time of death (each period length dt)
    
    # Author:      Justin Kirkby
# Reference:    1) Equity-Linked Guaranteed Minimum Death Benefits with Dollar Cost Averaging, J.L.Kirkby & D.Nguyen, 2021
#               2) An Efficient Transform Method For Asian Option Pricing, SIAM J. Financial Math., 2016
#################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_GMDB_DCA.m:17
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    addpath('../Asian_Options')
    addpath('../European_Options')
    addpath('../Geometric_Asian_Options')
    #################################
###  Step 1) CHOOSE CONTRACT/GENERAL PARAMETERS
#################################
    S_0=100
# Script_GMDB_DCA.m:28
    
    r=0.01
# Script_GMDB_DCA.m:29
    
    q=0.0
# Script_GMDB_DCA.m:30
    
    age=30
# Script_GMDB_DCA.m:31
    
    gmdb_params=cellarray([])
# Script_GMDB_DCA.m:33
    gmdb_params.contract_type = copy(1)
# Script_GMDB_DCA.m:34
    
    gmdb_params.alpha = copy(dot(2,S_0))
# Script_GMDB_DCA.m:35
    
    gmdb_params.gamma = copy(0.92)
# Script_GMDB_DCA.m:36
    
    gmdb_params.L = copy(10000)
# Script_GMDB_DCA.m:37
    
    gmdb_params.g = copy(0.01)
# Script_GMDB_DCA.m:38
    
    #################################
###  Step 2) CHOOSE MODEL PARAMETERS (Levy Models)
#################################
# -------------
# Choose Model for death/mortality
# -------------
    death_model=1
# Script_GMDB_DCA.m:47
    
    if death_model == 1:
        death_prob=make_mortality_table_pmf(age)
# Script_GMDB_DCA.m:50
    else:
        if death_model == 2:
            death_prob=make_combo_2_expos_pmf(3,- 2,0.08,0.12,110 - age + 1)
# Script_GMDB_DCA.m:52
        else:
            if death_model == 3:
                # manually specify probability of death
                death_prob=concat([0.01,0.05,0.1,0.2,0.1,0.05,0.001,0.5,0.2])
# Script_GMDB_DCA.m:55
                death_prob=death_prob / sum(death_prob)
# Script_GMDB_DCA.m:56
    
    gmdb_params.death_prob = copy(death_prob)
# Script_GMDB_DCA.m:58
    # -------------
# Choose Levy Model for risky asset
# -------------
    model=1
# Script_GMDB_DCA.m:63
    
    params=cellarray([])
# Script_GMDB_DCA.m:65
    if model == 1:
        params.sigmaBSM = copy(0.15)
# Script_GMDB_DCA.m:67
    else:
        if model == 2:
            params.C = copy(0.02)
# Script_GMDB_DCA.m:70
            params.G = copy(5)
# Script_GMDB_DCA.m:71
            params.MM = copy(15)
# Script_GMDB_DCA.m:72
            params.Y = copy(1.2)
# Script_GMDB_DCA.m:73
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_GMDB_DCA.m:76
                params.beta = copy(- 5)
# Script_GMDB_DCA.m:77
                params.delta = copy(0.5)
# Script_GMDB_DCA.m:78
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_GMDB_DCA.m:81
                    params.lam = copy(0.4)
# Script_GMDB_DCA.m:82
                    params.muj = copy(- 0.12)
# Script_GMDB_DCA.m:83
                    params.sigmaj = copy(0.18)
# Script_GMDB_DCA.m:84
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_GMDB_DCA.m:87
                        params.lam = copy(3)
# Script_GMDB_DCA.m:88
                        params.p_up = copy(0.2)
# Script_GMDB_DCA.m:89
                        params.eta1 = copy(25)
# Script_GMDB_DCA.m:90
                        params.eta2 = copy(10)
# Script_GMDB_DCA.m:91
                    else:
                        if model == 8:
                            params.sigma = copy(0.2)
# Script_GMDB_DCA.m:94
                            params.nu = copy(0.85)
# Script_GMDB_DCA.m:95
                            params.theta = copy(0)
# Script_GMDB_DCA.m:96
    
    #################################
###  Step 3) CHOOSE PROJ PARAMETERS
#################################
    freq=1
# Script_GMDB_DCA.m:102
    
    dt=1 / freq
# Script_GMDB_DCA.m:103
    proj_params=cellarray([])
# Script_GMDB_DCA.m:105
    proj_params.N = copy(2 ** 7)
# Script_GMDB_DCA.m:106
    
    proj_params.L1 = copy(8)
# Script_GMDB_DCA.m:107
    
    proj_params.model = copy(model)
# Script_GMDB_DCA.m:108
    modelInput=getModelInput(model,dt,r,q,params)
# Script_GMDB_DCA.m:110
    #################################
### PRICE
#################################
    
    plot_death_prob=1
# Script_GMDB_DCA.m:116
    if plot_death_prob == 1:
        plot(arange(1,length(death_prob)),death_prob,'k-','linewidth',1.1)
        xlabel('$M_\tau = n$','interpreter','latex')
        ylabel('probability, $p^\omega_n$','interpreter','latex')
    
    tic
    proj_params.L1 = copy(12)
# Script_GMDB_DCA.m:125
    
    price2,opt2,L2=PROJ_GMDB_DCA_Fast(proj_params,S_0,gmdb_params,r,q,modelInput,nargout=3)
# Script_GMDB_DCA.m:126
    toc
    fprintf('Price: %.8f, Option: %.8f, L: %.8f \n',price2,opt2,L2)