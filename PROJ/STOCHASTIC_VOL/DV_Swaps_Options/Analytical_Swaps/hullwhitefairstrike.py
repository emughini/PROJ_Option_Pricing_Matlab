# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# hullwhitefairstrike.m

    
@function
def hullwhitefairstrike(r=None,V0=None,sigma=None,mu=None,T=None,rho=None,n=None,*args,**kwargs):
    varargin = hullwhitefairstrike.varargin
    nargin = hullwhitefairstrike.nargin

    # From C. Bernard and Z. Cui, Prices and Asymptotics for Discrete Variance
# Swaps, Applied Mathematical Finance 2014, 21(2), 140-173
    
    ############### for Hull-White - Proposition 4.1 #####
    
    KcHW=continuousHW(mu,T,V0)
# hullwhitefairstrike.m:7
    KdHW=discreteHW(mu,T,rho,sigma,V0,r,n)
# hullwhitefairstrike.m:8
    
@function
def continuousHW(mu=None,T=None,V0=None,*args,**kwargs):
    varargin = continuousHW.varargin
    nargin = continuousHW.nargin

    res=dot(V0,(exp(dot(T,mu)) - 1)) / T / mu
# hullwhitefairstrike.m:11
    return res
    
if __name__ == '__main__':
    pass
    
    
@function
def discreteHW(mu=None,T=None,rho=None,sigma=None,V0=None,r=None,n=None,*args,**kwargs):
    varargin = discreteHW.varargin
    nargin = discreteHW.nargin

    Kc=continuousHW(mu,T,V0)
# hullwhitefairstrike.m:15
    res=((dot(r ** 2,T)) / n + dot((1 - dot(r,T) / n),Kc) - dot(dot(V0 ** 2,(exp(dot((dot(2,mu) + sigma ** 2),T)) - 1)),(exp(dot(mu,T) / n) - 1)) / (dot(dot(dot(dot(2,T),mu),(mu + sigma ** 2)),(exp(dot((dot(2,mu) + sigma ** 2),T) / n) - 1))) + dot(V0 ** 2,(exp(dot((dot(2,mu) + sigma ** 2),T)) - 1)) / (dot(dot(dot(2,T),(dot(2,mu) + sigma ** 2)),(mu + sigma ** 2))) + dot(dot(dot(dot(dot(8,rho),(exp(dot(dot(3,(dot(4,mu) + sigma ** 2)),T) / 8) - 1)),V0 ** (3 / 2)),sigma),(exp(dot(mu,T) / n) - 1)) / (dot(dot(dot(mu,T),(dot(4,mu) + dot(3,sigma ** 2))),(exp(dot(dot(3,(dot(4,mu) + sigma ** 2)),T) / (dot(8,n))) - 1))) - dot(dot(dot(dot(64,rho),(exp(dot(dot(3,(dot(4,mu) + sigma ** 2)),T) / 8) - 1)),V0 ** (3 / 2)),sigma) / (dot(dot(dot(3,T),(dot(4,mu) + sigma ** 2)),(dot(4,mu) + dot(3,sigma ** 2)))))
# hullwhitefairstrike.m:16
    return res
    
if __name__ == '__main__':
    pass
    
    return res
    
if __name__ == '__main__':
    pass
    