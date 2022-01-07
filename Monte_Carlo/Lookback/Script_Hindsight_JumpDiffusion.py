# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_Hindsight_JumpDiffusion.m

    ##################################################################
### MONTE CARLO HINDSIGHT OPTION PRICER for Diffusions AND Jump Diffusions
##################################################################
# Descritpion: Script to Price Hinsight options in Diffusion and Jump Diffusion Models
#              using the Monte Carlo Simulation
# Author:      Justin Kirkby
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_Hindsight_JumpDiffusion.m:9
    cd(folder)
    addpath('../')
    # ---------------------
#  Contract/Market Params
# ---------------------
    call=1
# Script_Hindsight_JumpDiffusion.m:17
    
    S_0=100
# Script_Hindsight_JumpDiffusion.m:18
    
    M=252
# Script_Hindsight_JumpDiffusion.m:19
    
    r=0.05
# Script_Hindsight_JumpDiffusion.m:20
    
    q=0.0
# Script_Hindsight_JumpDiffusion.m:21
    
    T=1
# Script_Hindsight_JumpDiffusion.m:22
    
    Kvec=dot(S_0,concat([0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.5,1.6]))
# Script_Hindsight_JumpDiffusion.m:24
    
    # ---------------------
# Model Params
# ---------------------
    sigma=0.2
# Script_Hindsight_JumpDiffusion.m:30
    
    jumpModel=0
# Script_Hindsight_JumpDiffusion.m:31
    
    # ---------------------
# Sim Params
# ---------------------
    N_sim=10 ** 4
# Script_Hindsight_JumpDiffusion.m:36
    
    mult=2
# Script_Hindsight_JumpDiffusion.m:37
    
    #################################
    
    jumpParams=cellarray([])
# Script_Hindsight_JumpDiffusion.m:40
    if jumpModel == 1:
        lambda_=1
# Script_Hindsight_JumpDiffusion.m:43
        muJ=- 0.1
# Script_Hindsight_JumpDiffusion.m:43
        sigJ=0.3
# Script_Hindsight_JumpDiffusion.m:43
        jumpParams.kappa = copy(exp(muJ + dot(0.5,sigJ ** 2)) - 1)
# Script_Hindsight_JumpDiffusion.m:45
        jumpParams.lambda = copy(lambda_)
# Script_Hindsight_JumpDiffusion.m:45
        jumpParams.muJ = copy(muJ)
# Script_Hindsight_JumpDiffusion.m:45
        jumpParams.sigJ = copy(sigJ)
# Script_Hindsight_JumpDiffusion.m:45
    else:
        if jumpModel == 2:
            lambda_=1
# Script_Hindsight_JumpDiffusion.m:48
            p_up=0.5
# Script_Hindsight_JumpDiffusion.m:49
            eta1=25
# Script_Hindsight_JumpDiffusion.m:50
            eta2=30
# Script_Hindsight_JumpDiffusion.m:51
            kappa=dot(p_up,eta1) / (eta1 - 1) + dot((1 - p_up),eta2) / (eta2 + 1) - 1
# Script_Hindsight_JumpDiffusion.m:53
            jumpParams.lambda = copy(lambda_)
# Script_Hindsight_JumpDiffusion.m:54
            jumpParams.kappa = copy(kappa)
# Script_Hindsight_JumpDiffusion.m:54
            jumpParams.eta1 = copy(eta1)
# Script_Hindsight_JumpDiffusion.m:54
            jumpParams.eta2 = copy(eta2)
# Script_Hindsight_JumpDiffusion.m:54
            jumpParams.p_up = copy(p_up)
# Script_Hindsight_JumpDiffusion.m:54
        else:
            if jumpModel == 3:
                lambda_=1
# Script_Hindsight_JumpDiffusion.m:57
                a1=- 0.05
# Script_Hindsight_JumpDiffusion.m:58
                b1=0.07
# Script_Hindsight_JumpDiffusion.m:59
                a2=0.02
# Script_Hindsight_JumpDiffusion.m:60
                b2=0.03
# Script_Hindsight_JumpDiffusion.m:61
                p_up=0.6
# Script_Hindsight_JumpDiffusion.m:62
                kappa=dot(p_up,exp(a1 + dot(0.5,b1 ** 2))) + dot((1 - p_up),exp(a2 + dot(0.5,b2 ** 2))) - 1
# Script_Hindsight_JumpDiffusion.m:64
                jumpParams.lambda = copy(lambda_)
# Script_Hindsight_JumpDiffusion.m:65
                jumpParams.kappa = copy(kappa)
# Script_Hindsight_JumpDiffusion.m:65
                jumpParams.a1 = copy(a1)
# Script_Hindsight_JumpDiffusion.m:65
                jumpParams.b1 = copy(b1)
# Script_Hindsight_JumpDiffusion.m:65
                jumpParams.a2 = copy(a2)
# Script_Hindsight_JumpDiffusion.m:65
                jumpParams.b2 = copy(b2)
# Script_Hindsight_JumpDiffusion.m:65
                jumpParams.p_up = copy(p_up)
# Script_Hindsight_JumpDiffusion.m:65
    
    ################################################
    
    M_mult=dot(M,mult)
# Script_Hindsight_JumpDiffusion.m:70
    
    Spath=Simulate_Jump_Diffusion_func(N_sim,M_mult + 1,T,S_0,r,q,sigma,jumpModel,jumpParams)
# Script_Hindsight_JumpDiffusion.m:71
    disc=exp(dot(- r,T))
# Script_Hindsight_JumpDiffusion.m:73
    prices,stdErrs=Price_MC_Hindsight_Strikes_func(Spath,call,Kvec,M,mult,disc,nargout=2)
# Script_Hindsight_JumpDiffusion.m:74
    # Plot
    plot(Kvec,prices)
    ylabel('price')
    xlabel('strike')
    grid('on')