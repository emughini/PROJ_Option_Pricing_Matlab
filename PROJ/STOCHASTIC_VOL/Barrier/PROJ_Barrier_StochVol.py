# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_Barrier_StochVol.m

    
@function
def PROJ_Barrier_StochVol(numeric_param=None,call=None,down=None,S_0=None,W=None,H=None,M=None,r=None,T=None,psi_J=None,model=None,modparam=None,*args,**kwargs):
    varargin = PROJ_Barrier_StochVol.varargin
    nargin = PROJ_Barrier_StochVol.nargin

    #########################################################
# About: Pricing Function for Barrier Options using CTMC Approximation + PROJ method
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
# H  : Barrier (either up and out, or down and out... No double barrier yet
# call : 1 for a call, else a put (easily can add digitals, etc)
# down : 1 for down-and-out, else up and out
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
    
    N=numeric_param.N
# PROJ_Barrier_StochVol.m:53
    alph=numeric_param.alph
# PROJ_Barrier_StochVol.m:54
    m_0=numeric_param.m_0
# PROJ_Barrier_StochVol.m:55
    gridMethod=numeric_param.gridMethod
# PROJ_Barrier_StochVol.m:56
    gamma=numeric_param.gamma
# PROJ_Barrier_StochVol.m:57
    gridMultParam=numeric_param.gridMultParam
# PROJ_Barrier_StochVol.m:58
    K=N / 2
# PROJ_Barrier_StochVol.m:60
    dx=dot(2,alph) / (N - 1)
# PROJ_Barrier_StochVol.m:61
    a=1 / dx
# PROJ_Barrier_StochVol.m:61
    lws=log(W / S_0)
# PROJ_Barrier_StochVol.m:62
    dt=T / M
# PROJ_Barrier_StochVol.m:63
    ######  Gaussian Quad Constants
    q_plus=(1 + sqrt(3 / 5)) / 2
# PROJ_Barrier_StochVol.m:66
    q_minus=(1 - sqrt(3 / 5)) / 2
# PROJ_Barrier_StochVol.m:66
    b3=sqrt(15)
# PROJ_Barrier_StochVol.m:67
    b4=b3 / 10
# PROJ_Barrier_StochVol.m:67
    #### PAYOFF CONSTANTS-----------------------------------
    varthet_01=dot(exp(dot(0.5,dx)),(dot(5,cosh(dot(b4,dx))) - dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Barrier_StochVol.m:70
    varthet_m10=dot(exp(dot(- 0.5,dx)),(dot(5,cosh(dot(b4,dx))) + dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Barrier_StochVol.m:71
    varthet_star=varthet_01 + varthet_m10
# PROJ_Barrier_StochVol.m:72
    ####////////////////////////////////////////////////////////
#### INITIALIZE LOG ASSET GRIDS (value grids)
####////////////////////////////////////////////////////////
    if down == 1:
        l=log(H / S_0)
# PROJ_Barrier_StochVol.m:78
        xmin=copy(l)
# PROJ_Barrier_StochVol.m:79
        nnot=floor(1 - dot(xmin,a))
# PROJ_Barrier_StochVol.m:80
        dx=l / (1 - nnot)
# PROJ_Barrier_StochVol.m:81
        a=1 / dx
# PROJ_Barrier_StochVol.m:81
    else:
        lws=log(W / S_0)
# PROJ_Barrier_StochVol.m:83
        u=log(H / S_0)
# PROJ_Barrier_StochVol.m:84
        nnot=floor(K - dot(a,u))
# PROJ_Barrier_StochVol.m:85
        dx=u / (K - nnot)
# PROJ_Barrier_StochVol.m:86
        a=1 / dx
# PROJ_Barrier_StochVol.m:87
        xmin=u - dot((K - 1),dx)
# PROJ_Barrier_StochVol.m:88
    
    nbar=floor(dot(a,(lws - xmin)) + 1)
# PROJ_Barrier_StochVol.m:91
    rho=lws - (xmin + dot((nbar - 1),dx))
# PROJ_Barrier_StochVol.m:92
    zeta=dot(a,rho)
# PROJ_Barrier_StochVol.m:93
    ####////////////////////////////////////////////////////////
#### Intialize Q matrix and variance set
####////////////////////////////////////////////////////////
    
    t=T / 2
# PROJ_Barrier_StochVol.m:99
    lx,v0,ux=get_variance_grid_boundaries(model,modparam,t,gamma,nargout=3)
# PROJ_Barrier_StochVol.m:100
    mu_func,sig_func=get_SV_variance_grid_diffusion_funcs(model,modparam,nargout=2)
# PROJ_Barrier_StochVol.m:102
    boundaryMethod=1
# PROJ_Barrier_StochVol.m:103
    center=copy(v0)
# PROJ_Barrier_StochVol.m:104
    
    Q,v=Q_Matrix_AllForms(m_0,mu_func,sig_func,lx,ux,gridMethod,gridMultParam,center,boundaryMethod,nargout=2)
# PROJ_Barrier_StochVol.m:106
    ####////////////////////////////////////////////////////////
#### Populate the Matrix Exponentials
####////////////////////////////////////////////////////////
    
    dxi=dot(dot(2,pi),a) / N
# PROJ_Barrier_StochVol.m:112
    xi=dot(dxi,(arange(0,N - 1)).T)
# PROJ_Barrier_StochVol.m:113
    v1,v2,fv=get_SV_matrix_expo_inputs(model,modparam,psi_J,dt,v,dxi,r,nargout=3)
# PROJ_Barrier_StochVol.m:115
    EXP_A=get_SV_matrix_exponential(Q,dt,xi,v1,v2,fv,psi_J,m_0,N)
# PROJ_Barrier_StochVol.m:116
    ####////////////////////////////////////////////////////////
#### Construct Toepliz Array Of Arrays
####////////////////////////////////////////////////////////
    a2=a ** 2
# PROJ_Barrier_StochVol.m:121
    Cons2=dot(dot(24,a2),exp(dot(- r,dt))) / N
# PROJ_Barrier_StochVol.m:122
    zmin=dot((1 - K),dx)
# PROJ_Barrier_StochVol.m:123
    
    xi=dot(dxi,(arange(1,N - 1)))
# PROJ_Barrier_StochVol.m:125
    
    hvec=multiply(exp(dot(dot(- 1j,zmin),xi)),(sin(xi / (dot(2,a))) / xi) ** 2.0) / (2 + cos(xi / a))
# PROJ_Barrier_StochVol.m:126
    BETA=zeros(N,m_0,m_0)
# PROJ_Barrier_StochVol.m:128
    
    grand=zeros(1,N - 1)
# PROJ_Barrier_StochVol.m:129
    ### NOTE the (k,j) rather than (j,k)
    for j in arange(1,m_0).reshape(-1):
        for k in arange(1,m_0).reshape(-1):
            for n in arange(1,N - 1).reshape(-1):
                grand[n]=dot(hvec(n),EXP_A(k,j,n + 1))
# PROJ_Barrier_StochVol.m:135
            beta=dot(Cons2,real(fft(concat([EXP_A(k,j,1) / (dot(24,a2)),grand]))))
# PROJ_Barrier_StochVol.m:137
            toepM=concat([[beta(arange(K,1,- 1)).T],[0],[beta(arange(dot(2,K) - 1,K,- 1),+ 1).T]])
# PROJ_Barrier_StochVol.m:138
            BETA[arange(),j,k]=fft(toepM)
# PROJ_Barrier_StochVol.m:139
    
    ####////////////////////////////////////////////////////////
#### Initialiaze THETA (based on terminal payoff)
####////////////////////////////////////////////////////////
    if down == 1:
        if call == 1:
            sigma=1 - zeta
# PROJ_Barrier_StochVol.m:148
            sigma_plus=dot((q_plus - 0.5),sigma)
# PROJ_Barrier_StochVol.m:148
            sigma_minus=dot((q_minus - 0.5),sigma)
# PROJ_Barrier_StochVol.m:148
            es1=exp(dot(dx,sigma_plus))
# PROJ_Barrier_StochVol.m:149
            es2=exp(dot(dx,sigma_minus))
# PROJ_Barrier_StochVol.m:149
            dbar_0=0.5 + dot(zeta,(dot(0.5,zeta) - 1))
# PROJ_Barrier_StochVol.m:151
            dbar_1=dot(sigma,(1 - dot(0.5,sigma)))
# PROJ_Barrier_StochVol.m:152
            d_0=dot(dot(exp(dot((rho + dx),0.5)),sigma ** 2) / 18,(dot(5,(dot((1 - q_minus),es2) + dot((1 - q_plus),es1))) + 4))
# PROJ_Barrier_StochVol.m:153
            d_1=dot(dot(exp(dot((rho - dx),0.5)),sigma) / 18,(dot(5,(dot((dot(0.5,(zeta + 1)) + sigma_minus),es2) + dot((dot(0.5,(zeta + 1)) + sigma_plus),es1))) + dot(4,(zeta + 1))))
# PROJ_Barrier_StochVol.m:154
            THET=zeros(K,m_0)
# PROJ_Barrier_StochVol.m:157
            THET[nbar,1]=dot(W,(dot(exp(- rho),d_0) - dbar_0))
# PROJ_Barrier_StochVol.m:158
            THET[nbar + 1,1]=dot(W,(dot(exp(dx - rho),(varthet_01 + d_1)) - (0.5 + dbar_1)))
# PROJ_Barrier_StochVol.m:159
            THET[arange(nbar + 2,K),1]=dot(dot(exp(xmin + dot(dx,(arange(nbar + 1,K - 1)))),S_0),varthet_star) - W
# PROJ_Barrier_StochVol.m:160
        else:
            zeta_plus=dot(zeta,q_plus)
# PROJ_Barrier_StochVol.m:163
            zeta_minus=dot(zeta,q_minus)
# PROJ_Barrier_StochVol.m:163
            rho_plus=dot(rho,q_plus)
# PROJ_Barrier_StochVol.m:164
            rho_minus=dot(rho,q_minus)
# PROJ_Barrier_StochVol.m:164
            ed1=exp(rho_minus)
# PROJ_Barrier_StochVol.m:165
            ed2=exp(rho / 2)
# PROJ_Barrier_StochVol.m:165
            ed3=exp(rho_plus)
# PROJ_Barrier_StochVol.m:165
            dbar_1=zeta ** 2 / 2
# PROJ_Barrier_StochVol.m:167
            dbar_0=zeta - dbar_1
# PROJ_Barrier_StochVol.m:168
            d_0=dot(zeta,(dot(5,(dot((1 - zeta_minus),ed1) + dot((1 - zeta_plus),ed3))) + dot(dot(4,(2 - zeta)),ed2))) / 18
# PROJ_Barrier_StochVol.m:169
            d_1=dot(zeta,(dot(5,(dot(zeta_minus,ed1) + dot(zeta_plus,ed3))) + dot(dot(4,zeta),ed2))) / 18
# PROJ_Barrier_StochVol.m:170
            THET=zeros(K,m_0)
# PROJ_Barrier_StochVol.m:173
            THET[1,1]=W / 2 - dot(H,varthet_01)
# PROJ_Barrier_StochVol.m:174
            THET[arange(2,nbar - 1),1]=W - dot(dot(exp(xmin + dot(dx,(arange(1,nbar - 2)))),S_0),varthet_star)
# PROJ_Barrier_StochVol.m:175
            THET[nbar,1]=dot(W,(0.5 + dbar_0 - dot(exp(- rho),(varthet_m10 + d_0))))
# PROJ_Barrier_StochVol.m:176
            THET[nbar + 1,1]=dot(W,(dbar_1 - dot(exp(- rho),d_1)))
# PROJ_Barrier_StochVol.m:177
    else:
        if call == 1:
            sigma=1 - zeta
# PROJ_Barrier_StochVol.m:181
            sigma_plus=dot((q_plus - 0.5),sigma)
# PROJ_Barrier_StochVol.m:181
            sigma_minus=dot((q_minus - 0.5),sigma)
# PROJ_Barrier_StochVol.m:181
            es1=exp(dot(dx,sigma_plus))
# PROJ_Barrier_StochVol.m:182
            es2=exp(dot(dx,sigma_minus))
# PROJ_Barrier_StochVol.m:182
            dbar_0=0.5 + dot(zeta,(dot(0.5,zeta) - 1))
# PROJ_Barrier_StochVol.m:184
            dbar_1=dot(sigma,(1 - dot(0.5,sigma)))
# PROJ_Barrier_StochVol.m:185
            d_0=dot(dot(exp(dot((rho + dx),0.5)),sigma ** 2) / 18,(dot(5,(dot((1 - q_minus),es2) + dot((1 - q_plus),es1))) + 4))
# PROJ_Barrier_StochVol.m:186
            d_1=dot(dot(exp(dot((rho - dx),0.5)),sigma) / 18,(dot(5,(dot((dot(0.5,(zeta + 1)) + sigma_minus),es2) + dot((dot(0.5,(zeta + 1)) + sigma_plus),es1))) + dot(4,(zeta + 1))))
# PROJ_Barrier_StochVol.m:187
            THET=zeros(K,m_0)
# PROJ_Barrier_StochVol.m:190
            THET[nbar,1]=dot(W,(dot(exp(- rho),d_0) - dbar_0))
# PROJ_Barrier_StochVol.m:191
            THET[nbar + 1,1]=dot(W,(dot(exp(dx - rho),(varthet_01 + d_1)) - (0.5 + dbar_1)))
# PROJ_Barrier_StochVol.m:192
            THET[arange(nbar + 2,K - 1),1]=dot(dot(exp(xmin + dot(dx,(arange(nbar + 1,K - 2)))),S_0),varthet_star) - W
# PROJ_Barrier_StochVol.m:193
            THET[K,1]=dot(H,varthet_m10) - dot(0.5,W)
# PROJ_Barrier_StochVol.m:194
        else:
            zeta_plus=dot(zeta,q_plus)
# PROJ_Barrier_StochVol.m:197
            zeta_minus=dot(zeta,q_minus)
# PROJ_Barrier_StochVol.m:197
            rho_plus=dot(rho,q_plus)
# PROJ_Barrier_StochVol.m:198
            rho_minus=dot(rho,q_minus)
# PROJ_Barrier_StochVol.m:198
            ed1=exp(rho_minus)
# PROJ_Barrier_StochVol.m:199
            ed2=exp(rho / 2)
# PROJ_Barrier_StochVol.m:199
            ed3=exp(rho_plus)
# PROJ_Barrier_StochVol.m:199
            dbar_1=zeta ** 2 / 2
# PROJ_Barrier_StochVol.m:201
            dbar_0=zeta - dbar_1
# PROJ_Barrier_StochVol.m:202
            d_0=dot(zeta,(dot(5,(dot((1 - zeta_minus),ed1) + dot((1 - zeta_plus),ed3))) + dot(dot(4,(2 - zeta)),ed2))) / 18
# PROJ_Barrier_StochVol.m:203
            d_1=dot(zeta,(dot(5,(dot(zeta_minus,ed1) + dot(zeta_plus,ed3))) + dot(dot(4,zeta),ed2))) / 18
# PROJ_Barrier_StochVol.m:204
            THET=zeros(K,m_0)
# PROJ_Barrier_StochVol.m:207
            THET[arange(1,nbar - 1),1]=W - dot(dot(exp(xmin + dot(dx,(arange(0,nbar - 2)))),S_0),varthet_star)
# PROJ_Barrier_StochVol.m:208
            THET[nbar,1]=dot(W,(0.5 + dbar_0 - dot(exp(- rho),(varthet_m10 + d_0))))
# PROJ_Barrier_StochVol.m:209
            THET[nbar + 1,1]=dot(W,(dbar_1 - dot(exp(- rho),d_1)))
# PROJ_Barrier_StochVol.m:210
    
    ######################################
### Initialize Continuation Value
######################################
    CONT=zeros(K,m_0)
# PROJ_Barrier_StochVol.m:218
    ### Note: First column of THET used to store ThetM at intialization
    ThetTemp=fft(concat([[THET(arange(1,K),1)],[zeros(K,1)]]))
# PROJ_Barrier_StochVol.m:220
    for j in arange(1,m_0).reshape(-1):
        for k in arange(1,m_0).reshape(-1):
            p=ifft(multiply(BETA(arange(),j,k),ThetTemp))
# PROJ_Barrier_StochVol.m:223
            CONT[arange(),j]=CONT(arange(),j) + p(arange(1,K))
# PROJ_Barrier_StochVol.m:224
    
    ######################################
### LOOP through time
######################################
    for m in arange(M - 2,0,- 1).reshape(-1):
        #Step 1: update THETA
        for j in arange(1,m_0).reshape(-1):
            THET[1,j]=(dot(13,CONT(1,j)) + dot(15,CONT(2,j)) - dot(5,CONT(3,j)) + CONT(4,j)) / 48
# PROJ_Barrier_StochVol.m:234
            THET[K,j]=(dot(13,CONT(K,j)) + dot(15,CONT(K - 1,j)) - dot(5,CONT(K - 2,j)) + CONT(K - 3,j)) / 48
# PROJ_Barrier_StochVol.m:235
            THET[arange(2,K - 1),j]=(CONT(arange(1,K - 2),j) + dot(10,CONT(arange(2,K - 1),j)) + CONT(arange(3,K),j)) / 12
# PROJ_Barrier_StochVol.m:236
        #Step 2: sum up the convolutions
        CONT=zeros(K,m_0)
# PROJ_Barrier_StochVol.m:240
        for k in arange(1,m_0).reshape(-1):
            ThetTemp=fft(concat([[THET(arange(1,K),k)],[zeros(K,1)]]))
# PROJ_Barrier_StochVol.m:242
            for j in arange(1,m_0).reshape(-1):
                p=ifft(multiply(BETA(arange(),j,k),ThetTemp))
# PROJ_Barrier_StochVol.m:244
                CONT[arange(),j]=CONT(arange(),j) + p(arange(1,K))
# PROJ_Barrier_StochVol.m:245
    
    ######################################
# Interpolate to find price at v0
######################################
    k_0=2
# PROJ_Barrier_StochVol.m:253
    
    while v0 > v(k_0) and k_0 < m_0:

        k_0=k_0 + 1
# PROJ_Barrier_StochVol.m:255

    
    k_0=k_0 - 1
# PROJ_Barrier_StochVol.m:257
    ### Cubic Interpolation
# k_int = [(k_0-1) k_0 (k_0+1)];
# v_int = [v(k_int(1)) v(k_int(2)) v(k_int(3))];
# Vals_int = [CONT(nnot,(k_int(1))) CONT(nnot,(k_int(2))) CONT(nnot,(k_int(3)))];
# Val = spline(v_int,Vals_int,v0);
    
    ### Linear Interpolation (w.r.t initial regime)
    Vals_Interp=concat([CONT(nnot,(k_0)),CONT(nnot,(k_0 + 1))])
# PROJ_Barrier_StochVol.m:266
    
    price=Vals_Interp(1) + dot((Vals_Interp(2) - Vals_Interp(1)),(v0 - v(k_0))) / (v(k_0 + 1) - v(k_0))
# PROJ_Barrier_StochVol.m:267
    return price
    
if __name__ == '__main__':
    pass
    
    