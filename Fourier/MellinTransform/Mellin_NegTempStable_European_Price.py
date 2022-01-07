# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Mellin_NegTempStable_European_Price.m

    
@function
def Mellin_NegTempStable_European_Price(S_0=None,W=None,T=None,r=None,q=None,call=None,sigma=None,alpha=None,lambda_=None,N1=None,tol=None,*args,**kwargs):
    varargin = Mellin_NegTempStable_European_Price.varargin
    nargin = Mellin_NegTempStable_European_Price.nargin

    #########################################################
# About: Pricing Function for European Options using Mellin Transform
# Models Supported: Negative Tempered Stable
# Returns: price of contract
# Author: Justin Lars Kirkby/ Jean-Philippe Aguilar
    
    # Reference: 1) "Closed-form option pricing in exponential Levy models", Aguilar and Kirkby, 2021
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# S_0 = initial stock price (e.g. 100)
# W   = strike  (e.g. 100)
# r   = interest rate (e.g. 0.05)
# q   = dividend yield (e.g. 0.05)
# T   = time remaining until maturity (in years, e.g. T=1)
# call  = 1 for call (else put)
    
    # sigma = param in model
# alpha = param in model
# lambda = param in model
    
    # ----------------------
# Numerical Params 
# ----------------------
# N1  = maximum number summation terms in the series, will sum fewer terms
#       if error threshold (tol) is reached
# tol = desired error threshold of price (will stop adding terms once satisfied) 
#########################################################
    if nargin < 11:
        tol=0
# Mellin_NegTempStable_European_Price.m:32
    
    N2=copy(N1)
# Mellin_NegTempStable_European_Price.m:35
    N3=copy(N1)
# Mellin_NegTempStable_European_Price.m:36
    F=dot(W,exp(dot(- r,T)))
# Mellin_NegTempStable_European_Price.m:38
    w_=sigma ** alpha / cos(dot(alpha,pi) / 2)
# Mellin_NegTempStable_European_Price.m:39
    
    wts_=dot(w_,((lambda_ + 1) ** alpha - lambda_ ** alpha))
# Mellin_NegTempStable_European_Price.m:40
    c_=- w_ / gamma(- alpha)
# Mellin_NegTempStable_European_Price.m:41
    k_=log(S_0 / W) + dot((r - q + wts_),T)
# Mellin_NegTempStable_European_Price.m:43
    sum=0
# Mellin_NegTempStable_European_Price.m:44
    last=0
# Mellin_NegTempStable_European_Price.m:45
    cons=dot(F,exp(dot(dot(lambda_ ** alpha,w_),T))) / alpha
# Mellin_NegTempStable_European_Price.m:46
    tol=tol / cons
# Mellin_NegTempStable_European_Price.m:47
    wt=dot(- w_,T)
# Mellin_NegTempStable_European_Price.m:49
    start_N3=1
# Mellin_NegTempStable_European_Price.m:50
    
    for n1 in arange(0,N1).reshape(-1):
        fn1=factorial(n1)
# Mellin_NegTempStable_European_Price.m:53
        for n2 in arange(0,N2).reshape(-1):
            fn2=factorial(n2)
# Mellin_NegTempStable_European_Price.m:55
            for n3 in arange(start_N3,N3).reshape(-1):
                g=pochhammer(1 - n1 + n3,n2)
# Mellin_NegTempStable_European_Price.m:57
                c=(n1 - n2 - n3) / alpha
# Mellin_NegTempStable_European_Price.m:58
                term=dot(dot(dot(g,lambda_ ** n2),k_ ** n1),wt ** (- c)) / (dot(dot(fn1,fn2),gamma(1 - c)))
# Mellin_NegTempStable_European_Price.m:59
                sum=sum + term
# Mellin_NegTempStable_European_Price.m:60
        if n1 > 1 and abs(sum - last) < tol:
            break
        last=copy(sum)
# Mellin_NegTempStable_European_Price.m:66
    
    price=dot(cons,sum)
# Mellin_NegTempStable_European_Price.m:69
    if call != 1:
        price=price - (dot(S_0,exp(dot(- q,T))) - dot(W,exp(dot(- r,T))))
# Mellin_NegTempStable_European_Price.m:72
    
    return price
    
if __name__ == '__main__':
    pass
    
    
@function
def pochhammer(a=None,n=None,*args,**kwargs):
    varargin = pochhammer.varargin
    nargin = pochhammer.nargin

    if (a == 0 and n <= 0) or (n == 0 and a > 0):
        p=1
# Mellin_NegTempStable_European_Price.m:80
    else:
        if a == 0 and n > 0:
            p=0
# Mellin_NegTempStable_European_Price.m:82
        else:
            if a > 0:
                if n == 1:
                    p=copy(a)
# Mellin_NegTempStable_European_Price.m:85
                else:
                    if n > 0:
                        p=prod(arange(a,a + n - 1))
# Mellin_NegTempStable_European_Price.m:87
                    else:
                        p=copy(inf)
# Mellin_NegTempStable_European_Price.m:90
            else:
                p=neg_poch(a,n)
# Mellin_NegTempStable_European_Price.m:93
    
    
    return p
    
if __name__ == '__main__':
    pass
    
    
@function
def neg_poch(m=None,n=None,*args,**kwargs):
    varargin = neg_poch.varargin
    nargin = neg_poch.nargin

    # Used for (-m)_n, m >= 1
    
    m=- m
# Mellin_NegTempStable_European_Price.m:101
    if n > m:
        p=0
# Mellin_NegTempStable_European_Price.m:104
    else:
        p=dot((- 1) ** n,factorial(m)) / factorial(m - n)
# Mellin_NegTempStable_European_Price.m:106
    
    return p
    
if __name__ == '__main__':
    pass
    