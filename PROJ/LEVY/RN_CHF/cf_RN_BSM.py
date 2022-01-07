# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# cf_RN_BSM.m

    
@function
def cf_RN_BSM(u=None,r=None,T=None,sigma=None,*args,**kwargs):
    varargin = cf_RN_BSM.varargin
    nargin = cf_RN_BSM.nargin

    # Return: risk neutral chf evaluated at u
# r = interest rate (or inputs r-q)
# sigma = volatility (per time unit?)
# T = time units til maturity
    
    y=exp(dot(T,(dot(dot(1j,(r - dot(0.5,sigma ** 2))),u) - dot(dot(0.5,sigma ** 2),u ** 2))))
# cf_RN_BSM.m:7
    return y
    
if __name__ == '__main__':
    pass
    