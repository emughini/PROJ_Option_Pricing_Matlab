# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Mellin_NIG_European_Delta.m

    
@function
def Mellin_NIG_European_Delta(S_0=None,W=None,T=None,r=None,q=None,call=None,alpha=None,beta=None,delta=None,N1=None,*args,**kwargs):
    varargin = Mellin_NIG_European_Delta.varargin
    nargin = Mellin_NIG_European_Delta.nargin

    #UNTITLED2 Summary of this function goes here
#   Detailed explanation goes here
    
    N2=copy(N1)
# Mellin_NIG_European_Delta.m:5
    N3=copy(N1)
# Mellin_NIG_European_Delta.m:6
    f=dot(W,exp(dot(- r,T)))
# Mellin_NIG_European_Delta.m:8
    gam=sqrt(alpha ** 2 - beta ** 2)
# Mellin_NIG_European_Delta.m:10
    k0=log(S_0 / W) + dot((r - q + dot(delta,(sqrt(alpha ** 2 - (beta + 1) ** 2) - gam))),T)
# Mellin_NIG_European_Delta.m:11
    adt=dot(dot(alpha,delta),T)
# Mellin_NIG_European_Delta.m:12
    dta=dot(dot(0.5,delta),T) / alpha
# Mellin_NIG_European_Delta.m:13
    sum=0
# Mellin_NIG_European_Delta.m:15
    if beta == 0:
        # Symmetric Formula
        for n1 in arange(0,N1).reshape(-1):
            cons1=k0 ** n1 / factorial(n1)
# Mellin_NIG_European_Delta.m:20
            for n2 in arange(1,N2).reshape(-1):
                term=dot(besselk((n1 - n2) / 2 + 1,adt) / gamma((- n1 + n2 + 1) / 2),(dta) ** ((- n1 + n2) / 2))
# Mellin_NIG_European_Delta.m:22
                sum=sum + dot(cons1,term)
# Mellin_NIG_European_Delta.m:23
    else:
        # Asymmetric Formula
        pass
    
    cons=dot(dot(f,alpha),exp(dot(dot(alpha,delta),T))) / (dot(S_0,sqrt(pi)))
# Mellin_NIG_European_Delta.m:31
    DELTA=dot(cons,sum)
# Mellin_NIG_European_Delta.m:32
    if call != 1:
        DELTA=DELTA - exp(dot(- q,T))
# Mellin_NIG_European_Delta.m:36
    
    return DELTA
    
if __name__ == '__main__':
    pass
    