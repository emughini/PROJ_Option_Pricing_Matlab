# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_Asian.m

    
@function
def PROJ_Asian(N=None,alph=None,S_0=None,M=None,W=None,call=None,T=None,r=None,q=None,phiR=None,ER=None,*args,**kwargs):
    varargin = PROJ_Asian.varargin
    nargin = PROJ_Asian.nargin

    #########################################################
# About: Pricing Function for Arithmetic Asian Options using PROJ method
# Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# S_0 = initial stock price (e.g. 100)
# W   = strike  (e.g. 100)
# r   = interest rate (e.g. 0.05)
# q   = dividend yield (e.g. 0.05)
# T   = time remaining until maturity (in years, e.g. T=1)
# M   = number of subintervals of [0,T] (total of M+1 monitoring points in time grid, including S_0)
# call = 1 for call (else put)
# phiR =  risk neutral density of log return over time step dt = 1/M (function handle with single argument)
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# ER    = risk neutral expected return over increment dt=1/M (can set to zero if it is unknown)
# alph  = grid with is 2*alph
# N     = number of grid/basis points (power of 2, e.g. 2^12), resolution = 2*alph/(N-1)
#########################################################
    
    dt=T / M
# PROJ_Asian.m:28
    dx=dot(2,alph) / (N - 1)
# PROJ_Asian.m:29
    a=1 / dx
# PROJ_Asian.m:29
    A=dot(32,a ** 4)
# PROJ_Asian.m:31
    C_aN=A / N
# PROJ_Asian.m:32
    ### SHIFTS
    x1=zeros(1,M)
# PROJ_Asian.m:35
    x1[1]=ER
# PROJ_Asian.m:36
    for m in arange(2,M).reshape(-1):
        x1[m]=ER + log(1 + exp(x1(m - 1)))
# PROJ_Asian.m:38
        #x1(m) = log(m) + .5*(m+1)*ER;    ## LOWER BOUND SHIFT derived in APROJ paper
    
    Nm=floor(dot(a,(x1 - ER)))
# PROJ_Asian.m:42
    x1=ER + dot((1 - N / 2),dx) + dot(Nm,dx)
# PROJ_Asian.m:43
    NNM=N + Nm(M - 1)
# PROJ_Asian.m:44
    
    ystar=log(dot((M + 1),W) / S_0 - 1)
# PROJ_Asian.m:46
    nbar=floor(dot((ystar - x1(M)),a) + 1)
# PROJ_Asian.m:47
    if nbar + 1 > N:
        # In this case, we fall off the grid when doing final integration, 
    # so you are deep ITM for the put, try to increase alph
        alph=dot(1.25,alph)
# PROJ_Asian.m:52
        Val=PROJ_Asian(N,alph,S_0,M,W,call,T,r,q,phiR,ER)
# PROJ_Asian.m:53
        return Val
    
    dxi=dot(dot(2,pi),a) / N
# PROJ_Asian.m:57
    xi=dot(dxi,(arange(1,(N - 1))).T)
# PROJ_Asian.m:58
    PhiR=concat([[1],[phiR(xi)]])
# PROJ_Asian.m:59
    ###################################################################
### PSI Matrix: 5-Point GAUSSIAN
#################################################################
    PSI=zeros(N,NNM)
# PROJ_Asian.m:64
    
    PSI[1,arange()]=ones(1,NNM)
# PROJ_Asian.m:65
    #### Sample
    Neta=dot(5,(NNM)) + 15
# PROJ_Asian.m:68
    
    Neta5=(NNM) + 3
# PROJ_Asian.m:69
    g2=sqrt(5 - dot(2,sqrt(10 / 7))) / 6
# PROJ_Asian.m:70
    g3=sqrt(5 + dot(2,sqrt(10 / 7))) / 6
# PROJ_Asian.m:71
    v1=dot(0.5,128) / 225
# PROJ_Asian.m:72
    v2=dot(0.5,(322 + dot(13,sqrt(70)))) / 900
# PROJ_Asian.m:73
    v3=dot(0.5,(322 - dot(13,sqrt(70)))) / 900
# PROJ_Asian.m:74
    thet=zeros(1,Neta)
# PROJ_Asian.m:77
    
    thet[dot(5,(arange(1,Neta5))) - 2]=x1(1) - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1)))
# PROJ_Asian.m:78
    thet[dot(5,(arange(1,Neta5))) - 4]=x1(1) - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) - dot(dx,g3)
# PROJ_Asian.m:79
    thet[dot(5,(arange(1,Neta5))) - 3]=x1(1) - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) - dot(dx,g2)
# PROJ_Asian.m:80
    thet[dot(5,(arange(1,Neta5))) - 1]=x1(1) - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) + dot(dx,g2)
# PROJ_Asian.m:81
    thet[dot(5,(arange(1,Neta5)))]=x1(1) - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) + dot(dx,g3)
# PROJ_Asian.m:82
    #### Weights
    sig=concat([- 1.5 - g3,- 1.5 - g2,- 1.5,- 1.5 + g2,- 1.5 + g3,- 0.5 - g3,- 0.5 - g2,- 0.5,- 0.5 + g2,- 0.5 + g3])
# PROJ_Asian.m:86
    sig[arange(1,5)]=(sig(arange(1,5)) + 2) ** 3 / 6
# PROJ_Asian.m:87
    sig[arange(6,10)]=2 / 3 - dot(0.5,(sig(arange(6,10))) ** 3) - (sig(arange(6,10))) ** 2
# PROJ_Asian.m:88
    sig[concat([1,5,6,10])]=dot(v3,sig(concat([1,5,6,10])))
# PROJ_Asian.m:90
    sig[concat([2,4,7,9])]=dot(v2,sig(concat([2,4,7,9])))
# PROJ_Asian.m:91
    sig[concat([3,8])]=dot(v1,sig(concat([3,8])))
# PROJ_Asian.m:92
    #### Fill Matrix
    zz=exp(dot(dot(1j,dxi),log(1 + exp(thet))))
# PROJ_Asian.m:95
    thet=copy(zz)
# PROJ_Asian.m:96
    for j in arange(2,N - 1).reshape(-1):
        PSI[j,arange()]=dot(sig(1),(thet(arange(1,Neta - 19,5)) + thet(arange(20,Neta,5)))) + dot(sig(2),(thet(arange(2,Neta - 18,5)) + thet(arange(19,Neta - 1,5)))) + dot(sig(3),(thet(arange(3,Neta - 17,5)) + thet(arange(18,Neta - 2,5)))) + dot(sig(4),(thet(arange(4,Neta - 16,5)) + thet(arange(17,Neta - 3,5)))) + dot(sig(5),(thet(arange(5,Neta - 15,5)) + thet(arange(16,Neta - 4,5)))) + dot(sig(6),(thet(arange(6,Neta - 14,5)) + thet(arange(15,Neta - 5,5)))) + dot(sig(7),(thet(arange(7,Neta - 13,5)) + thet(arange(14,Neta - 6,5)))) + dot(sig(8),(thet(arange(8,Neta - 12,5)) + thet(arange(13,Neta - 7,5)))) + dot(sig(9),(thet(arange(9,Neta - 11,5)) + thet(arange(12,Neta - 8,5)))) + dot(sig(10),(thet(arange(10,Neta - 10,5)) + thet(arange(11,Neta - 9,5))))
# PROJ_Asian.m:100
        thet=multiply(thet,zz)
# PROJ_Asian.m:111
    
    ##-------------------------------------------------------------------------
    b0=1208 / 2520
# PROJ_Asian.m:115
    b1=1191 / 2520
# PROJ_Asian.m:115
    b2=120 / 2520
# PROJ_Asian.m:115
    b3=1 / 2520
# PROJ_Asian.m:115
    zeta=(sin(xi / (dot(2,a))) / xi) ** 4.0 / (b0 + dot(b1,cos(xi / a)) + dot(b2,cos(dot(2,xi) / a)) + dot(b3,cos(dot(3,xi) / a)))
# PROJ_Asian.m:116
    AA=1 / A
# PROJ_Asian.m:118
    beta=concat([[AA],[multiply(multiply(zeta,PhiR(arange(2,N))),exp(dot(dot(- 1j,x1(1)),xi)))]])
# PROJ_Asian.m:119
    
    beta=real(fft(beta))
# PROJ_Asian.m:120
    PhiR=dot(C_aN,PhiR)
# PROJ_Asian.m:122
    beta=multiply(dot(PSI(arange(),arange(1,N)),beta),PhiR)
# PROJ_Asian.m:123
    
    ##### Loop to find PSI_M
    for m in arange(3,M).reshape(-1):
        beta[arange(2,N)]=multiply(multiply(zeta,beta(arange(2,N))),exp(dot(dot(- 1j,x1(m - 1)),xi)))
# PROJ_Asian.m:127
        beta[1]=AA
# PROJ_Asian.m:127
        beta=real(fft(beta))
# PROJ_Asian.m:128
        beta=multiply(dot(PSI(arange(),arange(Nm(m - 1) + 1,Nm(m - 1) + N)),beta),PhiR)
# PROJ_Asian.m:129
    
    ##-------------------------------------------------------------------------
##### FINAL VALUE
    C=S_0 / (M + 1)
# PROJ_Asian.m:134
    D=W - C
# PROJ_Asian.m:135
    x1[M]=ystar - dot((nbar - 1),dx)
# PROJ_Asian.m:136
    beta[arange(2,N)]=multiply(multiply(zeta,beta(arange(2,N))),exp(dot(dot(- 1j,x1(M)),xi)))
# PROJ_Asian.m:138
    beta[1]=AA
# PROJ_Asian.m:138
    beta=real(fft(beta))
# PROJ_Asian.m:139
    ##-------------------------------------------------------------------------
    Cc1=dot(C,(exp(dot(- 7 / 4,dx)) / 54 + exp(dot(- 1.5,dx)) / 18 + exp(dot(- 1.25,dx)) / 2 + dot(7,exp(- dx)) / 27)) / 20
# PROJ_Asian.m:142
    Cc2=dot(dot(C,0.05),(28 / 27 + exp(dot(- 7 / 4,dx)) / 54 + exp(dot(- 1.5,dx)) / 18 + exp(dot(- 1.25,dx)) / 2 + dot(14,exp(- dx)) / 27 + dot(121 / 54,exp(dot(- 0.75,dx))) + dot(23 / 18,exp(dot(- 0.5,dx))) + dot(235 / 54,exp(dot(- 0.25,dx)))))
# PROJ_Asian.m:144
    Cc3=dot(C,((28 + dot(7,exp(- dx))) / 3 + (dot(14,exp(dx)) + exp(dot(- 7 / 4,dx)) + dot(242,cosh(dot(0.75,dx))) + dot(470,cosh(dot(0.25,dx)))) / 12 + dot(0.25,(exp(dot(- 1.5,dx)) + dot(9,exp(dot(- 1.25,dx))) + dot(46,cosh(dot(0.5,dx))))))) / 90
# PROJ_Asian.m:147
    Cc4=dot(C,(dot(14 / 3,(2 + cosh(dx))) + dot(0.5,(cosh(dot(1.5,dx)) + dot(9,cosh(dot(1.25,dx))) + dot(23,cosh(dot(0.5,dx))))) + dot(1 / 6,(cosh(dot(7 / 4,dx)) + dot(121,cosh(dot(0.75,dx))) + dot(235,cosh(dot(0.25,dx))))))) / 90
# PROJ_Asian.m:151
    ##-------------------------------------------------------------------------
    G=zeros(nbar + 1,1)
# PROJ_Asian.m:156
    E=exp(ystar - dot((nbar - 1),dx) + dot(dx,(arange(0,nbar))))
# PROJ_Asian.m:157
    G[nbar + 1]=D / 24 - dot(Cc1,E(nbar + 1))
# PROJ_Asian.m:159
    G[nbar]=dot(0.5,D) - dot(Cc2,E(nbar))
# PROJ_Asian.m:160
    G[nbar - 1]=dot(23,D) / 24 - dot(Cc3,E(nbar - 1))
# PROJ_Asian.m:161
    G[arange(1,nbar - 2)]=D - dot(Cc4,E(arange(1,nbar - 2)))
# PROJ_Asian.m:162
    ##-------------------------------------------------------------------------
    
    Val=dot(dot(C_aN,exp(dot(- r,T))),sum(multiply(beta(arange(1,nbar + 1)),G)))
# PROJ_Asian.m:165
    if call == 1:
        if r - q == 0:
            mult=M + 1
# PROJ_Asian.m:168
        else:
            mult=(exp(dot(dot((r - q),T),(1 + 1 / M))) - 1) / (exp(dot((r - q),dt)) - 1)
# PROJ_Asian.m:170
        Val=Val + dot(dot(C,exp(dot(- r,T))),mult) - dot(W,exp(dot(- r,T)))
# PROJ_Asian.m:172
    
    Val=max(0,Val)
# PROJ_Asian.m:175
    return Val
    
if __name__ == '__main__':
    pass
    