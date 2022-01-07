# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# ExplicitFD_BlackScholes_func.m

    
@function
def ExplicitFD_BlackScholes_func(S_0=None,K=None,r=None,T=None,sigma=None,call=None,dS=None,dt=None,Smax=None,Smin=None,*args,**kwargs):
    varargin = ExplicitFD_BlackScholes_func.varargin
    nargin = ExplicitFD_BlackScholes_func.nargin

    # Description: Explicit PDE Finite Difference method to price European Option in Black Scholes Model
# Author: Justin Kirkby
# NOTE: to ensure stability, we can choose dS, and then dt = dS^2 / Smax^2 / sigma^2;
    M=round((Smax - Smin) / dS)
# ExplicitFD_BlackScholes_func.m:5
    
    N=round(T / dt)
# ExplicitFD_BlackScholes_func.m:6
    
    # dS = Smax / M; # readjust
    dt=T / N
# ExplicitFD_BlackScholes_func.m:9
    
    vals=zeros(M + 1,N + 1)
# ExplicitFD_BlackScholes_func.m:11
    vS=linspace(Smin,Smax,M + 1).T
# ExplicitFD_BlackScholes_func.m:12
    vI=arange(0,M)
# ExplicitFD_BlackScholes_func.m:13
    vJ=arange(0,N)
# ExplicitFD_BlackScholes_func.m:14
    # Boundary Conditions
    if call == 1:
        vals[arange(),N + 1]=max(vS - K,0)
# ExplicitFD_BlackScholes_func.m:18
        vals[1,arange()]=0
# ExplicitFD_BlackScholes_func.m:19
        vals[M + 1,arange()]=Smax - dot(K,exp(dot(dot(- r,dt),(N - vJ))))
# ExplicitFD_BlackScholes_func.m:20
    else:
        vals[arange(),N + 1]=max(K - vS,0)
# ExplicitFD_BlackScholes_func.m:22
        vals[1,arange()]=dot(K,exp(dot(dot(- r,dt),(N - vJ))))
# ExplicitFD_BlackScholes_func.m:23
        vals[M + 1,arange()]=0
# ExplicitFD_BlackScholes_func.m:24
    
    # Tridiagonal Coefficients
    a=multiply(dot(dot(0.5,dt),(dot(sigma ** 2,vI) - r)),vI)
# ExplicitFD_BlackScholes_func.m:28
    b=1 - dot(dt,(dot(sigma ** 2,vI ** 2) + r))
# ExplicitFD_BlackScholes_func.m:29
    c=multiply(dot(dot(0.5,dt),(dot(sigma ** 2,vI) + r)),vI)
# ExplicitFD_BlackScholes_func.m:30
    # Solve (backward)
    for j in arange(N,1,- 1).reshape(-1):
        for i in arange(2,M).reshape(-1):
            vals[i,j]=dot(a(i),vals(i - 1,j + 1)) + dot(b(i),vals(i,j + 1)) + dot(c(i),vals(i + 1,j + 1))
# ExplicitFD_BlackScholes_func.m:35
    
    price=interp1(vS,vals(arange(),1),S_0)
# ExplicitFD_BlackScholes_func.m:39
    return price
    
if __name__ == '__main__':
    pass
    