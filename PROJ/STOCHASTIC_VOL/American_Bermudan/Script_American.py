# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_American.m

    ##################################################################
### American/Bermudan Option Pricier
##################################################################
# Descritpion: Script to Price Bermudan Options in Stochastic volatility models (with jumps)
#              using the PROJ method
# Author:      Justin Kirkby
# References:  (1) A unified approach to Bermudan and Barrier options under stochastic
#               volatility models with jumps. J. Economic Dynamics and Control, 2017
#              (2) American and Exotic option pricing with Jump Diffusions and Other Levy Processes.
#               J. Computational Finance, 2018
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_American.m:14
    cd(folder)
    addpath('../Helper_Functions')
    ###----------------------------
# Set Model/Contract Params
###----------------------------
    S_0=100
# Script_American.m:21
    
    W=100
# Script_American.m:22
    
    r=0.05
# Script_American.m:23
    
    T=0.5
# Script_American.m:24
    
    M=50
# Script_American.m:25
    
    ###----------------------------
# Set Numerical/Approximation Params
###----------------------------
    numeric_param=cellarray([])
# Script_American.m:31
    numeric_param.N = copy(2 ** 10)
# Script_American.m:32
    
    numeric_param.alph = copy(6)
# Script_American.m:33
    
    numeric_param.m_0 = copy(50)
# Script_American.m:35
    
    numeric_param.gamma = copy(3.3)
# Script_American.m:36
    
    numeric_param.gridMethod = copy(4)
# Script_American.m:37
    numeric_param.gridMultParam = copy(0.2)
# Script_American.m:38
    ###========================
#### Select Stochastic Volatility Model
###========================
    model=1
# Script_American.m:44
    
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
# Script_American.m:55
    
    # 1 = Normal Jumps
                  # 2 = Double Exponential Jumps
    
    ################################
#  Jump Model Parameters
################################
    jumpParams=cellarray([])
# Script_American.m:62
    if jumpModel == 0:
        jumpParams.Nothing = copy(0)
# Script_American.m:65
        psi_J=lambda u=None: dot(0,concat([u > 0]))
# Script_American.m:66
        c2Jump=0
# Script_American.m:68
        c4Jump=0
# Script_American.m:69
    else:
        if jumpModel == 1:
            lambda_=1
# Script_American.m:72
            muJ=- 0.12
# Script_American.m:72
            sigJ=0.15
# Script_American.m:72
            jumpParams.kappa = copy(exp(muJ + dot(0.5,sigJ ** 2)) - 1)
# Script_American.m:74
            jumpParams.lambda = copy(lambda_)
# Script_American.m:75
            jumpParams.muJ = copy(muJ)
# Script_American.m:75
            jumpParams.sigJ = copy(sigJ)
# Script_American.m:75
            psi_J=lambda u=None: dot(lambda_,(exp(dot(dot(1j,u),muJ) - dot(dot(0.5,sigJ ** 2),u ** 2)) - 1))
# Script_American.m:76
            c2Jump=dot(lambda_,(muJ ** 2 + sigJ ** 2))
# Script_American.m:78
            c4Jump=dot(lambda_,(muJ ** 4 + dot(dot(6,sigJ ** 2),muJ ** 2) + dot(dot(3,sigJ ** 4),lambda_)))
# Script_American.m:79
        else:
            if jumpModel == 2:
                lambda_=1
# Script_American.m:82
                p_up=0.5
# Script_American.m:83
                eta1=25
# Script_American.m:84
                eta2=30
# Script_American.m:85
                kappa=dot(p_up,eta1) / (eta1 - 1) + dot((1 - p_up),eta2) / (eta2 + 1) - 1
# Script_American.m:87
                jumpParams.lambda = copy(lambda_)
# Script_American.m:88
                jumpParams.kappa = copy(kappa)
# Script_American.m:88
                jumpParams.eta1 = copy(eta1)
# Script_American.m:88
                jumpParams.eta2 = copy(eta2)
# Script_American.m:88
                jumpParams.p_up = copy(p_up)
# Script_American.m:88
                psi_J=lambda u=None: dot(lambda_,(dot(p_up,eta1) / (eta1 - dot(1j,u)) + dot((1 - p_up),eta2) / (eta2 + dot(1j,u)) - 1))
# Script_American.m:89
                c2Jump=dot(dot(2,lambda_),p_up) / eta1 ** 2 + dot(dot(2,lambda_),(1 - p_up)) / eta2 ** 2
# Script_American.m:91
                c4Jump=dot(dot(24,lambda_),(p_up / eta1 ** 4 + (1 - p_up) / eta2 ** 4))
# Script_American.m:92
    
    ################################################
####    Set the Stochastic Volatility Model Component
################################################
    if model == 1:
        ###==============================
    ### HESTON MODEL  Parameters
    ###==============================
        modparam.eta = copy(4)
# Script_American.m:104
        modparam.theta = copy(0.035)
# Script_American.m:105
        modparam.rho = copy(- 0.75)
# Script_American.m:106
        modparam.Sigmav = copy(0.15)
# Script_American.m:107
        modparam.v0 = copy(0.04)
# Script_American.m:108
    else:
        if model == 2:
            ###=============================================================
    ### STEIN-STEIN MODEL  Parameters
    ###=============================================================
            modparam.eta = copy(2)
# Script_American.m:114
            modparam.theta = copy(0.18)
# Script_American.m:115
            modparam.Sigmav = copy(0.18)
# Script_American.m:116
            modparam.v0 = copy(0.22)
# Script_American.m:117
            modparam.rho = copy(- 0.5)
# Script_American.m:118
        else:
            if model == 3:
                ###=============================================================
    ### 3/2 MODEL  Parameters
    ###=============================================================
                modparam.Sigmav = copy(0.15)
# Script_American.m:124
                modparam.eta = copy(4)
# Script_American.m:125
                modparam.rho = copy(- 0.6)
# Script_American.m:126
                modparam.theta = copy(0.03)
# Script_American.m:127
                modparam.v0 = copy(0.03)
# Script_American.m:128
            else:
                if model == 4:
                    ###=============================================================
    ### 4/2 MODEL  Parameters
    ###=============================================================
                    modparam.eta = copy(3)
# Script_American.m:134
                    modparam.theta = copy(0.04)
# Script_American.m:135
                    modparam.rho = copy(- 0.7)
# Script_American.m:136
                    modparam.Sigmav = copy(0.25)
# Script_American.m:137
                    modparam.v0 = copy(0.04)
# Script_American.m:138
                    modparam.aa = copy(0.5)
# Script_American.m:139
                    modparam.bb = copy(dot(0.5,modparam.v0))
# Script_American.m:140
                else:
                    if model == 5:
                        ###=============================================================
    ### HULL-WHITE MODEL  Parameters
    ###=============================================================
                        modparam.av = copy(0.05)
# Script_American.m:146
                        modparam.rho = copy(- 0.6)
# Script_American.m:147
                        modparam.Sigmav = copy(0.6)
# Script_American.m:148
                        modparam.v0 = copy(0.03)
# Script_American.m:149
                    else:
                        if model == 6:
                            ###=============================================================
    ### SCOTT MODEL  Parameters
    ###=============================================================
                            modparam.eta = copy(2)
# Script_American.m:155
                            modparam.theta = copy(log(0.16))
# Script_American.m:156
                            modparam.Sigmav = copy(0.2)
# Script_American.m:157
                            modparam.v0 = copy(log(0.18))
# Script_American.m:158
                            modparam.rho = copy(- 0.9)
# Script_American.m:159
                        else:
                            if model == 7:
                                ###=============================================================
    ### ALPHA-HYPERGEOMETRIC MODEL  Parameters
    ###=============================================================
                                modparam.rho = copy(- 0.9)
# Script_American.m:165
                                modparam.Sigmav = copy(0.2)
# Script_American.m:166
                                modparam.v0 = copy(log(0.17))
# Script_American.m:167
                                modparam.eta = copy(0.05)
# Script_American.m:168
                                modparam.theta = copy(0.2)
# Script_American.m:169
                                modparam.av = copy(0.03)
# Script_American.m:170
    
    #################################################################
### PRICE
#################################################################
    tic
    price=PROJ_American_StochVol(numeric_param,M,r,T,S_0,W,psi_J,model,modparam)
# Script_American.m:177
    toc
    fprintf('%.8f \n',price)