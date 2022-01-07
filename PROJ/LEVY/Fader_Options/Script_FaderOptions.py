# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_FaderOptions.m

    ##################################################################
### FADER OPTION PRICER
##################################################################
# Descritpion: Script to Price Fader (Soft) Barrier options in Levy Models
#              using the PROJ method. 
# Fade-In Payoff is (1 - R)*(S_T - W)^+ for a call, where R is the proportion of time spent in knock-out region
#   (Note: Fade out can be priced by parity, (Fade-in + Fade-out = Vanilla), so Price(Fade-out) = Price(Vanilla) - Price(Fade-in)
# Author:      Justin Kirkby
# References:   
#              (1) Robust Barrier Option Pricing by Frame Projection under
#              Exponential Levy Dynamics, App. Math. Finance, 2017
#              (2) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
#              (3) Step Options, (Linetsky, V.), Math. Finance 1999.
##################################################################
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_FaderOptions.m:16
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    addpath('../Step_Options')
    ##############################################
###  Step 1): CONTRACT/GENERAL PARAMETERS
##############################################
    S_0=100
# Script_FaderOptions.m:25
    
    W=100
# Script_FaderOptions.m:26
    
    r=0.05
# Script_FaderOptions.m:27
    
    q=0.0
# Script_FaderOptions.m:28
    
    T=1
# Script_FaderOptions.m:29
    
    call=0
# Script_FaderOptions.m:30
    
    down=1
# Script_FaderOptions.m:31
    
    H=90
# Script_FaderOptions.m:32
    
    M=52
# Script_FaderOptions.m:33
    
    ##############################################
###  Step 2): CHOOSE MODEL PARAMETERS (Levy Models)
##############################################
    model=1
# Script_FaderOptions.m:39
    
    params=cellarray([])
# Script_FaderOptions.m:40
    if model == 1:
        params.sigmaBSM = copy(0.18)
# Script_FaderOptions.m:43
    else:
        if model == 2:
            params.C = copy(0.02)
# Script_FaderOptions.m:46
            params.G = copy(5)
# Script_FaderOptions.m:47
            params.MM = copy(15)
# Script_FaderOptions.m:48
            params.Y = copy(1.2)
# Script_FaderOptions.m:49
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_FaderOptions.m:52
                params.beta = copy(- 5)
# Script_FaderOptions.m:53
                params.delta = copy(0.5)
# Script_FaderOptions.m:54
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_FaderOptions.m:57
                    params.lam = copy(0.4)
# Script_FaderOptions.m:58
                    params.muj = copy(- 0.12)
# Script_FaderOptions.m:59
                    params.sigmaj = copy(0.18)
# Script_FaderOptions.m:60
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_FaderOptions.m:63
                        params.lam = copy(3)
# Script_FaderOptions.m:64
                        params.p_up = copy(0.2)
# Script_FaderOptions.m:65
                        params.eta1 = copy(25)
# Script_FaderOptions.m:66
                        params.eta2 = copy(10)
# Script_FaderOptions.m:67
    
    ##############################################
###  Step 3) CHOOSE PROJ PARAMETERS
##############################################
    logN=10
# Script_FaderOptions.m:73
    
    L1=10
# Script_FaderOptions.m:74
    
    # For Automated Parameter adjustment
    alphMult=1.1
# Script_FaderOptions.m:77
    TOLProb=5e-08
# Script_FaderOptions.m:78
    TOLMean=1e-05
# Script_FaderOptions.m:79
    ##############################################
### PRICE
##############################################
###  Note: rnCHF is the risk netural CHF, c1,c2,c4 are the cumulants
    modelInput=getModelInput(model,T / M,r,0,params)
# Script_FaderOptions.m:85
    N=2 ** logN
# Script_FaderOptions.m:86
    
    c1=modelInput.c1
# Script_FaderOptions.m:88
    c2=modelInput.c2
# Script_FaderOptions.m:88
    c4=modelInput.c4
# Script_FaderOptions.m:88
    rnCHF=modelInput.rnCHF
# Script_FaderOptions.m:88
    rnCHF_T=modelInput.rnCHF_T
# Script_FaderOptions.m:88
    if (down == 1 and call != 1) or (down != 1 and call == 1):
        tic
        price=PROJ_StepOption_AutoParam(N,- 1,call,down,S_0,W,H,M,r,q,rnCHF,T,L1,c2,c4,alphMult,TOLProb,TOLMean,rnCHF_T)
# Script_FaderOptions.m:93
        fprintf('PRICE: %.8f \n',price)
        toc
    else:
        fprintf('Sorry, currently only Up and out calls, and down and out puts have been coded \n')
    