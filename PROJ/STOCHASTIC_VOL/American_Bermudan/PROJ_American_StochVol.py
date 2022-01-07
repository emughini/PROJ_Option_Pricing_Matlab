# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_American_StochVol.m

    
@function
def PROJ_American_StochVol(numeric_param=None,M=None,r=None,T=None,S_0=None,W=None,psi_J=None,model=None,modparam=None,*args,**kwargs):
    varargin = PROJ_American_StochVol.varargin
    nargin = PROJ_American_StochVol.nargin

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
# W  : strike  (used instead of K)
    
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
#-------------------------------
    
    ### Note: be careful about the parameter Rho (vs rho used in algorithm)
    
    N=numeric_param.N
# PROJ_American_StochVol.m:51
    alph=numeric_param.alph
# PROJ_American_StochVol.m:52
    m_0=numeric_param.m_0
# PROJ_American_StochVol.m:53
    gridMethod=numeric_param.gridMethod
# PROJ_American_StochVol.m:54
    gamma=numeric_param.gamma
# PROJ_American_StochVol.m:55
    gridMultParam=numeric_param.gridMultParam
# PROJ_American_StochVol.m:56
    K=N / 2
# PROJ_American_StochVol.m:58
    dx=dot(2,alph) / (N - 1)
# PROJ_American_StochVol.m:59
    lws=log(W / S_0)
# PROJ_American_StochVol.m:60
    dt=T / M
# PROJ_American_StochVol.m:61
    ### GRID which aligns 0 as well as log(W/S_0)
    nnot=K / 2
# PROJ_American_StochVol.m:64
    dxtil=copy(dx)
# PROJ_American_StochVol.m:65
    
    nbar=floor(lws / dx + K / 2)
# PROJ_American_StochVol.m:66
    if abs(lws) < dxtil:
        dx=copy(dxtil)
# PROJ_American_StochVol.m:68
    else:
        if lws < 0:
            dx=lws / (1 + nbar - K / 2)
# PROJ_American_StochVol.m:70
            nbar=nbar + 1
# PROJ_American_StochVol.m:71
        else:
            if lws > 0:
                dx=lws / (nbar - K / 2)
# PROJ_American_StochVol.m:73
    
    a=1 / dx
# PROJ_American_StochVol.m:75
    xmin=dot((1 - K / 2),dx)
# PROJ_American_StochVol.m:76
    ####////////////////////////////////////////////////////////
#### Initialize THETA ... 
####////////////////////////////////////////////////////////
    THET=zeros(K,m_0)
# PROJ_American_StochVol.m:82
    
    ######  Gaussian Quad Constants
    q_plus=(1 + sqrt(3 / 5)) / 2
# PROJ_American_StochVol.m:85
    q_minus=(1 - sqrt(3 / 5)) / 2
# PROJ_American_StochVol.m:85
    b3=sqrt(15)
# PROJ_American_StochVol.m:86
    b4=b3 / 10
# PROJ_American_StochVol.m:86
    #### PAYOFF CONSTANTS-----------------------------------
    varthet_01=dot(exp(dot(0.5,dx)),(dot(5,cosh(dot(b4,dx))) - dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_American_StochVol.m:90
    varthet_m10=dot(exp(dot(- 0.5,dx)),(dot(5,cosh(dot(b4,dx))) + dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_American_StochVol.m:91
    varthet_star=varthet_01 + varthet_m10
# PROJ_American_StochVol.m:92
    #######
    Gs=zeros(K,1)
# PROJ_American_StochVol.m:95
    Gs[arange(1,nbar)]=dot(exp(xmin + dot(dx,(arange(0,nbar - 1)))),S_0)
# PROJ_American_StochVol.m:96
    #Define Terminal Theta Coeffs
    ThetM=zeros(K,1)
# PROJ_American_StochVol.m:99
    ThetM[arange(1,nbar - 1)]=W - dot(varthet_star,Gs(arange(1,nbar - 1)))
# PROJ_American_StochVol.m:100
    ThetM[nbar]=dot(W,(0.5 - varthet_m10))
# PROJ_American_StochVol.m:101
    Gs[arange(1,nbar)]=W - Gs(arange(1,nbar))
# PROJ_American_StochVol.m:102
    
    ####////////////////////////////////////////////////////////
#### Intialize Q matrix and variance set
####////////////////////////////////////////////////////////
    t=T / 2
# PROJ_American_StochVol.m:108
    lx,v0,ux=get_variance_grid_boundaries(model,modparam,t,gamma,nargout=3)
# PROJ_American_StochVol.m:109
    mu_func,sig_func=get_SV_variance_grid_diffusion_funcs(model,modparam,nargout=2)
# PROJ_American_StochVol.m:111
    boundaryMethod=1
# PROJ_American_StochVol.m:112
    center=copy(v0)
# PROJ_American_StochVol.m:114
    
    Q,v=Q_Matrix_AllForms(m_0,mu_func,sig_func,lx,ux,gridMethod,gridMultParam,center,boundaryMethod,nargout=2)
# PROJ_American_StochVol.m:116
    ####////////////////////////////////////////////////////////
#### Populate the Matrix Exponentials
####////////////////////////////////////////////////////////
    dxi=dot(dot(2,pi),a) / N
# PROJ_American_StochVol.m:121
    xi=dot(dxi,(arange(0,N - 1)).T)
# PROJ_American_StochVol.m:122
    v1,v2,fv=get_SV_matrix_expo_inputs(model,modparam,psi_J,dt,v,dxi,r,nargout=3)
# PROJ_American_StochVol.m:124
    EXP_A=get_SV_matrix_exponential(Q,dt,xi,v1,v2,fv,psi_J,m_0,N)
# PROJ_American_StochVol.m:125
    ####////////////////////////////////////////////////////////
#### Construct Toepliz Array Of Arrays
####////////////////////////////////////////////////////////
    a2=a ** 2
# PROJ_American_StochVol.m:130
    Cons2=dot(dot(24,a2),exp(dot(- r,dt))) / N
# PROJ_American_StochVol.m:131
    zmin=dot((1 - K),dx)
# PROJ_American_StochVol.m:132
    
    xi=dot(dxi,(arange(1,N - 1)))
# PROJ_American_StochVol.m:134
    
    hvec=multiply(exp(dot(dot(- 1j,zmin),xi)),(sin(xi / (dot(2,a))) / xi) ** 2.0) / (2 + cos(xi / a))
# PROJ_American_StochVol.m:135
    BETA=zeros(N,m_0,m_0)
# PROJ_American_StochVol.m:137
    
    grand=zeros(1,N - 1)
# PROJ_American_StochVol.m:138
    ### NOTE the (k,j) rather than (j,k)
    for j in arange(1,m_0).reshape(-1):
        for k in arange(1,m_0).reshape(-1):
            for n in arange(1,N - 1).reshape(-1):
                grand[n]=dot(hvec(n),EXP_A(k,j,n + 1))
# PROJ_American_StochVol.m:144
            beta=dot(Cons2,real(fft(concat([EXP_A(k,j,1) / (dot(24,a2)),grand]))))
# PROJ_American_StochVol.m:146
            toepM=concat([[beta(arange(K,1,- 1)).T],[0],[beta(arange(dot(2,K) - 1,K,- 1),+ 1).T]])
# PROJ_American_StochVol.m:147
            BETA[arange(),j,k]=fft(toepM)
# PROJ_American_StochVol.m:148
    
    ####////////////////////////////////////////////////////////
#### Initialize Continuation Value
####////////////////////////////////////////////////////////
# CONT = repmat(p(1:K),1,m_0);  #continuation value in each state (initialize with all equal)
    CONT=zeros(K,m_0)
# PROJ_American_StochVol.m:156
    ThetTemp=fft(concat([[ThetM(arange(1,K))],[zeros(K,1)]]))
# PROJ_American_StochVol.m:157
    for j in arange(1,m_0).reshape(-1):
        for k in arange(1,m_0).reshape(-1):
            p=ifft(multiply(BETA(arange(),j,k),ThetTemp))
# PROJ_American_StochVol.m:160
            CONT[arange(),j]=CONT(arange(),j) + p(arange(1,K))
# PROJ_American_StochVol.m:161
    
    ####////////////////////////////////////////////////////////
#### LOOP through time
####////////////////////////////////////////////////////////
    
    kstr_vecInit=dot(nbar,ones(m_0,1))
# PROJ_American_StochVol.m:169
    
    for m in arange(M - 2,0,- 1).reshape(-1):
        kstr_vec=copy(kstr_vecInit)
# PROJ_American_StochVol.m:172
        #Step 1: update THETA
        for j in arange(1,m_0).reshape(-1):
            while kstr_vec(j) > 2 and CONT(kstr_vec(j),j) > Gs(kstr_vec(j)):

                kstr_vec[j]=kstr_vec(j) - 1
# PROJ_American_StochVol.m:177

            if kstr_vec(j) >= 2:
                xkstr=xmin + dot((kstr_vec(j) - 1),dx)
# PROJ_American_StochVol.m:180
                Ck1=CONT(kstr_vec(j) - 1,j)
# PROJ_American_StochVol.m:182
                Ck2=CONT(kstr_vec(j),j)
# PROJ_American_StochVol.m:182
                Ck3=CONT(kstr_vec(j) + 1,j)
# PROJ_American_StochVol.m:182
                Gk2=Gs(kstr_vec(j))
# PROJ_American_StochVol.m:184
                Gk3=Gs(kstr_vec(j) + 1)
# PROJ_American_StochVol.m:184
                tmp1=Ck2 - Gk2
# PROJ_American_StochVol.m:186
                tmp2=Ck3 - Gk3
# PROJ_American_StochVol.m:186
                xstrs=(dot((xkstr + dx),tmp1) - dot(xkstr,tmp2)) / (tmp1 - tmp2)
# PROJ_American_StochVol.m:187
            else:
                kstr_vec[j]=1
# PROJ_American_StochVol.m:189
                xstrs=copy(xmin)
# PROJ_American_StochVol.m:189
                xkstr=copy(xmin)
# PROJ_American_StochVol.m:189
            rho=xstrs - xkstr
# PROJ_American_StochVol.m:192
            zeta=dot(a,rho)
# PROJ_American_StochVol.m:193
            zeta2=zeta ** 2
# PROJ_American_StochVol.m:195
            zeta3=dot(zeta,zeta2)
# PROJ_American_StochVol.m:195
            zeta4=dot(zeta,zeta3)
# PROJ_American_StochVol.m:195
            zeta_plus=dot(zeta,q_plus)
# PROJ_American_StochVol.m:196
            zeta_minus=dot(zeta,q_minus)
# PROJ_American_StochVol.m:196
            rho_plus=dot(rho,q_plus)
# PROJ_American_StochVol.m:197
            rho_minus=dot(rho,q_minus)
# PROJ_American_StochVol.m:197
            ed1=exp(rho_minus)
# PROJ_American_StochVol.m:199
            ed2=exp(rho / 2)
# PROJ_American_StochVol.m:199
            ed3=exp(rho_plus)
# PROJ_American_StochVol.m:199
            dbar_1=zeta2 / 2
# PROJ_American_StochVol.m:200
            dbar_0=zeta - dbar_1
# PROJ_American_StochVol.m:201
            d_0=dot(zeta,(dot(5,(dot((1 - zeta_minus),ed1) + dot((1 - zeta_plus),ed3))) + dot(dot(4,(2 - zeta)),ed2))) / 18
# PROJ_American_StochVol.m:202
            d_1=dot(dot(exp(- dx),zeta),(dot(5,(dot(zeta_minus,ed1) + dot(zeta_plus,ed3))) + dot(dot(4,zeta),ed2))) / 18
# PROJ_American_StochVol.m:203
            THET[arange(1,kstr_vec(j) - 1),j]=ThetM(arange(1,kstr_vec(j) - 1))
# PROJ_American_StochVol.m:205
            Ck4=CONT(kstr_vec(j) + 2,j)
# PROJ_American_StochVol.m:206
            THET[kstr_vec(j),j]=dot(W,(0.5 + dbar_0)) - dot(dot(S_0,exp(xkstr)),(varthet_m10 + d_0)) + dot(zeta4 / 8,(Ck1 - dot(2,Ck2) + Ck3)) + dot(zeta3 / 3,(Ck2 - Ck1)) + dot(zeta2 / 4,(Ck1 + dot(2,Ck2) - Ck3)) - dot(zeta,Ck2) - Ck1 / 24 + dot(5 / 12,Ck2) + Ck3 / 8
# PROJ_American_StochVol.m:208
            THET[kstr_vec(j) + 1,j]=dot(W,dbar_1) - dot(dot(S_0,exp(xkstr + dx)),d_1) + dot(zeta4 / 8,(- Ck2 + dot(2,Ck3) - Ck4)) + dot(zeta3 / 6,(dot(3,Ck2) - dot(4,Ck3) + Ck4)) - dot(dot(0.5,zeta2),Ck2) + (Ck2 + dot(10,Ck3) + Ck4) / 12
# PROJ_American_StochVol.m:213
            THET[arange(kstr_vec(j) + 2,K - 1),j]=(CONT(arange(kstr_vec(j) + 1,K - 2),j) + dot(10,CONT(arange(kstr_vec(j) + 2,K - 1),j)) + CONT(arange(kstr_vec(j) + 3,K),j)) / 12
# PROJ_American_StochVol.m:216
            THET[K,j]=(dot(13,CONT(K,j)) + dot(15,CONT(K - 1,j)) - dot(5,CONT(K - 2,j)) + CONT(K - 3,j)) / 48
# PROJ_American_StochVol.m:217
        CONT=zeros(K,m_0)
# PROJ_American_StochVol.m:221
        for k in arange(1,m_0).reshape(-1):
            ThetTemp=fft(concat([[THET(arange(1,K),k)],[zeros(K,1)]]))
# PROJ_American_StochVol.m:223
            for j in arange(1,m_0).reshape(-1):
                p=ifft(multiply(BETA(arange(),j,k),ThetTemp))
# PROJ_American_StochVol.m:225
                CONT[arange(),j]=CONT(arange(),j) + p(arange(1,K))
# PROJ_American_StochVol.m:226
    
    ####////////////////////////////////////////////////////////
#### Interpolate to find price at v0
####////////////////////////////////////////////////////////
    k_0=2
# PROJ_American_StochVol.m:235
    
    while v0 > v(k_0) and k_0 < m_0:

        k_0=k_0 + 1
# PROJ_American_StochVol.m:237

    
    k_0=k_0 - 1
# PROJ_American_StochVol.m:239
    ### Cubic spline
# k_int = [(k_0-2) (k_0-1) k_0 (k_0+1) (k_0+2)];
# v_int = [v(k_int(1)) v(k_int(2)) v(k_int(3)) v(k_int(4)) v(k_int(5))];
# Vals_int = [CONT(nnot,(k_int(1))) CONT(nnot,(k_int(2))) CONT(nnot,(k_int(3))) CONT(nnot,(k_int(4))) CONT(nnot,(k_int(5)))];
# Vals_int = max(Vals_int, Gs(nnot));
# 
# price = spline(v_int,Vals_int,v0);
    
    ### Linear Interpolation
### NOTE: we have assumed that are not in Case II (see paper.. this case occurs if 0 < ln(W/S_0) < Delta), otherwise we need 2 interpolations
    Vals_Interp=concat([max(CONT(nnot,(k_0)),Gs(nnot)),max(CONT(nnot,(k_0 + 1)),Gs(nnot))])
# PROJ_American_StochVol.m:251
    price=Vals_Interp(1) + dot((Vals_Interp(2) - Vals_Interp(1)),(v0 - v(k_0))) / (v(k_0 + 1) - v(k_0))
# PROJ_American_StochVol.m:252
    return price
    
if __name__ == '__main__':
    pass
    