# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Mellin_SymmetricVG_European_Price.m

    
@function
def Mellin_SymmetricVG_European_Price(S_0=None,W=None,T=None,r=None,q=None,call=None,sigma=None,nu=None,N1=None,tol=None,*args,**kwargs):
    varargin = Mellin_SymmetricVG_European_Price.varargin
    nargin = Mellin_SymmetricVG_European_Price.nargin

    #########################################################
# About: Pricing Function for European Options using Mellin Transform (Aguilar 2019)
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
    if nargin < 10:
        tol=0
# Mellin_SymmetricVG_European_Price.m:29
    
    F=dot(W,exp(dot(- r,T)))
# Mellin_SymmetricVG_European_Price.m:32
    k=log(S_0 / F) - dot(q,T)
# Mellin_SymmetricVG_European_Price.m:33
    theta=0
# Mellin_SymmetricVG_European_Price.m:35
    w_vg=log(1 - dot(theta,nu) - dot(dot(dot(0.5,sigma),sigma),nu)) / nu
# Mellin_SymmetricVG_European_Price.m:36
    
    k_vg=k + dot(w_vg,T)
# Mellin_SymmetricVG_European_Price.m:37
    if k_vg < 0:
        price=price_minus(F,T,sigma,nu,N1,k_vg,tol)
# Mellin_SymmetricVG_European_Price.m:40
    else:
        if k_vg > 0:
            p_minus=price_minus(F,T,- sigma,nu,N1,k_vg,tol)
# Mellin_SymmetricVG_European_Price.m:43
            price=dot(S_0,exp(dot(- q,T))) - dot(W,exp(dot(- r,T))) - p_minus
# Mellin_SymmetricVG_European_Price.m:44
        else:
            price=price_zero(F,T,sigma,nu,N1,tol)
# Mellin_SymmetricVG_European_Price.m:47
    
    if call != 1:
        price=price - (dot(S_0,exp(dot(- q,T))) - dot(W,exp(dot(- r,T))))
# Mellin_SymmetricVG_European_Price.m:51
    
    return price
    
if __name__ == '__main__':
    pass
    
    
@function
def price_minus(F=None,T=None,sigma=None,nu=None,N1=None,k_vg=None,tol=None,*args,**kwargs):
    varargin = price_minus.varargin
    nargin = price_minus.nargin

    tau_vg=T / nu - 0.5 + dot(sqrt(2),1e-12)
# Mellin_SymmetricVG_European_Price.m:58
    
    sigma_vg=dot(sigma,sqrt(nu / 2))
# Mellin_SymmetricVG_European_Price.m:59
    N2=copy(N1)
# Mellin_SymmetricVG_European_Price.m:61
    mult=F / (dot(2,gamma(T / nu)))
# Mellin_SymmetricVG_European_Price.m:63
    tol=tol / mult
# Mellin_SymmetricVG_European_Price.m:64
    last=0
# Mellin_SymmetricVG_European_Price.m:66
    sum=0
# Mellin_SymmetricVG_European_Price.m:67
    for n1 in arange(0,N1).reshape(-1):
        cons1=(- 1) ** n1 / factorial(n1)
# Mellin_SymmetricVG_European_Price.m:69
        cons2=(- k_vg / sigma_vg) ** n1
# Mellin_SymmetricVG_European_Price.m:70
        for n2 in arange(1,N2).reshape(-1):
            t1=dot(dot(gamma((- n1 + n2 + 1) / 2 + tau_vg) / gamma((- n1 + n2) / 2 + 1),cons2),sigma_vg ** n2)
# Mellin_SymmetricVG_European_Price.m:73
            t2=dot(dot(dot(2,gamma(dot(- 2,n1) - n2 - 1 - dot(2,tau_vg))) / gamma(- n1 + 0.5 - tau_vg),(- k_vg / sigma_vg) ** (dot(2,n1) + 1 + dot(2,tau_vg))),(- k_vg) ** n2)
# Mellin_SymmetricVG_European_Price.m:76
            sum=sum + dot(cons1,(t1 + t2))
# Mellin_SymmetricVG_European_Price.m:79
        if n1 > 1 and abs(sum - last) < tol:
            break
        last=copy(sum)
# Mellin_SymmetricVG_European_Price.m:84
    
    sum=dot(sum,mult)
# Mellin_SymmetricVG_European_Price.m:87
    return sum
    
if __name__ == '__main__':
    pass
    
    
@function
def price_zero(F=None,T=None,sigma=None,nu=None,N1=None,tol=None,*args,**kwargs):
    varargin = price_zero.varargin
    nargin = price_zero.nargin

    tau_vg=T / nu - 0.5 + dot(sqrt(2),1e-12)
# Mellin_SymmetricVG_European_Price.m:92
    
    sigma_vg=dot(sigma,sqrt(nu / 2))
# Mellin_SymmetricVG_European_Price.m:93
    mult=F / (dot(2,gamma(T / nu)))
# Mellin_SymmetricVG_European_Price.m:95
    tol=tol / mult
# Mellin_SymmetricVG_European_Price.m:96
    last=0
# Mellin_SymmetricVG_European_Price.m:97
    sum=0
# Mellin_SymmetricVG_European_Price.m:98
    for n in arange(1,N1).reshape(-1):
        t1=dot(sigma_vg ** n,gamma((n + 1) / 2 + tau_vg)) / gamma(n / 2 + 1)
# Mellin_SymmetricVG_European_Price.m:100
        sum=sum + t1
# Mellin_SymmetricVG_European_Price.m:101
        if n1 > 1 and abs(sum - last) < tol:
            break
        last=copy(sum)
# Mellin_SymmetricVG_European_Price.m:105
    
    sum=dot(sum,mult)
# Mellin_SymmetricVG_European_Price.m:107
    return sum
    
if __name__ == '__main__':
    pass
    