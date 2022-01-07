# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Mellin_SymmetricVG_European_Gamma.m

    
@function
def Mellin_SymmetricVG_European_Gamma(S_0=None,W=None,T=None,r=None,q=None,sigma=None,nu=None,N1=None,*args,**kwargs):
    varargin = Mellin_SymmetricVG_European_Gamma.varargin
    nargin = Mellin_SymmetricVG_European_Gamma.nargin

    #########################################################
# About: Gamma Function for European Options using Mellin Transform (Aguilar, Kirkby, Korbel 2020)
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
# sigma = param in VG model
# nu = param in VG model
    
    # ----------------------
# Numerical Params 
# ----------------------
# N1     = number summation terms in the series
#########################################################
    
    T=T + dot(1e-07,sqrt(2))
# Mellin_SymmetricVG_European_Gamma.m:28
    
    f=dot(W,exp(dot(- r,T)))
# Mellin_SymmetricVG_European_Gamma.m:30
    k=log(S_0 / f) - dot(q,T)
# Mellin_SymmetricVG_European_Gamma.m:31
    theta=0
# Mellin_SymmetricVG_European_Gamma.m:33
    w_vg=log(1 - dot(theta,nu) - dot(dot(dot(0.5,sigma),sigma),nu)) / nu
# Mellin_SymmetricVG_European_Gamma.m:34
    
    k_vg=k + dot(w_vg,T)
# Mellin_SymmetricVG_European_Gamma.m:35
    if k_vg < 0:
        gam=gam_minus(S_0,f,T,sigma,nu,N1,k_vg)
# Mellin_SymmetricVG_European_Gamma.m:38
    else:
        if k_vg > 0:
            gam=- gam_minus(S_0,f,T,- sigma,nu,N1,k_vg)
# Mellin_SymmetricVG_European_Gamma.m:41
        else:
            gam=gam_zero(S_0,f,T,sigma,nu)
# Mellin_SymmetricVG_European_Gamma.m:44
    
    return gam
    
if __name__ == '__main__':
    pass
    
    
@function
def gam_minus(S=None,f=None,T=None,sigma=None,nu=None,N1=None,k_vg=None,*args,**kwargs):
    varargin = gam_minus.varargin
    nargin = gam_minus.nargin

    tau_vg=T / nu - 0.5 + dot(sqrt(2),1e-12)
# Mellin_SymmetricVG_European_Gamma.m:51
    
    sigma_vg=dot(sigma,sqrt(nu / 2))
# Mellin_SymmetricVG_European_Gamma.m:52
    gam=0
# Mellin_SymmetricVG_European_Gamma.m:54
    for n in arange(0,N1).reshape(-1):
        t1=dot(gamma(- n / 2 + tau_vg) / gamma((- n + 1) / 2),(- k_vg / sigma_vg) ** (n))
# Mellin_SymmetricVG_European_Gamma.m:57
        t2=dot(dot(2,gamma(dot(- 2,n) - dot(2,tau_vg))) / gamma(- n + 0.5 - tau_vg),(- k_vg / sigma_vg) ** (dot(2,n) + dot(2,tau_vg)))
# Mellin_SymmetricVG_European_Gamma.m:58
        cons1=(- 1) ** n / factorial(n)
# Mellin_SymmetricVG_European_Gamma.m:60
        gam=gam + dot(cons1,(t1 + t2))
# Mellin_SymmetricVG_European_Gamma.m:61
    
    gam=dot(gam,f) / (dot(dot(dot(dot(2,S),S),sigma_vg),gamma(T / nu)))
# Mellin_SymmetricVG_European_Gamma.m:64
    return gam
    
if __name__ == '__main__':
    pass
    
    
@function
def gam_zero(S=None,f=None,T=None,sigma=None,nu=None,*args,**kwargs):
    varargin = gam_zero.varargin
    nargin = gam_zero.nargin

    tau_vg=T / nu - 0.5 + dot(sqrt(2),1e-12)
# Mellin_SymmetricVG_European_Gamma.m:69
    
    sigma_vg=dot(sigma,sqrt(nu / 2))
# Mellin_SymmetricVG_European_Gamma.m:70
    gam=dot(f / (dot(dot(dot(dot(dot(2,sqrt(pi)),S),S),sigma_vg),gamma(T / nu))),gamma(tau_vg - 0.5)) / gamma(T / nu)
# Mellin_SymmetricVG_European_Gamma.m:72
    return gam
    
if __name__ == '__main__':
    pass
    