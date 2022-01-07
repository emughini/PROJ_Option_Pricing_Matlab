# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_Lookback.m

    
@function
def PROJ_Lookback(N=None,alpha=None,S_0=None,W=None,call=None,r=None,q=None,M=None,T=None,rnSYMB=None,floating_strike=None,*args,**kwargs):
    varargin = PROJ_Lookback.varargin
    nargin = PROJ_Lookback.nargin

    #########################################################
# About: Pricing Function for Discrete Lookback/Hindsight Options using PROJ method
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
# floating_strike = 1 for floating strike contract (else fixed strike)
# rnSYMB = risk netural symbol function (function handle with single argument)
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# alpha  = grid with is 2*alpha
# N     = number of grid/basis points (power of 2, e.g. 2^12), resolution = 2*alph/(N-1)
#########################################################
    
    dx=dot(2,alpha) / (N - 1)
# PROJ_Lookback.m:28
    a=1 / dx
# PROJ_Lookback.m:28
    K=N / 2
# PROJ_Lookback.m:29
    dt=T / M
# PROJ_Lookback.m:30
    zmin=dot((1 - K),dx)
# PROJ_Lookback.m:31
    if (floating_strike == 1 and call != 1) or (floating_strike != 1 and call == 1):
        # floating strike put or fixed strike call (ie we find max of process)
        rnCHFstar=lambda u=None: exp(dot(dt,(rnSYMB(u - 1j) - (r - q))))
# PROJ_Lookback.m:35
    else:
        error('This contract type not currently finished. Implementaion in progress')
        #rnCHFstar = @(u)exp(dt*(rnSYMB(u-1i) + (r-q)));   # min(X) = -max(-X)
        rnCHFstar=lambda u=None: exp(dot(dt,(rnSYMB(- u - 1j) - (r - q))))
# PROJ_Lookback.m:41
    
    Cons=dot(32,a ** 4) / N
# PROJ_Lookback.m:44
    b0=1208 / 2520
# PROJ_Lookback.m:45
    b1=1191 / 2520
# PROJ_Lookback.m:45
    b2=120 / 2520
# PROJ_Lookback.m:45
    b3=1 / 2520
# PROJ_Lookback.m:45
    grandG=lambda w=None: multiply(rnCHFstar(w),(sin(w / (dot(2,a))) / w) ** 4.0) / (b0 + dot(b1,cos(w / a)) + dot(b2,cos(dot(2,w) / a)) + dot(b3,cos(dot(3,w) / a)))
# PROJ_Lookback.m:46
    dw=dot(dot(2,pi),a) / N
# PROJ_Lookback.m:47
    grand=dot(dw,(arange(1,N - 1)))
# PROJ_Lookback.m:47
    
    beta=dot(Cons,real(fft(concat([1 / (dot(32,a ** 4)),multiply(exp(dot(dot(- 1j,zmin),grand)),feval(grandG,grand))]))))
# PROJ_Lookback.m:48
    Lambda=dot(a,(dot(2 / 3,beta(arange(K,1,- 1)).T) + dot(1 / 6,(beta(arange(K + 1,2,- 1)).T + concat([beta(arange(K - 1,1,- 1)),0]).T))))
# PROJ_Lookback.m:50
    toepM=concat([[beta(arange(K,1,- 1)).T],[0],[beta(arange(dot(2,K) - 1,K,- 1),+ 1).T]])
# PROJ_Lookback.m:51
    toepM=fft(toepM)
# PROJ_Lookback.m:51
    #### Simpson rule
    weights=ones(1,K)
# PROJ_Lookback.m:54
    weights[1]=0.5
# PROJ_Lookback.m:54
    weights[K]=0.5
# PROJ_Lookback.m:54
    #### m = 1
    fvec=copy(Lambda)
# PROJ_Lookback.m:57
    
    Thet=zeros(K,1)
# PROJ_Lookback.m:58
    #### Extra
    Evec1=concat([beta(arange(K - 1,1,- 1)),0]).T
# PROJ_Lookback.m:61
    d11=1757 / 17280
# PROJ_Lookback.m:63
    d22=21757 / 30240
# PROJ_Lookback.m:63
    d33=2371 / 20160
# PROJ_Lookback.m:63
    d44=149 / 6048
# PROJ_Lookback.m:63
    d55=- 613 / 120960
# PROJ_Lookback.m:63
    h2=- 1 / 720
# PROJ_Lookback.m:64
    h1=31 / 180
# PROJ_Lookback.m:64
    h0=79 / 120
# PROJ_Lookback.m:64
    #Cubic interpolation for the extra vec
    v1=73 / 2520
# PROJ_Lookback.m:67
    v2=47 / 2520
# PROJ_Lookback.m:67
    v3=- 19 / 2520
# PROJ_Lookback.m:67
    v4=1 / 630
# PROJ_Lookback.m:67
    for m in arange(2,M,1).reshape(-1):
        zm=1 - dot(dot(dx,weights),fvec)
# PROJ_Lookback.m:70
        ############
        Thetastar1=dot(v1,fvec(1)) + dot(v2,fvec(2)) + dot(v3,fvec(3)) + dot(v4,fvec(4))
# PROJ_Lookback.m:73
        Thet[1]=(dot(13,fvec(1)) + dot(15,fvec(2)) - dot(5,fvec(3)) + fvec(4)) / 48
# PROJ_Lookback.m:74
        Thet[2]=dot(d11,fvec(1)) + dot(d22,fvec(2)) + dot(d33,fvec(3)) + dot(d44,fvec(4)) + dot(d55,fvec(5))
# PROJ_Lookback.m:75
        Thet[arange(3,K - 2)]=dot(h0,fvec(arange(3,K - 2))) + dot(h1,(fvec(arange(2,K - 3)) + fvec(arange(4,K - 1)))) + dot(h2,(fvec(arange(1,K - 4)) + fvec(arange(5,K))))
# PROJ_Lookback.m:76
        Thet[K - 1]=dot(d11,fvec(K)) + dot(d22,fvec(K - 1)) + dot(d33,fvec(K - 2)) + dot(d44,fvec(K - 3)) + dot(d55,fvec(K - 4))
# PROJ_Lookback.m:77
        Thet[K]=(dot(13,fvec(K)) + dot(15,fvec(K - 1)) - dot(5,fvec(K - 2)) + fvec(K - 3)) / 48
# PROJ_Lookback.m:78
        p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Lookback.m:81
        fvec[arange(1,K)]=p(arange(1,K)) + dot(zm,Lambda) + dot(Thetastar1,Evec1)
# PROJ_Lookback.m:82
    
    # All contracts are priced w.r.t floating strike looback put using parity
    
    if floating_strike == 1:
        if call != 1:
            #===========================
            E=(dot(dx,(dot(weights,(multiply((exp(dot(dx,(arange(0,K - 1)).T)) - ones(K,1)),fvec))))))
# PROJ_Lookback.m:91
            Value=dot(dot(S_0,exp(dot(- q,T))),(E))
# PROJ_Lookback.m:92
            #===========================
        else:
            E=(dot(dx,(dot(weights,(multiply((ones(K,1) - exp(dot(- dx,(arange(0,K - 1)).T))),fvec))))))
# PROJ_Lookback.m:96
            Value=dot(dot(min(W,S_0),exp(dot(- q,T))),(E))
# PROJ_Lookback.m:97
    else:
        if call != 1:
            # W*exp(-r*T) - S_0*exp(-q*T) +
            E=(dot(dx,(dot(weights,(multiply((ones(K,1) - exp(dot(- dx,(arange(0,K - 1)).T))),fvec))))))
# PROJ_Lookback.m:104
            V_fsc=dot(dot(min(W,S_0),exp(dot(- q,T))),(E))
# PROJ_Lookback.m:105
            Value=dot(W,exp(dot(- r,T))) - dot(S_0,exp(dot(- q,T))) + V_fsc
# PROJ_Lookback.m:106
        else:
            #===========================
            E=(dot(dx,(dot(weights,(multiply((exp(dot(dx,(arange(0,K - 1)).T)) - ones(K,1)),fvec))))))
# PROJ_Lookback.m:110
            V_fsp=dot(dot(max(S_0,W),exp(dot(- q,T))),(E))
# PROJ_Lookback.m:111
            Value=V_fsp + dot(S_0,exp(dot(- q,T))) - dot(exp(dot(- r,T)),W)
# PROJ_Lookback.m:112
    
    return Value
    
if __name__ == '__main__':
    pass
    