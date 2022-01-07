# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# SYMB_RN_NIG.m

    
@function
def SYMB_RN_NIG(u=None,r=None,alph=None,bet=None,delt=None,*args,**kwargs):
    varargin = SYMB_RN_NIG.varargin
    nargin = SYMB_RN_NIG.nargin

    # Returns Risk Neutral SYMBOL
#   Detailed explanation goes here
    asq=alph ** 2
# SYMB_RN_NIG.m:4
    bsq=bet ** 2
# SYMB_RN_NIG.m:5
    temp=sqrt(asq - bsq)
# SYMB_RN_NIG.m:6
    yy=dot(- delt,(sqrt(asq - (bet + dot(1j,u)) ** 2) - temp))
# SYMB_RN_NIG.m:7
    
    RNmu=r + dot(delt,(sqrt(asq - (bet + 1) ** 2) - temp))
# SYMB_RN_NIG.m:8
    y=dot(dot(1j,u),RNmu) + yy
# SYMB_RN_NIG.m:9
    return y
    
if __name__ == '__main__':
    pass
    