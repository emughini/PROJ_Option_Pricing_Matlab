# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_DoubleBarrierOptions.m

    ##################################################################
### DOUBLE BARRIER OPTION PRICER
##################################################################
# Descritpion: Script to Price Double Barrier options in Levy Models
#              using the PROJ method
# Author:      Justin Kirkby
# References:  (1) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
#              (2) Robust Barrier Option Pricing by Frame Projection under
#              Exponential Levy Dynamics, App. Math. Finance, 2017
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_DoubleBarrierOptions.m:13
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    ##############################################
### Step 1) CHOOSE CONTRACT/GENERAL PARAMETERS
##############################################
    S_0=100
# Script_DoubleBarrierOptions.m:21
    
    W=100
# Script_DoubleBarrierOptions.m:22
    
    r=0.05
# Script_DoubleBarrierOptions.m:23
    
    q=0.02
# Script_DoubleBarrierOptions.m:24
    
    T=1
# Script_DoubleBarrierOptions.m:25
    
    call=1
# Script_DoubleBarrierOptions.m:26
    
    L=80
# Script_DoubleBarrierOptions.m:27
    
    U=120
# Script_DoubleBarrierOptions.m:28
    
    M=52
# Script_DoubleBarrierOptions.m:29
    
    ##############################################
###  Step 2) CHOOSE MODEL PARAMETERS 
##############################################
    model=1
# Script_DoubleBarrierOptions.m:35
    
    params=cellarray([])
# Script_DoubleBarrierOptions.m:36
    if model == 1:
        params.sigmaBSM = copy(0.2)
# Script_DoubleBarrierOptions.m:39
    else:
        if model == 2:
            params.C = copy(0.02)
# Script_DoubleBarrierOptions.m:42
            params.G = copy(5)
# Script_DoubleBarrierOptions.m:43
            params.MM = copy(15)
# Script_DoubleBarrierOptions.m:44
            params.Y = copy(1.2)
# Script_DoubleBarrierOptions.m:45
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_DoubleBarrierOptions.m:48
                params.beta = copy(- 5)
# Script_DoubleBarrierOptions.m:49
                params.delta = copy(0.5)
# Script_DoubleBarrierOptions.m:50
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_DoubleBarrierOptions.m:53
                    params.lam = copy(0.4)
# Script_DoubleBarrierOptions.m:54
                    params.muj = copy(- 0.12)
# Script_DoubleBarrierOptions.m:55
                    params.sigmaj = copy(0.18)
# Script_DoubleBarrierOptions.m:56
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_DoubleBarrierOptions.m:59
                        params.lam = copy(3)
# Script_DoubleBarrierOptions.m:60
                        params.p_up = copy(0.2)
# Script_DoubleBarrierOptions.m:61
                        params.eta1 = copy(25)
# Script_DoubleBarrierOptions.m:62
                        params.eta2 = copy(10)
# Script_DoubleBarrierOptions.m:63
    
    ##############################################
###  Step 3) CHOOSE PROJ PARAMETERS
##############################################
    
    logN=13
# Script_DoubleBarrierOptions.m:71
    
    L1=8
# Script_DoubleBarrierOptions.m:72
    
    ##############################################
### PRICE
##############################################
###  Note: rnCHF is the risk netural CHF, c1,c2,c4 are the cumulants
    modelInput=getModelInput(model,T / M,r,q,params)
# Script_DoubleBarrierOptions.m:78
    alpha=getTruncationAlpha(T,L1,modelInput,model)
# Script_DoubleBarrierOptions.m:80
    N=2 ** logN
# Script_DoubleBarrierOptions.m:81
    
    tic
    price=PROJ_Double_Barrier(N,alpha,call,L,U,S_0,W,M,T,r,modelInput.rnCHF)
# Script_DoubleBarrierOptions.m:84
    toc
    fprintf('%.8f \n',price)