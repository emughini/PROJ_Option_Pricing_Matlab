# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# cf_RN_NIG.m

    
@function
def cf_RN_NIG(u=None,r=None,T=None,alpha=None,beta=None,delta=None,*args,**kwargs):
    varargin = cf_RN_NIG.varargin
    nargin = cf_RN_NIG.nargin

    
    #
    asq=alpha ** 2
# cf_RN_NIG.m:4
    bsq=beta ** 2
# cf_RN_NIG.m:5
    temp=sqrt(asq - bsq)
# cf_RN_NIG.m:6
    y=dot(- delta,(sqrt(asq - (beta + dot(1j,u)) ** 2) - temp))
# cf_RN_NIG.m:7
    
    RNmu=r + dot(delta,(sqrt(asq - (beta + 1) ** 2) - temp))
# cf_RN_NIG.m:8
    y=exp(dot(T,(dot(dot(1j,u),RNmu) + y)))
# cf_RN_NIG.m:9
    return y
    
if __name__ == '__main__':
    pass
    