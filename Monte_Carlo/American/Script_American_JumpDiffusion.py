# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_American_JumpDiffusion.m

    ##################################################################
### MONTE CARLO AMERICAN OPTION PRICER for Jump Diffusions
##################################################################
# Descritpion: Script to Price American options in Difusion/Jump Diffusion Models
#              using the Monte Carlo Simulation (Longstaff-Schwartz)
# Author:      Justin Kirkby
##################################################################
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_American_JumpDiffusion.m:8
    cd(folder)
    addpath('../')
    # ---------------------
#  Contract/Market Params
# ---------------------
    call=0
# Script_American_JumpDiffusion.m:15
    
    S_0=100
# Script_American_JumpDiffusion.m:16
    
    r=0.05
# Script_American_JumpDiffusion.m:17
    
    q=0.0
# Script_American_JumpDiffusion.m:18
    
    T=1
# Script_American_JumpDiffusion.m:19
    
    Kvec=dot(S_0,concat([0.9,0.95,1,1.05,1.1]))
# Script_American_JumpDiffusion.m:20
    
    # ---------------------
# Model Params
# ---------------------
    sigma=0.15
# Script_American_JumpDiffusion.m:25
    
    jumpModel=0
# Script_American_JumpDiffusion.m:26
    
    # ---------------------
# Sim Params
# ---------------------
    N_sim=dot(2,10 ** 4)
# Script_American_JumpDiffusion.m:31
    M=250
# Script_American_JumpDiffusion.m:32
    #################################
    
    jumpParams=cellarray([])
# Script_American_JumpDiffusion.m:35
    if jumpModel == 1:
        lambda_=1
# Script_American_JumpDiffusion.m:38
        muJ=- 0.1
# Script_American_JumpDiffusion.m:38
        sigJ=0.3
# Script_American_JumpDiffusion.m:38
        jumpParams.kappa = copy(exp(muJ + dot(0.5,sigJ ** 2)) - 1)
# Script_American_JumpDiffusion.m:40
        jumpParams.lambda = copy(lambda_)
# Script_American_JumpDiffusion.m:40
        jumpParams.muJ = copy(muJ)
# Script_American_JumpDiffusion.m:40
        jumpParams.sigJ = copy(sigJ)
# Script_American_JumpDiffusion.m:40
    else:
        if jumpModel == 2:
            lambda_=1
# Script_American_JumpDiffusion.m:43
            p_up=0.5
# Script_American_JumpDiffusion.m:44
            eta1=25
# Script_American_JumpDiffusion.m:45
            eta2=30
# Script_American_JumpDiffusion.m:46
            kappa=dot(p_up,eta1) / (eta1 - 1) + dot((1 - p_up),eta2) / (eta2 + 1) - 1
# Script_American_JumpDiffusion.m:48
            jumpParams.lambda = copy(lambda_)
# Script_American_JumpDiffusion.m:49
            jumpParams.kappa = copy(kappa)
# Script_American_JumpDiffusion.m:49
            jumpParams.eta1 = copy(eta1)
# Script_American_JumpDiffusion.m:49
            jumpParams.eta2 = copy(eta2)
# Script_American_JumpDiffusion.m:49
            jumpParams.p_up = copy(p_up)
# Script_American_JumpDiffusion.m:49
        else:
            if jumpModel == 3:
                lambda_=1
# Script_American_JumpDiffusion.m:52
                a1=- 0.05
# Script_American_JumpDiffusion.m:53
                b1=0.07
# Script_American_JumpDiffusion.m:54
                a2=0.02
# Script_American_JumpDiffusion.m:55
                b2=0.03
# Script_American_JumpDiffusion.m:56
                p_up=0.6
# Script_American_JumpDiffusion.m:57
                kappa=dot(p_up,exp(a1 + dot(0.5,b1 ** 2))) + dot((1 - p_up),exp(a2 + dot(0.5,b2 ** 2))) - 1
# Script_American_JumpDiffusion.m:59
                jumpParams.lambda = copy(lambda_)
# Script_American_JumpDiffusion.m:60
                jumpParams.kappa = copy(kappa)
# Script_American_JumpDiffusion.m:60
                jumpParams.a1 = copy(a1)
# Script_American_JumpDiffusion.m:60
                jumpParams.b1 = copy(b1)
# Script_American_JumpDiffusion.m:60
                jumpParams.a2 = copy(a2)
# Script_American_JumpDiffusion.m:60
                jumpParams.b2 = copy(b2)
# Script_American_JumpDiffusion.m:60
                jumpParams.p_up = copy(p_up)
# Script_American_JumpDiffusion.m:60
    
    ################################################
    
    Spath=Simulate_Jump_Diffusion_func(N_sim,M,T,S_0,r,q,sigma,jumpModel,jumpParams)
# Script_American_JumpDiffusion.m:65
    dt=T / M
# Script_American_JumpDiffusion.m:67
    disc=exp(dot(- r,dt))
# Script_American_JumpDiffusion.m:67
    prices,stdErrs=Price_MC_American_Strikes_func(Spath,disc,call,Kvec,nargout=2)
# Script_American_JumpDiffusion.m:68
    # Plot
    plot(Kvec,prices)
    ylabel('price')
    xlabel('strike')
    grid('on')