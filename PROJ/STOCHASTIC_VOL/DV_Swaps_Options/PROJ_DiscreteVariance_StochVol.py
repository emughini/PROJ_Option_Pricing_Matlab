# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_DiscreteVariance_StochVol.m

    
@function
def PROJ_DiscreteVariance_StochVol(numeric_param=None,M=None,r=None,T=None,K=None,psi_J=None,model=None,modparam=None,contract=None,*args,**kwargs):
    varargin = PROJ_DiscreteVariance_StochVol.varargin
    nargin = PROJ_DiscreteVariance_StochVol.nargin

    #########################################################
# About: Pricing Discrete variance swaps and options using CTMC Approximation + PROJ method
# Models Supported: Stochastic Volatility (including jumps)
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # References:  (1) A unified approach to Bermudan and Barrier options under stochastic
#               volatility models with jumps. J. Economic Dynamics and Control, 2017
#              (2) Robust barrier option pricing by Frame Projection under
#               exponential Levy Dynamics. Applied Mathematical Finance, 2018.
    
    # ----------------------
# Contract Params 
# ----------------------
# T  : number of years (T = 2 is two years, T = .5 is half a year)
# M  : number of subintervals of [0,T] (total of M+1 points in time grid)
# K  : strike  (used instead of K)
    
    # contract: 
#           1 = Variance Swap, 
#           2 = Volatility Swap, 
#           3 = Call on Variance, 
#           4 = Put on Variance
    
    # NOTE: right now only 1 and 3 are supported
    
    # ----------------------
# Model Params 
# ----------------------
# S_0: initial Underlying
# r  : interest rate 
# psi_J: characteristic exponenent of jump part...
#        function handdle: psi_J(xi) = lambda*(phi(xi) -1)
# model:
#        1 = HESTON:      Sigmav, v0, rho, eta, theta
#        2 = STEIN-STEIN: Sigmav, v0, rho, eta, theta
#        3 = 3/2 MODEL:   Sigmav, v0, rho, eta, theta
#        4 = 4/2 MODEL:   Sigmav, v0, rho, eta, theta, aa, bb
#        5 = HULL-WHITE:  Sigmav, v0, rho
#        6 = SCOTT:       Sigmav, v0, rho, eta, theta
#        7 = ALPHA-HYPER: Sigmav, v0, rho, eta, theta
    
    # modparam: contains all necessary params for the specific model (see below during assingment which ones are needed)
    
    # ----------------------
# Numerical Params 
# ----------------------
# numeric_parm: container of numerical params
#   N  : size of density grid (value grid is K:=N/2)
#   alph: density gridwith param, density on [-alph,alph]... value grid width = alph
#   m_0: number of states to approximate the Heston model with
#   gamma: var grid width parameter, grid is +/- gamma*stddev(variance process)
#   gridMethod: which type of var grid to use (typcially use 4)
    
    ####################################################################
    
    N=numeric_param.N
# PROJ_DiscreteVariance_StochVol.m:58
    alph=numeric_param.alph
# PROJ_DiscreteVariance_StochVol.m:59
    m_0=numeric_param.m_0
# PROJ_DiscreteVariance_StochVol.m:60
    gridMethod=numeric_param.gridMethod
# PROJ_DiscreteVariance_StochVol.m:61
    gamma=numeric_param.gamma
# PROJ_DiscreteVariance_StochVol.m:62
    varGridMult=numeric_param.gridMultParam
# PROJ_DiscreteVariance_StochVol.m:63
    dx=dot(2,alph) / (N - 1)
# PROJ_DiscreteVariance_StochVol.m:65
    dt=T / M
# PROJ_DiscreteVariance_StochVol.m:66
    a=1 / dx
# PROJ_DiscreteVariance_StochVol.m:67
    A=dot(32,a ** 4)
# PROJ_DiscreteVariance_StochVol.m:68
    C_aN=A / N
# PROJ_DiscreteVariance_StochVol.m:69
    xmin=dot((1 - N / 2),dx)
# PROJ_DiscreteVariance_StochVol.m:70
    ####////////////////////////////////////////////////////////
#### Intialize Q matrix and variance set
####////////////////////////////////////////////////////////
    t=T / 2
# PROJ_DiscreteVariance_StochVol.m:75
    lx,v0,ux=get_variance_grid_boundaries(model,modparam,t,gamma,nargout=3)
# PROJ_DiscreteVariance_StochVol.m:76
    mu_func,sig_func=get_SV_variance_grid_diffusion_funcs(model,modparam,nargout=2)
# PROJ_DiscreteVariance_StochVol.m:78
    boundaryMethod=1
# PROJ_DiscreteVariance_StochVol.m:79
    center=copy(v0)
# PROJ_DiscreteVariance_StochVol.m:80
    
    Q,v=Q_Matrix_AllForms(m_0,mu_func,sig_func,lx,ux,gridMethod,varGridMult,center,boundaryMethod,nargout=2)
# PROJ_DiscreteVariance_StochVol.m:82
    ####////////////////////////////////////////////////////////
#### Populate the Matrix Exponentials
####////////////////////////////////////////////////////////
    dxi=dot(dot(2,pi),a) / N
# PROJ_DiscreteVariance_StochVol.m:88
    xi=dot(dxi,(arange(0,N - 1)).T)
# PROJ_DiscreteVariance_StochVol.m:89
    v1,v2,fv=get_SV_matrix_expo_inputs(model,modparam,psi_J,dt,v,dxi,r,nargout=3)
# PROJ_DiscreteVariance_StochVol.m:91
    # Compute Matrix Exponentials for each xi(j)
    EXP_A=get_SV_matrix_exponential(Q,dt,xi,v1,v2,fv,psi_J,m_0,N)
# PROJ_DiscreteVariance_StochVol.m:93
    # ###################################################################
# ### PSI Matrix: 5-Point GAUSSIAN
# #################################################################
    NNM=copy(N)
# PROJ_DiscreteVariance_StochVol.m:99
    
    PSI=zeros(N - 1,NNM)
# PROJ_DiscreteVariance_StochVol.m:100
    
    #### Sample
    Neta=dot(5,(NNM)) + 15
# PROJ_DiscreteVariance_StochVol.m:103
    
    Neta5=(NNM) + 3
# PROJ_DiscreteVariance_StochVol.m:104
    g2=sqrt(5 - dot(2,sqrt(10 / 7))) / 6
# PROJ_DiscreteVariance_StochVol.m:105
    g3=sqrt(5 + dot(2,sqrt(10 / 7))) / 6
# PROJ_DiscreteVariance_StochVol.m:106
    v1=dot(0.5,128) / 225
# PROJ_DiscreteVariance_StochVol.m:107
    v2=dot(0.5,(322 + dot(13,sqrt(70)))) / 900
# PROJ_DiscreteVariance_StochVol.m:107
    v3=dot(0.5,(322 - dot(13,sqrt(70)))) / 900
# PROJ_DiscreteVariance_StochVol.m:107
    thet=zeros(1,Neta)
# PROJ_DiscreteVariance_StochVol.m:109
    
    thet[dot(5,(arange(1,Neta5))) - 2]=xmin - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1)))
# PROJ_DiscreteVariance_StochVol.m:110
    thet[dot(5,(arange(1,Neta5))) - 4]=xmin - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) - dot(dx,g3)
# PROJ_DiscreteVariance_StochVol.m:111
    thet[dot(5,(arange(1,Neta5))) - 3]=xmin - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) - dot(dx,g2)
# PROJ_DiscreteVariance_StochVol.m:112
    thet[dot(5,(arange(1,Neta5))) - 1]=xmin - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) + dot(dx,g2)
# PROJ_DiscreteVariance_StochVol.m:113
    thet[dot(5,(arange(1,Neta5)))]=xmin - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) + dot(dx,g3)
# PROJ_DiscreteVariance_StochVol.m:114
    #### Weights
    sig=concat([- 1.5 - g3,- 1.5 - g2,- 1.5,- 1.5 + g2,- 1.5 + g3,- 0.5 - g3,- 0.5 - g2,- 0.5,- 0.5 + g2,- 0.5 + g3])
# PROJ_DiscreteVariance_StochVol.m:117
    sig[arange(1,5)]=(sig(arange(1,5)) + 2) ** 3 / 6
# PROJ_DiscreteVariance_StochVol.m:118
    sig[arange(6,10)]=2 / 3 - dot(0.5,(sig(arange(6,10))) ** 3) - (sig(arange(6,10))) ** 2
# PROJ_DiscreteVariance_StochVol.m:119
    sig[concat([1,5,6,10])]=dot(v3,sig(concat([1,5,6,10])))
# PROJ_DiscreteVariance_StochVol.m:121
    sig[concat([2,4,7,9])]=dot(v2,sig(concat([2,4,7,9])))
# PROJ_DiscreteVariance_StochVol.m:121
    sig[concat([3,8])]=dot(v1,sig(concat([3,8])))
# PROJ_DiscreteVariance_StochVol.m:121
    sig=dot(C_aN,sig)
# PROJ_DiscreteVariance_StochVol.m:122
    #### Fill Matrix  (NOTE: this can be made MORE EFFICIENT by using symmetery of x^2)
    zz=exp(dot(dot(1j,dxi),thet ** 2))
# PROJ_DiscreteVariance_StochVol.m:125
    
    thet=copy(zz)
# PROJ_DiscreteVariance_StochVol.m:126
    for j in arange(1,N - 1).reshape(-1):
        PSI[j,arange()]=dot(sig(1),(thet(arange(1,Neta - 19,5)) + thet(arange(20,Neta,5)))) + dot(sig(2),(thet(arange(2,Neta - 18,5)) + thet(arange(19,Neta - 1,5)))) + dot(sig(3),(thet(arange(3,Neta - 17,5)) + thet(arange(18,Neta - 2,5)))) + dot(sig(4),(thet(arange(4,Neta - 16,5)) + thet(arange(17,Neta - 3,5)))) + dot(sig(5),(thet(arange(5,Neta - 15,5)) + thet(arange(16,Neta - 4,5)))) + dot(sig(6),(thet(arange(6,Neta - 14,5)) + thet(arange(15,Neta - 5,5)))) + dot(sig(7),(thet(arange(7,Neta - 13,5)) + thet(arange(14,Neta - 6,5)))) + dot(sig(8),(thet(arange(8,Neta - 12,5)) + thet(arange(13,Neta - 7,5)))) + dot(sig(9),(thet(arange(9,Neta - 11,5)) + thet(arange(12,Neta - 8,5)))) + dot(sig(10),(thet(arange(10,Neta - 10,5)) + thet(arange(11,Neta - 9,5))))
# PROJ_DiscreteVariance_StochVol.m:129
        thet=multiply(thet,zz)
# PROJ_DiscreteVariance_StochVol.m:140
    
    ###################################################################
### Find phi_{Y_1}
#################################################################
    
    xi=dot(dxi,(arange(1,N - 1)).T)
# PROJ_DiscreteVariance_StochVol.m:147
    
    b0=1208 / 2520
# PROJ_DiscreteVariance_StochVol.m:148
    b1=1191 / 2520
# PROJ_DiscreteVariance_StochVol.m:148
    b2=120 / 2520
# PROJ_DiscreteVariance_StochVol.m:148
    b3=1 / 2520
# PROJ_DiscreteVariance_StochVol.m:148
    zeta=(sin(xi / (dot(2,a))) / xi) ** 4.0 / (b0 + dot(b1,cos(xi / a)) + dot(b2,cos(dot(2,xi) / a)) + dot(b3,cos(dot(3,xi) / a)))
# PROJ_DiscreteVariance_StochVol.m:149
    hvec=multiply(exp(dot(dot(- 1j,xmin),xi)),zeta)
# PROJ_DiscreteVariance_StochVol.m:150
    
    #Note: PHIY is not defined for xi = 0
    PHIY_old=zeros(N - 1,m_0)
# PROJ_DiscreteVariance_StochVol.m:153
    PHIY_new=zeros(N - 1,m_0)
# PROJ_DiscreteVariance_StochVol.m:154
    
    #Find beta in first stage (using chf of Phi_Y1)
    for j in arange(1,m_0).reshape(-1):
        #Step 1: characteristic function of log return
        for n in arange(1,N - 1).reshape(-1):
            PHIY_old[n,j]=sum(EXP_A(arange(1,m_0),j,n + 1))
# PROJ_DiscreteVariance_StochVol.m:160
        #Step 2: invert characteristic function of log return (ie this is beta)
        BetaTemp=real(fft(concat([[1 / A],[multiply(PHIY_old(arange(),j),hvec)]])))
# PROJ_DiscreteVariance_StochVol.m:164
        #Step 3: Phi_{Y_1}^j
        PHIY_new[arange(),j]=dot(PSI,BetaTemp)
# PROJ_DiscreteVariance_StochVol.m:167
    
    ###################################################################
### Find PHI
#################################################################
    PHI=ones(m_0,m_0,N - 1)
# PROJ_DiscreteVariance_StochVol.m:174
    ### use PHIY_old for temp storage
    grand=zeros(N - 1,1)
# PROJ_DiscreteVariance_StochVol.m:176
    
    for j in arange(1,m_0).reshape(-1):
        for k in arange(1,m_0).reshape(-1):
            #First Invert chf to get p_{j,k}
            for n in arange(1,N - 1).reshape(-1):
                grand[n]=dot(hvec(n),EXP_A(k,j,n + 1))
# PROJ_DiscreteVariance_StochVol.m:181
            BetaTemp=real(fft(concat([[EXP_A(k,j,1) / A],[grand]])))
# PROJ_DiscreteVariance_StochVol.m:183
            PHI[j,k,arange()]=dot(PSI,BetaTemp)
# PROJ_DiscreteVariance_StochVol.m:184
    
    clear('EXP_A')
    for m in arange(2,M).reshape(-1):
        for n in arange(1,N - 1).reshape(-1):
            PHIY_new[n,arange()]=dot(PHIY_new(n,arange()),PHI(arange(),arange(),n).T)
# PROJ_DiscreteVariance_StochVol.m:192
    
    ####////////////////////////////////////////////////////////
#### Interpolate to find bracketing initial volatilities
####////////////////////////////////////////////////////////
    k_0=2
# PROJ_DiscreteVariance_StochVol.m:199
    
    while v0 >= v(k_0) and k_0 < m_0:

        k_0=k_0 + 1
# PROJ_DiscreteVariance_StochVol.m:201

    
    k_0=k_0 - 1
# PROJ_DiscreteVariance_StochVol.m:203
    #########################
    cubicTerminal=1
# PROJ_DiscreteVariance_StochVol.m:206
    
    #########################
    if contract == 1:
        if cubicTerminal == 1:
            xmin=- dx
# PROJ_DiscreteVariance_StochVol.m:210
        else:
            xmin=0
# PROJ_DiscreteVariance_StochVol.m:212
    else:
        if contract == 3:
            if cubicTerminal == 1:
                xmin=dot(K,T) - dx
# PROJ_DiscreteVariance_StochVol.m:216
            else:
                xmin=dot(K,T)
# PROJ_DiscreteVariance_StochVol.m:218
    
    if cubicTerminal == 1:
        if contract == 1 or contract == 3:
            grid=- dx + dot(dx,(arange(0,N - 1)))
# PROJ_DiscreteVariance_StochVol.m:224
            grid[1]=grid(1) / 24 + dx / 20
# PROJ_DiscreteVariance_StochVol.m:226
            grid[2]=dot(dx,7) / 30
# PROJ_DiscreteVariance_StochVol.m:227
            grid[3]=dot(grid(3),23) / 24 + dx / 20
# PROJ_DiscreteVariance_StochVol.m:228
    else:
        if contract == 1 or contract == 3:
            grid=dot(dx,(arange(0,N - 1)))
# PROJ_DiscreteVariance_StochVol.m:232
            grid[1]=dx / 6
# PROJ_DiscreteVariance_StochVol.m:233
        A=dot(24,a ** 2)
# PROJ_DiscreteVariance_StochVol.m:235
        C_aN=A / N
# PROJ_DiscreteVariance_StochVol.m:236
        zeta=(sin(xi / (dot(2,a))) / xi) ** 2.0 / (2 + cos(xi / a))
# PROJ_DiscreteVariance_StochVol.m:237
    
    if xmin != 0:
        hvec=multiply(exp(dot(dot(- 1j,xmin),xi)),zeta)
# PROJ_DiscreteVariance_StochVol.m:241
    else:
        hvec=copy(zeta)
# PROJ_DiscreteVariance_StochVol.m:243
    
    
    vals=concat([0,0])
# PROJ_DiscreteVariance_StochVol.m:247
    ks=concat([k_0,k_0 + 1])
# PROJ_DiscreteVariance_StochVol.m:248
    for l in arange(1,2).reshape(-1):
        j=ks(l)
# PROJ_DiscreteVariance_StochVol.m:251
        BetaTemp=real(fft(concat([[1 / A],[multiply(hvec,PHIY_new(arange(),j))]])))
# PROJ_DiscreteVariance_StochVol.m:252
        if contract == 1 or contract == 3:
            vals[l]=dot(grid(arange(1,N / 2)),BetaTemp(arange(1,N / 2)))
# PROJ_DiscreteVariance_StochVol.m:254
            vals[l]=dot(C_aN,vals(l))
# PROJ_DiscreteVariance_StochVol.m:255
    
    if gridMethod == 5 or gridMethod == 6:
        Approx=vals(1)
# PROJ_DiscreteVariance_StochVol.m:261
    else:
        Approx=vals(1) + dot((vals(2) - vals(1)),(v0 - v(k_0))) / (v(k_0 + 1) - v(k_0))
# PROJ_DiscreteVariance_StochVol.m:263
    
    
    if contract == 1:
        price=Approx / T
# PROJ_DiscreteVariance_StochVol.m:267
    else:
        if contract == 3:
            price=dot(exp(dot(- r,T)),Approx) / T
# PROJ_DiscreteVariance_StochVol.m:269
        else:
            fprintf('Only contract types 1 and 3 are currently supported \n')
    
    return price
    
if __name__ == '__main__':
    pass
    