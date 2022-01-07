# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_European_Barrier_American.m

    ##################################################################
### American/Bermudan Option Pricier for SABR
##################################################################
# Descritpion: Script to Price Bermudan Options in SABR Model using CTMC Method
# Author:      Justin Kirkby
# References:  (1) General Valuation Framework for SABR and Stochastic Local Volatility
#                   Models. SIAM J. Financial Mathematics, 2018.
# Disclaimer: this is research code, not production code. The parameter settings etc 
#            should not be expected to work as is in all cases. Determining the right parameter
#            settings will depend on your usecase. This is left up to the user. 
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_European_Barrier_American.m:13
    cd(folder)
    addpath('../Helper_Functions')
    ##################################################################
    
    # -----------------
# Contract/Market Params
# -----------------
    T=1
# Script_European_Barrier_American.m:22
    r=0.0
# Script_European_Barrier_American.m:23
    S_0=1.1
# Script_European_Barrier_American.m:24
    
    Kvec=dot(S_0,concat([0.6,0.8,0.9,0.95,1.0,1.05,1.1,1.2,1.4]))
# Script_European_Barrier_American.m:25
    call=0
# Script_European_Barrier_American.m:26
    
    M=100
# Script_European_Barrier_American.m:27
    
    contract_type=1
# Script_European_Barrier_American.m:29
    
    L=dot(0.6,S_0)
# Script_European_Barrier_American.m:30
    
    # -----------------
# Numerical Params
# -----------------
    CTMCParams.m_0 = copy(30)
# Script_European_Barrier_American.m:35
    CTMCParams.N = copy(90)
# Script_European_Barrier_American.m:36
    CTMCParams.gridMult_v = copy(0.5)
# Script_European_Barrier_American.m:37
    CTMCParams.gridMult_s = copy(0.05)
# Script_European_Barrier_American.m:38
    
    CTMCParams.gamma = copy(6)
# Script_European_Barrier_American.m:39
    
    # -----------------
# Model Params
# -----------------
    ModParams.beta = copy(0.6)
# Script_European_Barrier_American.m:44
    ModParams.alpha = copy(0.08)
# Script_European_Barrier_American.m:45
    ModParams.v0 = copy(0.2)
# Script_European_Barrier_American.m:46
    ModParams.rho = copy(0)
# Script_European_Barrier_American.m:47
    # ModParams.beta   = .6;
# ModParams.alpha  = 0.3;
# ModParams.v0     = 0.25;
# ModParams.rho    = -0.5;
    
    # ModParams.beta   = .7;
# ModParams.alpha  = 0.08;
# ModParams.v0     = 0.2;
# ModParams.rho    = 0;
    
    # ModParams.beta   = .3;
# ModParams.alpha  = 0.6;
# ModParams.v0     = 0.4;
# ModParams.rho    = 0;
    
    #################################################################
### PRICE
#################################################################
    tic
    prices=SABR_EurBarAmer_func(call,M,T,S_0,Kvec,r,CTMCParams,ModParams,contract_type,L)
# Script_European_Barrier_American.m:68
    toc
    fprintf('%.8f \n',prices)
    plot(Kvec / S_0,prices)
    ylabel('price','interpreter','latex')
    xlabel('moneyness, $K/S_0$','interpreter','latex')
    grid('on')