# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Mellin_FMLS_European_Price.m

    
@function
def Mellin_FMLS_European_Price(S_0=None,W=None,T=None,r=None,q=None,call=None,sigma=None,alpha=None,N1=None,tol=None,*args,**kwargs):
    varargin = Mellin_FMLS_European_Price.varargin
    nargin = Mellin_FMLS_European_Price.nargin

    #########################################################
# About: Pricing Function for European Options using Mellin Transform
# Models Supported: Finite Moment Log Stable (FMLS)
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
    
    # ----------------------
# Numerical Params 
# ----------------------
# N1  = maximum number summation terms in the series, will sum fewer terms
#       if error threshold (tol) is reached
# tol = desired error threshold of price (will stop adding terms once satisfied) 
#########################################################
    
    if nargin < 10:
        tol=0
# Mellin_FMLS_European_Price.m:32
    
    N2=copy(N1)
# Mellin_FMLS_European_Price.m:35
    F=dot(W,exp(dot(- r,T)))
# Mellin_FMLS_European_Price.m:37
    w_=sigma ** alpha / cos(dot(pi,alpha) / 2)
# Mellin_FMLS_European_Price.m:38
    k_=log(S_0 / W) + dot((r - q + w_),T)
# Mellin_FMLS_European_Price.m:39
    sum=0
# Mellin_FMLS_European_Price.m:40
    last=0
# Mellin_FMLS_European_Price.m:40
    wt=dot(- w_,T)
# Mellin_FMLS_European_Price.m:42
    cons=F / alpha
# Mellin_FMLS_European_Price.m:43
    tol=tol / cons
# Mellin_FMLS_European_Price.m:44
    for n1 in arange(0,N1).reshape(-1):
        fn1=factorial(n1)
# Mellin_FMLS_European_Price.m:47
        kn1=k_ ** n1
# Mellin_FMLS_European_Price.m:48
        for n2 in arange(1,N2).reshape(-1):
            c=(n1 - n2) / alpha
# Mellin_FMLS_European_Price.m:50
            numer=dot(kn1,wt ** (- c))
# Mellin_FMLS_European_Price.m:51
            denom=dot(fn1,gamma(1 - c))
# Mellin_FMLS_European_Price.m:52
            sum=sum + numer / denom
# Mellin_FMLS_European_Price.m:53
        if n1 > 1 and abs(sum - last) < tol:
            break
        last=copy(sum)
# Mellin_FMLS_European_Price.m:58
    
    price=dot(cons,sum)
# Mellin_FMLS_European_Price.m:62
    if call != 1:
        price=price - (dot(S_0,exp(dot(- q,T))) - dot(W,exp(dot(- r,T))))
# Mellin_FMLS_European_Price.m:65
    
    return price
    
if __name__ == '__main__':
    pass
    