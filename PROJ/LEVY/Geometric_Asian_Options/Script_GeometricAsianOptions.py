# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_GeometricAsianOptions.m

    ##################################################################
### GEOMETRIC ASIAN OPTION PRICER  (RUN SCRIPT)
##################################################################
# Descritpion: Script to Price Geometric Asian options in Levy Models using the PROJ method
# Author:      Justin Kirkby
    
    # Reference:   (1) An Efficient Transform Method For Asian Option Pricing, SIAM J. Financial Math., 2016
#              (2) Efficient Option Pricing by Frame Duality with the Fast Fourier Transform. 
#                  SIAM J. Financial Math (2015), Kirkby, J.L
    
    #################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_GeometricAsianOptions.m:13
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    #################################
###  Step 1) CHOOSE CONTRACT/GENERAL PARAMETERS
#################################
    call=1
# Script_GeometricAsianOptions.m:22
    
    S_0=100
# Script_GeometricAsianOptions.m:23
    
    W=100
# Script_GeometricAsianOptions.m:24
    
    r=0.05
# Script_GeometricAsianOptions.m:25
    
    q=0.0
# Script_GeometricAsianOptions.m:26
    
    T=1
# Script_GeometricAsianOptions.m:27
    
    M=52
# Script_GeometricAsianOptions.m:28
    
    #################################
###  Step 2) CHOOSE MODEL PARAMETERS (Levy Models)
#################################
    model=1
# Script_GeometricAsianOptions.m:33
    
    params=cellarray([])
# Script_GeometricAsianOptions.m:34
    if model == 1:
        params.sigmaBSM = copy(0.15)
# Script_GeometricAsianOptions.m:37
    else:
        if model == 2:
            params.C = copy(0.02)
# Script_GeometricAsianOptions.m:40
            params.G = copy(5)
# Script_GeometricAsianOptions.m:41
            params.MM = copy(15)
# Script_GeometricAsianOptions.m:42
            params.Y = copy(1.2)
# Script_GeometricAsianOptions.m:43
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_GeometricAsianOptions.m:46
                params.beta = copy(- 5)
# Script_GeometricAsianOptions.m:47
                params.delta = copy(0.5)
# Script_GeometricAsianOptions.m:48
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_GeometricAsianOptions.m:51
                    params.lam = copy(0.4)
# Script_GeometricAsianOptions.m:52
                    params.muj = copy(- 0.12)
# Script_GeometricAsianOptions.m:53
                    params.sigmaj = copy(0.18)
# Script_GeometricAsianOptions.m:54
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_GeometricAsianOptions.m:57
                        params.lam = copy(3)
# Script_GeometricAsianOptions.m:58
                        params.p_up = copy(0.2)
# Script_GeometricAsianOptions.m:59
                        params.eta1 = copy(25)
# Script_GeometricAsianOptions.m:60
                        params.eta2 = copy(10)
# Script_GeometricAsianOptions.m:61
                    else:
                        if model == 8:
                            params.sigma = copy(0.2)
# Script_GeometricAsianOptions.m:64
                            params.nu = copy(0.85)
# Script_GeometricAsianOptions.m:65
                            params.theta = copy(0)
# Script_GeometricAsianOptions.m:66
    
    #################################
###  Step 3) CHOOSE PROJ PARAMETERS
#################################
    UseCumulant=1
# Script_GeometricAsianOptions.m:73
    
    #---------------------
# APPROACH 1: Cumulant Based approach for grid width
# (see "Robust Option Pricing with Characteritics Functions and the BSpline Order of Density Projection")
#---------------------
    if UseCumulant == 1:
        logN=8
# Script_GeometricAsianOptions.m:80
        L1=10
# Script_GeometricAsianOptions.m:81
        #---------------------
# APPROACH 2: Manual GridWidth approach 
#---------------------
    else:
        P=6
# Script_GeometricAsianOptions.m:86
        Pbar=3
# Script_GeometricAsianOptions.m:87
    
    #################################
### PRICE
#################################
###  Note: rnCHF is the risk netural CHF, c1,c2,c4 are the cumulants
    dt=T / M
# Script_GeometricAsianOptions.m:94
    modelInput=getModelInput(model,dt,r,q,params)
# Script_GeometricAsianOptions.m:95
    if UseCumulant == 1:
        alpha=getTruncationAlpha(T,L1,modelInput,model)
# Script_GeometricAsianOptions.m:98
    else:
        logN=P + Pbar
# Script_GeometricAsianOptions.m:100
        alpha=2 ** Pbar / 2
# Script_GeometricAsianOptions.m:101
    
    N=2 ** logN
# Script_GeometricAsianOptions.m:103
    
    tic
    price=PROJ_Geometric_Asian(N,alpha,S_0,M,W,call,T,r,q,modelInput.rnSYMB)
# Script_GeometricAsianOptions.m:106
    toc
    fprintf('Geometric Price: %.8f \n',price)
    compare_arithmetic=1
# Script_GeometricAsianOptions.m:112
    if compare_arithmetic:
        addpath('../Asian_Options')
        price_arith=PROJ_Asian(N,alpha,S_0,M,W,call,T,r,q,modelInput.rnCHF,dot(modelInput.RNmu,dt))
# Script_GeometricAsianOptions.m:116
        fprintf('Arithmetic Price: %.8f \n',price_arith)
    
    