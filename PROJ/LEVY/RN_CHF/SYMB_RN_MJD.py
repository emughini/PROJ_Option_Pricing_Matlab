# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# SYMB_RN_MJD.m

    
@function
def SYMB_RN_MJD(u=None,r=None,sigma=None,muj=None,sigmaj=None,lam=None,*args,**kwargs):
    varargin = SYMB_RN_MJD.varargin
    nargin = SYMB_RN_MJD.nargin

    #UNTITLED3 Summary of this function goes here
#   Detailed explanation goes here
    sig2=dot(0.5,sigma ** 2)
# SYMB_RN_MJD.m:4
    sigj2=dot(0.5,sigmaj ** 2)
# SYMB_RN_MJD.m:4
    y=dot(dot(1j,(r - sig2 - dot(lam,(exp(muj + sigj2) - 1)))),u) - dot(sig2,u ** 2) + dot(lam,(exp(dot(dot(1j,u),muj) - dot(sigj2,u ** 2)) - 1))
# SYMB_RN_MJD.m:5
    return y
    
if __name__ == '__main__':
    pass
    