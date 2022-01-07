# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# cf_RN_MJD.m

    
@function
def cf_RN_MJD(u=None,r=None,T=None,sigma=None,muj=None,sigmaj=None,lam=None,*args,**kwargs):
    varargin = cf_RN_MJD.varargin
    nargin = cf_RN_MJD.nargin

    # Return: risk neutral chf evaluated at u
# r = interest rate
# sigma = volatility (per time unit?)
# T = time units til maturity
# Jump ~ N(muj,sigmaj^2), i.e jumps in log return are normal
# lam = E[#jumps per unit of T]
    
    sig2=dot(0.5,sigma ** 2)
# cf_RN_MJD.m:9
    sigj2=dot(0.5,sigmaj ** 2)
# cf_RN_MJD.m:10
    y=exp(dot(dot(dot(1j,(r - sig2 - dot(lam,(exp(muj + sigj2) - 1)))),u),T) - dot(dot(sig2,u ** 2),T) + dot(dot(lam,T),(exp(dot(dot(1j,u),muj) - dot(sigj2,u ** 2)) - 1)))
# cf_RN_MJD.m:11
    return y
    
if __name__ == '__main__':
    pass
    