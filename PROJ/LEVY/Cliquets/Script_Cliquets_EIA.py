# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_Cliquets_EIA.m

    ##################################################################
### Cliquet/Equity Index Annuity (EIA) PRICER (RUN SCRIPT)
##################################################################
# Descritpion: Script to Price Barrier options in Levy Models
#              using the PROJ method
# Author:      Justin Kirkby  (In coordination with Duy Nguyen and Zhenyu Cui)
# References:  (1) Equity-linked Annuity pricing with Cliquet-style
#               guarantees in regime-switching and stochastic volatility
#               models with jumps, Insurance: Math. and Economics, 2017
#              (2) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_Cliquets_EIA.m:14
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    ##########################################
### Step 1) CHOOSE CONTRACT/GENERAL PARAMETERS
##########################################
    r=0.05
# Script_Cliquets_EIA.m:22
    
    q=0.0
# Script_Cliquets_EIA.m:23
    
    T=1
# Script_Cliquets_EIA.m:24
    
    M=12
# Script_Cliquets_EIA.m:25
    
    ###########################
# contract: 1 = sum of local caps
#           2 = sum of local caps & floors
#           3 = cliquet: local & global caps & floors
#           4 = cliquet: local floor & cap, global floor, NO GLOBAL CAP  
#           5 = MPP: ie monthly point-to-point or Monthly Cap Sum (Bernard, Li)
#           6 = Multiplicative Cliquet (e.g. Hieber)
###########################
    contract=3
# Script_Cliquets_EIA.m:35
    
    ###########################
    contractParams.K = copy(1)
# Script_Cliquets_EIA.m:38
    
    if contract != 6:
        contractParams.C = copy(0.06)
# Script_Cliquets_EIA.m:41
        contractParams.CG = copy(dot(dot(0.75,M),contractParams.C))
# Script_Cliquets_EIA.m:42
        contractParams.F = copy(0.01)
# Script_Cliquets_EIA.m:43
        contractParams.FG = copy(dot(dot(1.25,M),contractParams.F))
# Script_Cliquets_EIA.m:44
    else:
        # Mutliplicative style cliquet
        contractParams.Alpha = copy(0.25)
# Script_Cliquets_EIA.m:47
        contractParams.C = copy(1.05)
# Script_Cliquets_EIA.m:48
        contractParams.F = copy(1.0)
# Script_Cliquets_EIA.m:49
    
    ############################################
### Step 2) CHOOSE MODEL PARAMETERS (Levy Models)
############################################
    model=1
# Script_Cliquets_EIA.m:55
    
    params=cellarray([])
# Script_Cliquets_EIA.m:56
    if model == 1:
        params.sigmaBSM = copy(0.15)
# Script_Cliquets_EIA.m:59
    else:
        if model == 2:
            params.C = copy(0.02)
# Script_Cliquets_EIA.m:62
            params.G = copy(5)
# Script_Cliquets_EIA.m:63
            params.MM = copy(15)
# Script_Cliquets_EIA.m:64
            params.Y = copy(1.2)
# Script_Cliquets_EIA.m:65
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_Cliquets_EIA.m:68
                params.beta = copy(- 5)
# Script_Cliquets_EIA.m:69
                params.delta = copy(0.5)
# Script_Cliquets_EIA.m:70
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_Cliquets_EIA.m:73
                    params.lam = copy(0.4)
# Script_Cliquets_EIA.m:74
                    params.muj = copy(- 0.12)
# Script_Cliquets_EIA.m:75
                    params.sigmaj = copy(0.18)
# Script_Cliquets_EIA.m:76
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_Cliquets_EIA.m:79
                        params.lam = copy(3)
# Script_Cliquets_EIA.m:80
                        params.p_up = copy(0.2)
# Script_Cliquets_EIA.m:81
                        params.eta1 = copy(25)
# Script_Cliquets_EIA.m:82
                        params.eta2 = copy(10)
# Script_Cliquets_EIA.m:83
    
    ############################################
### Step 3) CHOOSE PROJ PARAMETERS
############################################
    UseCumulant=1
# Script_Cliquets_EIA.m:90
    
    #---------------------
# APPROACH 1: Cumulant Based approach for grid width
# (see "Robust Option Pricing with Characteritics Functions and the BSpline Order of Density Projection")
#---------------------
    if UseCumulant == 1:
        logN=11
# Script_Cliquets_EIA.m:97
        L1=12
# Script_Cliquets_EIA.m:98
        #---------------------
# APPROACH 2: Manual GridWidth approach 
#---------------------
    else:
        P=7
# Script_Cliquets_EIA.m:103
        Pbar=3
# Script_Cliquets_EIA.m:104
    
    ############################################
### PRICE
############################################
###  Note: rnCHF is the risk netural CHF, c1,c2,c4 are the cumulants
    modelInput=getModelInput(model,T / M,r,q,params)
# Script_Cliquets_EIA.m:111
    if UseCumulant == 1:
        alpha=getTruncationAlpha(T,L1,modelInput,model)
# Script_Cliquets_EIA.m:114
    else:
        logN=P + Pbar
# Script_Cliquets_EIA.m:116
        alpha=2 ** Pbar / 2
# Script_Cliquets_EIA.m:117
    
    N=2 ** logN
# Script_Cliquets_EIA.m:119
    tic
    if contract == 6:
        price=PROJ_MultiplicativeCliquet(N,alpha,M,r,T,modelInput.rnCHF,contract,contractParams)
# Script_Cliquets_EIA.m:123
    else:
        price=PROJ_Cliquet(N,alpha,M,r,q,T,modelInput.rnCHF,contract,contractParams)
# Script_Cliquets_EIA.m:125
    
    toc
    fprintf('price: %.8f\n',price)