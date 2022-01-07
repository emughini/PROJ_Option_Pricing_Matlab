# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_EIA_Cliquet.m

    ##################################################################
### Cliquet/Equity-Indexed Annuity Option Pricer
##################################################################
# Descritpion: Script to Price Cliquets/Equity-Indexed Annuities in Stochastic volatility models (with jumps)
#              using the PROJ method + CTMC approximation
    
    # Author:      Justin Kirkby
# References:  (1) Equity-linked annuity pricing with cliquet-style guarantees in regime-switching 
#               and stochastic volatility models with jumps, IME, 2017, (w/ Z.Cui & D.Nguyen)
#              (2) Efficient option pricing by frame duality with the fast Fourier transform,
#                SIFIN, 2015
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_EIA_Cliquet.m:14
    cd(folder)
    addpath('../Helper_Functions')
    addpath('../DV_Swaps_Options')
    ###----------------------------
# Set Model/Contract Params
###----------------------------
    
    # contract: 1 = sum of local caps
#           2 = sum of local caps & floors
#           3 = cliquet: local & global caps & floors
#           4 = cliquet: local floor & cap, global floor, NO GLOBAL CAP  
#           5 = MPP: ie monthly point-to-point (COS) or Monthly Cap Sum (Bernard, Li)
    
    contract=3
# Script_EIA_Cliquet.m:29
    K=1
# Script_EIA_Cliquet.m:31
    
    r=0.05
# Script_EIA_Cliquet.m:32
    
    q=0
# Script_EIA_Cliquet.m:33
    
    T=1.0
# Script_EIA_Cliquet.m:34
    
    M=12
# Script_EIA_Cliquet.m:35
    
    contractParams.K = copy(1)
# Script_EIA_Cliquet.m:37
    
    contractParams.C = copy(0.04)
# Script_EIA_Cliquet.m:39
    
    contractParams.CG = copy(dot(dot(0.9,M),contractParams.C))
# Script_EIA_Cliquet.m:40
    
    contractParams.F = copy(0)
# Script_EIA_Cliquet.m:42
    
    contractParams.FG = copy(0)
# Script_EIA_Cliquet.m:43
    
    ###----------------------------
# Set Numerical/Approximation Params
###----------------------------
    numeric_param=cellarray([])
# Script_EIA_Cliquet.m:48
    numeric_param.N = copy(2 ** 10)
# Script_EIA_Cliquet.m:49
    
    numeric_param.m_0 = copy(50)
# Script_EIA_Cliquet.m:51
    
    numeric_param.gamma = copy(5.5)
# Script_EIA_Cliquet.m:52
    
    numeric_param.gridMethod = copy(4)
# Script_EIA_Cliquet.m:53
    numeric_param.gridMultParam = copy(0.8)
# Script_EIA_Cliquet.m:54
    L1=14
# Script_EIA_Cliquet.m:55
    ###========================
#### Select Stochastic Volatility Model
###========================
    model=1
# Script_EIA_Cliquet.m:60
    
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
# Script_EIA_Cliquet.m:71
    
    # 1 = Normal Jumps
                  # 2 = Double Exponential Jumps
    
    ################################
#  Jump Model Parameters
################################
    jumpParams=cellarray([])
# Script_EIA_Cliquet.m:78
    if jumpModel == 0:
        jumpParams.Nothing = copy(0)
# Script_EIA_Cliquet.m:81
        psi_J=lambda u=None: dot(0,concat([u > 0]))
# Script_EIA_Cliquet.m:82
        c2Jump=0
# Script_EIA_Cliquet.m:84
        c4Jump=0
# Script_EIA_Cliquet.m:85
    else:
        if jumpModel == 1:
            lambda_=1
# Script_EIA_Cliquet.m:88
            muJ=- 0.12
# Script_EIA_Cliquet.m:88
            sigJ=0.15
# Script_EIA_Cliquet.m:88
            jumpParams.kappa = copy(exp(muJ + dot(0.5,sigJ ** 2)) - 1)
# Script_EIA_Cliquet.m:90
            jumpParams.lambda = copy(lambda_)
# Script_EIA_Cliquet.m:91
            jumpParams.muJ = copy(muJ)
# Script_EIA_Cliquet.m:91
            jumpParams.sigJ = copy(sigJ)
# Script_EIA_Cliquet.m:91
            psi_J=lambda u=None: dot(lambda_,(exp(dot(dot(1j,u),muJ) - dot(dot(0.5,sigJ ** 2),u ** 2)) - 1))
# Script_EIA_Cliquet.m:92
            c2Jump=dot(lambda_,(muJ ** 2 + sigJ ** 2))
# Script_EIA_Cliquet.m:94
            c4Jump=dot(lambda_,(muJ ** 4 + dot(dot(6,sigJ ** 2),muJ ** 2) + dot(dot(3,sigJ ** 4),lambda_)))
# Script_EIA_Cliquet.m:95
        else:
            if jumpModel == 2:
                lambda_=1
# Script_EIA_Cliquet.m:98
                p_up=0.5
# Script_EIA_Cliquet.m:99
                eta1=25
# Script_EIA_Cliquet.m:100
                eta2=30
# Script_EIA_Cliquet.m:101
                kappa=dot(p_up,eta1) / (eta1 - 1) + dot((1 - p_up),eta2) / (eta2 + 1) - 1
# Script_EIA_Cliquet.m:103
                jumpParams.lambda = copy(lambda_)
# Script_EIA_Cliquet.m:104
                jumpParams.kappa = copy(kappa)
# Script_EIA_Cliquet.m:104
                jumpParams.eta1 = copy(eta1)
# Script_EIA_Cliquet.m:104
                jumpParams.eta2 = copy(eta2)
# Script_EIA_Cliquet.m:104
                jumpParams.p_up = copy(p_up)
# Script_EIA_Cliquet.m:104
                psi_J=lambda u=None: dot(lambda_,(dot(p_up,eta1) / (eta1 - dot(1j,u)) + dot((1 - p_up),eta2) / (eta2 + dot(1j,u)) - 1))
# Script_EIA_Cliquet.m:105
                c2Jump=dot(dot(2,lambda_),p_up) / eta1 ** 2 + dot(dot(2,lambda_),(1 - p_up)) / eta2 ** 2
# Script_EIA_Cliquet.m:107
                c4Jump=dot(dot(24,lambda_),(p_up / eta1 ** 4 + (1 - p_up) / eta2 ** 4))
# Script_EIA_Cliquet.m:108
    
    ################################################
####    Set the Stochastic Volatility Model Component
################################################
    if model == 1:
        ###==============================
    ### HESTON MODEL  Parameters
    ###==============================
        modparam.eta = copy(4)
# Script_EIA_Cliquet.m:120
        modparam.theta = copy(0.035)
# Script_EIA_Cliquet.m:121
        modparam.rho = copy(- 0.75)
# Script_EIA_Cliquet.m:122
        modparam.Sigmav = copy(0.15)
# Script_EIA_Cliquet.m:123
        modparam.v0 = copy(0.04)
# Script_EIA_Cliquet.m:124
    else:
        if model == 2:
            ###=============================================================
    ### STEIN-STEIN MODEL  Parameters
    ###=============================================================
            modparam.eta = copy(2)
# Script_EIA_Cliquet.m:130
            modparam.theta = copy(0.18)
# Script_EIA_Cliquet.m:131
            modparam.Sigmav = copy(0.18)
# Script_EIA_Cliquet.m:132
            modparam.v0 = copy(0.22)
# Script_EIA_Cliquet.m:133
            modparam.rho = copy(- 0.5)
# Script_EIA_Cliquet.m:134
        else:
            if model == 3:
                ###=============================================================
    ### 3/2 MODEL  Parameters
    ###=============================================================
                modparam.Sigmav = copy(0.1)
# Script_EIA_Cliquet.m:140
                modparam.eta = copy(3)
# Script_EIA_Cliquet.m:141
                modparam.rho = copy(- 0.7)
# Script_EIA_Cliquet.m:142
                modparam.theta = copy(0.04)
# Script_EIA_Cliquet.m:143
                modparam.v0 = copy(0.04)
# Script_EIA_Cliquet.m:144
            else:
                if model == 4:
                    ###=============================================================
    ### 4/2 MODEL  Parameters
    ###=============================================================
                    modparam.eta = copy(3)
# Script_EIA_Cliquet.m:150
                    modparam.theta = copy(0.04)
# Script_EIA_Cliquet.m:151
                    modparam.rho = copy(- 0.7)
# Script_EIA_Cliquet.m:152
                    modparam.Sigmav = copy(0.25)
# Script_EIA_Cliquet.m:153
                    modparam.v0 = copy(0.04)
# Script_EIA_Cliquet.m:154
                    modparam.aa = copy(0.5)
# Script_EIA_Cliquet.m:155
                    modparam.bb = copy(dot(0.5,modparam.v0))
# Script_EIA_Cliquet.m:156
                else:
                    if model == 5:
                        ###=============================================================
    ### HULL-WHITE MODEL  Parameters
    ###=============================================================
                        modparam.av = copy(0.05)
# Script_EIA_Cliquet.m:162
                        modparam.rho = copy(- 0.6)
# Script_EIA_Cliquet.m:163
                        modparam.Sigmav = copy(0.6)
# Script_EIA_Cliquet.m:164
                        modparam.v0 = copy(0.03)
# Script_EIA_Cliquet.m:165
                    else:
                        if model == 6:
                            ###=============================================================
    ### SCOTT MODEL  Parameters
    ###=============================================================
                            modparam.eta = copy(2)
# Script_EIA_Cliquet.m:171
                            modparam.theta = copy(log(0.16))
# Script_EIA_Cliquet.m:172
                            modparam.Sigmav = copy(0.2)
# Script_EIA_Cliquet.m:173
                            modparam.v0 = copy(log(0.18))
# Script_EIA_Cliquet.m:174
                            modparam.rho = copy(- 0.9)
# Script_EIA_Cliquet.m:175
                        else:
                            if model == 7:
                                ###=============================================================
    ### ALPHA-HYPERGEOMETRIC MODEL  Parameters
    ###=============================================================
                                modparam.rho = copy(- 0.9)
# Script_EIA_Cliquet.m:181
                                modparam.Sigmav = copy(0.2)
# Script_EIA_Cliquet.m:182
                                modparam.v0 = copy(log(0.17))
# Script_EIA_Cliquet.m:183
                                modparam.eta = copy(0.05)
# Script_EIA_Cliquet.m:184
                                modparam.theta = copy(0.2)
# Script_EIA_Cliquet.m:185
                                modparam.av = copy(0.03)
# Script_EIA_Cliquet.m:186
    
    #################################################################
### PRICE
#################################################################
    tic
    #density projection grid on [-alpha,alpha]
    numeric_param.alph = copy(GetAlph_DisreteVariance(c2Jump,c4Jump,model,modparam,T,L1))
# Script_EIA_Cliquet.m:195
    price=PROJ_Cliquet_EIA_StochVol(numeric_param,M,r,q,T,psi_J,model,modparam,contract,contractParams)
# Script_EIA_Cliquet.m:197
    toc
    fprintf('%.8f \n',price)