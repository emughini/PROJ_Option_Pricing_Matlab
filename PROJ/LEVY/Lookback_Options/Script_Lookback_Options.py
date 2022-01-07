# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_Lookback_Options.m

    ##################################################################
### LOOKBACK / HINDSIGHT OPTION PRICER
##################################################################
# Descritpion: Script to Price Lookback/Hindsight options in Levy Models
#              using the PROJ method
# Author:      Justin Kirkby
# References:  (1) American and Exotic Option Pricing with Jump Diffusions
#               and other Levy Processes, J. Computational Finance 2018
#              (2) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_Lookback_Options.m:12
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    #################################
###  CONTRACT/GENERAL PARAMETERS
#################################
# Floating Strike (Lookback) Put:  max{S_m: 0<=m<=M} - S_T
# Floating Strike (Lookback) Call: S_T - min{S_m: 0<=m<=M}
# Fixed Strike (Hindsight) Put: (W - min{S_m: 0<=m<=M})^+
# Fixed Strike (Hindsight) Call: (max{S_m: 0<=m<=M} - W)^+
    
    S_0=100
# Script_Lookback_Options.m:26
    
    W=100
# Script_Lookback_Options.m:27
    
    r=0.1
# Script_Lookback_Options.m:28
    
    q=0.05
# Script_Lookback_Options.m:29
    
    T=0.5
# Script_Lookback_Options.m:30
    
    M=50
# Script_Lookback_Options.m:32
    ################                      
# NOTE: currently Only floating strike Put, and fixed Strike Call Are Supported
# The other two contract types will be finished soon (hopefully)
################
    call=1
# Script_Lookback_Options.m:38
    floating_strike=0
# Script_Lookback_Options.m:39
    
    # for floating strike, W (strike) is irrelevant param
    if logical_not((floating_strike == 1 and call != 1)) and logical_not((floating_strike != 1 and call == 1)):
        error('This contract type not currently finished. Implementaion in progress')
    
    #################################
    model=1
# Script_Lookback_Options.m:46
    
    #################################
    
    #################################
###  CHOOSE PROJ PARAMETERS
#################################
    order=3
# Script_Lookback_Options.m:52
    
    UseCumulant=1
# Script_Lookback_Options.m:53
    
    #---------------------
# APPROACH 1: Cumulant Based approach for grid width
# (see "Robust Option Pricing with Characteritics Functions and the BSpline Order of Density Projection")
#---------------------
    if UseCumulant == 1:
        logN=13
# Script_Lookback_Options.m:60
        L1=12
# Script_Lookback_Options.m:61
        #---------------------
# APPROACH 2: Manual GridWidth approach 
#---------------------
    else:
        P=7
# Script_Lookback_Options.m:66
        Pbar=2
# Script_Lookback_Options.m:67
    
    #################################
###  CHOOSE MODEL PARAMETERS 
###  Note: rnCHF is the risk netural CHF, c1,c2,c4 are the cumulants
#################################
    params=cellarray([])
# Script_Lookback_Options.m:74
    if model == 1:
        params.sigmaBSM = copy(0.3)
# Script_Lookback_Options.m:77
    else:
        if model == 2:
            params.C = copy(4)
# Script_Lookback_Options.m:80
            params.G = copy(50)
# Script_Lookback_Options.m:81
            params.MM = copy(60)
# Script_Lookback_Options.m:82
            params.Y = copy(0.7)
# Script_Lookback_Options.m:83
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_Lookback_Options.m:86
                params.beta = copy(- 5)
# Script_Lookback_Options.m:87
                params.delta = copy(0.5)
# Script_Lookback_Options.m:88
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_Lookback_Options.m:91
                    params.lam = copy(0.4)
# Script_Lookback_Options.m:92
                    params.muj = copy(- 0.12)
# Script_Lookback_Options.m:93
                    params.sigmaj = copy(0.18)
# Script_Lookback_Options.m:94
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_Lookback_Options.m:97
                        params.lam = copy(3)
# Script_Lookback_Options.m:98
                        params.p_up = copy(0.2)
# Script_Lookback_Options.m:99
                        params.eta1 = copy(25)
# Script_Lookback_Options.m:100
                        params.eta2 = copy(10)
# Script_Lookback_Options.m:101
    
    #################################
### PRICE
#################################
    modelInput=getModelInput(model,T / M,r,q,params)
# Script_Lookback_Options.m:108
    if UseCumulant == 1:
        alpha=getTruncationAlpha(T,L1,modelInput,model)
# Script_Lookback_Options.m:111
    else:
        logN=P + Pbar
# Script_Lookback_Options.m:113
        alpha=2 ** Pbar / 2
# Script_Lookback_Options.m:114
    
    N=2 ** logN
# Script_Lookback_Options.m:117
    tic
    price=PROJ_Lookback(N,alpha,S_0,W,call,r,q,M,T,modelInput.rnSYMB,floating_strike)
# Script_Lookback_Options.m:120
    toc
    fprintf('%.8f \n',price)