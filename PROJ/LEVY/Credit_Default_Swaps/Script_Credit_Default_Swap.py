# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_Credit_Default_Swap.m

    ##################################################################
### CREDIT DEFAULT SWAP / DEFAULT PROBABILITY CALCULATOR
##################################################################
# Descritpion: Script to Calc Fair Spread of Credit Default Swaps (and default probabilities) in Levy Models
#              using the PROJ method
# Author:      Justin Kirkby
# References:  (1) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
#              (2) American and exotic option pricing with jump diffusions and other Levy Processes,
#               J. Compuational Finance, 2018
##################################################################
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_Credit_Default_Swap.m:12
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    ##############################################
### Step 1) CHOOSE CONTRACT/GENERAL PARAMETERS
##############################################
# For details on CDS model, see reference (2) above
    r=0.04
# Script_Credit_Default_Swap.m:21
    
    T=1
# Script_Credit_Default_Swap.m:22
    
    M=52
# Script_Credit_Default_Swap.m:23
    
    R=0.4
# Script_Credit_Default_Swap.m:24
    
    L=0.4
# Script_Credit_Default_Swap.m:25
    
    ##############################################
###  Step 2) CHOOSE MODEL PARAMETERS 
##############################################
    model=1
# Script_Credit_Default_Swap.m:30
    
    params=cellarray([])
# Script_Credit_Default_Swap.m:31
    if model == 1:
        params.sigmaBSM = copy(0.2)
# Script_Credit_Default_Swap.m:34
    else:
        if model == 2:
            params.C = copy(0.02)
# Script_Credit_Default_Swap.m:37
            params.G = copy(5)
# Script_Credit_Default_Swap.m:38
            params.MM = copy(15)
# Script_Credit_Default_Swap.m:39
            params.Y = copy(1.2)
# Script_Credit_Default_Swap.m:40
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_Credit_Default_Swap.m:43
                params.beta = copy(- 5)
# Script_Credit_Default_Swap.m:44
                params.delta = copy(0.5)
# Script_Credit_Default_Swap.m:45
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_Credit_Default_Swap.m:48
                    params.lam = copy(0.4)
# Script_Credit_Default_Swap.m:49
                    params.muj = copy(- 0.12)
# Script_Credit_Default_Swap.m:50
                    params.sigmaj = copy(0.18)
# Script_Credit_Default_Swap.m:51
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_Credit_Default_Swap.m:54
                        params.lam = copy(3)
# Script_Credit_Default_Swap.m:55
                        params.p_up = copy(0.2)
# Script_Credit_Default_Swap.m:56
                        params.eta1 = copy(25)
# Script_Credit_Default_Swap.m:57
                        params.eta2 = copy(10)
# Script_Credit_Default_Swap.m:58
    
    ##############################################
###  Step 3) CHOOSE PROJ PARAMETERS
##############################################
    UseCumulant=1
# Script_Credit_Default_Swap.m:65
    
    mult=2
# Script_Credit_Default_Swap.m:66
    
    #---------------------
# APPROACH 1: Cumulant Based approach for grid width
# (see "Robust Option Pricing with Characteritics Functions and the BSpline Order of Density Projection")
#---------------------
    if UseCumulant == 1:
        logN=14
# Script_Credit_Default_Swap.m:73
        L1=12
# Script_Credit_Default_Swap.m:74
        #---------------------
# APPROACH 2: Manual GridWidth approach 
#---------------------
    else:
        P=10
# Script_Credit_Default_Swap.m:79
        Pbar=3
# Script_Credit_Default_Swap.m:80
    
    ##############################################
### PRICE
##############################################
###  Note: rnCHF is the risk netural CHF, c1,c2,c4 are the cumulants
    modelInput=getModelInput(model,T / M,r,0,params)
# Script_Credit_Default_Swap.m:87
    if UseCumulant == 1:
        alpha=getTruncationAlpha(T,L1,modelInput,model)
# Script_Credit_Default_Swap.m:90
    else:
        logN=P + Pbar
# Script_Credit_Default_Swap.m:92
        alpha=2 ** Pbar / 2
# Script_Credit_Default_Swap.m:93
    
    N=2 ** logN
# Script_Credit_Default_Swap.m:95
    
    tic
    prob,spread=PROJ_CDS(R,L,M,T,r,N,alpha,mult,modelInput.rnCHF,nargout=2)
# Script_Credit_Default_Swap.m:98
    toc
    fprintf('Default Prob: %.8f \n',prob)
    fprintf('CDS Spread: %.8f \n',spread)