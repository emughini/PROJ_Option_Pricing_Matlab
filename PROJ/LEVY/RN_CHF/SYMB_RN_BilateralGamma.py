# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# SYMB_RN_BilateralGamma.m

    
@function
def SYMB_RN_BilateralGamma(u=None,r=None,alpha_p=None,lam_p=None,alpha_m=None,lam_m=None,*args,**kwargs):
    varargin = SYMB_RN_BilateralGamma.varargin
    nargin = SYMB_RN_BilateralGamma.nargin

    # Risk-Neutral Levy Symbol for Bilateral Gamma model
    
    zeta=- log(dot((lam_p / (lam_p - 1)) ** alpha_p,(lam_m / (lam_m + 1)) ** alpha_m))
# SYMB_RN_BilateralGamma.m:4
    RNmu=r + zeta
# SYMB_RN_BilateralGamma.m:5
    y=dot(dot(1j,u),RNmu) + log(multiply((lam_p / (lam_p - dot(1j,u))) ** alpha_p,(lam_m / (lam_m + dot(1j,u))) ** alpha_m))
# SYMB_RN_BilateralGamma.m:7
    return y
    
if __name__ == '__main__':
    pass
    