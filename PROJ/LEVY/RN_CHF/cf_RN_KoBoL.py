# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# cf_RN_KoBoL.m

    
@function
def cf_RN_KoBoL(u=None,T=None,r=None,c=None,lam_p=None,lam_m=None,nu=None,*args,**kwargs):
    varargin = cf_RN_KoBoL.varargin
    nargin = cf_RN_KoBoL.nargin

    # KoBoL RN CHF - NOTE: params have been
# written in correspondence with CGMY, which is a subclass of KoBoL
    C=copy(c)
# cf_RN_KoBoL.m:4
    M=copy(lam_p)
# cf_RN_KoBoL.m:4
    G=- lam_m
# cf_RN_KoBoL.m:4
    Y=copy(nu)
# cf_RN_KoBoL.m:4
    m=dot(dot(C,gamma(- Y)),((M - 1) ** Y - M ** Y + (G + 1) ** Y - G ** Y))
# cf_RN_KoBoL.m:5
    
    y=dot(dot(dot(C,T),gamma(- Y)),((M - dot(1j,u)) ** Y - M ** Y + (G + dot(1j,u)) ** Y - G ** Y))
# cf_RN_KoBoL.m:6
    
    y=exp(dot(dot(dot(1j,u),T),(r - m)) + y)
# cf_RN_KoBoL.m:7
    return y
    
if __name__ == '__main__':
    pass
    