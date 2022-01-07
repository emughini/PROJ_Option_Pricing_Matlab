# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_European.m

    
@function
def PROJ_European(order=None,N=None,alph=None,r=None,q=None,T=None,S_0=None,W=None,call=None,rnCHF=None,c1=None,*args,**kwargs):
    varargin = PROJ_European.varargin
    nargin = PROJ_European.nargin

    #########################################################
# About: Pricing Function for European Options using PROJ method
# Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # References:  1) Efficient Option Pricing by Frame Duality with the Fast Fourier Transform. 
#                 SIAM J. Financial Math (2015), Kirkby, J.L
#              2) Robust option pricing with characteristic functions and the B-spline order of density projection,
#                 J. Compuational Finance (2017), Kirkby, J.L
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# S_0 = initial stock price (e.g. 100)
# W   = strike  (e.g. 100)
# r   = interest rate (e.g. 0.05)
# q   = dividend yield (e.g. 0.05)
# T   = time remaining until maturity (in years, e.g. T=1)
# call  = 1 for call (else put)
# rnCHF = risk netural characteristic function (function handle with single argument)
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# order = 0,1,2,3  (Order of spline: Haar,Linear,Quadratic,Cubic
# c1    = mean return, first cumulant (incorporates T.. can safefly set to zero for small maturities, say T<=2)
# alph  = grid with is 2*alph
# N     = number of grid/basis points (power of 2, e.g. 2^12), resolution = 2*alph/(N-1)
#########################################################
    
    dx=dot(2,alph) / (N - 1)
# PROJ_European.m:33
    a=1 / dx
# PROJ_European.m:33
    lws=log(W / S_0)
# PROJ_European.m:35
    lam=c1 - dot((N / 2 - 1),dx)
# PROJ_European.m:36
    nbar=floor(dot(a,(lws - lam)) + 1)
# PROJ_European.m:37
    if nbar >= N:
        nbar=N - 1
# PROJ_European.m:39
    
    xmin=lws - dot((nbar - 1),dx)
# PROJ_European.m:41
    dw=dot(2,pi) / (dot(N,dx))
# PROJ_European.m:43
    omega=(arange(dw,dot((N - 1),dw),dw))
# PROJ_European.m:44
    
    ##########################################################################
#-----------   CUBIC  ---------------------
##########################################################################
    if order == 3:
        b0=1208 / 2520
# PROJ_European.m:50
        b1=1191 / 2520
# PROJ_European.m:50
        b2=120 / 2520
# PROJ_European.m:50
        b3=1 / 2520
# PROJ_European.m:50
        grand=lambda w=None: multiply(rnCHF(w),(sin(w / (dot(2,a))) / w) ** 4.0) / (b0 + dot(b1,cos(w / a)) + dot(b2,cos(dot(2,w) / a)) + dot(b3,cos(dot(3,w) / a)))
# PROJ_European.m:51
        beta=real(fft(concat([1 / (dot(32,a ** 4)),multiply(exp(dot(dot(- 1j,xmin),omega)),feval(grand,omega))])))
# PROJ_European.m:52
        G=zeros(1,nbar + 1)
# PROJ_European.m:54
        G[nbar + 1]=dot(W,(1 / 24 - dot(dot(1 / 20,exp(dx)),(exp(dot(- 7 / 4,dx)) / 54 + exp(dot(- 1.5,dx)) / 18 + exp(dot(- 1.25,dx)) / 2 + dot(7,exp(- dx)) / 27))))
# PROJ_European.m:55
        G[nbar]=dot(W,(0.5 - dot(0.05,(28 / 27 + exp(dot(- 7 / 4,dx)) / 54 + exp(dot(- 1.5,dx)) / 18 + exp(dot(- 1.25,dx)) / 2 + dot(14,exp(- dx)) / 27 + dot(121 / 54,exp(dot(- 0.75,dx))) + dot(23 / 18,exp(dot(- 0.5,dx))) + dot(235 / 54,exp(dot(- 0.25,dx)))))))
# PROJ_European.m:57
        G[nbar - 1]=dot(W,(23 / 24 - dot(exp(- dx) / 90,((28 + dot(7,exp(- dx))) / 3 + (dot(14,exp(dx)) + exp(dot(- 7 / 4,dx)) + dot(242,cosh(dot(0.75,dx))) + dot(470,cosh(dot(0.25,dx)))) / 12 + dot(0.25,(exp(dot(- 1.5,dx)) + dot(9,exp(dot(- 1.25,dx))) + dot(46,cosh(dot(0.5,dx)))))))))
# PROJ_European.m:60
        G[arange(1,nbar - 2)]=W - dot(dot(S_0,exp(xmin + dot(dx,(arange(0,nbar - 3))))) / 90,(dot(14 / 3,(2 + cosh(dx))) + dot(0.5,(cosh(dot(1.5,dx)) + dot(9,cosh(dot(1.25,dx))) + dot(23,cosh(dot(0.5,dx))))) + dot(1 / 6,(cosh(dot(7 / 4,dx)) + dot(121,cosh(dot(0.75,dx))) + dot(235,cosh(dot(0.25,dx)))))))
# PROJ_European.m:64
        Cons=dot(32,a ** 4)
# PROJ_European.m:68
        ##########################################################################
#-----------     QUADRATIC  ---------------------
##########################################################################
    else:
        if order == 2:
            grand=lambda w=None: multiply(rnCHF(w),(sin(w / (dot(2,a))) / w) ** 3.0) / (dot(26,cos(w / a)) + cos(dot(2,w) / a) + 33)
# PROJ_European.m:73
            beta=real(fft(concat([1 / (dot(960,a ** 3)),multiply(exp(dot(dot(- 1j,xmin),omega)),feval(grand,omega))])))
# PROJ_European.m:74
            G=zeros(1,nbar + 1)
# PROJ_European.m:76
            G[nbar + 1]=dot(W,(1 / 48 - dot(exp(dx),(exp(dot(- 11 / 8,dx)) / 720 + exp(dot(- 1.25,dx)) / 480 + exp(dot(- 9 / 8,dx)) / 80 + dot(7 / 1440,exp(- dx))))))
# PROJ_European.m:77
            G[nbar]=dot(W,(0.5 - dot(0.1,(7 / 24 + exp(dot(- 1.25,dx)) / 9 + exp(- dx) / 6 + exp(dot(- 0.75,dx)) + dot(7 / 12,exp(dot(- 0.5,dx))) + dot(13 / 12,exp(dot(- 3 / 8,dx))) + dot(11 / 24,exp(- dx / 4)) + dot(47 / 36,exp(- dx / 8))))))
# PROJ_European.m:78
            G[nbar - 1]=dot(W,(47 / 48 - dot(dot(exp(- dx),0.1),(1 + exp(dot(- 1.25,dx)) / 9 + exp(- dx) / 6 + exp(dot(- 0.75,dx)) + dot(7 / 9,exp(dot(- 0.5,dx))) + dot(44 / 9,cosh(dx / 4)) + dot(7 / 12,exp(dot(0.5,dx))) + dot(49 / 72,exp(dot(5 / 8,dx))) + dot(3 / 16,exp(dot(0.75,dx))) + dot(25 / 72,exp(dot(7 / 8,dx))) + dot(7 / 144,exp(dx))))))
# PROJ_European.m:79
            G[arange(1,nbar - 2)]=W - dot(dot(dot(exp(xmin + dot(dx,(arange(0,nbar - 3)))),S_0),0.1),(1 + dot(2 / 9,cosh(dot(1.25,dx))) + cosh(dx) / 3 + dot(2,cosh(dot(0.75,dx))) + dot(14 / 9,cosh(dot(0.5,dx))) + dot(44 / 9,cosh(dot(0.25,dx)))))
# PROJ_European.m:81
            Cons=dot(960,a ** (3))
# PROJ_European.m:83
            ##########################################################################
#-----------     LINEAR  ---------------------
##########################################################################
        else:
            if order == 1:
                grand=lambda w=None: multiply(rnCHF(w),(sin(w / (dot(2,a))) / w) ** 2.0) / (2 + cos(w / a))
# PROJ_European.m:88
                beta=real(fft(concat([1 / (dot(24,a ** 2)),multiply(exp(dot(dot(- 1j,xmin),omega)),feval(grand,omega))])))
# PROJ_European.m:89
                G=zeros(1,nbar)
# PROJ_European.m:91
                G[nbar]=dot(W,(0.5 - (7 / 6 + dot(4 / 3,exp(dot(- 0.75,dx))) + exp(dot(- 0.5,dx)) + dot(4,exp(dot(- 0.25,dx)))) / 15))
# PROJ_European.m:92
                G[arange(1,nbar - 1)]=W - dot(dot(exp(xmin + dot(dx,(arange(0,nbar - 2)))),S_0) / 15,(7 / 3 + dot(8 / 3,cosh(dot(0.75,dx))) + dot(2,cosh(dot(0.5,dx))) + dot(8,cosh(dot(0.25,dx)))))
# PROJ_European.m:93
                Cons=dot(24,a ** 2)
# PROJ_European.m:95
                ##########################################################################
#-----------     HAAR  ---------------------
##########################################################################
            else:
                if order == 0:
                    grand=lambda w=None: multiply(rnCHF(w),(sin(w / (dot(2,a))) / w))
# PROJ_European.m:100
                    beta=real(fft(concat([1 / (dot(4,a)),multiply(exp(dot(dot(- 1j,xmin),omega)),feval(grand,omega))])))
# PROJ_European.m:101
                    G=zeros(1,nbar)
# PROJ_European.m:103
                    G[nbar]=dot(W,(0.5 - dot(a,(1 - exp(dot(- 0.5,dx))))))
# PROJ_European.m:104
                    G[arange(1,nbar - 1)]=W - dot(dot(dot(dot(exp(xmin + dot(dx,(arange(0,nbar - 2)))),S_0),2),a),sinh(dx / 2))
# PROJ_European.m:105
                    Cons=dot(4,a)
# PROJ_European.m:107
    
    ##########################################################################
    
    if call == 1:
        price=dot(dot(dot(Cons,exp(dot(- r,T))) / N,G),(beta(arange(1,length(G))).T)) + dot(S_0,exp(dot(- q,T))) - dot(W,exp(dot(- r,T)))
# PROJ_European.m:112
    else:
        price=dot(dot(dot(Cons,exp(dot(- r,T))) / N,G),(beta(arange(1,length(G))).T))
# PROJ_European.m:114
    
    price=max(price,0)
# PROJ_European.m:117
    
    return price
    
if __name__ == '__main__':
    pass
    