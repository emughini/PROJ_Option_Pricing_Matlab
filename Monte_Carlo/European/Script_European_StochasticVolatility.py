# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_European_StochasticVolatility.m

    ##################################################################
# Descritpion: Script to Price European options under Stochastic Volatility Models (with Jumps) using Monte Carlo simulation
# Author:      Justin Kirkby
# For more details on these models see:
#          (1) A General Framework for discretely sampled realized
#              variance derivatives in stocahstic volatility models with
#              jumps, EJOR, 2017
#          (2) A unified approach to Bermudan and Barrier options under stochastic
#               volatility models with jumps. J. Economic Dynamics and Control, 2017
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_European_StochasticVolatility.m:12
    cd(folder)
    addpath('../')
    # ---------------------
#  Contract/Market Params
# ---------------------
    call=1
# Script_European_StochasticVolatility.m:20
    
    S_0=100
# Script_European_StochasticVolatility.m:21
    
    r=0.05
# Script_European_StochasticVolatility.m:22
    
    q=0.0
# Script_European_StochasticVolatility.m:23
    
    T=1
# Script_European_StochasticVolatility.m:24
    
    Kvec=dot(S_0,concat([0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.5,1.6]))
# Script_European_StochasticVolatility.m:25
    
    ###========================
#### Select Stochastic Volatility Model
###========================
    model=1
# Script_European_StochasticVolatility.m:30
    
    # 2 = Stein-Stein
              # 3 = 3/2 Model
              # 4 = 4/2 Model
              # 5 = Hull White (output compares with analytical)
              # 6 = Scott
              # 7 = Alpha-Hypergeometric
    
    ###========================
#### Select Jump Model
###========================
    jumpModel=0
# Script_European_StochasticVolatility.m:41
    
    # 1 = Normal Jumps
                  # 2 = Double Exponential Jumps
                  # 3 = Mixed normal Jumps
    
    # ---------------------
# Sim Params
# ---------------------
    N_sim=10 ** 4
# Script_European_StochasticVolatility.m:49
    M=500
# Script_European_StochasticVolatility.m:50
    #################################
    
    jumpParams=cellarray([])
# Script_European_StochasticVolatility.m:54
    if jumpModel == 1:
        lambda_=1
# Script_European_StochasticVolatility.m:57
        muJ=- 0.1
# Script_European_StochasticVolatility.m:58
        sigJ=0.3
# Script_European_StochasticVolatility.m:59
        jumpParams.kappa = copy(exp(muJ + dot(0.5,sigJ ** 2)) - 1)
# Script_European_StochasticVolatility.m:61
        jumpParams.lambda = copy(lambda_)
# Script_European_StochasticVolatility.m:61
        jumpParams.muJ = copy(muJ)
# Script_European_StochasticVolatility.m:61
        jumpParams.sigJ = copy(sigJ)
# Script_European_StochasticVolatility.m:61
    else:
        if jumpModel == 2:
            lambda_=1
# Script_European_StochasticVolatility.m:64
            p_up=0.5
# Script_European_StochasticVolatility.m:65
            eta1=25
# Script_European_StochasticVolatility.m:66
            eta2=30
# Script_European_StochasticVolatility.m:67
            kappa=dot(p_up,eta1) / (eta1 - 1) + dot((1 - p_up),eta2) / (eta2 + 1) - 1
# Script_European_StochasticVolatility.m:69
            jumpParams.lambda = copy(lambda_)
# Script_European_StochasticVolatility.m:70
            jumpParams.kappa = copy(kappa)
# Script_European_StochasticVolatility.m:70
            jumpParams.eta1 = copy(eta1)
# Script_European_StochasticVolatility.m:70
            jumpParams.eta2 = copy(eta2)
# Script_European_StochasticVolatility.m:70
            jumpParams.p_up = copy(p_up)
# Script_European_StochasticVolatility.m:70
        else:
            if jumpModel == 3:
                lambda_=1
# Script_European_StochasticVolatility.m:73
                a1=- 0.05
# Script_European_StochasticVolatility.m:74
                b1=0.07
# Script_European_StochasticVolatility.m:75
                a2=0.02
# Script_European_StochasticVolatility.m:76
                b2=0.03
# Script_European_StochasticVolatility.m:77
                p_up=0.6
# Script_European_StochasticVolatility.m:78
                kappa=dot(p_up,exp(a1 + dot(0.5,b1 ** 2))) + dot((1 - p_up),exp(a2 + dot(0.5,b2 ** 2))) - 1
# Script_European_StochasticVolatility.m:80
                jumpParams.lambda = copy(lambda_)
# Script_European_StochasticVolatility.m:81
                jumpParams.kappa = copy(kappa)
# Script_European_StochasticVolatility.m:81
                jumpParams.a1 = copy(a1)
# Script_European_StochasticVolatility.m:81
                jumpParams.b1 = copy(b1)
# Script_European_StochasticVolatility.m:81
                jumpParams.a2 = copy(a2)
# Script_European_StochasticVolatility.m:81
                jumpParams.b2 = copy(b2)
# Script_European_StochasticVolatility.m:81
                jumpParams.p_up = copy(p_up)
# Script_European_StochasticVolatility.m:81
    
    ################################################
####    Set the Stochastic Volatility Model Component
################################################
    if model == 1:
        ###==============================
    ### HESTON MODEL  Parameters
    ###==============================
        modparam.eta = copy(4)
# Script_European_StochasticVolatility.m:91
        modparam.theta = copy(0.035)
# Script_European_StochasticVolatility.m:92
        modparam.rho = copy(- 0.75)
# Script_European_StochasticVolatility.m:93
        modparam.Sigmav = copy(0.15)
# Script_European_StochasticVolatility.m:94
        modparam.v0 = copy(0.04)
# Script_European_StochasticVolatility.m:95
    else:
        if model == 2:
            ###=============================================================
    ### STEIN-STEIN MODEL  Parameters
    ###=============================================================
            modparam.eta = copy(2)
# Script_European_StochasticVolatility.m:101
            modparam.theta = copy(0.18)
# Script_European_StochasticVolatility.m:102
            modparam.Sigmav = copy(0.18)
# Script_European_StochasticVolatility.m:103
            modparam.v0 = copy(0.22)
# Script_European_StochasticVolatility.m:104
            modparam.rho = copy(- 0.5)
# Script_European_StochasticVolatility.m:105
        else:
            if model == 3:
                ###=============================================================
    ### 3/2 MODEL  Parameters
    ###=============================================================
                modparam.Sigmav = copy(0.1)
# Script_European_StochasticVolatility.m:111
                modparam.eta = copy(3)
# Script_European_StochasticVolatility.m:112
                modparam.rho = copy(- 0.7)
# Script_European_StochasticVolatility.m:113
                modparam.theta = copy(0.04)
# Script_European_StochasticVolatility.m:114
                modparam.v0 = copy(0.04)
# Script_European_StochasticVolatility.m:115
            else:
                if model == 4:
                    ###=============================================================
    ### 4/2 MODEL  Parameters
    ###=============================================================
                    modparam.eta = copy(3)
# Script_European_StochasticVolatility.m:121
                    modparam.theta = copy(0.04)
# Script_European_StochasticVolatility.m:122
                    modparam.rho = copy(- 0.7)
# Script_European_StochasticVolatility.m:123
                    modparam.Sigmav = copy(0.25)
# Script_European_StochasticVolatility.m:124
                    modparam.v0 = copy(0.04)
# Script_European_StochasticVolatility.m:125
                    modparam.aa = copy(0.5)
# Script_European_StochasticVolatility.m:126
                    modparam.bb = copy(dot(0.5,modparam.v0))
# Script_European_StochasticVolatility.m:127
                else:
                    if model == 5:
                        ###=============================================================
    ### HULL-WHITE MODEL  Parameters
    ###=============================================================
                        modparam.av = copy(0.05)
# Script_European_StochasticVolatility.m:133
                        modparam.rho = copy(- 0.6)
# Script_European_StochasticVolatility.m:134
                        modparam.Sigmav = copy(0.6)
# Script_European_StochasticVolatility.m:135
                        modparam.v0 = copy(0.03)
# Script_European_StochasticVolatility.m:136
                    else:
                        if model == 6:
                            ###=============================================================
    ### SCOTT MODEL  Parameters
    ###=============================================================
                            modparam.eta = copy(2)
# Script_European_StochasticVolatility.m:142
                            modparam.theta = copy(log(0.16))
# Script_European_StochasticVolatility.m:143
                            modparam.Sigmav = copy(0.2)
# Script_European_StochasticVolatility.m:144
                            modparam.v0 = copy(log(0.18))
# Script_European_StochasticVolatility.m:145
                            modparam.rho = copy(- 0.9)
# Script_European_StochasticVolatility.m:146
                        else:
                            if model == 7:
                                ###=============================================================
    ### ALPHA-HYPERGEOMETRIC MODEL  Parameters
    ###=============================================================
                                modparam.rho = copy(- 0.9)
# Script_European_StochasticVolatility.m:152
                                modparam.Sigmav = copy(0.2)
# Script_European_StochasticVolatility.m:153
                                modparam.v0 = copy(log(0.17))
# Script_European_StochasticVolatility.m:154
                                modparam.eta = copy(0.05)
# Script_European_StochasticVolatility.m:155
                                modparam.theta = copy(0.2)
# Script_European_StochasticVolatility.m:156
                                modparam.av = copy(0.03)
# Script_European_StochasticVolatility.m:157
    
    ###############################################
    
    Spath=Simulate_StochVol_Jumps_func(N_sim,M,T,S_0,r,q,model,modparam,jumpModel,jumpParams)
# Script_European_StochasticVolatility.m:162
    histogram(Spath(arange(),end()))
    disc=exp(dot(- r,T))
# Script_European_StochasticVolatility.m:165
    prices,stdErrs=Price_MC_European_Strikes_func(Spath,disc,call,Kvec,nargout=2)
# Script_European_StochasticVolatility.m:166
    plot(Kvec,prices)
    ylabel('price')
    xlabel('strike')
    grid('on')