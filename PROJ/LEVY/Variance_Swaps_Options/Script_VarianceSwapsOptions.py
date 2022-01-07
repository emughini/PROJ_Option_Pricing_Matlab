# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_VarianceSwapsOptions.m

    ##################################################################
### DISCRETE VARIANCE SWAP/OPTION PRICER
##################################################################
# Descritpion: Script to Price Barrier options in Levy Models
#              using the PROJ method
# Author:      Justin Kirkby
# References:  (1) A General Framework for discretely sampled realized
#              variance derivatives in stocahstic volatility models with
#              jumps, EJOR, 2017
#              (2) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
##################################################################
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_VarianceSwapsOptions.m:13
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    ################################################
###  Step 1) CHOOSE CONTRACT/GENERAL PARAMETERS
################################################
    K=0.01
# Script_VarianceSwapsOptions.m:21
    
    r=0.05
# Script_VarianceSwapsOptions.m:22
    
    q=0.0
# Script_VarianceSwapsOptions.m:23
    
    T=1
# Script_VarianceSwapsOptions.m:24
    
    M=252
# Script_VarianceSwapsOptions.m:25
    
    contract=1
# Script_VarianceSwapsOptions.m:27
    
    ################################################
###  Step 2) CHOOSE MODEL PARAMETERS (Levy Models)
################################################
    
    model=1
# Script_VarianceSwapsOptions.m:33
    
    params=cellarray([])
# Script_VarianceSwapsOptions.m:34
    if model == 1:
        params.sigmaBSM = copy(0.18)
# Script_VarianceSwapsOptions.m:37
    else:
        if model == 2:
            params.C = copy(0.02)
# Script_VarianceSwapsOptions.m:40
            params.G = copy(5)
# Script_VarianceSwapsOptions.m:41
            params.MM = copy(15)
# Script_VarianceSwapsOptions.m:42
            params.Y = copy(1.2)
# Script_VarianceSwapsOptions.m:43
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_VarianceSwapsOptions.m:46
                params.beta = copy(- 5)
# Script_VarianceSwapsOptions.m:47
                params.delta = copy(0.5)
# Script_VarianceSwapsOptions.m:48
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_VarianceSwapsOptions.m:51
                    params.lam = copy(0.4)
# Script_VarianceSwapsOptions.m:52
                    params.muj = copy(- 0.12)
# Script_VarianceSwapsOptions.m:53
                    params.sigmaj = copy(0.18)
# Script_VarianceSwapsOptions.m:54
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_VarianceSwapsOptions.m:57
                        params.lam = copy(3)
# Script_VarianceSwapsOptions.m:58
                        params.p_up = copy(0.2)
# Script_VarianceSwapsOptions.m:59
                        params.eta1 = copy(25)
# Script_VarianceSwapsOptions.m:60
                        params.eta2 = copy(10)
# Script_VarianceSwapsOptions.m:61
    
    ################################################
###  Step 3) CHOOSE PROJ PARAMETERS
################################################
    UseCumulant=1
# Script_VarianceSwapsOptions.m:68
    
    #---------------------
# APPROACH 1: Cumulant Based approach for grid width
# (see "Robust Option Pricing with Characteritics Functions and the BSpline Order of Density Projection")
#---------------------
    if UseCumulant == 1:
        logN=10
# Script_VarianceSwapsOptions.m:75
        L1=14
# Script_VarianceSwapsOptions.m:76
        #---------------------
# APPROACH 2: Manual GridWidth approach 
#---------------------
    else:
        P=7
# Script_VarianceSwapsOptions.m:81
        Pbar=3
# Script_VarianceSwapsOptions.m:82
    
    #################################
### PRICE
#################################
###  Note: rnCHF is the risk netural CHF, c1,c2,c4 are the cumulants
    modelInput=getModelInput(model,T / M,r,q,params)
# Script_VarianceSwapsOptions.m:89
    if UseCumulant == 1:
        alpha=getTruncationAlpha(T,L1,modelInput,model)
# Script_VarianceSwapsOptions.m:92
    else:
        logN=P + Pbar
# Script_VarianceSwapsOptions.m:94
        alpha=2 ** Pbar / 2
# Script_VarianceSwapsOptions.m:95
    
    N=2 ** logN
# Script_VarianceSwapsOptions.m:97
    tic
    price=PROJ_DiscreteVariance_Swaps_Options(N,alpha,M,r,T,K,modelInput.rnCHF,contract)
# Script_VarianceSwapsOptions.m:100
    toc
    fprintf('price: %.8f\n',price)
    if contract == 1:
        c2=modelInput.c2
# Script_VarianceSwapsOptions.m:106
        c1=modelInput.c1
# Script_VarianceSwapsOptions.m:106
        analytical=c2 + dot(c1 ** 2,T) / M
# Script_VarianceSwapsOptions.m:107
        fprintf('analytical SWAP price: %.8f \n',analytical)
        fprintf('----------------------------\n')
        fprintf('Error: %.2e\n',analytical - price)
    