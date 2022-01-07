# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# SYMB_RN_VG.m

    
@function
def SYMB_RN_VG(u=None,r=None,sigma=None,nu=None,theta=None,*args,**kwargs):
    varargin = SYMB_RN_VG.varargin
    nargin = SYMB_RN_VG.nargin

    # Risk-Neutral Levy Symbol for Variance Gamma model
    sig2=dot(0.5,sigma ** 2)
# SYMB_RN_VG.m:3
    RNmu=r + log(1 - dot(theta,nu) - dot(sig2,nu)) / nu
# SYMB_RN_VG.m:4
    y=log(1 - dot(dot(dot(1j,theta),nu),u) + dot(dot(sig2,nu),u ** 2)) / nu
# SYMB_RN_VG.m:5
    y=dot(dot(1j,u),RNmu) - y
# SYMB_RN_VG.m:6
    return y
    
if __name__ == '__main__':
    pass
    