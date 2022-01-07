# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_SwingOptions.m

    ##################################################################
### SWING OPTION PRICER (RUN SCRIPT)
##################################################################
# Descritpion: Script to Price Swing options in Levy Models using the PROJ method 
#               Supports 1) Constant and Linear Recovery Type Contracts
#                        2) Fixed Rights Contracts
#              
# Author:      Justin Kirkby
# References:  (1) Swing Option Pricing by Dynamic Programming with B-Spline Density Projection
#                   Int. J. Theoretical and App. Finance (2019)
#              (2) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_SwingOptions.m:15
    cd(folder)
    addpath('./coeff_funcs')
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    ##############################################
###  Step 1) CHOOSE CONTRACT/GENERAL PARAMETERS
##############################################
    S_0=40
# Script_SwingOptions.m:25
    
    # Payoff constants (see paper for definition of payoff function)
    K1=10
# Script_SwingOptions.m:28
    
    K2=20
# Script_SwingOptions.m:29
    
    K3=40
# Script_SwingOptions.m:30
    
    K4=50
# Script_SwingOptions.m:31
    
    r=0.05
# Script_SwingOptions.m:33
    
    q=0.0
# Script_SwingOptions.m:34
    
    # Common Contract Params
    Dmax=5
# Script_SwingOptions.m:37
    
    T=1
# Script_SwingOptions.m:38
    
    # Contract Specific Params
    swing_type=3
# Script_SwingOptions.m:41
    
    if swing_type == 1:
        tau1=1 / 4
# Script_SwingOptions.m:44
        Mtau=12
# Script_SwingOptions.m:45
    else:
        if swing_type == 2:
            rho_tau=1 / 6
# Script_SwingOptions.m:47
            Mtau=12
# Script_SwingOptions.m:48
        else:
            if swing_type == 3:
                Ns=5
# Script_SwingOptions.m:50
                M=50
# Script_SwingOptions.m:51
    
    ##############################################
###  Step 2) CHOOSE MODEL PARAMETERS  (Levy Models)
##############################################
    model=1
# Script_SwingOptions.m:57
    
    params=cellarray([])
# Script_SwingOptions.m:58
    if model == 1:
        params.sigmaBSM = copy(0.3)
# Script_SwingOptions.m:61
    else:
        if model == 2:
            #     params.C  = 4; 
#     params.G  = 5; 
#     params.MM = 25; 
#     params.Y  = 0.8;
            params.C = copy(1)
# Script_SwingOptions.m:69
            params.G = copy(20)
# Script_SwingOptions.m:70
            params.MM = copy(30)
# Script_SwingOptions.m:71
            params.Y = copy(1.7)
# Script_SwingOptions.m:72
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_SwingOptions.m:75
                params.beta = copy(- 5)
# Script_SwingOptions.m:76
                params.delta = copy(0.5)
# Script_SwingOptions.m:77
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_SwingOptions.m:80
                    params.lam = copy(0.4)
# Script_SwingOptions.m:81
                    params.muj = copy(- 0.12)
# Script_SwingOptions.m:82
                    params.sigmaj = copy(0.18)
# Script_SwingOptions.m:83
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_SwingOptions.m:86
                        params.lam = copy(3)
# Script_SwingOptions.m:87
                        params.p_up = copy(0.2)
# Script_SwingOptions.m:88
                        params.eta1 = copy(25)
# Script_SwingOptions.m:89
                        params.eta2 = copy(10)
# Script_SwingOptions.m:90
                    else:
                        if model == 6:
                            params.v_0 = copy(0.0175)
# Script_SwingOptions.m:93
                            params.theta = copy(0.0398)
# Script_SwingOptions.m:94
                            params.kappa = copy(1.5768)
# Script_SwingOptions.m:95
                            params.sigma_v = copy(0.5751)
# Script_SwingOptions.m:96
                            params.rho = copy(- 0.5711)
# Script_SwingOptions.m:97
    
    ##############################################
###  Step 3) CHOOSE PROJ PARAMETERS
##############################################
    L1=20
# Script_SwingOptions.m:103
    
    logN=14
# Script_SwingOptions.m:104
    
    ##############################################
### PRICE
##############################################
    modelInput=getModelInput(model,T,r,q,params)
# Script_SwingOptions.m:109
    alpha=getTruncationAlpha(T,L1,modelInput,model)
# Script_SwingOptions.m:110
    N=2 ** logN
# Script_SwingOptions.m:111
    
    Ks=concat([K1,K2,K3,K4])
# Script_SwingOptions.m:112
    T_0=0
# Script_SwingOptions.m:113
    
    if swing_type == 1:
        tic
        price=PROJ_Swing_ConstantRecovery_Aug(r,S_0,Dmax,T_0,T,tau1,Mtau,N,alpha,modelInput.rnSYMB,Ks)
# Script_SwingOptions.m:118
        toc
    else:
        if swing_type == 2:
            tic
            price=PROJ_Swing_LinearRec(r,S_0,Dmax,rho_tau,T_0,T,Mtau,N,alpha,modelInput.rnSYMB,Ks)
# Script_SwingOptions.m:122
            toc
        else:
            if swing_type == 3:
                modelInput=getModelInput(model,T / M,r,q,params)
# Script_SwingOptions.m:125
                tic
                price=PROJ_Swing_FixedRights(M,N,alpha,modelInput.rnCHF,r,Dmax,T_0,T,Ns,S_0,Ks)
# Script_SwingOptions.m:127
                toc
    
    fprintf('%.8f \n',price)