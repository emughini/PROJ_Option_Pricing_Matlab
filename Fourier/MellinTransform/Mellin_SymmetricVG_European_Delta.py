# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Mellin_SymmetricVG_European_Delta.m

    
@function
def Mellin_SymmetricVG_European_Delta(S_0=None,W=None,T=None,r=None,q=None,call=None,sigma=None,nu=None,N1=None,*args,**kwargs):
    varargin = Mellin_SymmetricVG_European_Delta.varargin
    nargin = Mellin_SymmetricVG_European_Delta.nargin

    #########################################################
# About: Delta Function for European Options using Mellin Transform (Aguilar, Kirkby, Korbel, 2020)
# Models Supported: Symmetric Variance Gamma Model, VG(sigma, 0, nu)
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # Reference: 1) "Some pricing tools for the Variance Gamma model", J-P Aguilar, 2020
#            2) "Pricing, risk and volatility in subordinated marketmodels", Aguilar, Kirkby, Korbel, 2020
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# S_0 = initial stock price (e.g. 100)
# W   = strike  (e.g. 100)
# r   = interest rate (e.g. 0.05)
# q   = dividend yield (e.g. 0.05)
# T   = time remaining until maturity (in years, e.g. T=1)
# call  = 1 for call (else put)
# sigma = param in VG model
# nu = param in VG model
    
    # ----------------------
# Numerical Params 
# ----------------------
# N1     = number summation terms in the series
#########################################################
    T=T + dot(1e-07,sqrt(2))
# Mellin_SymmetricVG_European_Delta.m:28
    f=dot(W,exp(dot(- r,T)))
# Mellin_SymmetricVG_European_Delta.m:30
    k=log(S_0 / f) - dot(q,T)
# Mellin_SymmetricVG_European_Delta.m:31
    theta=0
# Mellin_SymmetricVG_European_Delta.m:33
    w_vg=log(1 - dot(theta,nu) - dot(dot(dot(0.5,sigma),sigma),nu)) / nu
# Mellin_SymmetricVG_European_Delta.m:34
    
    k_vg=k + dot(w_vg,T)
# Mellin_SymmetricVG_European_Delta.m:35
    if k_vg < 0:
        delta=delta_minus(S_0,f,T,sigma,nu,N1,k_vg)
# Mellin_SymmetricVG_European_Delta.m:38
    else:
        if k_vg > 0:
            p_minus=delta_minus(S_0,f,T,- sigma,nu,N1,k_vg)
# Mellin_SymmetricVG_European_Delta.m:41
            delta=exp(dot(- q,T)) - p_minus
# Mellin_SymmetricVG_European_Delta.m:42
        else:
            delta=delta_zero(S_0,f,T,sigma,nu,N1)
# Mellin_SymmetricVG_European_Delta.m:45
    
    if call != 1:
        delta=delta - exp(dot(- q,T))
# Mellin_SymmetricVG_European_Delta.m:49
    
    return delta
    
if __name__ == '__main__':
    pass
    
    
@function
def delta_minus(S=None,f=None,T=None,sigma=None,nu=None,N1=None,k_vg=None,*args,**kwargs):
    varargin = delta_minus.varargin
    nargin = delta_minus.nargin

    tau_vg=T / nu - 0.5 + dot(sqrt(2),1e-12)
# Mellin_SymmetricVG_European_Delta.m:56
    
    sigma_vg=dot(sigma,sqrt(nu / 2))
# Mellin_SymmetricVG_European_Delta.m:57
    N2=copy(N1)
# Mellin_SymmetricVG_European_Delta.m:59
    delta=0
# Mellin_SymmetricVG_European_Delta.m:61
    for n1 in arange(0,N1).reshape(-1):
        cons1=(- 1) ** n1 / factorial(n1)
# Mellin_SymmetricVG_European_Delta.m:63
        cons2=(- k_vg / sigma_vg) ** (n1 - 1)
# Mellin_SymmetricVG_European_Delta.m:64
        for n2 in arange(1,N2).reshape(-1):
            t1=dot(dot(dot(- n1,gamma((- n1 + n2 + 1) / 2 + tau_vg)) / gamma((- n1 + n2) / 2 + 1),cons2),sigma_vg ** (n2 - 1))
# Mellin_SymmetricVG_European_Delta.m:67
            t2=dot(dot(dot(2,gamma(dot(- 2,n1) - n2 - dot(2,tau_vg))) / gamma(- n1 + 0.5 - tau_vg),(- k_vg / sigma_vg) ** (dot(2,n1) + 1 + dot(2,tau_vg))),(- k_vg) ** (n2 - 1))
# Mellin_SymmetricVG_European_Delta.m:70
            delta=delta + dot(cons1,(t1 + t2))
# Mellin_SymmetricVG_European_Delta.m:73
    
    delta=dot(delta,f) / (dot(dot(2,S),gamma(T / nu)))
# Mellin_SymmetricVG_European_Delta.m:77
    return delta
    
if __name__ == '__main__':
    pass
    
    
@function
def delta_zero(S=None,f=None,T=None,sigma=None,nu=None,N1=None,*args,**kwargs):
    varargin = delta_zero.varargin
    nargin = delta_zero.nargin

    tau_vg=T / nu - 0.5 + dot(sqrt(2),1e-12)
# Mellin_SymmetricVG_European_Delta.m:82
    
    sigma_vg=dot(sigma,sqrt(nu / 2))
# Mellin_SymmetricVG_European_Delta.m:83
    delta=0
# Mellin_SymmetricVG_European_Delta.m:85
    for n in arange(1,N1).reshape(-1):
        t1=dot(sigma_vg ** (n - 1),gamma((n) / 2 + tau_vg)) / gamma((n + 1) / 2)
# Mellin_SymmetricVG_European_Delta.m:87
        delta=delta + t1
# Mellin_SymmetricVG_European_Delta.m:88
    
    delta=dot(delta,f) / (dot(dot(2,S),gamma(T / nu)))
# Mellin_SymmetricVG_European_Delta.m:90
    return delta
    
if __name__ == '__main__':
    pass
    