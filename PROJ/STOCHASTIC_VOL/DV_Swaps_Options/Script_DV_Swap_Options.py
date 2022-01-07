# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_DV_Swap_Options.m

    ##################################################################
### Discrete Variance Swap / Option Pricer
##################################################################
# Descritpion: Script to Price Discrete Variance Swap / Options under stochastic volatility models (with jumps)
# Author:      Justin Kirkby
# References:  (1) A General Framework for discretely sampled realized
#              variance derivatives in stocahstic volatility models with
#              jumps, EJOR, 2017
#              (2) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_DV_Swap_Options.m:13
    cd(folder)
    addpath('../Helper_Functions')
    addpath('./Analytical_Swaps')
    ###----------------------------
# Set Model/Contract Params
###----------------------------
    
    contract=1
# Script_DV_Swap_Options.m:23
    
    K=0.0
# Script_DV_Swap_Options.m:24
    
    r=0.01
# Script_DV_Swap_Options.m:25
    
    q=0
# Script_DV_Swap_Options.m:26
    
    T=0.5
# Script_DV_Swap_Options.m:27
    
    M=20
# Script_DV_Swap_Options.m:28
    
    ###----------------------------
# Set Numerical/Approximation Params
###----------------------------
    numeric_param=cellarray([])
# Script_DV_Swap_Options.m:33
    numeric_param.N = copy(2 ** 9)
# Script_DV_Swap_Options.m:34
    
    numeric_param.m_0 = copy(40)
# Script_DV_Swap_Options.m:35
    
    numeric_param.gamma = copy(5.5)
# Script_DV_Swap_Options.m:36
    
    numeric_param.gridMethod = copy(4)
# Script_DV_Swap_Options.m:37
    numeric_param.gridMultParam = copy(0.8)
# Script_DV_Swap_Options.m:38
    L1=14
# Script_DV_Swap_Options.m:39
    
    ###========================
#### Select Stochastic Volatility Model
###========================
    model=1
# Script_DV_Swap_Options.m:44
    
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
# Script_DV_Swap_Options.m:55
    
    # 1 = Normal Jumps
                  # 2 = Double Exponential Jumps
    
    ################################
#  Jump Model Parameters
################################
    jumpParams=cellarray([])
# Script_DV_Swap_Options.m:62
    if jumpModel == 0:
        jumpParams.Nothing = copy(0)
# Script_DV_Swap_Options.m:65
        psi_J=lambda u=None: dot(0,concat([u > 0]))
# Script_DV_Swap_Options.m:66
        c2Jump=0
# Script_DV_Swap_Options.m:68
        c4Jump=0
# Script_DV_Swap_Options.m:69
    else:
        if jumpModel == 1:
            lambda_=1
# Script_DV_Swap_Options.m:72
            muJ=- 0.12
# Script_DV_Swap_Options.m:72
            sigJ=0.15
# Script_DV_Swap_Options.m:72
            jumpParams.kappa = copy(exp(muJ + dot(0.5,sigJ ** 2)) - 1)
# Script_DV_Swap_Options.m:74
            jumpParams.lambda = copy(lambda_)
# Script_DV_Swap_Options.m:75
            jumpParams.muJ = copy(muJ)
# Script_DV_Swap_Options.m:75
            jumpParams.sigJ = copy(sigJ)
# Script_DV_Swap_Options.m:75
            psi_J=lambda u=None: dot(lambda_,(exp(dot(dot(1j,u),muJ) - dot(dot(0.5,sigJ ** 2),u ** 2)) - 1))
# Script_DV_Swap_Options.m:76
            c2Jump=dot(lambda_,(muJ ** 2 + sigJ ** 2))
# Script_DV_Swap_Options.m:78
            c4Jump=dot(lambda_,(muJ ** 4 + dot(dot(6,sigJ ** 2),muJ ** 2) + dot(dot(3,sigJ ** 4),lambda_)))
# Script_DV_Swap_Options.m:79
        else:
            if jumpModel == 2:
                lambda_=1
# Script_DV_Swap_Options.m:82
                p_up=0.5
# Script_DV_Swap_Options.m:83
                eta1=25
# Script_DV_Swap_Options.m:84
                eta2=30
# Script_DV_Swap_Options.m:85
                kappa=dot(p_up,eta1) / (eta1 - 1) + dot((1 - p_up),eta2) / (eta2 + 1) - 1
# Script_DV_Swap_Options.m:87
                jumpParams.lambda = copy(lambda_)
# Script_DV_Swap_Options.m:88
                jumpParams.kappa = copy(kappa)
# Script_DV_Swap_Options.m:88
                jumpParams.eta1 = copy(eta1)
# Script_DV_Swap_Options.m:88
                jumpParams.eta2 = copy(eta2)
# Script_DV_Swap_Options.m:88
                jumpParams.p_up = copy(p_up)
# Script_DV_Swap_Options.m:88
                psi_J=lambda u=None: dot(lambda_,(dot(p_up,eta1) / (eta1 - dot(1j,u)) + dot((1 - p_up),eta2) / (eta2 + dot(1j,u)) - 1))
# Script_DV_Swap_Options.m:89
                c2Jump=dot(dot(2,lambda_),p_up) / eta1 ** 2 + dot(dot(2,lambda_),(1 - p_up)) / eta2 ** 2
# Script_DV_Swap_Options.m:91
                c4Jump=dot(dot(24,lambda_),(p_up / eta1 ** 4 + (1 - p_up) / eta2 ** 4))
# Script_DV_Swap_Options.m:92
    
    ################################################
####    Set the Stochastic Volatility Model Component
################################################
    if model == 1:
        ###==============================
    ### HESTON MODEL  Parameters
    ###==============================
        modparam.eta = copy(3.99)
# Script_DV_Swap_Options.m:103
        modparam.theta = copy(0.014)
# Script_DV_Swap_Options.m:104
        modparam.rho = copy(- 0.79)
# Script_DV_Swap_Options.m:105
        modparam.Sigmav = copy(0.27)
# Script_DV_Swap_Options.m:106
        modparam.v0 = copy((0.0994) ** 2)
# Script_DV_Swap_Options.m:107
    else:
        if model == 2:
            ###=============================================================
    ### STEIN-STEIN MODEL  Parameters
    ###=============================================================
            modparam.eta = copy(2)
# Script_DV_Swap_Options.m:113
            modparam.theta = copy(0.18)
# Script_DV_Swap_Options.m:114
            modparam.Sigmav = copy(0.18)
# Script_DV_Swap_Options.m:115
            modparam.v0 = copy(0.22)
# Script_DV_Swap_Options.m:116
            modparam.rho = copy(- 0.5)
# Script_DV_Swap_Options.m:117
        else:
            if model == 3:
                ###=============================================================
    ### 3/2 MODEL  Parameters
    ###=============================================================
                modparam.Sigmav = copy(0.1)
# Script_DV_Swap_Options.m:123
                modparam.eta = copy(3)
# Script_DV_Swap_Options.m:124
                modparam.rho = copy(- 0.7)
# Script_DV_Swap_Options.m:125
                modparam.theta = copy(0.04)
# Script_DV_Swap_Options.m:126
                modparam.v0 = copy(0.04)
# Script_DV_Swap_Options.m:127
            else:
                if model == 4:
                    ###=============================================================
    ### 4/2 MODEL  Parameters
    ###=============================================================
                    modparam.eta = copy(3)
# Script_DV_Swap_Options.m:133
                    modparam.theta = copy(0.04)
# Script_DV_Swap_Options.m:134
                    modparam.rho = copy(- 0.7)
# Script_DV_Swap_Options.m:135
                    modparam.Sigmav = copy(0.25)
# Script_DV_Swap_Options.m:136
                    modparam.v0 = copy(0.04)
# Script_DV_Swap_Options.m:137
                    modparam.aa = copy(0.5)
# Script_DV_Swap_Options.m:138
                    modparam.bb = copy(dot(0.5,modparam.v0))
# Script_DV_Swap_Options.m:139
                else:
                    if model == 5:
                        ###=============================================================
    ### HULL-WHITE MODEL  Parameters
    ###=============================================================
                        modparam.av = copy(0.05)
# Script_DV_Swap_Options.m:145
                        modparam.rho = copy(- 0.6)
# Script_DV_Swap_Options.m:146
                        modparam.Sigmav = copy(0.6)
# Script_DV_Swap_Options.m:147
                        modparam.v0 = copy(0.03)
# Script_DV_Swap_Options.m:148
                    else:
                        if model == 6:
                            ###=============================================================
    ### SCOTT MODEL  Parameters
    ###=============================================================
                            modparam.eta = copy(2)
# Script_DV_Swap_Options.m:154
                            modparam.theta = copy(log(0.16))
# Script_DV_Swap_Options.m:155
                            modparam.Sigmav = copy(0.2)
# Script_DV_Swap_Options.m:156
                            modparam.v0 = copy(log(0.18))
# Script_DV_Swap_Options.m:157
                            modparam.rho = copy(- 0.9)
# Script_DV_Swap_Options.m:158
                        else:
                            if model == 7:
                                ###=============================================================
    ### ALPHA-HYPERGEOMETRIC MODEL  Parameters
    ###=============================================================
                                modparam.rho = copy(- 0.9)
# Script_DV_Swap_Options.m:164
                                modparam.Sigmav = copy(0.2)
# Script_DV_Swap_Options.m:165
                                modparam.v0 = copy(log(0.17))
# Script_DV_Swap_Options.m:166
                                modparam.eta = copy(0.05)
# Script_DV_Swap_Options.m:167
                                modparam.theta = copy(0.2)
# Script_DV_Swap_Options.m:168
                                modparam.av = copy(0.03)
# Script_DV_Swap_Options.m:169
    
    ##############################################################
#   PRICE CONTACT
##############################################################
#density projection grid on [-alpha,alpha]
    numeric_param.alph = copy(GetAlph_DisreteVariance(c2Jump,c4Jump,model,modparam,T,L1))
# Script_DV_Swap_Options.m:177
    PROJ_Price=PROJ_DiscreteVariance_StochVol(numeric_param,M,r,T,K,psi_J,model,modparam,contract)
# Script_DV_Swap_Options.m:179
    fprintf('PROJ Price: %.8f \n',PROJ_Price)
    ### In the special cases where analytic prices are known, also print the error
    if model == 1 and jumpModel == 0 and contract == 1:
        ref,KcH=hestonfairstrike(r,modparam.v0,modparam.theta,modparam.eta,modparam.Sigmav,T,modparam.rho,M,nargout=2)
# Script_DV_Swap_Options.m:184
        fprintf('Analytical Price: %.8f \n',ref)
        fprintf('Error: %.3e \n',PROJ_Price - ref)
    else:
        if model == 5 and jumpModel == 0 and contract == 1:
            ref,KcH=hullwhitefairstrike(r,modparam.v0,modparam.Sigmav,modparam.av,T,modparam.rho,M,nargout=2)
# Script_DV_Swap_Options.m:189
            Error1=PROJ_Price - ref
# Script_DV_Swap_Options.m:190
            fprintf('Analytical Price: %.8f \n',ref)
            fprintf('Error: %.3e \n',PROJ_Price - ref)
    