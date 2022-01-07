# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# cf_RN_BilateralGamma.m

    
@function
def cf_RN_BilateralGamma(u=None,r=None,T=None,alpha_p=None,lam_p=None,alpha_m=None,lam_m=None,*args,**kwargs):
    varargin = cf_RN_BilateralGamma.varargin
    nargin = cf_RN_BilateralGamma.nargin

    # Risk-Neutral Characterisitc Function for Bilateral Gamma model
    zeta=- log(dot((lam_p / (lam_p - 1)) ** alpha_p,(lam_m / (lam_m + 1)) ** alpha_m))
# cf_RN_BilateralGamma.m:3
    RNmu=r + zeta
# cf_RN_BilateralGamma.m:4
    y=multiply(multiply(exp(dot(T,(dot(dot(1j,u),RNmu)))),(lam_p / (lam_p - dot(1j,u))) ** (dot(alpha_p,T))),(lam_m / (lam_m + dot(1j,u))) ** (dot(alpha_m,T)))
# cf_RN_BilateralGamma.m:6
    return y
    
if __name__ == '__main__':
    pass
    