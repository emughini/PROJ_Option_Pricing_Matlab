# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_BermudanOptions.m

    ##################################################################
### Bermudan OPTION PRICER
##################################################################
# Descritpion: Script to Price Bermudan/American options in Levy Models
#              using the PROJ method
# Author:      Justin Kirkby
# References:  (1) American and exotic option pricing with jump diffusions and other Levy Processes,
#               J. Compuational Finance, 2018
#              (2) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_BermudanOptions.m:13
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    ############################################
###  Step 1) CONTRACT/GENERAL PARAMETERS
############################################
    S_0=100
# Script_BermudanOptions.m:22
    
    W=105
# Script_BermudanOptions.m:23
    
    r=0.05
# Script_BermudanOptions.m:24
    
    q=0.0
# Script_BermudanOptions.m:25
    
    T=1
# Script_BermudanOptions.m:26
    
    M=500
# Script_BermudanOptions.m:27
    
    ############################################
###  Step 2) CHOOSE MODEL PARAMETERS  (Levy Models)
############################################
    model=1
# Script_BermudanOptions.m:32
    
    params=cellarray([])
# Script_BermudanOptions.m:33
    if model == 1:
        params.sigmaBSM = copy(0.15)
# Script_BermudanOptions.m:36
    else:
        if model == 2:
            params.C = copy(0.02)
# Script_BermudanOptions.m:39
            params.G = copy(5)
# Script_BermudanOptions.m:40
            params.MM = copy(15)
# Script_BermudanOptions.m:41
            params.Y = copy(1.2)
# Script_BermudanOptions.m:42
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_BermudanOptions.m:45
                params.beta = copy(- 5)
# Script_BermudanOptions.m:46
                params.delta = copy(0.5)
# Script_BermudanOptions.m:47
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_BermudanOptions.m:50
                    params.lam = copy(0.4)
# Script_BermudanOptions.m:51
                    params.muj = copy(- 0.12)
# Script_BermudanOptions.m:52
                    params.sigmaj = copy(0.18)
# Script_BermudanOptions.m:53
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_BermudanOptions.m:56
                        params.lam = copy(3)
# Script_BermudanOptions.m:57
                        params.p_up = copy(0.2)
# Script_BermudanOptions.m:58
                        params.eta1 = copy(25)
# Script_BermudanOptions.m:59
                        params.eta2 = copy(10)
# Script_BermudanOptions.m:60
    
    ############################################
###  Step 3) CHOOSE PROJ PARAMETERS
############################################
    UseCumulant=1
# Script_BermudanOptions.m:67
    
    #---------------------
# APPROACH 1: Cumulant Based approach for grid width
# (see "Robust Option Pricing with Characteritics Functions and the BSpline Order of Density Projection")
#---------------------
    if UseCumulant == 1:
        logN=12
# Script_BermudanOptions.m:74
        L1=12
# Script_BermudanOptions.m:75
        #---------------------
# APPROACH 2: Manual GridWidth approach 
#---------------------
    else:
        P=7
# Script_BermudanOptions.m:80
        Pbar=3
# Script_BermudanOptions.m:81
    
    ############################################
### PRICE
############################################
###  Note: rnCHF is the risk netural CHF, c1,c2,c4 are the cumulants
    modelInput=getModelInput(model,T / M,r,q,params)
# Script_BermudanOptions.m:88
    if UseCumulant == 1:
        alpha=getTruncationAlpha(T,L1,modelInput,model)
# Script_BermudanOptions.m:91
    else:
        logN=P + Pbar
# Script_BermudanOptions.m:93
        alpha=2 ** Pbar / 2
# Script_BermudanOptions.m:94
    
    N=2 ** logN
# Script_BermudanOptions.m:96
    
    tic
    price=PROJ_Bermudan_Put(M,S_0,W,r,T,modelInput.rnCHF,N,alpha)
# Script_BermudanOptions.m:99
    toc
    fprintf('%.8f \n',price)