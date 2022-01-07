# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_TC_Levy_VarSwap.m

    ##################################################################
### Variance Swaps - Time Changed Heston Option Pricer (This example is a time-changed representation of Heston's model)
##################################################################
# Descritpion: Script to Price Discrete Variance Swap under Hestons Model
# Author:      Justin Kirkby
# References:  (1) A General Framework for tim changed Markov Processes and Applications
#              European J. Operational research, 2019
#              (2) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
##################################################################
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_TC_Levy_VarSwap.m:11
    cd(folder)
    addpath('../Helper_Functions')
    addpath('../../STOCHASTIC_VOL/DV_Swaps_Options/Analytical_Swaps')
    addpath('../../STOCHASTIC_VOL/Helper_Functions')
    # ==========================
# CTMC Params
# ==========================
    ParamsCtmc.varGridMult = copy(0.05)
# Script_TC_Levy_VarSwap.m:21
    ParamsCtmc.gamma = copy(6)
# Script_TC_Levy_VarSwap.m:22
    
    ParamsCtmc.Nx = copy(70)
# Script_TC_Levy_VarSwap.m:23
    
    n=0
# Script_TC_Levy_VarSwap.m:24
    
    # ==========================
# Contract/Market Params
    T=1
# Script_TC_Levy_VarSwap.m:28
    
    r=0.05
# Script_TC_Levy_VarSwap.m:29
    
    q=0.0
# Script_TC_Levy_VarSwap.m:30
    
    # ==========================
    
    # ############################
# #### Heston Example   # Y_t = W_t - t/2
    eta=3
# Script_TC_Levy_VarSwap.m:35
    theta=0.04
# Script_TC_Levy_VarSwap.m:36
    Sigmav=0.1
# Script_TC_Levy_VarSwap.m:37
    v0=0.04
# Script_TC_Levy_VarSwap.m:38
    rho=0.0
# Script_TC_Levy_VarSwap.m:39
    
    ###################################
    ParamsDiffus.model = copy(1)
# Script_TC_Levy_VarSwap.m:43
    ParamsDiffus.eta = copy(eta)
# Script_TC_Levy_VarSwap.m:44
    ParamsDiffus.rho = copy(rho)
# Script_TC_Levy_VarSwap.m:44
    ParamsDiffus.theta = copy(theta)
# Script_TC_Levy_VarSwap.m:44
    ParamsDiffus.Sigmav = copy(Sigmav)
# Script_TC_Levy_VarSwap.m:44
    ParamsDiffus.v0 = copy(v0)
# Script_TC_Levy_VarSwap.m:44
    hFunc=lambda u=None: u
# Script_TC_Levy_VarSwap.m:46
    
    levyExponent=lambda z=None: dot(dot(- 0.5,1j),z) - dot(0.5,z ** 2)
# Script_TC_Levy_VarSwap.m:47
    mvec=concat([12,52,252])
# Script_TC_Levy_VarSwap.m:49
    
    time_iter=20
# Script_TC_Levy_VarSwap.m:50
    for m in arange(1,length(mvec)).reshape(-1):
        M=mvec(m)
# Script_TC_Levy_VarSwap.m:53
        tic
        for i in arange(1,time_iter).reshape(-1):
            price=TC_Levy_VarianceSwap(r,q,T,M,levyExponent,hFunc,n,ParamsDiffus,ParamsCtmc)
# Script_TC_Levy_VarSwap.m:56
        time=toc / time_iter
# Script_TC_Levy_VarSwap.m:58
        ref,KcH=hestonfairstrike(r,v0,theta,eta,Sigmav,T,rho,M,nargout=2)
# Script_TC_Levy_VarSwap.m:61
        error=price - ref
# Script_TC_Levy_VarSwap.m:62
        fprintf('%.0f & %.8f & %.8f & %.1e & %.3f \n',m,ref,price,abs(error),time)
    