# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# BinomialLattice_BlackScholes_func.m

    
@function
def BinomialLattice_BlackScholes_func(S_0=None,K=None,r=None,T=None,sigma=None,M=None,call=None,american=None,*args,**kwargs):
    varargin = BinomialLattice_BlackScholes_func.varargin
    nargin = BinomialLattice_BlackScholes_func.nargin

    # European and American/Bermudan Option pricer 
# Model: Black Scholes Merton
# Author: Justin Kirkby
    
    dt=T / M
# BinomialLattice_BlackScholes_func.m:6
    u=exp(dot(sigma,sqrt(dt)))
# BinomialLattice_BlackScholes_func.m:7
    d=1 / u
# BinomialLattice_BlackScholes_func.m:8
    p=(exp(dot(r,dt)) - d) / (u - d)
# BinomialLattice_BlackScholes_func.m:9
    discount=exp(dot(- r,dt))
# BinomialLattice_BlackScholes_func.m:10
    p_u=dot(discount,p)
# BinomialLattice_BlackScholes_func.m:11
    p_d=dot(discount,(1 - p))
# BinomialLattice_BlackScholes_func.m:12
    # Determine Payoff Function
    if call == 1:
        payoff=lambda C=None,S=None: max(C,S - K)
# BinomialLattice_BlackScholes_func.m:16
    else:
        payoff=lambda C=None,S=None: max(C,K - S)
# BinomialLattice_BlackScholes_func.m:18
    
    Svals=zeros(dot(2,M) + 1,1)
# BinomialLattice_BlackScholes_func.m:21
    Svals[M + 1]=S_0
# BinomialLattice_BlackScholes_func.m:22
    for i in arange(1,M).reshape(-1):
        Svals[M + 1 + i]=dot(u,Svals(M + i))
# BinomialLattice_BlackScholes_func.m:24
        Svals[M + 1 - i]=dot(d,Svals(M + 2 - i))
# BinomialLattice_BlackScholes_func.m:25
    
    # Initialize Terminal Payoff
    Pvals=zeros(dot(2,M) + 1,1)
# BinomialLattice_BlackScholes_func.m:29
    for i in arange(1,dot(2,M) + 1,2).reshape(-1):
        Pvals[i]=payoff(0,Svals(i))
# BinomialLattice_BlackScholes_func.m:31
    
    # Calculate Price Recursively
    if american == 1:
        for tau in arange(1,M).reshape(-1):
            for i in arange((tau + 1),(dot(2,M) + 1 - tau),2).reshape(-1):
                cont=dot(p_u,Pvals(i + 1)) + dot(p_d,Pvals(i - 1))
# BinomialLattice_BlackScholes_func.m:38
                Pvals[i]=payoff(cont,Svals(i))
# BinomialLattice_BlackScholes_func.m:39
    else:
        for tau in arange(1,M).reshape(-1):
            for i in arange((tau + 1),(dot(2,M) + 1 - tau),2).reshape(-1):
                Pvals[i]=dot(p_u,Pvals(i + 1)) + dot(p_d,Pvals(i - 1))
# BinomialLattice_BlackScholes_func.m:45
    
    
    price=Pvals(M + 1)
# BinomialLattice_BlackScholes_func.m:50
    return price
    
if __name__ == '__main__':
    pass
    