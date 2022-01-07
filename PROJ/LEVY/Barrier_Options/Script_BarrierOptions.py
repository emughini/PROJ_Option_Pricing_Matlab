# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_BarrierOptions.m

    ##################################################################
### BARRIER OPTION PRICER
##################################################################
# Descritpion: Script to Price Barrier options in Levy Models
#              using the PROJ method
# Author:      Justin Kirkby
# References:  (1) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
#              (2) Robust Barrier Option Pricing by Frame Projection under
#              Exponential Levy Dynamics, App. Math. Finance, 2017
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_BarrierOptions.m:13
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    ##############################################
### Step 1) CHOOSE CONTRACT/GENERAL PARAMETERS
##############################################
    S_0=100
# Script_BarrierOptions.m:21
    
    W=100
# Script_BarrierOptions.m:22
    
    r=0.05
# Script_BarrierOptions.m:23
    
    q=0.02
# Script_BarrierOptions.m:24
    
    T=1
# Script_BarrierOptions.m:25
    
    call=1
# Script_BarrierOptions.m:26
    
    down=1
# Script_BarrierOptions.m:27
    
    H=90
# Script_BarrierOptions.m:28
    
    M=52
# Script_BarrierOptions.m:29
    
    rebate=5
# Script_BarrierOptions.m:31
    
    ##############################################
###  Step 2) CHOOSE MODEL PARAMETERS 
##############################################
    model=1
# Script_BarrierOptions.m:37
    
    params=cellarray([])
# Script_BarrierOptions.m:38
    if model == 1:
        params.sigmaBSM = copy(0.2)
# Script_BarrierOptions.m:41
    else:
        if model == 2:
            params.C = copy(0.02)
# Script_BarrierOptions.m:44
            params.G = copy(5)
# Script_BarrierOptions.m:45
            params.MM = copy(15)
# Script_BarrierOptions.m:46
            params.Y = copy(1.2)
# Script_BarrierOptions.m:47
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_BarrierOptions.m:50
                params.beta = copy(- 5)
# Script_BarrierOptions.m:51
                params.delta = copy(0.5)
# Script_BarrierOptions.m:52
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_BarrierOptions.m:55
                    params.lam = copy(0.4)
# Script_BarrierOptions.m:56
                    params.muj = copy(- 0.12)
# Script_BarrierOptions.m:57
                    params.sigmaj = copy(0.18)
# Script_BarrierOptions.m:58
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_BarrierOptions.m:61
                        params.lam = copy(3)
# Script_BarrierOptions.m:62
                        params.p_up = copy(0.2)
# Script_BarrierOptions.m:63
                        params.eta1 = copy(25)
# Script_BarrierOptions.m:64
                        params.eta2 = copy(10)
# Script_BarrierOptions.m:65
    
    ##############################################
###  Step 3) CHOOSE PROJ PARAMETERS
##############################################
    UseCumulant=1
# Script_BarrierOptions.m:72
    
    #---------------------
# APPROACH 1: Cumulant Based approach for grid width
# (see "Robust Option Pricing with Characteritics Functions and the BSpline Order of Density Projection")
#---------------------
    if UseCumulant == 1:
        logN=14
# Script_BarrierOptions.m:79
        L1=12
# Script_BarrierOptions.m:80
        #---------------------
# APPROACH 2: Manual GridWidth approach 
#---------------------
    else:
        P=8
# Script_BarrierOptions.m:85
        Pbar=3
# Script_BarrierOptions.m:86
    
    ##############################################
### PRICE
##############################################
###  Note: rnCHF is the risk netural CHF, c1,c2,c4 are the cumulants
    modelInput=getModelInput(model,T / M,r,q,params)
# Script_BarrierOptions.m:93
    if UseCumulant == 1:
        alpha=getTruncationAlpha(T,L1,modelInput,model)
# Script_BarrierOptions.m:96
    else:
        logN=P + Pbar
# Script_BarrierOptions.m:98
        alpha=2 ** Pbar / 2
# Script_BarrierOptions.m:99
    
    N=2 ** logN
# Script_BarrierOptions.m:101
    
    tic
    price=PROJ_Barrier(N,alpha,call,down,S_0,W,H,M,r,q,modelInput.rnCHF,T,rebate)
# Script_BarrierOptions.m:104
    toc
    fprintf('%.8f \n',price)