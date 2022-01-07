# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# SABR_Hagan_Obloj_ImpliedVol.m

    
@function
def SABR_Hagan_Obloj_ImpliedVol(Kvec=None,F0=None,nu=None,T=None,alpha=None,beta=None,rho=None,*args,**kwargs):
    varargin = SABR_Hagan_Obloj_ImpliedVol.varargin
    nargin = SABR_Hagan_Obloj_ImpliedVol.nargin

    # Calculates Implied volatility using asymptotic formulas from Obloj (correction to original SABR formulas)
# Kvec: strikes
# F0: initial forward price
# T: time to maturity of option
# (nu, alpha, beta, rho) are model parameters
    
    IVs=zeros(length(Kvec),1)
# SABR_Hagan_Obloj_ImpliedVol.m:8
    for k in arange(1,length(Kvec)).reshape(-1):
        K=Kvec(k)
# SABR_Hagan_Obloj_ImpliedVol.m:10
        z=dot((alpha / (dot(nu,(1 - beta)))),(F0 ** (1 - beta) - K ** (1 - beta)))
# SABR_Hagan_Obloj_ImpliedVol.m:12
        chiz=log((sqrt(1 - dot(dot(2,rho),z) + dot(z,z)) + z - rho) / (1 - rho))
# SABR_Hagan_Obloj_ImpliedVol.m:13
        FK=dot(F0,K)
# SABR_Hagan_Obloj_ImpliedVol.m:15
        sig0=dot(alpha,log(F0 / K)) / chiz
# SABR_Hagan_Obloj_ImpliedVol.m:17
        sig1=(dot((1 - beta),nu)) ** 2 / 24 / FK ** (1 - beta) + dot(0.25,(dot(dot(dot(rho,beta),alpha),nu))) / FK ** ((1 - beta) / 2) + dot((2 - dot(3,rho ** 2)) / 24,alpha ** 2)
# SABR_Hagan_Obloj_ImpliedVol.m:18
        IVs[k]=dot(sig0,(1.0 + dot(sig1,T)))
# SABR_Hagan_Obloj_ImpliedVol.m:22
    
    return IVs
    
if __name__ == '__main__':
    pass
    