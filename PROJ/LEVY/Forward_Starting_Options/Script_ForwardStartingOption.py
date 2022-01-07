# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_ForwardStartingOption.m

    ##################################################################
### FORWARD STARTING OPTION PRICER (RUN SCRIPT)
##################################################################
# Descritpion: Script to Price Forward Starting options in Levy/Heston Models
#              using the PROJ method
# Author:      Justin Kirkby
# References:  (1) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
#              (2) Robust Option Pricing with Characteristic Functions and
#              the B-Spline Order of density Projection, JCF, 2017
##################################################################
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_ForwardStartingOption.m:12
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    ##################################################
###  Step 1) CHOOSE CONTRACT/GENERAL PARAMETERS
##################################################
    call=1
# Script_ForwardStartingOption.m:20
    
    S_0=100
# Script_ForwardStartingOption.m:21
    
    r=0.05
# Script_ForwardStartingOption.m:22
    
    q=0.0
# Script_ForwardStartingOption.m:23
    
    T=1
# Script_ForwardStartingOption.m:24
    
    T1=0.25
# Script_ForwardStartingOption.m:25
    
    ##################################################
###  Step 2) CHOOSE MODEL PARAMETERS (Levy Models)
##################################################
    model=1
# Script_ForwardStartingOption.m:30
    
    params=cellarray([])
# Script_ForwardStartingOption.m:31
    if model == 1:
        params.sigmaBSM = copy(0.15)
# Script_ForwardStartingOption.m:34
    else:
        if model == 2:
            params.C = copy(0.02)
# Script_ForwardStartingOption.m:37
            params.G = copy(5)
# Script_ForwardStartingOption.m:38
            params.MM = copy(15)
# Script_ForwardStartingOption.m:39
            params.Y = copy(1.2)
# Script_ForwardStartingOption.m:40
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_ForwardStartingOption.m:43
                params.beta = copy(- 5)
# Script_ForwardStartingOption.m:44
                params.delta = copy(0.5)
# Script_ForwardStartingOption.m:45
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_ForwardStartingOption.m:48
                    params.lam = copy(0.4)
# Script_ForwardStartingOption.m:49
                    params.muj = copy(- 0.12)
# Script_ForwardStartingOption.m:50
                    params.sigmaj = copy(0.18)
# Script_ForwardStartingOption.m:51
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_ForwardStartingOption.m:54
                        params.lam = copy(3)
# Script_ForwardStartingOption.m:55
                        params.p_up = copy(0.2)
# Script_ForwardStartingOption.m:56
                        params.eta1 = copy(25)
# Script_ForwardStartingOption.m:57
                        params.eta2 = copy(10)
# Script_ForwardStartingOption.m:58
    
    ##################################################
### Step 3) CHOOSE PROJ PARAMETERS
##################################################
    UseCumulant=1
# Script_ForwardStartingOption.m:64
    
    #---------------------
# APPROACH 1: Cumulant Based approach for grid width
# (see "Robust Option Pricing with Characteritics Functions and the BSpline Order of Density Projection")
#---------------------
    if UseCumulant == 1:
        logN=14
# Script_ForwardStartingOption.m:71
        L1=12
# Script_ForwardStartingOption.m:72
        #---------------------
# APPROACH 2: Manual GridWidth approach 
#---------------------
    else:
        P=7
# Script_ForwardStartingOption.m:77
        Pbar=3
# Script_ForwardStartingOption.m:78
    
    ##################################################
### PRICE
##################################################
    
    T2=T - T1
# Script_ForwardStartingOption.m:85
    
    ###  Note: rnCHF is the risk netural CHF, c1,c2,c4 are the cumulants
    modelInput1=getModelInput(model,T1,r,q,params)
# Script_ForwardStartingOption.m:88
    modelInput2=getModelInput(model,T2,r,q,params)
# Script_ForwardStartingOption.m:89
    if UseCumulant == 1:
        alpha=getTruncationAlpha(T,L1,modelInput1,model)
# Script_ForwardStartingOption.m:92
    else:
        logN=P + Pbar
# Script_ForwardStartingOption.m:94
        alpha=2 ** Pbar / 2
# Script_ForwardStartingOption.m:95
    
    N=2 ** logN
# Script_ForwardStartingOption.m:97
    
    tic
    price=PROJ_ForwardStarting(N,alpha,r,q,T1,T2,S_0,call,modelInput1.rnCHF,modelInput2.rnCHF)
# Script_ForwardStartingOption.m:100
    toc
    fprintf('%.8f \n',price)