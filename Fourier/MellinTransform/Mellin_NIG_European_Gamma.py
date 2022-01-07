# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Mellin_NIG_European_Gamma.m

    
@function
def Mellin_NIG_European_Gamma(S_0=None,W=None,T=None,r=None,q=None,alpha=None,beta=None,delta=None,N1=None,*args,**kwargs):
    varargin = Mellin_NIG_European_Gamma.varargin
    nargin = Mellin_NIG_European_Gamma.nargin

    #UNTITLED2 Summary of this function goes here
#   Detailed explanation goes here
    
    f=dot(W,exp(dot(- r,T)))
# Mellin_NIG_European_Gamma.m:5
    gam=sqrt(alpha ** 2 - beta ** 2)
# Mellin_NIG_European_Gamma.m:7
    k0=log(S_0 / W) + dot((r - q + dot(delta,(sqrt(alpha ** 2 - (beta + 1) ** 2) - gam))),T)
# Mellin_NIG_European_Gamma.m:8
    adt=dot(dot(alpha,delta),T)
# Mellin_NIG_European_Gamma.m:9
    dta=dot(dot(0.5,delta),T) / alpha
# Mellin_NIG_European_Gamma.m:10
    sum=0
# Mellin_NIG_European_Gamma.m:12
    if beta == 0:
        # Symmetric Formula
        for n in arange(0,N1).reshape(-1):
            cons1=k0 ** n / factorial(n)
# Mellin_NIG_European_Gamma.m:17
            term=dot(besselk(n / 2 + 1,adt) / gamma((- n + 1) / 2),(dta) ** (- n / 2))
# Mellin_NIG_European_Gamma.m:18
            sum=sum + dot(cons1,term)
# Mellin_NIG_European_Gamma.m:19
    else:
        # Asymmetric Formula
        pass
    
    cons=dot(dot(f,alpha),exp(dot(dot(alpha,delta),T))) / (dot(dot(S_0,S_0),sqrt(pi)))
# Mellin_NIG_European_Gamma.m:26
    GAMMA=dot(cons,sum)
# Mellin_NIG_European_Gamma.m:27
    return GAMMA
    
if __name__ == '__main__':
    pass
    