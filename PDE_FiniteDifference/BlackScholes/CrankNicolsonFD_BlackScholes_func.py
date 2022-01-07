# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# CrankNicolsonFD_BlackScholes_func.m

    
@function
def CrankNicolsonFD_BlackScholes_func(S_0=None,K=None,r=None,T=None,sigma=None,call=None,dS=None,dt=None,Smax=None,Smin=None,*args,**kwargs):
    varargin = CrankNicolsonFD_BlackScholes_func.varargin
    nargin = CrankNicolsonFD_BlackScholes_func.nargin

    # Description: Crank-Nicolson PDE Finite Difference method to price European Option in Black Scholes Model
# Author: Justin Kirkby
    M=round((Smax - Smin) / dS)
# CrankNicolsonFD_BlackScholes_func.m:4
    
    N=round(T / dt)
# CrankNicolsonFD_BlackScholes_func.m:5
    
    dS=(Smax - Smin) / M
# CrankNicolsonFD_BlackScholes_func.m:7
    
    dt=T / N
# CrankNicolsonFD_BlackScholes_func.m:8
    
    vals=zeros(M + 1,N + 1)
# CrankNicolsonFD_BlackScholes_func.m:10
    vS=linspace(Smin,Smax,M + 1).T
# CrankNicolsonFD_BlackScholes_func.m:11
    vI=vS / dS
# CrankNicolsonFD_BlackScholes_func.m:12
    vJ=arange(0,N)
# CrankNicolsonFD_BlackScholes_func.m:13
    # Boundary Conditions
    if call == 1:
        vals[arange(),N + 1]=max(vS - K,0)
# CrankNicolsonFD_BlackScholes_func.m:17
        vals[1,arange()]=0
# CrankNicolsonFD_BlackScholes_func.m:18
        vals[M + 1,arange()]=Smax - dot(K,exp(dot(dot(- r,dt),(N - vJ))))
# CrankNicolsonFD_BlackScholes_func.m:19
    else:
        vals[arange(),N + 1]=max(K - vS,0)
# CrankNicolsonFD_BlackScholes_func.m:21
        vals[1,arange()]=dot(K,exp(dot(dot(- r,dt),(N - vJ))))
# CrankNicolsonFD_BlackScholes_func.m:22
        vals[M + 1,arange()]=0
# CrankNicolsonFD_BlackScholes_func.m:23
    
    # Tridiagonal Coefficients
    a=dot(dot(0.25,dt),(dot(sigma ** 2,(vI ** 2)) - dot(r,vI)))
# CrankNicolsonFD_BlackScholes_func.m:27
    b=dot(dot(- dt,0.5),(dot(sigma ** 2,(vI ** 2)) + r))
# CrankNicolsonFD_BlackScholes_func.m:28
    c=dot(dot(0.25,dt),(dot(sigma ** 2,(vI ** 2)) + dot(r,vI)))
# CrankNicolsonFD_BlackScholes_func.m:29
    M1=- diag(a(arange(3,M)),- 1) + diag(1 - b(arange(2,M))) - diag(c(arange(2,M - 1)),1)
# CrankNicolsonFD_BlackScholes_func.m:31
    L,U=lu(M1,nargout=2)
# CrankNicolsonFD_BlackScholes_func.m:32
    M2=diag(a(arange(3,M)),- 1) + diag(1 + b(arange(2,M))) + diag(c(arange(2,M - 1)),1)
# CrankNicolsonFD_BlackScholes_func.m:33
    # Solve systems (backward in time)
    for j in arange(N,1,- 1).reshape(-1):
        vals[arange(2,M),j]=numpy.linalg.solve(U,(numpy.linalg.solve(L,(dot(M2,vals(arange(2,M),j + 1))))))
# CrankNicolsonFD_BlackScholes_func.m:37
    
    price=interp1(vS,vals(arange(),1),S_0)
# CrankNicolsonFD_BlackScholes_func.m:40
    return price
    
if __name__ == '__main__':
    pass
    