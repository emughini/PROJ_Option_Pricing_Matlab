# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# TrinomialLattice_BlackScholes_func.m

    
@function
def TrinomialLattice_BlackScholes_func(S_0=None,K=None,r=None,T=None,sigma=None,M=None,call=None,american=None,*args,**kwargs):
    varargin = TrinomialLattice_BlackScholes_func.varargin
    nargin = TrinomialLattice_BlackScholes_func.nargin

    # European and American/Bermudan Option pricer 
# Model: Black Scholes Merton
# Author: Justin Kirkby
    
    dt=T / M
# TrinomialLattice_BlackScholes_func.m:6
    dx=dot(sigma,sqrt(dt))
# TrinomialLattice_BlackScholes_func.m:7
    
    s2=r - dot(0.5,sigma ** 2)
# TrinomialLattice_BlackScholes_func.m:8
    discount=exp(dot(- r,dt))
# TrinomialLattice_BlackScholes_func.m:9
    cons1=(dot(sigma ** 2,dt) + (dot(s2,dt)) ** 2) / dx ** 2
# TrinomialLattice_BlackScholes_func.m:10
    cons2=dot(s2,dt) / dx
# TrinomialLattice_BlackScholes_func.m:11
    p_u=dot(dot(discount,0.5),(cons1 + cons2))
# TrinomialLattice_BlackScholes_func.m:13
    p_m=dot(discount,(1 - cons1))
# TrinomialLattice_BlackScholes_func.m:14
    p_d=dot(dot(discount,0.5),(cons1 - cons2))
# TrinomialLattice_BlackScholes_func.m:15
    # Determine Payoff Function
    if call == 1:
        payoff=lambda C=None,S=None: max(C,S - K)
# TrinomialLattice_BlackScholes_func.m:20
    else:
        payoff=lambda C=None,S=None: max(C,K - S)
# TrinomialLattice_BlackScholes_func.m:22
    
    edx=exp(dx)
# TrinomialLattice_BlackScholes_func.m:25
    # Initialize terminal S grid values
    Svals=zeros(dot(2,M) + 1,1)
# TrinomialLattice_BlackScholes_func.m:28
    Svals[1]=dot(S_0,exp(dot(- M,dx)))
# TrinomialLattice_BlackScholes_func.m:29
    for i in arange(2,dot(2,M) + 1).reshape(-1):
        Svals[i]=dot(edx,Svals(i - 1))
# TrinomialLattice_BlackScholes_func.m:31
    
    # Initialize Terminal Payoff
    Pvals=zeros(dot(2,M) + 1,2)
# TrinomialLattice_BlackScholes_func.m:35
    tau=mod(M,2) + 1
# TrinomialLattice_BlackScholes_func.m:36
    for i in arange(1,dot(2,M) + 1).reshape(-1):
        Pvals[i,tau]=payoff(0,Svals(i))
# TrinomialLattice_BlackScholes_func.m:38
    
    # Calculate Price Recursively
    if american == 1:
        for tau in arange(M - 1,0,- 1).reshape(-1):
            k=mod(tau,2) + 1
# TrinomialLattice_BlackScholes_func.m:44
            k1=mod(tau + 1,2) + 1
# TrinomialLattice_BlackScholes_func.m:45
            for i in arange((M - tau + 1),(M + tau + 1)).reshape(-1):
                cont=dot(p_d,Pvals(i - 1,k1)) + dot(p_m,Pvals(i,k1)) + dot(p_u,Pvals(i + 1,k1))
# TrinomialLattice_BlackScholes_func.m:47
                Pvals[i,k]=payoff(cont,Svals(i))
# TrinomialLattice_BlackScholes_func.m:48
    else:
        for tau in arange(M - 1,0,- 1).reshape(-1):
            k=mod(tau,2) + 1
# TrinomialLattice_BlackScholes_func.m:53
            k1=mod(tau + 1,2) + 1
# TrinomialLattice_BlackScholes_func.m:54
            for i in arange((M - tau + 1),(M + tau + 1)).reshape(-1):
                Pvals[i,k]=dot(p_d,Pvals(i - 1,k1)) + dot(p_m,Pvals(i,k1)) + dot(p_u,Pvals(i + 1,k1))
# TrinomialLattice_BlackScholes_func.m:56
    
    
    price=Pvals(M + 1,1)
# TrinomialLattice_BlackScholes_func.m:61
    return price
    
if __name__ == '__main__':
    pass
    