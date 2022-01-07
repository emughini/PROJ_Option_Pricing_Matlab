# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# ImplicitFD_BlackScholes_func.m

    
@function
def ImplicitFD_BlackScholes_func(S_0=None,K=None,r=None,T=None,sigma=None,call=None,dS=None,dt=None,Smax=None,Smin=None,*args,**kwargs):
    varargin = ImplicitFD_BlackScholes_func.varargin
    nargin = ImplicitFD_BlackScholes_func.nargin

    # Description: Fully Implicit PDE Finite Difference method to price European Option in Black Scholes Model
# Author: Justin Kirkby
    M=round((Smax - Smin) / dS)
# ImplicitFD_BlackScholes_func.m:4
    
    N=round(T / dt)
# ImplicitFD_BlackScholes_func.m:5
    
    # dS = (Smax - Smin) / M; # readjust
    dt=T / N
# ImplicitFD_BlackScholes_func.m:8
    
    vals=zeros(M + 1,N + 1)
# ImplicitFD_BlackScholes_func.m:10
    vS=linspace(Smin,Smax,M + 1).T
# ImplicitFD_BlackScholes_func.m:11
    vI=arange(0,M)
# ImplicitFD_BlackScholes_func.m:12
    vJ=arange(0,N)
# ImplicitFD_BlackScholes_func.m:13
    # Boundary Conditions
    if call == 1:
        vals[arange(),N + 1]=max(vS - K,0)
# ImplicitFD_BlackScholes_func.m:17
        vals[1,arange()]=0
# ImplicitFD_BlackScholes_func.m:18
        vals[M + 1,arange()]=Smax - dot(K,exp(dot(dot(- r,dt),(N - vJ))))
# ImplicitFD_BlackScholes_func.m:19
    else:
        vals[arange(),N + 1]=max(K - vS,0)
# ImplicitFD_BlackScholes_func.m:21
        vals[1,arange()]=dot(K,exp(dot(dot(- r,dt),(N - vJ))))
# ImplicitFD_BlackScholes_func.m:22
        vals[M + 1,arange()]=0
# ImplicitFD_BlackScholes_func.m:23
    
    # Tridiagonal Coefficients
    a=dot(0.5,(dot(dot(r,dt),vI) - dot(dot(sigma ** 2,dt),(vI ** 2))))
# ImplicitFD_BlackScholes_func.m:27
    b=1 + dot(dot(sigma ** 2,dt),(vI ** 2)) + dot(r,dt)
# ImplicitFD_BlackScholes_func.m:28
    c=dot(- 0.5,(dot(dot(r,dt),vI) + dot(dot(sigma ** 2,dt),(vI ** 2))))
# ImplicitFD_BlackScholes_func.m:29
    cvec=diag(a(arange(3,M)),- 1) + diag(b(arange(2,M))) + diag(c(arange(2,M - 1)),1)
# ImplicitFD_BlackScholes_func.m:31
    L,U=lu(cvec,nargout=2)
# ImplicitFD_BlackScholes_func.m:32
    # Solve systems (backward in time)
    z=zeros(M - 1,1)
# ImplicitFD_BlackScholes_func.m:35
    for j in arange(N,1,- 1).reshape(-1):
        z[1]=dot(- a(2),vals(1,j))
# ImplicitFD_BlackScholes_func.m:37
        vals[arange(2,M),j]=numpy.linalg.solve(U,(numpy.linalg.solve(L,(vals(arange(2,M),j + 1) + z))))
# ImplicitFD_BlackScholes_func.m:38
    
    price=interp1(vS,vals(arange(),1),S_0)
# ImplicitFD_BlackScholes_func.m:41
    return price
    
if __name__ == '__main__':
    pass
    