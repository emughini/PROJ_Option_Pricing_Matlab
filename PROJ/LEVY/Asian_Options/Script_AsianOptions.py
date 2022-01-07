# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_AsianOptions.m

    ##################################################################
### ASIAN OPTION PRICER  (RUN SCRIPT)
##################################################################
# Descritpion: Script to Price Asian options in Levy Models using the PROJ method
# Author:      Justin Kirkby
# Reference:   (1) An Efficient Transform Method For Asian Option Pricing, SIAM J. Financial Math., 2016
#              (2) American and Exotic Option Pricing with Jump Diffusions
#              and other Levy Processes, Journal of Computational Finance, 2018
#################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_AsianOptions.m:11
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    #################################
###  Step 1) CHOOSE CONTRACT/GENERAL PARAMETERS
#################################
    call=0
# Script_AsianOptions.m:20
    
    S_0=100
# Script_AsianOptions.m:21
    
    W=100
# Script_AsianOptions.m:22
    
    r=0.05
# Script_AsianOptions.m:23
    
    q=0.0
# Script_AsianOptions.m:24
    
    T=1
# Script_AsianOptions.m:25
    
    M=52
# Script_AsianOptions.m:26
    
    #################################
###  Step 2) CHOOSE MODEL PARAMETERS (Levy Models)
#################################
    model=1
# Script_AsianOptions.m:31
    
    params=cellarray([])
# Script_AsianOptions.m:32
    if model == 1:
        params.sigmaBSM = copy(0.15)
# Script_AsianOptions.m:35
    else:
        if model == 2:
            params.C = copy(0.02)
# Script_AsianOptions.m:38
            params.G = copy(5)
# Script_AsianOptions.m:39
            params.MM = copy(15)
# Script_AsianOptions.m:40
            params.Y = copy(1.2)
# Script_AsianOptions.m:41
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_AsianOptions.m:44
                params.beta = copy(- 5)
# Script_AsianOptions.m:45
                params.delta = copy(0.5)
# Script_AsianOptions.m:46
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_AsianOptions.m:49
                    params.lam = copy(0.4)
# Script_AsianOptions.m:50
                    params.muj = copy(- 0.12)
# Script_AsianOptions.m:51
                    params.sigmaj = copy(0.18)
# Script_AsianOptions.m:52
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_AsianOptions.m:55
                        params.lam = copy(3)
# Script_AsianOptions.m:56
                        params.p_up = copy(0.2)
# Script_AsianOptions.m:57
                        params.eta1 = copy(25)
# Script_AsianOptions.m:58
                        params.eta2 = copy(10)
# Script_AsianOptions.m:59
                    else:
                        if model == 8:
                            params.sigma = copy(0.2)
# Script_AsianOptions.m:62
                            params.nu = copy(0.85)
# Script_AsianOptions.m:63
                            params.theta = copy(0)
# Script_AsianOptions.m:64
    
    #################################
###  Step 3) CHOOSE PROJ PARAMETERS
#################################
    UseCumulant=1
# Script_AsianOptions.m:70
    
    #---------------------
# APPROACH 1: Cumulant Based approach for grid width
# (see "Robust Option Pricing with Characteritics Functions and the BSpline Order of Density Projection")
#---------------------
    if UseCumulant == 1:
        logN=8
# Script_AsianOptions.m:77
        L1=10
# Script_AsianOptions.m:78
        #---------------------
# APPROACH 2: Manual GridWidth approach 
#---------------------
    else:
        P=6
# Script_AsianOptions.m:83
        Pbar=3
# Script_AsianOptions.m:84
    
    #################################
### PRICE
#################################
###  Note: rnCHF is the risk netural CHF, c1,c2,c4 are the cumulants
    dt=T / M
# Script_AsianOptions.m:91
    modelInput=getModelInput(model,dt,r,q,params)
# Script_AsianOptions.m:92
    if UseCumulant == 1:
        alpha=getTruncationAlpha(T,L1,modelInput,model)
# Script_AsianOptions.m:95
    else:
        logN=P + Pbar
# Script_AsianOptions.m:97
        alpha=2 ** Pbar / 2
# Script_AsianOptions.m:98
    
    N=2 ** logN
# Script_AsianOptions.m:100
    
    tic
    price=PROJ_Asian(N,alpha,S_0,M,W,call,T,r,q,modelInput.rnCHF,dot(modelInput.RNmu,dt))
# Script_AsianOptions.m:103
    toc
    fprintf('%.8f \n',price)