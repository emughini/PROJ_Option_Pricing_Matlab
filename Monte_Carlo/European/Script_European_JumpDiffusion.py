# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_European_JumpDiffusion.m

    ##################################################################
### MONTE CARLO EUROPEAN OPTION PRICER for Jump Diffusions
##################################################################
# Descritpion: Script to Price European options in Difusion/Jump Diffusion Models
#              using the Monte Carlo Simulation
# Author:      Justin Kirkby
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_European_JumpDiffusion.m:9
    cd(folder)
    addpath('../')
    # ---------------------
#  Contract/Market Params
# ---------------------
    call=1
# Script_European_JumpDiffusion.m:17
    
    S_0=100
# Script_European_JumpDiffusion.m:18
    
    r=0.05
# Script_European_JumpDiffusion.m:19
    
    q=0.0
# Script_European_JumpDiffusion.m:20
    
    T=1
# Script_European_JumpDiffusion.m:21
    
    Kvec=dot(S_0,concat([0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.5,1.6]))
# Script_European_JumpDiffusion.m:22
    
    # ---------------------
# Model Params
# ---------------------
    sigma=0.2
# Script_European_JumpDiffusion.m:27
    
    jumpModel=0
# Script_European_JumpDiffusion.m:28
    
    # ---------------------
# Sim Params
# ---------------------
    N_sim=10 ** 4
# Script_European_JumpDiffusion.m:33
    M=500
# Script_European_JumpDiffusion.m:34
    #################################
    
    jumpParams=cellarray([])
# Script_European_JumpDiffusion.m:37
    if jumpModel == 1:
        lambda_=1
# Script_European_JumpDiffusion.m:40
        muJ=- 0.1
# Script_European_JumpDiffusion.m:40
        sigJ=0.3
# Script_European_JumpDiffusion.m:40
        jumpParams.kappa = copy(exp(muJ + dot(0.5,sigJ ** 2)) - 1)
# Script_European_JumpDiffusion.m:42
        jumpParams.lambda = copy(lambda_)
# Script_European_JumpDiffusion.m:42
        jumpParams.muJ = copy(muJ)
# Script_European_JumpDiffusion.m:42
        jumpParams.sigJ = copy(sigJ)
# Script_European_JumpDiffusion.m:42
    else:
        if jumpModel == 2:
            lambda_=1
# Script_European_JumpDiffusion.m:45
            p_up=0.5
# Script_European_JumpDiffusion.m:46
            eta1=25
# Script_European_JumpDiffusion.m:47
            eta2=30
# Script_European_JumpDiffusion.m:48
            kappa=dot(p_up,eta1) / (eta1 - 1) + dot((1 - p_up),eta2) / (eta2 + 1) - 1
# Script_European_JumpDiffusion.m:50
            jumpParams.lambda = copy(lambda_)
# Script_European_JumpDiffusion.m:51
            jumpParams.kappa = copy(kappa)
# Script_European_JumpDiffusion.m:51
            jumpParams.eta1 = copy(eta1)
# Script_European_JumpDiffusion.m:51
            jumpParams.eta2 = copy(eta2)
# Script_European_JumpDiffusion.m:51
            jumpParams.p_up = copy(p_up)
# Script_European_JumpDiffusion.m:51
        else:
            if jumpModel == 3:
                lambda_=1
# Script_European_JumpDiffusion.m:54
                a1=- 0.05
# Script_European_JumpDiffusion.m:55
                b1=0.07
# Script_European_JumpDiffusion.m:56
                a2=0.02
# Script_European_JumpDiffusion.m:57
                b2=0.03
# Script_European_JumpDiffusion.m:58
                p_up=0.6
# Script_European_JumpDiffusion.m:59
                kappa=dot(p_up,exp(a1 + dot(0.5,b1 ** 2))) + dot((1 - p_up),exp(a2 + dot(0.5,b2 ** 2))) - 1
# Script_European_JumpDiffusion.m:61
                jumpParams.lambda = copy(lambda_)
# Script_European_JumpDiffusion.m:62
                jumpParams.kappa = copy(kappa)
# Script_European_JumpDiffusion.m:62
                jumpParams.a1 = copy(a1)
# Script_European_JumpDiffusion.m:62
                jumpParams.b1 = copy(b1)
# Script_European_JumpDiffusion.m:62
                jumpParams.a2 = copy(a2)
# Script_European_JumpDiffusion.m:62
                jumpParams.b2 = copy(b2)
# Script_European_JumpDiffusion.m:62
                jumpParams.p_up = copy(p_up)
# Script_European_JumpDiffusion.m:62
    
    ################################################
    
    Spath=Simulate_Jump_Diffusion_func(N_sim,M,T,S_0,r,q,sigma,jumpModel,jumpParams)
# Script_European_JumpDiffusion.m:67
    histogram(Spath(arange(),end()))
    disc=exp(dot(- r,T))
# Script_European_JumpDiffusion.m:70
    prices,stdErrs=Price_MC_European_Strikes_func(Spath,disc,call,Kvec,nargout=2)
# Script_European_JumpDiffusion.m:71
    # Plot
    plot(Kvec,prices)
    ylabel('price')
    xlabel('strike')
    grid('on')