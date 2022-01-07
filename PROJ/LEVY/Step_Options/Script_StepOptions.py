# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_StepOptions.m

    ##################################################################
### STEP OPTION PRICER
##################################################################
# Descritpion: Script to Price Step (Soft) Barrier options in Levy Models
#              using the PROJ method
# Payoff is exp(-stepRho*R)*(S_T - W)^+ for a call, where R is the proportion of time spent in knock-out region
    
    #   NOTE: Similar contract is Fader option, (1 - R)*(S_T - W)^+ ... see Fader Option Script
    
    # Author:      Justin Kirkby
# References:   
#              (1) Robust Barrier Option Pricing by Frame Projection under
#              Exponential Levy Dynamics, App. Math. Finance, 2017
#              (2) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
#              (3) Step Options, (Linetsky, V.), Math. Finance 1999.
##################################################################
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_StepOptions.m:18
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    ##############################################
###  Step 1): CONTRACT/GENERAL PARAMETERS
##############################################
    S_0=100
# Script_StepOptions.m:27
    
    W=100
# Script_StepOptions.m:28
    
    r=0.05
# Script_StepOptions.m:29
    
    q=0.0
# Script_StepOptions.m:30
    
    T=1
# Script_StepOptions.m:31
    
    call=0
# Script_StepOptions.m:32
    
    down=1
# Script_StepOptions.m:33
    
    H=90
# Script_StepOptions.m:34
    
    M=52
# Script_StepOptions.m:35
    
    stepRho=20
# Script_StepOptions.m:37
    ##############################################
###  Step 2): CHOOSE MODEL PARAMETERS (Levy Models)
##############################################
    model=1
# Script_StepOptions.m:42
    
    params=cellarray([])
# Script_StepOptions.m:43
    if model == 1:
        params.sigmaBSM = copy(0.18)
# Script_StepOptions.m:46
    else:
        if model == 2:
            params.C = copy(0.02)
# Script_StepOptions.m:49
            params.G = copy(5)
# Script_StepOptions.m:50
            params.MM = copy(15)
# Script_StepOptions.m:51
            params.Y = copy(1.2)
# Script_StepOptions.m:52
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_StepOptions.m:55
                params.beta = copy(- 5)
# Script_StepOptions.m:56
                params.delta = copy(0.5)
# Script_StepOptions.m:57
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_StepOptions.m:60
                    params.lam = copy(0.4)
# Script_StepOptions.m:61
                    params.muj = copy(- 0.12)
# Script_StepOptions.m:62
                    params.sigmaj = copy(0.18)
# Script_StepOptions.m:63
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_StepOptions.m:66
                        params.lam = copy(3)
# Script_StepOptions.m:67
                        params.p_up = copy(0.2)
# Script_StepOptions.m:68
                        params.eta1 = copy(25)
# Script_StepOptions.m:69
                        params.eta2 = copy(10)
# Script_StepOptions.m:70
    
    ##############################################
###  Step 3) CHOOSE PROJ PARAMETERS
##############################################
    logN=10
# Script_StepOptions.m:76
    
    L1=10
# Script_StepOptions.m:77
    
    # For Automated Parameter adjustment
    alphMult=1.1
# Script_StepOptions.m:80
    TOLProb=5e-08
# Script_StepOptions.m:81
    TOLMean=1e-05
# Script_StepOptions.m:82
    ##############################################
### PRICE
##############################################
###  Note: rnCHF is the risk netural CHF, c1,c2,c4 are the cumulants
    modelInput=getModelInput(model,T / M,r,0,params)
# Script_StepOptions.m:88
    N=2 ** logN
# Script_StepOptions.m:89
    
    c1=modelInput.c1
# Script_StepOptions.m:91
    c2=modelInput.c2
# Script_StepOptions.m:91
    c4=modelInput.c4
# Script_StepOptions.m:91
    rnCHF=modelInput.rnCHF
# Script_StepOptions.m:91
    rnCHF_T=modelInput.rnCHF_T
# Script_StepOptions.m:91
    if (down == 1 and call != 1) or (down != 1 and call == 1):
        tic
        price=PROJ_StepOption_AutoParam(N,stepRho,call,down,S_0,W,H,M,r,q,rnCHF,T,L1,c2,c4,alphMult,TOLProb,TOLMean,rnCHF_T)
# Script_StepOptions.m:96
        fprintf('PRICE: %.8f \n',price)
        toc
    else:
        fprintf('Sorry, currently only Up and out calls, and down and out puts have been coded \n')
    