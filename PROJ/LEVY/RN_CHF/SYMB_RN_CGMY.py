# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# SYMB_RN_CGMY.m

    
@function
def SYMB_RN_CGMY(u=None,r=None,C=None,G=None,M=None,Y=None,*args,**kwargs):
    varargin = SYMB_RN_CGMY.varargin
    nargin = SYMB_RN_CGMY.nargin

    # Returns Risk Neutral SYMBOL
# C,G,M>0 , Y <2
    m=dot(dot(C,gamma(- Y)),((M - 1) ** Y - M ** Y + (G + 1) ** Y - G ** Y))
# SYMB_RN_CGMY.m:4
    
    y=dot(dot(C,gamma(- Y)),((M - dot(1j,u)) ** Y - M ** Y + (G + dot(1j,u)) ** Y - G ** Y))
# SYMB_RN_CGMY.m:5
    
    y=dot(dot(1j,u),(r - m)) + y
# SYMB_RN_CGMY.m:6
    return y
    
if __name__ == '__main__':
    pass
    