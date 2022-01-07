# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_ParisianOptions.m

    ##################################################################
### PARISIAN OPTION PRICER
##################################################################
# Descritpion: Script to Parisian Barrier options in Levy Models
#              using the PROJ method
# Author:      Justin Kirkby
# References:   
#              (1) Robust Barrier Option Pricing by Frame Projection under
#              Exponential Levy Dynamics, App. Math. Finance, 2017
#              (2) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
##################################################################
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_ParisianOptions.m:13
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    ##############################################
###  Step 1): CONTRACT/GENERAL PARAMETERS
##############################################
    S_0=100
# Script_ParisianOptions.m:22
    
    W=100
# Script_ParisianOptions.m:23
    
    r=0.05
# Script_ParisianOptions.m:24
    
    T=1
# Script_ParisianOptions.m:25
    
    call=0
# Script_ParisianOptions.m:26
    
    down=1
# Script_ParisianOptions.m:27
    
    H=80
# Script_ParisianOptions.m:28
    
    M=52
# Script_ParisianOptions.m:29
    
    # NOTE: currently only Up and Out Calls, and Down and Out Puts have been coded
    
    Gamm=5
# Script_ParisianOptions.m:33
    
    resetting=1
# Script_ParisianOptions.m:34
    
    # Note: resetting options reset once underlying reenters the "continuation region"
                # Cumulative Parisian options (resetting = 0) never forget how many times, and are less forgiving (hence cheaper)
    
    ##############################################
###  Step 2): CHOOSE MODEL PARAMETERS (Levy Models)
##############################################
    model=1
# Script_ParisianOptions.m:41
    
    params=cellarray([])
# Script_ParisianOptions.m:42
    if model == 1:
        params.sigmaBSM = copy(0.18)
# Script_ParisianOptions.m:45
    else:
        if model == 2:
            params.C = copy(0.02)
# Script_ParisianOptions.m:48
            params.G = copy(5)
# Script_ParisianOptions.m:49
            params.MM = copy(15)
# Script_ParisianOptions.m:50
            params.Y = copy(1.2)
# Script_ParisianOptions.m:51
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_ParisianOptions.m:54
                params.beta = copy(- 5)
# Script_ParisianOptions.m:55
                params.delta = copy(0.5)
# Script_ParisianOptions.m:56
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_ParisianOptions.m:59
                    params.lam = copy(0.4)
# Script_ParisianOptions.m:60
                    params.muj = copy(- 0.12)
# Script_ParisianOptions.m:61
                    params.sigmaj = copy(0.18)
# Script_ParisianOptions.m:62
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_ParisianOptions.m:65
                        params.lam = copy(3)
# Script_ParisianOptions.m:66
                        params.p_up = copy(0.2)
# Script_ParisianOptions.m:67
                        params.eta1 = copy(25)
# Script_ParisianOptions.m:68
                        params.eta2 = copy(10)
# Script_ParisianOptions.m:69
    
    ##############################################
###  Step 3) CHOOSE PROJ PARAMETERS
##############################################
    UseCumulant=1
# Script_ParisianOptions.m:75
    
    #---------------------
# APPROACH 1: Cumulant Based approach for grid width
# (see "Robust Option Pricing with Characteritics Functions and the BSpline Order of Density Projection")
#---------------------
    if UseCumulant == 1:
        logN=12
# Script_ParisianOptions.m:82
        L1=12
# Script_ParisianOptions.m:83
        #---------------------
# APPROACH 2: Manual GridWidth approach 
#---------------------
    else:
        P=8
# Script_ParisianOptions.m:88
        Pbar=3
# Script_ParisianOptions.m:89
    
    ##############################################
### PRICE
##############################################
###  Note: rnCHF is the risk netural CHF, c1,c2,c4 are the cumulants
    modelInput=getModelInput(model,T / M,r,0,params)
# Script_ParisianOptions.m:96
    if UseCumulant == 1:
        alpha=getTruncationAlpha(T,L1,modelInput,model)
# Script_ParisianOptions.m:99
    else:
        logN=P + Pbar
# Script_ParisianOptions.m:101
        alpha=2 ** Pbar / 2
# Script_ParisianOptions.m:102
    
    N=2 ** logN
# Script_ParisianOptions.m:104
    
    if (down == 1 and call != 1) or (down != 1 and call == 1):
        tic
        price=PROJ_Parisian(N,call,down,S_0,W,H,M,r,modelInput.rnCHF,T,Gamm,resetting,alpha)
# Script_ParisianOptions.m:108
        fprintf('%.8f \n',price)
        toc
    else:
        fprintf('Sorry, currently only Up and out calls, and down and out puts have been coded \n')
    