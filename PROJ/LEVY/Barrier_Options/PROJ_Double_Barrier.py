# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_Double_Barrier.m

    
@function
def PROJ_Double_Barrier(N=None,alph=None,call=None,L=None,U=None,S_0=None,W=None,M=None,T=None,r=None,rnCHF=None,*args,**kwargs):
    varargin = PROJ_Double_Barrier.varargin
    nargin = PROJ_Double_Barrier.nargin

    #########################################################
# About: Pricing Function for Discrete Double Barrier Options using PROJ method
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
# [L,U] = barriers
# rnCHF = risk netural characteristic function (function handle with single argument)
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# N     = number of grid/basis points (power of 2, e.g. 2^12), resolution = 2*alph/(N-1)
#########################################################
    
    l=log(L / S_0)
# PROJ_Double_Barrier.m:28
    u=log(U / S_0)
# PROJ_Double_Barrier.m:28
    dt=T / M
# PROJ_Double_Barrier.m:28
    K=N / 2
# PROJ_Double_Barrier.m:30
    dx=(u - l) / (K - 1)
# PROJ_Double_Barrier.m:31
    a=1 / dx
# PROJ_Double_Barrier.m:32
    E=ceil(dot(2,alph) / (u - l))
# PROJ_Double_Barrier.m:34
    if M <= 12:
        E=min(E,4)
# PROJ_Double_Barrier.m:36
    else:
        E=min(E,3)
# PROJ_Double_Barrier.m:38
    
    a2=a ** 2
# PROJ_Double_Barrier.m:42
    N_Ee=dot(E,N)
# PROJ_Double_Barrier.m:43
    Cons2=dot(dot(24,a2),exp(dot(- r,dt))) / N_Ee
# PROJ_Double_Barrier.m:44
    grand=lambda w=None: multiply(rnCHF(w),(sin(w / (dot(2,a))) / w) ** 2.0) / (2 + cos(w / a))
# PROJ_Double_Barrier.m:47
    dw=dot(dot(2,pi),a) / N_Ee
# PROJ_Double_Barrier.m:48
    omega=(arange(dw,dot((N_Ee - 1),dw),dw))
# PROJ_Double_Barrier.m:49
    
    zmin=dot((1 - dot(E,K)),dx)
# PROJ_Double_Barrier.m:50
    
    beta=dot(Cons2,real(fft(concat([1 / (dot(24,a ** 2)),multiply(exp(dot(dot(- 1j,zmin),omega)),feval(grand,omega))]))))
# PROJ_Double_Barrier.m:51
    toepM=concat([[beta(arange(dot(E,K),dot((E - 1),K) + 1,- 1)).T],[0],[beta(arange(dot((E + 1),K) - 1,dot(E,K) + 1,- 1)).T]])
# PROJ_Double_Barrier.m:53
    toepM=fft(toepM)
# PROJ_Double_Barrier.m:54
    ##################################
#STEP 1: Payoff Coefficients
##################################
    xmin=copy(l)
# PROJ_Double_Barrier.m:60
    nnot=floor(1 - dot(xmin,a))
# PROJ_Double_Barrier.m:61
    
    lws=log(W / S_0)
# PROJ_Double_Barrier.m:62
    nbar=floor(dot(a,(lws - xmin)) + 1)
# PROJ_Double_Barrier.m:63
    rho=lws - (xmin + dot((nbar - 1),dx))
# PROJ_Double_Barrier.m:64
    zeta=dot(a,rho)
# PROJ_Double_Barrier.m:65
    xnbar=xmin + dot((nbar - 1),dx)
# PROJ_Double_Barrier.m:66
    Thet=zeros(K,1)
# PROJ_Double_Barrier.m:68
    Cons3=1 / 48
# PROJ_Double_Barrier.m:69
    Cons4=1 / 12
# PROJ_Double_Barrier.m:70
    ######  Gaussian Quad Constants
    q_plus=(1 + sqrt(3 / 5)) / 2
# PROJ_Double_Barrier.m:73
    q_minus=(1 - sqrt(3 / 5)) / 2
# PROJ_Double_Barrier.m:73
    b3=sqrt(15)
# PROJ_Double_Barrier.m:74
    b4=b3 / 10
# PROJ_Double_Barrier.m:74
    #### PAYOFF CONSTANTS-----------------------------------
    varthet_01=dot(exp(dot(0.5,dx)),(dot(5,cosh(dot(b4,dx))) - dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Double_Barrier.m:78
    varthet_m10=dot(exp(dot(- 0.5,dx)),(dot(5,cosh(dot(b4,dx))) + dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Double_Barrier.m:79
    varthet_star=varthet_01 + varthet_m10
# PROJ_Double_Barrier.m:80
    if call == 1:
        sigma=1 - zeta
# PROJ_Double_Barrier.m:83
        sigma_plus=dot((q_plus - 0.5),sigma)
# PROJ_Double_Barrier.m:83
        sigma_minus=dot((q_minus - 0.5),sigma)
# PROJ_Double_Barrier.m:83
        es1=exp(dot(dx,sigma_plus))
# PROJ_Double_Barrier.m:84
        es2=exp(dot(dx,sigma_minus))
# PROJ_Double_Barrier.m:84
        dbar_0=0.5 + dot(zeta,(dot(0.5,zeta) - 1))
# PROJ_Double_Barrier.m:85
        dbar_1=dot(sigma,(1 - dot(0.5,sigma)))
# PROJ_Double_Barrier.m:86
        d_0=dot(dot(exp(dot((rho + dx),0.5)),sigma ** 2) / 18,(dot(5,(dot((1 - q_minus),es2) + dot((1 - q_plus),es1))) + 4))
# PROJ_Double_Barrier.m:88
        d_1=dot(dot(exp(dot((rho - dx),0.5)),sigma) / 18,(dot(5,(dot((dot(0.5,(zeta + 1)) + sigma_minus),es2) + dot((dot(0.5,(zeta + 1)) + sigma_plus),es1))) + dot(4,(zeta + 1))))
# PROJ_Double_Barrier.m:89
        Thet[nbar]=dot(W,(dot(exp(- rho),d_0) - dbar_0))
# PROJ_Double_Barrier.m:92
        Thet[nbar + 1]=dot(W,(dot(exp(dx - rho),(varthet_01 + d_1)) - (0.5 + dbar_1)))
# PROJ_Double_Barrier.m:93
        Thet[arange(nbar + 2,K - 1)]=dot(dot(exp(xmin + dot(dx,(arange(nbar + 1,K - 2)))),S_0),varthet_star) - W
# PROJ_Double_Barrier.m:94
        Thet[K]=dot(U,varthet_m10) - W / 2
# PROJ_Double_Barrier.m:95
        p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Double_Barrier.m:97
        Val=p(arange(1,K))
# PROJ_Double_Barrier.m:98
        for m in arange(M - 2,0,- 1).reshape(-1):
            Thet[1]=dot(Cons3,(dot(13,Val(1)) + dot(15,Val(2)) - dot(5,Val(3)) + Val(4)))
# PROJ_Double_Barrier.m:101
            Thet[K]=dot(Cons3,(dot(13,Val(K)) + dot(15,Val(K - 1)) - dot(5,Val(K - 2)) + Val(K - 3)))
# PROJ_Double_Barrier.m:102
            Thet[arange(2,K - 1)]=dot(Cons4,(Val(arange(1,K - 2)) + dot(10,Val(arange(2,K - 1))) + Val(arange(3,K))))
# PROJ_Double_Barrier.m:103
            p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Double_Barrier.m:105
            Val=p(arange(1,K))
# PROJ_Double_Barrier.m:106
    else:
        zeta_plus=dot(zeta,q_plus)
# PROJ_Double_Barrier.m:111
        zeta_minus=dot(zeta,q_minus)
# PROJ_Double_Barrier.m:111
        rho_plus=dot(rho,q_plus)
# PROJ_Double_Barrier.m:112
        rho_minus=dot(rho,q_minus)
# PROJ_Double_Barrier.m:112
        ed1=exp(rho_minus)
# PROJ_Double_Barrier.m:114
        ed2=exp(rho / 2)
# PROJ_Double_Barrier.m:114
        ed3=exp(rho_plus)
# PROJ_Double_Barrier.m:114
        dbar_1=zeta ** 2 / 2
# PROJ_Double_Barrier.m:116
        dbar_0=zeta - dbar_1
# PROJ_Double_Barrier.m:117
        d_0=dot(zeta,(dot(5,(dot((1 - zeta_minus),ed1) + dot((1 - zeta_plus),ed3))) + dot(dot(4,(2 - zeta)),ed2))) / 18
# PROJ_Double_Barrier.m:118
        d_1=dot(zeta,(dot(5,(dot(zeta_minus,ed1) + dot(zeta_plus,ed3))) + dot(dot(4,zeta),ed2))) / 18
# PROJ_Double_Barrier.m:119
        Thet[1]=W / 2 - dot(L,varthet_01)
# PROJ_Double_Barrier.m:121
        Thet[arange(2,nbar - 1)]=W - dot(dot(exp(xmin + dot(dx,(arange(1,nbar - 2)))),S_0),varthet_star)
# PROJ_Double_Barrier.m:122
        Thet[nbar]=dot(W,(0.5 + dbar_0 - dot(exp(- rho),(varthet_m10 + d_0))))
# PROJ_Double_Barrier.m:123
        Thet[nbar + 1]=dot(W,(dbar_1 - dot(exp(- rho),d_1)))
# PROJ_Double_Barrier.m:124
        p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Double_Barrier.m:126
        Val=p(arange(1,K))
# PROJ_Double_Barrier.m:127
        for m in arange(M - 2,0,- 1).reshape(-1):
            Thet[1]=dot(Cons3,(dot(13,Val(1)) + dot(15,Val(2)) - dot(5,Val(3)) + Val(4)))
# PROJ_Double_Barrier.m:130
            Thet[K]=dot(Cons3,(dot(13,Val(K)) + dot(15,Val(K - 1)) - dot(5,Val(K - 2)) + Val(K - 3)))
# PROJ_Double_Barrier.m:131
            Thet[arange(2,K - 1)]=dot(Cons4,(Val(arange(1,K - 2)) + dot(10,Val(arange(2,K - 1))) + Val(arange(3,K))))
# PROJ_Double_Barrier.m:132
            p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Double_Barrier.m:134
            Val=p(arange(1,K))
# PROJ_Double_Barrier.m:135
    
    xnot=l + dot((nnot - 1),dx)
# PROJ_Double_Barrier.m:139
    xs=concat([xnot - dot(2,dx),xnot - dx,xnot,xnot + dx,xnot + dot(2,dx)])
# PROJ_Double_Barrier.m:140
    ys=concat([Val(nnot - 2),Val(nnot - 1),Val(nnot),Val(nnot + 1),Val(nnot + 2)])
# PROJ_Double_Barrier.m:141
    price=spline(xs,ys,0)
# PROJ_Double_Barrier.m:142
    return price
    
if __name__ == '__main__':
    pass
    