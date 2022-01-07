# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# cf_RN_CGMY.m

    
@function
def cf_RN_CGMY(u=None,T=None,r=None,C=None,G=None,M=None,Y=None,*args,**kwargs):
    varargin = cf_RN_CGMY.varargin
    nargin = cf_RN_CGMY.nargin

    # CGMY RN CHF
# C,G,M>0 , Y <2
    m=dot(dot(C,gamma(- Y)),((M - 1) ** Y - M ** Y + (G + 1) ** Y - G ** Y))
# cf_RN_CGMY.m:4
    
    y=dot(dot(dot(C,T),gamma(- Y)),((M - dot(1j,u)) ** Y - M ** Y + (G + dot(1j,u)) ** Y - G ** Y))
# cf_RN_CGMY.m:5
    
    y=exp(dot(dot(dot(1j,u),T),(r - m)) + y)
# cf_RN_CGMY.m:6
    return y
    
if __name__ == '__main__':
    pass
    