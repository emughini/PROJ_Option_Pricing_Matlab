# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PoissonRnd.m

    
@function
def PoissonRnd(n=None,theta=None,*args,**kwargs):
    varargin = PoissonRnd.varargin
    nargin = PoissonRnd.nargin

    # Returns a column vector of size n of Poisson Random Variables
# For a Poisson process, use theta = lambda*dt, where lambda is arrival rate
# Density: exp(-theta)*(theta)^k/(k!)
    
    #Uses method on page 128, Figure 3.9 of glasserman
    Unif=rand(n,1)
# PoissonRnd.m:7
    Poi=zeros(n,1)
# PoissonRnd.m:8
    for j in arange(1,n).reshape(-1):
        p=exp(- theta)
# PoissonRnd.m:11
        F=copy(p)
# PoissonRnd.m:12
        N=0
# PoissonRnd.m:13
        U=Unif(j)
# PoissonRnd.m:14
        while U > F:

            N=N + 1
# PoissonRnd.m:16
            p=dot(p,theta) / N
# PoissonRnd.m:17
            F=F + p
# PoissonRnd.m:18

        Poi[j]=N
# PoissonRnd.m:20
    
    return Poi
    
if __name__ == '__main__':
    pass
    