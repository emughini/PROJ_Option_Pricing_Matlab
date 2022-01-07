# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# SYMB_RN_BSM.m

    
@function
def SYMB_RN_BSM(u=None,r=None,sigma=None,*args,**kwargs):
    varargin = SYMB_RN_BSM.varargin
    nargin = SYMB_RN_BSM.nargin

    # Return: risk neutral SYMBOL evaluated at u
# r = interest rate (or inputs r-q)
# sigma = volatility (per time unit?)
    
    y=dot(dot(1j,(r - dot(0.5,sigma ** 2))),u) - dot(dot(0.5,sigma ** 2),u ** 2)
# SYMB_RN_BSM.m:6
    return y
    
if __name__ == '__main__':
    pass
    