# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_European.m

    ##################################################################
### Barrier Option Pricier
##################################################################
# Descritpion: Script to Price European Options in Stochastic volatility models (with jumps)
#              using the PROJ method
# Author:      Justin Kirkby
# References:  (1) A unified approach to Bermudan and Barrier options under stochastic
#               volatility models with jumps. J. Economic Dynamics and Control, 2017
#              (2) Robust barrier option pricing by Frame Projection under
#               exponential Levy Dynamics. Applied Mathematical Finance, 2018.
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_European.m:13
    cd(folder)
    addpath('../Helper_Functions')
    addpath('../Barrier')
    ###----------------------------
# Set Model/Contract Params
###----------------------------
    S_0=100
# Script_European.m:21
    W=100
# Script_European.m:22
    
    r=0.05
# Script_European.m:23
    q=0
# Script_European.m:23
    T=0.25
# Script_European.m:24
    M=1
# Script_European.m:25
    call=1
# Script_European.m:26
    ###----------------------------
# Set Numerical/Approximation Params
###----------------------------
    numeric_param=cellarray([])
# Script_European.m:31
    numeric_param.N = copy(2 ** 10)
# Script_European.m:32
    
    numeric_param.alph = copy(5)
# Script_European.m:33
    
    numeric_param.m_0 = copy(20)
# Script_European.m:35
    
    numeric_param.gamma = copy(5)
# Script_European.m:36
    
    numeric_param.gridMethod = copy(4)
# Script_European.m:37
    numeric_param.gridMultParam = copy(0.2)
# Script_European.m:38
    ###========================
#### Select Stochastic Volatility Model
###========================
    model=1
# Script_European.m:43
    
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
# Script_European.m:54
    
    # 1 = Normal Jumps
                  # 2 = Double Exponential Jumps
    
    ################################
#  Jump Model Parameters
################################
    jumpParams=cellarray([])
# Script_European.m:61
    if jumpModel == 0:
        jumpParams.Nothing = copy(0)
# Script_European.m:64
        psi_J=lambda u=None: dot(0,concat([u > 0]))
# Script_European.m:65
        c2Jump=0
# Script_European.m:67
        c4Jump=0
# Script_European.m:68
    else:
        if jumpModel == 1:
            lambda_=1
# Script_European.m:71
            muJ=- 0.12
# Script_European.m:71
            sigJ=0.15
# Script_European.m:71
            jumpParams.kappa = copy(exp(muJ + dot(0.5,sigJ ** 2)) - 1)
# Script_European.m:73
            jumpParams.lambda = copy(lambda_)
# Script_European.m:74
            jumpParams.muJ = copy(muJ)
# Script_European.m:74
            jumpParams.sigJ = copy(sigJ)
# Script_European.m:74
            psi_J=lambda u=None: dot(lambda_,(exp(dot(dot(1j,u),muJ) - dot(dot(0.5,sigJ ** 2),u ** 2)) - 1))
# Script_European.m:75
            c2Jump=dot(lambda_,(muJ ** 2 + sigJ ** 2))
# Script_European.m:77
            c4Jump=dot(lambda_,(muJ ** 4 + dot(dot(6,sigJ ** 2),muJ ** 2) + dot(dot(3,sigJ ** 4),lambda_)))
# Script_European.m:78
        else:
            if jumpModel == 2:
                lambda_=1
# Script_European.m:81
                p_up=0.5
# Script_European.m:82
                eta1=25
# Script_European.m:83
                eta2=30
# Script_European.m:84
                kappa=dot(p_up,eta1) / (eta1 - 1) + dot((1 - p_up),eta2) / (eta2 + 1) - 1
# Script_European.m:86
                jumpParams.lambda = copy(lambda_)
# Script_European.m:87
                jumpParams.kappa = copy(kappa)
# Script_European.m:87
                jumpParams.eta1 = copy(eta1)
# Script_European.m:87
                jumpParams.eta2 = copy(eta2)
# Script_European.m:87
                jumpParams.p_up = copy(p_up)
# Script_European.m:87
                psi_J=lambda u=None: dot(lambda_,(dot(p_up,eta1) / (eta1 - dot(1j,u)) + dot((1 - p_up),eta2) / (eta2 + dot(1j,u)) - 1))
# Script_European.m:88
                c2Jump=dot(dot(2,lambda_),p_up) / eta1 ** 2 + dot(dot(2,lambda_),(1 - p_up)) / eta2 ** 2
# Script_European.m:90
                c4Jump=dot(dot(24,lambda_),(p_up / eta1 ** 4 + (1 - p_up) / eta2 ** 4))
# Script_European.m:91
    
    ################################################
####    Set the Stochastic Volatility Model Component
################################################
    if model == 1:
        ###==============================
    ### HESTON MODEL  Parameters
    ###==============================
        modparam.eta = copy(4)
# Script_European.m:103
        modparam.theta = copy(0.035)
# Script_European.m:104
        modparam.rho = copy(- 0.75)
# Script_European.m:105
        modparam.Sigmav = copy(0.15)
# Script_European.m:106
        modparam.v0 = copy(0.04)
# Script_European.m:107
    else:
        if model == 2:
            ###=============================================================
    ### STEIN-STEIN MODEL  Parameters
    ###=============================================================
            modparam.eta = copy(2)
# Script_European.m:113
            modparam.theta = copy(0.18)
# Script_European.m:114
            modparam.Sigmav = copy(0.18)
# Script_European.m:115
            modparam.v0 = copy(0.22)
# Script_European.m:116
            modparam.rho = copy(- 0.5)
# Script_European.m:117
        else:
            if model == 3:
                ###=============================================================
    ### 3/2 MODEL  Parameters
    ###=============================================================
                modparam.Sigmav = copy(0.1)
# Script_European.m:123
                modparam.eta = copy(3)
# Script_European.m:124
                modparam.rho = copy(- 0.7)
# Script_European.m:125
                modparam.theta = copy(0.04)
# Script_European.m:126
                modparam.v0 = copy(0.04)
# Script_European.m:127
            else:
                if model == 4:
                    ###=============================================================
    ### 4/2 MODEL  Parameters
    ###=============================================================
                    modparam.eta = copy(3)
# Script_European.m:133
                    modparam.theta = copy(0.04)
# Script_European.m:134
                    modparam.rho = copy(- 0.7)
# Script_European.m:135
                    modparam.Sigmav = copy(0.25)
# Script_European.m:136
                    modparam.v0 = copy(0.04)
# Script_European.m:137
                    modparam.aa = copy(0.5)
# Script_European.m:138
                    modparam.bb = copy(dot(0.5,modparam.v0))
# Script_European.m:139
                else:
                    if model == 5:
                        ###=============================================================
    ### HULL-WHITE MODEL  Parameters
    ###=============================================================
                        modparam.av = copy(0.05)
# Script_European.m:145
                        modparam.rho = copy(- 0.6)
# Script_European.m:146
                        modparam.Sigmav = copy(0.6)
# Script_European.m:147
                        modparam.v0 = copy(0.03)
# Script_European.m:148
                    else:
                        if model == 6:
                            ###=============================================================
    ### SCOTT MODEL  Parameters
    ###=============================================================
                            modparam.eta = copy(2)
# Script_European.m:154
                            modparam.theta = copy(log(0.16))
# Script_European.m:155
                            modparam.Sigmav = copy(0.2)
# Script_European.m:156
                            modparam.v0 = copy(log(0.18))
# Script_European.m:157
                            modparam.rho = copy(- 0.9)
# Script_European.m:158
                        else:
                            if model == 7:
                                ###=============================================================
    ### ALPHA-HYPERGEOMETRIC MODEL  Parameters
    ###=============================================================
                                modparam.rho = copy(- 0.9)
# Script_European.m:164
                                modparam.Sigmav = copy(0.2)
# Script_European.m:165
                                modparam.v0 = copy(log(0.17))
# Script_European.m:166
                                modparam.eta = copy(0.05)
# Script_European.m:167
                                modparam.theta = copy(0.2)
# Script_European.m:168
                                modparam.av = copy(0.03)
# Script_European.m:169
    
    #################################################################
### PRICE
#################################################################
    
    # NOTE: this prices using Barrier algo, in future, this will call its own function
    if call == 1:
        down=1
# Script_European.m:178
        H=S_0 / 8
# Script_European.m:178
    else:
        down=0
# Script_European.m:180
        H=dot(S_0,8)
# Script_European.m:180
    
    tic
    price=PROJ_Barrier_StochVol(numeric_param,call,down,S_0,W,H,M,r,T,psi_J,model,modparam)
# Script_European.m:184
    toc
    fprintf('%.8f \n',price)
    if model == 1:
        addpath('../../LEVY/European_Options')
        addpath('../../LEVY/Helper_Functions')
        addpath('../../LEVY/RN_CHF')
        modelInput=getModelInput(6,T,r,q,modparam)
# Script_European.m:194
        L1=14
# Script_European.m:195
        alpha=getTruncationAlpha(T,L1,modelInput,6)
# Script_European.m:195
        N=2 ** 14
# Script_European.m:195
        order=3
# Script_European.m:195
        ref=PROJ_European(order,N,alpha,r,q,T,S_0,W,call,modelInput.rnCHF,dot(modelInput.c1,T))
# Script_European.m:197
        fprintf('Relative Error: %.3e\n',(price - ref) / price)
    