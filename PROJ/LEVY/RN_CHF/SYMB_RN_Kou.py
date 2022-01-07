# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# SYMB_RN_Kou.m

    
@function
def SYMB_RN_Kou(u=None,r=None,sigma=None,lam=None,p_up=None,eta1=None,eta2=None,*args,**kwargs):
    varargin = SYMB_RN_Kou.varargin
    nargin = SYMB_RN_Kou.nargin

    # Kou Double Exponential RN symbol
# p_up = prob of upward jump
    
    sig2=dot(0.5,sigma ** 2)
# SYMB_RN_Kou.m:5
    temp1=r - sig2 - dot(lam,(dot((1 - p_up),eta2) / (eta2 + 1) + dot(p_up,eta1) / (eta1 - 1) - 1))
# SYMB_RN_Kou.m:6
    temp2=dot(- sig2,u ** 2) + dot(lam,(dot((1 - p_up),eta2) / (eta2 + dot(1j,u)) + dot(p_up,eta1) / (eta1 - dot(1j,u)) - 1))
# SYMB_RN_Kou.m:7
    y=dot(dot(1j,u),temp1) + temp2
# SYMB_RN_Kou.m:8
    return y
    
if __name__ == '__main__':
    pass
    