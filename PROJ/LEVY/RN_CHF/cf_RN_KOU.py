# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# cf_RN_KOU.m

    
@function
def cf_RN_KOU(u=None,T=None,r=None,sigma=None,lam=None,p_up=None,eta1=None,eta2=None,*args,**kwargs):
    varargin = cf_RN_KOU.varargin
    nargin = cf_RN_KOU.nargin

    # Kou Double Exponential RN CHF
# p_up = prob of upward jump
    sig2=dot(0.5,sigma ** 2)
# cf_RN_KOU.m:4
    temp1=r - sig2 - dot(lam,(dot((1 - p_up),eta2) / (eta2 + 1) + dot(p_up,eta1) / (eta1 - 1) - 1))
# cf_RN_KOU.m:5
    temp2=dot(- sig2,u ** 2) + dot(lam,(dot((1 - p_up),eta2) / (eta2 + dot(1j,u)) + dot(p_up,eta1) / (eta1 - dot(1j,u)) - 1))
# cf_RN_KOU.m:6
    y=exp(dot(dot(dot(T,1j),u),temp1) + dot(T,temp2))
# cf_RN_KOU.m:7
    return y
    
if __name__ == '__main__':
    pass
    