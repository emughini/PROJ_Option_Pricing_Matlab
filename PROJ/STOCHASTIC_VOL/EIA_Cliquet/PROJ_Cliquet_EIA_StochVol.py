# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_Cliquet_EIA_StochVol.m

    
@function
def PROJ_Cliquet_EIA_StochVol(numeric_param=None,M=None,r=None,q=None,T=None,psi_J=None,model=None,modparam=None,contract=None,contractParams=None,*args,**kwargs):
    varargin = PROJ_Cliquet_EIA_StochVol.varargin
    nargin = PROJ_Cliquet_EIA_StochVol.nargin

    #########################################################
# About: Pricing Function for American PUT Option using CTMC Approximation + PROJ method
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
    
    # contract: 1 = sum of local caps
#           2 = sum of local caps & floors
#           3 = cliquet: local & global caps & floors
#           4 = cliquet: local floor & cap, global floor, NO GLOBAL CAP  
#           5 = MPP: ie monthly point-to-point or Monthly Cap Sum (Bernard, Li)
    
    # contractParams:
# 	K  : Strike/Notional
# 	C  : Local Cap
# 	CG : Global cap
# 	F  : Local Floor
# 	FG : Global Floor
# 
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
    
    #########################################################
    
    N=numeric_param.N
# PROJ_Cliquet_EIA_StochVol.m:62
    alph=numeric_param.alph
# PROJ_Cliquet_EIA_StochVol.m:63
    m_0=numeric_param.m_0
# PROJ_Cliquet_EIA_StochVol.m:64
    gridMethod=numeric_param.gridMethod
# PROJ_Cliquet_EIA_StochVol.m:65
    gamma=numeric_param.gamma
# PROJ_Cliquet_EIA_StochVol.m:66
    varGridMult=numeric_param.gridMultParam
# PROJ_Cliquet_EIA_StochVol.m:67
    dx=dot(2,alph) / (N - 1)
# PROJ_Cliquet_EIA_StochVol.m:69
    a=1 / dx
# PROJ_Cliquet_EIA_StochVol.m:69
    
    dt=T / M
# PROJ_Cliquet_EIA_StochVol.m:70
    xmin=dot((1 - N / 2),dx)
# PROJ_Cliquet_EIA_StochVol.m:72
    
    ### Contract Parameters (Not all of these apply to every contact type)
    K=contractParams.K
# PROJ_Cliquet_EIA_StochVol.m:75
    
    C=contractParams.C
# PROJ_Cliquet_EIA_StochVol.m:77
    
    F=contractParams.F
# PROJ_Cliquet_EIA_StochVol.m:78
    
    CG=contractParams.CG
# PROJ_Cliquet_EIA_StochVol.m:79
    
    FG=contractParams.FG
# PROJ_Cliquet_EIA_StochVol.m:80
    
    lc=log(1 + C)
# PROJ_Cliquet_EIA_StochVol.m:83
    lf=log(1 + F)
# PROJ_Cliquet_EIA_StochVol.m:84
    ### Choose xmin so that CAP lc is a member
    klc=floor(dot(a,(lc - xmin))) + 1
# PROJ_Cliquet_EIA_StochVol.m:87
    
    xklc=xmin + dot((klc - 1),dx)
# PROJ_Cliquet_EIA_StochVol.m:88
    xmin=xmin + (lc - xklc)
# PROJ_Cliquet_EIA_StochVol.m:89
    
    klf=floor(dot(a,(lf - xmin))) + 1
# PROJ_Cliquet_EIA_StochVol.m:91
    #xklf = xmin + (klf - 1)*dx;  #NOTE: defined with the new xmin
    
    if contract == 1 or contract == 5:
        hlocalCF=lambda x=None: multiply((exp(x) - 1),(x < lc)) + dot(C,(x >= lc))
# PROJ_Cliquet_EIA_StochVol.m:95
    else:
        if contract == 2 or contract == 3 or contract == 4:
            #NOTE: we should then possibly stretch the grid so that lf is a member
            if klc != klf:
                dx=(lc - lf) / (klc - klf)
# PROJ_Cliquet_EIA_StochVol.m:99
                a=1 / dx
# PROJ_Cliquet_EIA_StochVol.m:99
                xmin=lf - dot((klf - 1),dx)
# PROJ_Cliquet_EIA_StochVol.m:100
            hlocalCF=lambda x=None: dot(F,(x <= lf)) + multiply(multiply((exp(x) - 1),(x < lc)),(x > lf)) + dot(C,(x >= lc))
# PROJ_Cliquet_EIA_StochVol.m:102
    
    A=dot(32,a ** 4)
# PROJ_Cliquet_EIA_StochVol.m:105
    C_aN=A / N
# PROJ_Cliquet_EIA_StochVol.m:106
    ####////////////////////////////////////////////////////////
#### Intialize Q matrix and variance set
####////////////////////////////////////////////////////////
    t=T / 2
# PROJ_Cliquet_EIA_StochVol.m:111
    lx,v0,ux=get_variance_grid_boundaries(model,modparam,t,gamma,nargout=3)
# PROJ_Cliquet_EIA_StochVol.m:112
    mu_func,sig_func=get_SV_variance_grid_diffusion_funcs(model,modparam,nargout=2)
# PROJ_Cliquet_EIA_StochVol.m:114
    boundaryMethod=1
# PROJ_Cliquet_EIA_StochVol.m:115
    center=copy(v0)
# PROJ_Cliquet_EIA_StochVol.m:116
    
    Q,v=Q_Matrix_AllForms(m_0,mu_func,sig_func,lx,ux,gridMethod,varGridMult,center,boundaryMethod,nargout=2)
# PROJ_Cliquet_EIA_StochVol.m:118
    ####////////////////////////////////////////////////////////
#### Populate the Matrix Exponentials
####////////////////////////////////////////////////////////
    dxi=dot(dot(2,pi),a) / N
# PROJ_Cliquet_EIA_StochVol.m:123
    xi=dot(dxi,(arange(0,N - 1)).T)
# PROJ_Cliquet_EIA_StochVol.m:124
    v1,v2,fv=get_SV_matrix_expo_inputs(model,modparam,psi_J,dt,v,dxi,r,nargout=3)
# PROJ_Cliquet_EIA_StochVol.m:126
    # Compute Matrix Exponentials for each xi(j)
    EXP_A=get_SV_matrix_exponential(Q,dt,xi,v1,v2,fv,psi_J,m_0,N)
# PROJ_Cliquet_EIA_StochVol.m:128
    # ###################################################################
# ### PSI Matrix: 5-Point GAUSSIAN
# #################################################################
    if contract == 2 or contract == 3 or contract == 4:
        leftGridPoint=lf - dx
# PROJ_Cliquet_EIA_StochVol.m:134
        NNM=klc - klf + 3
# PROJ_Cliquet_EIA_StochVol.m:135
    else:
        if contract == 1 or contract == 5:
            leftGridPoint=copy(xmin)
# PROJ_Cliquet_EIA_StochVol.m:138
            NNM=klc + 1
# PROJ_Cliquet_EIA_StochVol.m:139
        else:
            #NOTE: this can be made more efficient by putting an upper bound, to reflect lc
            leftGridPoint=copy(xmin)
# PROJ_Cliquet_EIA_StochVol.m:142
            NNM=copy(N)
# PROJ_Cliquet_EIA_StochVol.m:143
    
    
    PSI=zeros(N - 1,NNM)
# PROJ_Cliquet_EIA_StochVol.m:147
    
    #### Sample
    Neta=dot(5,(NNM)) + 15
# PROJ_Cliquet_EIA_StochVol.m:150
    
    Neta5=(NNM) + 3
# PROJ_Cliquet_EIA_StochVol.m:151
    g2=sqrt(5 - dot(2,sqrt(10 / 7))) / 6
# PROJ_Cliquet_EIA_StochVol.m:152
    g3=sqrt(5 + dot(2,sqrt(10 / 7))) / 6
# PROJ_Cliquet_EIA_StochVol.m:153
    v1=dot(0.5,128) / 225
# PROJ_Cliquet_EIA_StochVol.m:154
    v2=dot(0.5,(322 + dot(13,sqrt(70)))) / 900
# PROJ_Cliquet_EIA_StochVol.m:154
    v3=dot(0.5,(322 - dot(13,sqrt(70)))) / 900
# PROJ_Cliquet_EIA_StochVol.m:154
    thet=zeros(1,Neta)
# PROJ_Cliquet_EIA_StochVol.m:156
    
    thet[dot(5,(arange(1,Neta5))) - 2]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1)))
# PROJ_Cliquet_EIA_StochVol.m:157
    thet[dot(5,(arange(1,Neta5))) - 4]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) - dot(dx,g3)
# PROJ_Cliquet_EIA_StochVol.m:158
    thet[dot(5,(arange(1,Neta5))) - 3]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) - dot(dx,g2)
# PROJ_Cliquet_EIA_StochVol.m:159
    thet[dot(5,(arange(1,Neta5))) - 1]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) + dot(dx,g2)
# PROJ_Cliquet_EIA_StochVol.m:160
    thet[dot(5,(arange(1,Neta5)))]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) + dot(dx,g3)
# PROJ_Cliquet_EIA_StochVol.m:161
    #### Weights
    sig=concat([- 1.5 - g3,- 1.5 - g2,- 1.5,- 1.5 + g2,- 1.5 + g3,- 0.5 - g3,- 0.5 - g2,- 0.5,- 0.5 + g2,- 0.5 + g3])
# PROJ_Cliquet_EIA_StochVol.m:164
    sig[arange(1,5)]=(sig(arange(1,5)) + 2) ** 3 / 6
# PROJ_Cliquet_EIA_StochVol.m:165
    sig[arange(6,10)]=2 / 3 - dot(0.5,(sig(arange(6,10))) ** 3) - (sig(arange(6,10))) ** 2
# PROJ_Cliquet_EIA_StochVol.m:166
    sig[concat([1,5,6,10])]=dot(v3,sig(concat([1,5,6,10])))
# PROJ_Cliquet_EIA_StochVol.m:168
    sig[concat([2,4,7,9])]=dot(v2,sig(concat([2,4,7,9])))
# PROJ_Cliquet_EIA_StochVol.m:168
    sig[concat([3,8])]=dot(v1,sig(concat([3,8])))
# PROJ_Cliquet_EIA_StochVol.m:168
    ##################################
###NEW STEP: multiple sig by Upsilon_{a,N}
    sig=dot(C_aN,sig)
# PROJ_Cliquet_EIA_StochVol.m:172
    
    ##################################
#### Fill Matrix
#### NOTE: this can be made MORE EFFICIENT by using symmetery of x^2
    
    #zz  = exp(1i*dxi*log(1+exp(thet)));
#zz  = exp(1i*dxi*thet.^2); ## in general, 1i*dxh(thet)
    zz=exp(dot(dot(1j,dxi),hlocalCF(thet)))
# PROJ_Cliquet_EIA_StochVol.m:180
    thet=copy(zz)
# PROJ_Cliquet_EIA_StochVol.m:181
    for j in arange(1,N - 1).reshape(-1):
        PSI[j,arange()]=dot(sig(1),(thet(arange(1,Neta - 19,5)) + thet(arange(20,Neta,5)))) + dot(sig(2),(thet(arange(2,Neta - 18,5)) + thet(arange(19,Neta - 1,5)))) + dot(sig(3),(thet(arange(3,Neta - 17,5)) + thet(arange(18,Neta - 2,5)))) + dot(sig(4),(thet(arange(4,Neta - 16,5)) + thet(arange(17,Neta - 3,5)))) + dot(sig(5),(thet(arange(5,Neta - 15,5)) + thet(arange(16,Neta - 4,5)))) + dot(sig(6),(thet(arange(6,Neta - 14,5)) + thet(arange(15,Neta - 5,5)))) + dot(sig(7),(thet(arange(7,Neta - 13,5)) + thet(arange(14,Neta - 6,5)))) + dot(sig(8),(thet(arange(8,Neta - 12,5)) + thet(arange(13,Neta - 7,5)))) + dot(sig(9),(thet(arange(9,Neta - 11,5)) + thet(arange(12,Neta - 8,5)))) + dot(sig(10),(thet(arange(10,Neta - 10,5)) + thet(arange(11,Neta - 9,5))))
# PROJ_Cliquet_EIA_StochVol.m:184
        thet=multiply(thet,zz)
# PROJ_Cliquet_EIA_StochVol.m:195
    
    # ###################################################################
# ### Find phi_{Y_1}
# #################################################################
    xi=dot(dxi,(arange(1,N - 1)).T)
# PROJ_Cliquet_EIA_StochVol.m:202
    
    b0=1208 / 2520
# PROJ_Cliquet_EIA_StochVol.m:204
    b1=1191 / 2520
# PROJ_Cliquet_EIA_StochVol.m:204
    b2=120 / 2520
# PROJ_Cliquet_EIA_StochVol.m:204
    b3=1 / 2520
# PROJ_Cliquet_EIA_StochVol.m:204
    zeta=(sin(xi / (dot(2,a))) / xi) ** 4.0 / (b0 + dot(b1,cos(xi / a)) + dot(b2,cos(dot(2,xi) / a)) + dot(b3,cos(dot(3,xi) / a)))
# PROJ_Cliquet_EIA_StochVol.m:205
    hvec=multiply(exp(dot(dot(- 1j,xmin),xi)),zeta)
# PROJ_Cliquet_EIA_StochVol.m:206
    
    PHIY_old=zeros(N - 1,m_0)
# PROJ_Cliquet_EIA_StochVol.m:208
    PHIY_new=zeros(N - 1,m_0)
# PROJ_Cliquet_EIA_StochVol.m:209
    
    #BetaTemp = zeros(N,1);
    PHI=zeros(m_0,m_0,N - 1)
# PROJ_Cliquet_EIA_StochVol.m:211
    grand=zeros(N - 1,1)
# PROJ_Cliquet_EIA_StochVol.m:212
    
    expFxi=exp(dot(dot(1j,F),xi))
# PROJ_Cliquet_EIA_StochVol.m:214
    expCxi=exp(dot(dot(1j,C),xi))
# PROJ_Cliquet_EIA_StochVol.m:215
    if contract == 2 or contract == 3 or contract == 4:
        for j in arange(1,m_0).reshape(-1):
            #Step 1: characteristic function of log return
            for n in arange(1,N - 1).reshape(-1):
                PHIY_old[n,j]=sum(EXP_A(arange(1,m_0),j,n + 1))
# PROJ_Cliquet_EIA_StochVol.m:221
            #Step 2: invert characteristic function of log return (ie this is beta)
            BetaTemp=real(fft(concat([[1 / A],[multiply(PHIY_old(arange(),j),hvec)]])))
# PROJ_Cliquet_EIA_StochVol.m:224
            #Step 3: Phi_{Y_1}^j
            PHIY_new[arange(),j]=dot(PSI,BetaTemp(arange(klf - 1,klc + 1)))
# PROJ_Cliquet_EIA_StochVol.m:227
            sumBetaLeft=dot(C_aN,sum(BetaTemp(arange(1,klf - 2))))
# PROJ_Cliquet_EIA_StochVol.m:229
            sumBetaRight=1 - sumBetaLeft - dot(C_aN,sum(BetaTemp(arange(klf - 1,klc + 1))))
# PROJ_Cliquet_EIA_StochVol.m:230
            PHIY_new[arange(),j]=PHIY_new(arange(),j) + dot(expFxi,sumBetaLeft) + dot(expCxi,sumBetaRight)
# PROJ_Cliquet_EIA_StochVol.m:231
        # Define xiBig so that it can be added to a 3D matrix
        xiBigF=zeros(1,1,N - 1)
# PROJ_Cliquet_EIA_StochVol.m:235
        xiBigC=zeros(1,1,N - 1)
# PROJ_Cliquet_EIA_StochVol.m:236
        xiBigF[1,1,arange()]=expFxi
# PROJ_Cliquet_EIA_StochVol.m:237
        xiBigC[1,1,arange()]=expCxi
# PROJ_Cliquet_EIA_StochVol.m:238
        if M > 1:
            for j in arange(1,m_0).reshape(-1):
                for k in arange(1,m_0).reshape(-1):
                    #First Invert chf to get p_{j,k}
                    for n in arange(1,N - 1).reshape(-1):
                        grand[n]=dot(hvec(n),EXP_A(k,j,n + 1))
# PROJ_Cliquet_EIA_StochVol.m:246
                    BetaTemp=real(fft(concat([[EXP_A(k,j,1) / A],[grand]])))
# PROJ_Cliquet_EIA_StochVol.m:248
                    PHI[j,k,arange()]=dot(PSI,BetaTemp(arange(klf - 1,klc + 1)))
# PROJ_Cliquet_EIA_StochVol.m:250
                    sumBetaLeft=dot(C_aN,sum(BetaTemp(arange(1,klf - 2))))
# PROJ_Cliquet_EIA_StochVol.m:251
                    sumBetaRight=dot(C_aN,sum(BetaTemp(arange(klc + 2,N))))
# PROJ_Cliquet_EIA_StochVol.m:252
                    PHI[j,k,arange()]=PHI(j,k,arange()) + dot(xiBigF,sumBetaLeft) + dot(xiBigC,sumBetaRight)
# PROJ_Cliquet_EIA_StochVol.m:254
    else:
        if contract == 5:
            ### ADD CODE
            fprintf('-------------------------------\n')
            fprintf('NOTE: HAVENT ADDED CODE FOR THIS CONTRACT\n\n\n')
            fprintf('-------------------------------\n')
    
    #Main Recursion
    for m in arange(2,M).reshape(-1):
        for n in arange(1,N - 1).reshape(-1):
            PHIY_new[n,arange()]=dot(PHIY_new(n,arange()),PHI(arange(),arange(),n).T)
# PROJ_Cliquet_EIA_StochVol.m:268
    
    ##########################################################################
##########################################################################
### Redfine ymin for the final inversion
    
    #REDO FOR contract == 2 or ==3
    if contract == 1 or contract == 2:
        ymin=dot(M,(exp(dot((r - q),dt)) - 1)) + dot((1 - N / 2),dx)
# PROJ_Cliquet_EIA_StochVol.m:279
        grid=ymin + dot(dx,(arange(0,N - 1)))
# PROJ_Cliquet_EIA_StochVol.m:280
    else:
        if contract == 3:
            CminusF=CG - FG
# PROJ_Cliquet_EIA_StochVol.m:283
            ymin=FG - dx
# PROJ_Cliquet_EIA_StochVol.m:284
            kc=floor(dot(a,(CG - ymin))) + 1
# PROJ_Cliquet_EIA_StochVol.m:285
            z=dot(a,(CG - (ymin + dot((kc - 1),dx))))
# PROJ_Cliquet_EIA_StochVol.m:286
            z2=z ** 2
# PROJ_Cliquet_EIA_StochVol.m:287
            z3=dot(z,z2)
# PROJ_Cliquet_EIA_StochVol.m:287
            z4=dot(z,z3)
# PROJ_Cliquet_EIA_StochVol.m:287
            z5=dot(z,z4)
# PROJ_Cliquet_EIA_StochVol.m:287
            theta=zeros(1,N / 2)
# PROJ_Cliquet_EIA_StochVol.m:289
            theta[1]=dx / 120
# PROJ_Cliquet_EIA_StochVol.m:290
            theta[2]=dot(dx,7) / 30
# PROJ_Cliquet_EIA_StochVol.m:291
            theta[3]=dot(dx,121) / 120
# PROJ_Cliquet_EIA_StochVol.m:292
            theta[arange(4,kc - 2)]=dot(dx,(arange(2,kc - 4)))
# PROJ_Cliquet_EIA_StochVol.m:293
            k=kc - 1
# PROJ_Cliquet_EIA_StochVol.m:294
            theta[k]=dot(dx,(dot(k,(- z4 / 24 + z3 / 6 - z2 / 4 + z / 6 + 23 / 24)) - z5 / 30 + z4 / 6 - z3 / 3 + z2 / 3 - z / 6 - 59 / 30)) + dot(CminusF,(z - 1) ** 4) / 24
# PROJ_Cliquet_EIA_StochVol.m:295
            k=copy(kc)
# PROJ_Cliquet_EIA_StochVol.m:297
            theta[k]=dot(dx,(dot(k,(z4 / 8 - z3 / 3 + dot(2,z) / 3 + 0.5)) + z5 / 10 - z4 / 2 + dot(2,z3) / 3 + z2 / 3 - dot(4,z) / 3 - 37 / 30)) + dot(CminusF,(- z4 / 8 + z3 / 3 - dot(2,z) / 3 + 1 / 2))
# PROJ_Cliquet_EIA_StochVol.m:298
            k=kc + 1
# PROJ_Cliquet_EIA_StochVol.m:300
            theta[k]=dot(dx,(dot(k,(- z4 / 8 + z3 / 6 + z2 / 4 + z / 6 + 1 / 24)) - z5 / 10 + z4 / 2 - z3 / 3 - dot(2,z2) / 3 - z / 2 - 2 / 15)) + dot(CminusF,(0.5 + dot(1 / 24,(dot(3,z4) - dot(4,z3) - dot(6,z2) - dot(4,z) + 11))))
# PROJ_Cliquet_EIA_StochVol.m:301
            k=kc + 2
# PROJ_Cliquet_EIA_StochVol.m:303
            theta[k]=dot(dx,(z5 / 30 + dot((k - 4),z4) / 24)) + dot(CminusF,(1 - z4 / 24))
# PROJ_Cliquet_EIA_StochVol.m:304
            theta[arange(kc + 3,N / 2)]=CminusF
# PROJ_Cliquet_EIA_StochVol.m:305
        else:
            if contract == 4 or contract == 5:
                ymin=FG - dx
# PROJ_Cliquet_EIA_StochVol.m:308
                theta=zeros(1,N / 2)
# PROJ_Cliquet_EIA_StochVol.m:309
                theta[1]=dx / 120
# PROJ_Cliquet_EIA_StochVol.m:310
                theta[2]=dot(dx,7) / 30
# PROJ_Cliquet_EIA_StochVol.m:311
                theta[3]=dot(dx,121) / 120
# PROJ_Cliquet_EIA_StochVol.m:312
                theta[arange(4,N / 2)]=dot(dx,(arange(2,N / 2 - 2)))
# PROJ_Cliquet_EIA_StochVol.m:313
    
    ### Test with FILTER
    applyFilter=0
# PROJ_Cliquet_EIA_StochVol.m:318
    if applyFilter == 1:
        epsM=1.2204e-16
# PROJ_Cliquet_EIA_StochVol.m:320
        alphaeps=- log(epsM)
# PROJ_Cliquet_EIA_StochVol.m:321
        pp=2
# PROJ_Cliquet_EIA_StochVol.m:322
        filter=exp(dot(- alphaeps,(xi / (dot(dot(2,pi),a))) ** pp))
# PROJ_Cliquet_EIA_StochVol.m:323
        hvec=multiply(multiply(filter,exp(dot(dot(- 1j,ymin),xi))),zeta)
# PROJ_Cliquet_EIA_StochVol.m:324
    else:
        hvec=multiply(exp(dot(dot(- 1j,ymin),xi)),zeta)
# PROJ_Cliquet_EIA_StochVol.m:326
    
    # # #### Plot PHI #####h = figure;
# h = figure;
# set(h,'defaultTextInterpreter','latex');
# dualGrand = .5*32*a^4*phi(2:N/1).*zeta(1:N/1-1);
# xGrid = [0; xi(1:N/1-1)];
# #plot(xGrid, abs([1; phi(2:N/1)]), xGrid, abs([1; dualGrand]), '--')
# p = plot(xGrid, abs([1; phi(2:N/1)]),'g', xGrid, abs([1; dualGrand]), 'r--', xGrid, abs([1; dualGrand.*filter]), 'b:');
# set(p,'MarkerSize',5,'LineWidth',1.1);
# ylabel('$|$Integrand$|$','Interpreter','LaTex')
# xlabel('$\xi$','Interpreter','LaTex')
# legend({'ChF','DualChF','Filtered'},'Interpreter','LaTex')
# ###plot(abs(dualGrand.*filter))
# ###plot(.5*32*a^4*zeta)
    
    #BetaTemp = real(fft([1/A; hvec.*PHIY_new(:,1)])); 
# ######
# grid = ymin + dx*(0:N-1); #defined here only for plotting (grid is defined above in case of contract 1 or 2)
# plot(grid,C_aN*BetaTemp)
# ######
    
    ####////////////////////////////////////////////////////////
#### Interpolate to find bracketing initial volatilities
####////////////////////////////////////////////////////////
    k_0=2
# PROJ_Cliquet_EIA_StochVol.m:354
    
    while v0 >= v(k_0) and k_0 < m_0:

        k_0=k_0 + 1
# PROJ_Cliquet_EIA_StochVol.m:356

    
    k_0=k_0 - 1
# PROJ_Cliquet_EIA_StochVol.m:358
    vals=concat([0,0])
# PROJ_Cliquet_EIA_StochVol.m:359
    ks=concat([k_0,k_0 + 1])
# PROJ_Cliquet_EIA_StochVol.m:360
    if contract == 1 or contract == 2:
        BetaTemp=real(fft(concat([[1 / A],[multiply(hvec,PHIY_new(arange(),ks(1)))]])))
# PROJ_Cliquet_EIA_StochVol.m:363
        vals[1]=dot(dot(dot(dot(K,exp(dot(- r,T))),C_aN),grid(arange(1,N))),BetaTemp(arange(1,N)))
# PROJ_Cliquet_EIA_StochVol.m:364
        BetaTemp=real(fft(concat([[1 / A],[multiply(hvec,PHIY_new(arange(),ks(2)))]])))
# PROJ_Cliquet_EIA_StochVol.m:366
        vals[2]=dot(dot(dot(dot(K,exp(dot(- r,T))),C_aN),grid(arange(1,N))),BetaTemp(arange(1,N)))
# PROJ_Cliquet_EIA_StochVol.m:367
    else:
        if contract == 3 or contract == 4 or contract == 5:
            BetaTemp=real(fft(concat([[1 / A],[multiply(hvec,PHIY_new(arange(),ks(1)))]])))
# PROJ_Cliquet_EIA_StochVol.m:370
            vals[1]=dot(dot(K,exp(dot(- r,T))),(FG + dot(dot(C_aN,theta),BetaTemp(arange(1,N / 2)))))
# PROJ_Cliquet_EIA_StochVol.m:371
            BetaTemp=real(fft(concat([[1 / A],[multiply(hvec,PHIY_new(arange(),ks(2)))]])))
# PROJ_Cliquet_EIA_StochVol.m:373
            vals[2]=dot(dot(K,exp(dot(- r,T))),(FG + dot(dot(C_aN,theta),BetaTemp(arange(1,N / 2)))))
# PROJ_Cliquet_EIA_StochVol.m:374
    
    #Linear Interpolation
    if gridMethod == 5 or gridMethod == 6:
        price=vals(1)
# PROJ_Cliquet_EIA_StochVol.m:379
    else:
        price=vals(1) + dot((vals(2) - vals(1)),(v0 - v(k_0))) / (v(k_0 + 1) - v(k_0))
# PROJ_Cliquet_EIA_StochVol.m:381
    
    return price
    
if __name__ == '__main__':
    pass
    