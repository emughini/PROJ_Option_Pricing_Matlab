# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_GMDB_DCA_Fast.m

    
@function
def PROJ_GMDB_DCA_Fast(proj_params=None,S_0=None,gmdb_params=None,r=None,q=None,modelInput=None,*args,**kwargs):
    varargin = PROJ_GMDB_DCA_Fast.varargin
    nargin = PROJ_GMDB_DCA_Fast.nargin

    #########################################################
# About: Pricing Function for DCA-Style Garuanteed Minimum Withdraw Benefit (GMWB) using PROJ method
#        This version is based on a dollar cost average style investment account (see reference below)
    
    # Terminal Payoff:  Payoff(tau) = L*exp(g*tau) + (Gam(tau) - L*exp(g*tau))^+
#                      Gam(tau) = S_M * sum_{m=0}^M(alpha*gamma / S_m)
#                          tau  = time of death (discrete periods)
#                            M  = number of periods until time of death (each period length dt)
    
    # Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Returns: price of contract
    
    # Author: Justin Lars Kirkby
# References: 1) Equity-Linked  Guaranteed Minimum Death Benefits with Dollar Cost Averaging, J.L.Kirkby & D.Nguyen, 2021
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# S_0 = initial stock price (e.g. 100)
# r   = interest rate (e.g. 0.05)
# q   = dividend yield (e.g. 0.05)
# M   = number of subintervals of [0,T] (total of M+1 monitoring points in time grid, including S_0)
# gmdb_params = container of GMDB contract params, see below
# modelInput =  model inputs, see below
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# proj_params = numerical params
#   proj_params.N = number of basis elements, e.g. N = 2^10
#   proj_params.L1 = gridwidth param, e.g. L1 = 8
    
    #########################################################
    
    # ------------------
# GMDB Contract Params
# ------------------
    L=gmdb_params.L
# PROJ_GMDB_DCA_Fast.m:39
    
    alpha=gmdb_params.alpha
# PROJ_GMDB_DCA_Fast.m:40
    
    gamma=gmdb_params.gamma
# PROJ_GMDB_DCA_Fast.m:41
    
    contract_type=gmdb_params.contract_type
# PROJ_GMDB_DCA_Fast.m:42
    
    p=gmdb_params.death_prob
# PROJ_GMDB_DCA_Fast.m:43
    
    g=gmdb_params.g
# PROJ_GMDB_DCA_Fast.m:44
    # ------------------
# Model Inputs
# ------------------
    dt=modelInput.dt
# PROJ_GMDB_DCA_Fast.m:49
    
    phiR=modelInput.rnCHF
# PROJ_GMDB_DCA_Fast.m:50
    
    call=1
# PROJ_GMDB_DCA_Fast.m:53
    ER=0
# PROJ_GMDB_DCA_Fast.m:54
    Z=gen_func(- r,dt,p)
# PROJ_GMDB_DCA_Fast.m:56
    if g == 0:
        Zrg=copy(Z)
# PROJ_GMDB_DCA_Fast.m:58
    else:
        Zrg=gen_func(- (r - g),dt,p)
# PROJ_GMDB_DCA_Fast.m:60
    
    if L == - 1:
        MF=gen_func(r - q - g,dt,p)
# PROJ_GMDB_DCA_Fast.m:64
        Zg=gen_func(- g,dt,p)
# PROJ_GMDB_DCA_Fast.m:65
        L=dot(dot(alpha,gamma),(dot(exp(dot((r - q),dt)),MF) - Zg)) / (exp(dot((r - q),dt)) - 1)
# PROJ_GMDB_DCA_Fast.m:66
    
    Mmax=length(p)
# PROJ_GMDB_DCA_Fast.m:69
    Tmax=dot(Mmax,dt)
# PROJ_GMDB_DCA_Fast.m:69
    pr_alpha=getTruncationAlpha(Tmax,proj_params.L1,modelInput,modelInput.model)
# PROJ_GMDB_DCA_Fast.m:70
    #########################################
    N=proj_params.N
# PROJ_GMDB_DCA_Fast.m:73
    dx=dot(2,pr_alpha) / (N - 1)
# PROJ_GMDB_DCA_Fast.m:74
    a=1 / dx
# PROJ_GMDB_DCA_Fast.m:74
    A=dot(32,a ** 4)
# PROJ_GMDB_DCA_Fast.m:75
    C_aN=A / N
# PROJ_GMDB_DCA_Fast.m:76
    ### SHIFTS
    x1=zeros(1,Mmax)
# PROJ_GMDB_DCA_Fast.m:81
    if contract_type == 1:
        strikes=dot(dot(S_0,L),exp(dot(dot(g,dt),(arange(1,Mmax))))) / (dot(dot(alpha,gamma),(arange(2,Mmax + 1))))
# PROJ_GMDB_DCA_Fast.m:84
    else:
        strikes=dot(S_0,ones(1,Mmax))
# PROJ_GMDB_DCA_Fast.m:86
    
    for m in arange(1,Mmax).reshape(-1):
        if m == 1:
            x1[m]=ER
# PROJ_GMDB_DCA_Fast.m:92
        else:
            x1[m]=ER + log(1 + exp(x1(m - 1)))
# PROJ_GMDB_DCA_Fast.m:94
        #x1(m) = log(m) + .5*(m+1)*ER;    ## LOWER BOUND SHIFT derived in APROJ paper
    
    Nm=floor(dot(a,(x1 - ER)))
# PROJ_GMDB_DCA_Fast.m:99
    x1=ER + dot((1 - N / 2),dx) + dot(Nm,dx)
# PROJ_GMDB_DCA_Fast.m:100
    NNM=N + Nm(Mmax - 1)
# PROJ_GMDB_DCA_Fast.m:101
    
    ### Now check that we wont fall off the grid later
    for m in arange(1,Mmax).reshape(-1):
        ystar=log(dot((m + 1),strikes(m)) / S_0 - 1)
# PROJ_GMDB_DCA_Fast.m:105
        nbar=floor(dot((ystar - x1(m)),a) + 1)
# PROJ_GMDB_DCA_Fast.m:106
        if nbar + 1 > N:
            proj_params.L1 = copy(dot(proj_params.L1,1.25))
# PROJ_GMDB_DCA_Fast.m:109
            price,opt,L=PROJ_GMDB_DCA_Fast(proj_params,S_0,gmdb_params,r,q,modelInput,nargout=3)
# PROJ_GMDB_DCA_Fast.m:110
            return price,opt,L
    
    dxi=dot(dot(2,pi),a) / N
# PROJ_GMDB_DCA_Fast.m:115
    xi=dot(dxi,(arange(1,(N - 1))).T)
# PROJ_GMDB_DCA_Fast.m:116
    PhiR=concat([[1],[phiR(xi)]])
# PROJ_GMDB_DCA_Fast.m:117
    b0=1208 / 2520
# PROJ_GMDB_DCA_Fast.m:119
    b1=1191 / 2520
# PROJ_GMDB_DCA_Fast.m:119
    b2=120 / 2520
# PROJ_GMDB_DCA_Fast.m:119
    b3=1 / 2520
# PROJ_GMDB_DCA_Fast.m:119
    zeta=(sin(xi / (dot(2,a))) / xi) ** 4.0 / (b0 + dot(b1,cos(xi / a)) + dot(b2,cos(dot(2,xi) / a)) + dot(b3,cos(dot(3,xi) / a)))
# PROJ_GMDB_DCA_Fast.m:120
    AA=1 / A
# PROJ_GMDB_DCA_Fast.m:121
    ###################################################################
### PSI Matrix: 5-Point GAUSSIAN
#################################################################
    PSI=make_PSI(N,NNM,x1(1),dx,dxi)
# PROJ_GMDB_DCA_Fast.m:127
    ##############
# STEP 1) Value the European!!!
##############
    beta=concat([[AA],[multiply(multiply(zeta,PhiR(arange(2,N))),exp(dot(dot(- 1j,x1(1)),xi)))]])
# PROJ_GMDB_DCA_Fast.m:132
    
    beta=real(fft(beta))
# PROJ_GMDB_DCA_Fast.m:133
    s=european_price(zeta,PhiR,xi,dx,r,q,dt,strikes(1),S_0,ER,N,a,call)
# PROJ_GMDB_DCA_Fast.m:135
    s=dot(dot(p(1),2),s)
# PROJ_GMDB_DCA_Fast.m:136
    ##############
# STEP 2) Value the rest
##############
    
    PhiR=dot(C_aN,PhiR)
# PROJ_GMDB_DCA_Fast.m:142
    beta=multiply(dot(PSI(arange(),arange(1,N)),beta),PhiR)
# PROJ_GMDB_DCA_Fast.m:143
    
    ##################################################
    
    ##### Loop to find PSI_M
    for n in arange(2,Mmax).reshape(-1):
        opt_v=intermediate_asian_price(N,dx,dt,xi,zeta,beta,x1(n),n,r,q,strikes(n),S_0)
# PROJ_GMDB_DCA_Fast.m:149
        beta[arange(2,N)]=multiply(multiply(zeta,beta(arange(2,N))),exp(dot(dot(- 1j,x1(n)),xi)))
# PROJ_GMDB_DCA_Fast.m:152
        beta[1]=AA
# PROJ_GMDB_DCA_Fast.m:152
        beta=real(fft(beta))
# PROJ_GMDB_DCA_Fast.m:153
        if n < Mmax:
            beta=multiply(dot(PSI(arange(),arange(Nm(n) + 1,Nm(n) + N)),beta),PhiR)
# PROJ_GMDB_DCA_Fast.m:155
        s=s + dot(dot(p(n),(n + 1)),opt_v)
# PROJ_GMDB_DCA_Fast.m:158
    
    opt=dot(dot(s,alpha),gamma) / S_0
# PROJ_GMDB_DCA_Fast.m:162
    price=dot(L,Zrg) - dot(alpha,(exp(dot(r,dt)) - Z)) / (exp(dot(r,dt)) - 1) + opt
# PROJ_GMDB_DCA_Fast.m:163
    return price,opt,L
    
if __name__ == '__main__':
    pass
    
    
@function
def make_PSI(N=None,NNM=None,x_1=None,dx=None,dxi=None,*args,**kwargs):
    varargin = make_PSI.varargin
    nargin = make_PSI.nargin

    ###################################################################
### PSI Matrix: 5-Point GAUSSIAN
#################################################################
    PSI=zeros(N,NNM)
# PROJ_GMDB_DCA_Fast.m:172
    
    PSI[1,arange()]=ones(1,NNM)
# PROJ_GMDB_DCA_Fast.m:173
    #### Sample
    Neta=dot(5,(NNM)) + 15
# PROJ_GMDB_DCA_Fast.m:176
    
    Neta5=(NNM) + 3
# PROJ_GMDB_DCA_Fast.m:177
    g2=sqrt(5 - dot(2,sqrt(10 / 7))) / 6
# PROJ_GMDB_DCA_Fast.m:178
    g3=sqrt(5 + dot(2,sqrt(10 / 7))) / 6
# PROJ_GMDB_DCA_Fast.m:179
    v1=dot(0.5,128) / 225
# PROJ_GMDB_DCA_Fast.m:180
    v2=dot(0.5,(322 + dot(13,sqrt(70)))) / 900
# PROJ_GMDB_DCA_Fast.m:181
    v3=dot(0.5,(322 - dot(13,sqrt(70)))) / 900
# PROJ_GMDB_DCA_Fast.m:182
    thet=zeros(1,Neta)
# PROJ_GMDB_DCA_Fast.m:185
    
    thet[dot(5,(arange(1,Neta5))) - 2]=x_1 - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1)))
# PROJ_GMDB_DCA_Fast.m:186
    thet[dot(5,(arange(1,Neta5))) - 4]=x_1 - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) - dot(dx,g3)
# PROJ_GMDB_DCA_Fast.m:187
    thet[dot(5,(arange(1,Neta5))) - 3]=x_1 - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) - dot(dx,g2)
# PROJ_GMDB_DCA_Fast.m:188
    thet[dot(5,(arange(1,Neta5))) - 1]=x_1 - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) + dot(dx,g2)
# PROJ_GMDB_DCA_Fast.m:189
    thet[dot(5,(arange(1,Neta5)))]=x_1 - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) + dot(dx,g3)
# PROJ_GMDB_DCA_Fast.m:190
    #### Weights
    sig=concat([- 1.5 - g3,- 1.5 - g2,- 1.5,- 1.5 + g2,- 1.5 + g3,- 0.5 - g3,- 0.5 - g2,- 0.5,- 0.5 + g2,- 0.5 + g3])
# PROJ_GMDB_DCA_Fast.m:194
    sig[arange(1,5)]=(sig(arange(1,5)) + 2) ** 3 / 6
# PROJ_GMDB_DCA_Fast.m:195
    sig[arange(6,10)]=2 / 3 - dot(0.5,(sig(arange(6,10))) ** 3) - (sig(arange(6,10))) ** 2
# PROJ_GMDB_DCA_Fast.m:196
    sig[concat([1,5,6,10])]=dot(v3,sig(concat([1,5,6,10])))
# PROJ_GMDB_DCA_Fast.m:198
    sig[concat([2,4,7,9])]=dot(v2,sig(concat([2,4,7,9])))
# PROJ_GMDB_DCA_Fast.m:199
    sig[concat([3,8])]=dot(v1,sig(concat([3,8])))
# PROJ_GMDB_DCA_Fast.m:200
    #### Fill Matrix
    zz=exp(dot(dot(1j,dxi),log(1 + exp(thet))))
# PROJ_GMDB_DCA_Fast.m:203
    thet=copy(zz)
# PROJ_GMDB_DCA_Fast.m:204
    for j in arange(2,N - 1).reshape(-1):
        PSI[j,arange()]=dot(sig(1),(thet(arange(1,Neta - 19,5)) + thet(arange(20,Neta,5)))) + dot(sig(2),(thet(arange(2,Neta - 18,5)) + thet(arange(19,Neta - 1,5)))) + dot(sig(3),(thet(arange(3,Neta - 17,5)) + thet(arange(18,Neta - 2,5)))) + dot(sig(4),(thet(arange(4,Neta - 16,5)) + thet(arange(17,Neta - 3,5)))) + dot(sig(5),(thet(arange(5,Neta - 15,5)) + thet(arange(16,Neta - 4,5)))) + dot(sig(6),(thet(arange(6,Neta - 14,5)) + thet(arange(15,Neta - 5,5)))) + dot(sig(7),(thet(arange(7,Neta - 13,5)) + thet(arange(14,Neta - 6,5)))) + dot(sig(8),(thet(arange(8,Neta - 12,5)) + thet(arange(13,Neta - 7,5)))) + dot(sig(9),(thet(arange(9,Neta - 11,5)) + thet(arange(12,Neta - 8,5)))) + dot(sig(10),(thet(arange(10,Neta - 10,5)) + thet(arange(11,Neta - 9,5))))
# PROJ_GMDB_DCA_Fast.m:208
        thet=multiply(thet,zz)
# PROJ_GMDB_DCA_Fast.m:219
    
    return PSI
    
if __name__ == '__main__':
    pass
    
    
@function
def intermediate_asian_price(N=None,dx=None,dt=None,xi=None,zeta=None,chf=None,x_1=None,M=None,r=None,q=None,W=None,S_0=None,*args,**kwargs):
    varargin = intermediate_asian_price.varargin
    nargin = intermediate_asian_price.nargin

    call=1
# PROJ_GMDB_DCA_Fast.m:224
    a=1 / dx
# PROJ_GMDB_DCA_Fast.m:225
    A=dot(32,a ** 4)
# PROJ_GMDB_DCA_Fast.m:226
    AA=1 / A
# PROJ_GMDB_DCA_Fast.m:227
    C_aN=A / N
# PROJ_GMDB_DCA_Fast.m:228
    T=dot(M,dt)
# PROJ_GMDB_DCA_Fast.m:229
    ##### FINAL VALUE
    ystar=log(dot((M + 1),W) / S_0 - 1)
# PROJ_GMDB_DCA_Fast.m:232
    nbar=floor(dot((ystar - x_1),a) + 1)
# PROJ_GMDB_DCA_Fast.m:233
    C=S_0 / (M + 1)
# PROJ_GMDB_DCA_Fast.m:234
    D=W - C
# PROJ_GMDB_DCA_Fast.m:235
    x_1=ystar - dot((nbar - 1),dx)
# PROJ_GMDB_DCA_Fast.m:236
    beta[arange(2,N)]=multiply(multiply(zeta,chf(arange(2,N))),exp(dot(dot(- 1j,x_1),xi)))
# PROJ_GMDB_DCA_Fast.m:238
    beta[1]=AA
# PROJ_GMDB_DCA_Fast.m:238
    beta=real(fft(beta)).T
# PROJ_GMDB_DCA_Fast.m:239
    Cc1=dot(C,(exp(dot(- 7 / 4,dx)) / 54 + exp(dot(- 1.5,dx)) / 18 + exp(dot(- 1.25,dx)) / 2 + dot(7,exp(- dx)) / 27)) / 20
# PROJ_GMDB_DCA_Fast.m:243
    Cc2=dot(dot(C,0.05),(28 / 27 + exp(dot(- 7 / 4,dx)) / 54 + exp(dot(- 1.5,dx)) / 18 + exp(dot(- 1.25,dx)) / 2 + dot(14,exp(- dx)) / 27 + dot(121 / 54,exp(dot(- 0.75,dx))) + dot(23 / 18,exp(dot(- 0.5,dx))) + dot(235 / 54,exp(dot(- 0.25,dx)))))
# PROJ_GMDB_DCA_Fast.m:245
    Cc3=dot(C,((28 + dot(7,exp(- dx))) / 3 + (dot(14,exp(dx)) + exp(dot(- 7 / 4,dx)) + dot(242,cosh(dot(0.75,dx))) + dot(470,cosh(dot(0.25,dx)))) / 12 + dot(0.25,(exp(dot(- 1.5,dx)) + dot(9,exp(dot(- 1.25,dx))) + dot(46,cosh(dot(0.5,dx))))))) / 90
# PROJ_GMDB_DCA_Fast.m:248
    Cc4=dot(C,(dot(14 / 3,(2 + cosh(dx))) + dot(0.5,(cosh(dot(1.5,dx)) + dot(9,cosh(dot(1.25,dx))) + dot(23,cosh(dot(0.5,dx))))) + dot(1 / 6,(cosh(dot(7 / 4,dx)) + dot(121,cosh(dot(0.75,dx))) + dot(235,cosh(dot(0.25,dx))))))) / 90
# PROJ_GMDB_DCA_Fast.m:252
    G=zeros(nbar + 1,1)
# PROJ_GMDB_DCA_Fast.m:256
    E=exp(ystar - dot((nbar - 1),dx) + dot(dx,(arange(0,nbar))))
# PROJ_GMDB_DCA_Fast.m:257
    G[nbar + 1]=D / 24 - dot(Cc1,E(nbar + 1))
# PROJ_GMDB_DCA_Fast.m:259
    G[nbar]=dot(0.5,D) - dot(Cc2,E(nbar))
# PROJ_GMDB_DCA_Fast.m:260
    G[nbar - 1]=dot(23,D) / 24 - dot(Cc3,E(nbar - 1))
# PROJ_GMDB_DCA_Fast.m:261
    G[arange(1,nbar - 2)]=D - dot(Cc4,E(arange(1,nbar - 2)))
# PROJ_GMDB_DCA_Fast.m:262
    Val=dot(dot(C_aN,exp(dot(- r,T))),sum(multiply(beta(arange(1,nbar + 1)),G)))
# PROJ_GMDB_DCA_Fast.m:264
    if call == 1:
        if r - q == 0:
            mult=M + 1
# PROJ_GMDB_DCA_Fast.m:267
        else:
            mult=(exp(dot(dot((r - q),T),(1 + 1 / M))) - 1) / (exp(dot((r - q),dt)) - 1)
# PROJ_GMDB_DCA_Fast.m:269
        Val=Val + dot(dot(C,exp(dot(- r,T))),mult) - dot(W,exp(dot(- r,T)))
# PROJ_GMDB_DCA_Fast.m:271
    
    Val=max(0,Val)
# PROJ_GMDB_DCA_Fast.m:273
    return Val
    
if __name__ == '__main__':
    pass
    
    
@function
def european_price(zeta=None,PhiR=None,xi=None,dx=None,r=None,q=None,T=None,W=None,S_0=None,c1=None,N=None,a=None,call=None,*args,**kwargs):
    varargin = european_price.varargin
    nargin = european_price.nargin

    W=dot(2,W) - S_0
# PROJ_GMDB_DCA_Fast.m:280
    
    lws=log(W / S_0)
# PROJ_GMDB_DCA_Fast.m:282
    lam=c1 - dot((N / 2 - 1),dx)
# PROJ_GMDB_DCA_Fast.m:283
    nbar=floor(dot(a,(lws - lam)) + 1)
# PROJ_GMDB_DCA_Fast.m:284
    if nbar >= N:
        nbar=N - 1
# PROJ_GMDB_DCA_Fast.m:286
    
    xmin=lws - dot((nbar - 1),dx)
# PROJ_GMDB_DCA_Fast.m:288
    Cons=dot(32,a ** 4)
# PROJ_GMDB_DCA_Fast.m:291
    beta=concat([[1 / Cons],[multiply(multiply(zeta,PhiR(arange(2,N))),exp(dot(dot(- 1j,xmin),xi)))]])
# PROJ_GMDB_DCA_Fast.m:293
    
    beta=real(fft(beta)).T
# PROJ_GMDB_DCA_Fast.m:294
    G=zeros(1,nbar + 1)
# PROJ_GMDB_DCA_Fast.m:296
    G[nbar + 1]=dot(W,(1 / 24 - dot(dot(1 / 20,exp(dx)),(exp(dot(- 7 / 4,dx)) / 54 + exp(dot(- 1.5,dx)) / 18 + exp(dot(- 1.25,dx)) / 2 + dot(7,exp(- dx)) / 27))))
# PROJ_GMDB_DCA_Fast.m:297
    G[nbar]=dot(W,(0.5 - dot(0.05,(28 / 27 + exp(dot(- 7 / 4,dx)) / 54 + exp(dot(- 1.5,dx)) / 18 + exp(dot(- 1.25,dx)) / 2 + dot(14,exp(- dx)) / 27 + dot(121 / 54,exp(dot(- 0.75,dx))) + dot(23 / 18,exp(dot(- 0.5,dx))) + dot(235 / 54,exp(dot(- 0.25,dx)))))))
# PROJ_GMDB_DCA_Fast.m:299
    G[nbar - 1]=dot(W,(23 / 24 - dot(exp(- dx) / 90,((28 + dot(7,exp(- dx))) / 3 + (dot(14,exp(dx)) + exp(dot(- 7 / 4,dx)) + dot(242,cosh(dot(0.75,dx))) + dot(470,cosh(dot(0.25,dx)))) / 12 + dot(0.25,(exp(dot(- 1.5,dx)) + dot(9,exp(dot(- 1.25,dx))) + dot(46,cosh(dot(0.5,dx)))))))))
# PROJ_GMDB_DCA_Fast.m:302
    G[arange(1,nbar - 2)]=W - dot(dot(S_0,exp(xmin + dot(dx,(arange(0,nbar - 3))))) / 90,(dot(14 / 3,(2 + cosh(dx))) + dot(0.5,(cosh(dot(1.5,dx)) + dot(9,cosh(dot(1.25,dx))) + dot(23,cosh(dot(0.5,dx))))) + dot(1 / 6,(cosh(dot(7 / 4,dx)) + dot(121,cosh(dot(0.75,dx))) + dot(235,cosh(dot(0.25,dx)))))))
# PROJ_GMDB_DCA_Fast.m:306
    if call == 1:
        price=dot(dot(dot(Cons,exp(dot(- r,T))) / N,G),(beta(arange(1,length(G))).T)) + dot(S_0,exp(dot(- q,T))) - dot(W,exp(dot(- r,T)))
# PROJ_GMDB_DCA_Fast.m:311
    else:
        price=dot(dot(dot(Cons,exp(dot(- r,T))) / N,G),(beta(arange(1,length(G))).T))
# PROJ_GMDB_DCA_Fast.m:313
    
    price=dot(0.5,max(price,0))
# PROJ_GMDB_DCA_Fast.m:316
    
    return price
    
if __name__ == '__main__':
    pass
    