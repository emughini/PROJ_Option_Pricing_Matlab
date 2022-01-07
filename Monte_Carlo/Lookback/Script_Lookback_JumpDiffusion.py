# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_Lookback_JumpDiffusion.m

    ##################################################################
### MONTE CARLO LOOKBACK OPTION PRICER for Diffusions AND Jump Diffusions
##################################################################
# Descritpion: Script to Price Lookback options in Diffusion and Jump Diffusion Models
#              using the Monte Carlo Simulation
# Author:      Justin Kirkby
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_Lookback_JumpDiffusion.m:9
    cd(folder)
    addpath('../')
    # ---------------------
#  Contract/Market Params
# ---------------------
    call=1
# Script_Lookback_JumpDiffusion.m:17
    
    S_0=100
# Script_Lookback_JumpDiffusion.m:18
    
    M=252
# Script_Lookback_JumpDiffusion.m:19
    
    r=0.05
# Script_Lookback_JumpDiffusion.m:20
    
    q=0.0
# Script_Lookback_JumpDiffusion.m:21
    
    T=1
# Script_Lookback_JumpDiffusion.m:22
    
    # ---------------------
# Model Params
# ---------------------
    sigma=0.2
# Script_Lookback_JumpDiffusion.m:28
    
    jumpModel=0
# Script_Lookback_JumpDiffusion.m:29
    
    # ---------------------
# Sim Params
# ---------------------
    N_sim=10 ** 5
# Script_Lookback_JumpDiffusion.m:34
    
    mult=3
# Script_Lookback_JumpDiffusion.m:35
    
    #################################
    
    jumpParams=cellarray([])
# Script_Lookback_JumpDiffusion.m:38
    if jumpModel == 1:
        lambda_=1
# Script_Lookback_JumpDiffusion.m:41
        muJ=- 0.1
# Script_Lookback_JumpDiffusion.m:41
        sigJ=0.3
# Script_Lookback_JumpDiffusion.m:41
        jumpParams.kappa = copy(exp(muJ + dot(0.5,sigJ ** 2)) - 1)
# Script_Lookback_JumpDiffusion.m:43
        jumpParams.lambda = copy(lambda_)
# Script_Lookback_JumpDiffusion.m:43
        jumpParams.muJ = copy(muJ)
# Script_Lookback_JumpDiffusion.m:43
        jumpParams.sigJ = copy(sigJ)
# Script_Lookback_JumpDiffusion.m:43
    else:
        if jumpModel == 2:
            lambda_=1
# Script_Lookback_JumpDiffusion.m:46
            p_up=0.5
# Script_Lookback_JumpDiffusion.m:47
            eta1=25
# Script_Lookback_JumpDiffusion.m:48
            eta2=30
# Script_Lookback_JumpDiffusion.m:49
            kappa=dot(p_up,eta1) / (eta1 - 1) + dot((1 - p_up),eta2) / (eta2 + 1) - 1
# Script_Lookback_JumpDiffusion.m:51
            jumpParams.lambda = copy(lambda_)
# Script_Lookback_JumpDiffusion.m:52
            jumpParams.kappa = copy(kappa)
# Script_Lookback_JumpDiffusion.m:52
            jumpParams.eta1 = copy(eta1)
# Script_Lookback_JumpDiffusion.m:52
            jumpParams.eta2 = copy(eta2)
# Script_Lookback_JumpDiffusion.m:52
            jumpParams.p_up = copy(p_up)
# Script_Lookback_JumpDiffusion.m:52
        else:
            if jumpModel == 3:
                lambda_=1
# Script_Lookback_JumpDiffusion.m:55
                a1=- 0.05
# Script_Lookback_JumpDiffusion.m:56
                b1=0.07
# Script_Lookback_JumpDiffusion.m:57
                a2=0.02
# Script_Lookback_JumpDiffusion.m:58
                b2=0.03
# Script_Lookback_JumpDiffusion.m:59
                p_up=0.6
# Script_Lookback_JumpDiffusion.m:60
                kappa=dot(p_up,exp(a1 + dot(0.5,b1 ** 2))) + dot((1 - p_up),exp(a2 + dot(0.5,b2 ** 2))) - 1
# Script_Lookback_JumpDiffusion.m:62
                jumpParams.lambda = copy(lambda_)
# Script_Lookback_JumpDiffusion.m:63
                jumpParams.kappa = copy(kappa)
# Script_Lookback_JumpDiffusion.m:63
                jumpParams.a1 = copy(a1)
# Script_Lookback_JumpDiffusion.m:63
                jumpParams.b1 = copy(b1)
# Script_Lookback_JumpDiffusion.m:63
                jumpParams.a2 = copy(a2)
# Script_Lookback_JumpDiffusion.m:63
                jumpParams.b2 = copy(b2)
# Script_Lookback_JumpDiffusion.m:63
                jumpParams.p_up = copy(p_up)
# Script_Lookback_JumpDiffusion.m:63
    
    ################################################
    
    M_mult=dot(M,mult)
# Script_Lookback_JumpDiffusion.m:68
    
    Spath=Simulate_Jump_Diffusion_func(N_sim,M_mult + 1,T,S_0,r,q,sigma,jumpModel,jumpParams)
# Script_Lookback_JumpDiffusion.m:69
    disc=exp(dot(- r,T))
# Script_Lookback_JumpDiffusion.m:71
    price,stdErr=Price_MC_Lookback_func(Spath,call,M,mult,disc,nargout=2)
# Script_Lookback_JumpDiffusion.m:72