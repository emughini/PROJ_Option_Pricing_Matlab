# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_EuropeanOptions.m

    ##################################################################
### EUROPEAN OPTION PRICER (RUN SCRIPT)
##################################################################
# Descritpion: Script to Price European options in Regime Switching Diffusion Models
#              using the PROJ method
# Author:      Justin Kirkby
# References:  (1) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
#              (2) A unified approach to Bermudan and Barrier options under stochastic
#               volatility models with jumps. J. Economic Dynamics and Control, 2017
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_EuropeanOptions.m:13
    cd(folder)
    addpath('../')
    ##############################################
###  Step 1) CHOOSE CONTRACT/GENERAL PARAMETERS
##############################################
    call=1
# Script_EuropeanOptions.m:20
    
    S_0=100
# Script_EuropeanOptions.m:21
    
    W=100
# Script_EuropeanOptions.m:22
    
    r=0.05
# Script_EuropeanOptions.m:23
    
    q=0.0
# Script_EuropeanOptions.m:24
    
    T=1
# Script_EuropeanOptions.m:25
    
    ##############################################
###  Step 2) CHOOSE MODEL PARAMETERS 
##############################################
    
    # Transition Matrix (dictates how the regimes transition)
    Q=concat([[- 1,0.5,0.5],[0.5,- 1,0.5],[0.5,0.5,- 1]])
# Script_EuropeanOptions.m:32
    sigma_vec=concat([0.15,0.25,0.35])
# Script_EuropeanOptions.m:36
    
    initial_state=1
# Script_EuropeanOptions.m:38
    ##############################################
###  Step 3) CHOOSE PROJ PARAMETERS
##############################################
    order=3
# Script_EuropeanOptions.m:43
    
    logN=8
# Script_EuropeanOptions.m:44
    
    L1=8
# Script_EuropeanOptions.m:45
    
    ##############################################
### PRICE
##############################################
    alpha=dot(dot(L1,sqrt(T)),max(sigma_vec))
# Script_EuropeanOptions.m:50
    
    N=2 ** logN
# Script_EuropeanOptions.m:51
    
    tic
    price=PROJ_RegimeSwitching_European(order,N,alpha,r,q,T,S_0,W,call,Q,sigma_vec,initial_state)
# Script_EuropeanOptions.m:54
    toc
    fprintf('%.8f \n',price)