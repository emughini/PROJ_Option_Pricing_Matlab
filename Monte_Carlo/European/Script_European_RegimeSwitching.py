# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_European_RegimeSwitching.m

    ##################################################################
# Descritpion: Script to Price European options under Regime Switching Diffusion Models using Monte Carlo simulation
# Author:      Justin Kirkby
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_European_RegimeSwitching.m:6
    cd(folder)
    addpath('../')
    # ---------------------
#  Contract/Market Params
# ---------------------
    call=1
# Script_European_RegimeSwitching.m:14
    
    S_0=100
# Script_European_RegimeSwitching.m:15
    
    r=0.05
# Script_European_RegimeSwitching.m:16
    
    q=0.0
# Script_European_RegimeSwitching.m:17
    
    T=1
# Script_European_RegimeSwitching.m:18
    
    Kvec=dot(S_0,concat([0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.5,1.6]))
# Script_European_RegimeSwitching.m:19
    
    # ---------------------
# Regime Switching Diffusion Params
# ---------------------
# Transition Matrix (dictates how the regimes transition)
    Q=concat([[- 1,0.5,0.5],[0.5,- 1,0.5],[0.5,0.5,- 1]])
# Script_European_RegimeSwitching.m:25
    drift_vec=concat([r - q,r - q,r - q])
# Script_European_RegimeSwitching.m:29
    
    sigma_vec=concat([0.15,0.25,0.35])
# Script_European_RegimeSwitching.m:30
    
    initial_state=1
# Script_European_RegimeSwitching.m:32
    # ---------------------
# Sim Params
# ---------------------
    N_sim=dot(5,10 ** 5)
# Script_European_RegimeSwitching.m:37
    M=500
# Script_European_RegimeSwitching.m:38
    #################################
    
    method=2
# Script_European_RegimeSwitching.m:41
    
    tic
    if method == 1:
        Spath=Simulate_RegimeSwitching_Diffusion_func(N_sim,M,T,S_0,drift_vec,sigma_vec,Q,initial_state)
# Script_European_RegimeSwitching.m:45
    else:
        Spath=Simulate_RegimeSwitching_Diffusion_Unbiased(N_sim,T,S_0,drift_vec,sigma_vec,Q,initial_state)
# Script_European_RegimeSwitching.m:48
    
    time=copy(toc)
# Script_European_RegimeSwitching.m:50
    histogram(Spath)
    disc=exp(dot(- r,T))
# Script_European_RegimeSwitching.m:54
    prices,stdErrs=Price_MC_European_Strikes_func(Spath,disc,call,Kvec,nargout=2)
# Script_European_RegimeSwitching.m:55
    plot(Kvec,prices)
    ylabel('price')
    xlabel('strike')
    grid('on')