# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# hestonfairstrike.m

    
@function
def hestonfairstrike(r=None,V0=None,theta=None,kappa=None,gamma=None,T=None,rho=None,n=None,*args,**kwargs):
    varargin = hestonfairstrike.varargin
    nargin = hestonfairstrike.nargin

    # From C. Bernard and Z. Cui, Prices and Asymptotics for Discrete Variance
# Swaps, Applied Mathematical Finance 2014, 21(2), 140-173
    
    ###### for Heston - Proposition 3.1 ######
    KcH=continuousstrikeHeston(theta,T,kappa,V0)
# hestonfairstrike.m:6
    KdH=discreteHeston(n,rho,r,kappa,theta,gamma,T,V0)
# hestonfairstrike.m:7
    ################################# Proposition 3.1 #########
    
@function
def continuousstrikeHeston(theta=None,T=None,kappa=None,V0=None,*args,**kwargs):
    varargin = continuousstrikeHeston.varargin
    nargin = continuousstrikeHeston.nargin

    # Expected integral of Vs between 0 and T
    # need to be divided by T
    K=(dot(theta,T) + dot((1 - exp(dot(- kappa,T))),(V0 - theta)) / kappa) / T
# hestonfairstrike.m:13
    return K
    
if __name__ == '__main__':
    pass
    
    
@function
def discreteHeston(n=None,rho=None,r=None,kappa=None,theta=None,gamma=None,T=None,V0=None,*args,**kwargs):
    varargin = discreteHeston.varargin
    nargin = discreteHeston.nargin

    # sum of E[ln(S_{ti+1}/S_{ti})^2] for i=0 to n, such that ti=i*T/n Vs
    Kd=dot((1 / (dot(8,T))),((dot(dot(dot(dot(2,n),V0 ** 2),kappa),exp(dot(dot(2,T),kappa) / n)) + dot(dot(dot(dot(dot(8,rho),kappa),gamma),V0),n) - dot(dot(dot(dot(4,theta ** 2),T),kappa ** 2),exp(dot(dot(2,T),kappa) / n)) + dot(dot(dot(dot(dot(dot(2,gamma ** 2),theta),exp(dot(dot(2,T),kappa) / n)),T),kappa),n) - dot(dot(dot(dot(3,theta),gamma ** 2),n),exp(dot(dot(2,T),kappa) / n)) - dot(dot(dot(dot(8,kappa ** 2),theta),n),exp(dot(dot(2,T),kappa) / n)) - dot(dot(dot(dot(dot(dot(8,rho),kappa),gamma),exp(dot(- T,kappa))),n),V0) - dot(dot(dot(dot(8,kappa ** 2),exp(dot(dot(- T,kappa),(n - 2)) / n)),V0),n) + dot(dot(dot(dot(4,exp(dot(dot(- T,kappa),(n - 2)) / n)),theta ** 2),T),kappa ** 2) + dot(dot(dot(dot(2,gamma ** 2),exp(dot(dot(- 2,T),kappa))),n),V0) - dot(dot(dot(dot(4,theta),V0),T),kappa ** 2) + dot(dot(dot(dot(8,kappa ** 2),exp(dot(- T,kappa))),n),V0) + dot(dot(dot(dot(8,kappa ** 2),V0),n),exp(dot(dot(2,T),kappa) / n)) + dot(dot(dot(dot(4,exp(dot(dot(- T,kappa),(dot(2,n) - 1)) / n)),n),V0 ** 2),kappa) + dot(dot(dot(dot(dot(dot(8,rho),kappa ** 2),gamma),exp(dot(dot(- T,kappa),(n - 1)) / n)),theta),T) + dot(dot(dot(8,kappa ** 2),n),theta) - dot(dot(dot(dot(dot(8,rho),kappa),gamma),theta),n ** 2) + dot(dot(dot(dot(2,gamma ** 2),exp(dot(dot(- T,kappa),(dot(2,n) - 1)) / n)),n),theta) - dot(dot(dot(8,kappa ** 2),n),V0) - dot(dot(dot(dot(4,theta),V0),n),kappa) - dot(dot(dot(2,kappa ** 3),theta ** 2),T ** 2) - dot(dot(dot(gamma ** 2,exp(dot(dot(dot(- 2,T),kappa),(n - 1)) / n)),n),theta) - dot(dot(dot(dot(4,exp(dot(- T,kappa))),theta ** 2),T),kappa ** 2) - dot(dot(dot(dot(4,V0),gamma ** 2),T),kappa) + dot(dot(dot(dot(dot(8,kappa ** 2),T),r),V0),exp(dot(dot(- T,kappa),(n - 2)) / n)) + dot(dot(dot(dot(dot(dot(8,rho),kappa),gamma),theta),n),exp(dot(dot(2,T),kappa) / n)) - dot(dot(dot(dot(2,exp(dot(dot(2,T),kappa) / n)),n ** 2),theta),gamma ** 2) + dot(dot(dot(dot(dot(dot(8,rho),kappa ** 2),gamma),exp(dot(- T,kappa))),theta),T) + dot(dot(dot(dot(dot(8,kappa ** 2),T),r),theta),exp(dot(- T,kappa))) + dot(dot(dot(dot(dot(4,exp(dot(- T,kappa))),theta),V0),T),kappa ** 2) + dot(dot(dot(dot(dot(4,gamma ** 2),exp(dot(- T,kappa))),V0),T),kappa) - dot(dot(dot(dot(4,exp(dot(T,kappa) / n)),theta ** 2),n),kappa) - dot(dot(dot(dot(4,exp(dot(T,kappa) / n)),n),V0 ** 2),kappa) - dot(dot(dot(dot(dot(4,exp(dot(dot(- T,kappa),(n - 2)) / n)),theta),V0),T),kappa ** 2) + dot(dot(dot(dot(dot(dot(8,rho),kappa),gamma),exp(dot(dot(- T,kappa),(n - 2)) / n)),V0),n) - dot(dot(dot(dot(8,kappa ** 2),exp(dot(- T,kappa))),n),theta) + dot(dot(dot(dot(dot(dot(8,rho),kappa ** 2),gamma),theta),T),n) - dot(dot(dot(dot(dot(8,kappa ** 2),T),r),V0),exp(dot(dot(2,T),kappa) / n)) - dot(dot(dot(dot(dot(dot(8,rho),kappa ** 2),gamma),exp(dot(dot(- T,kappa),(n - 1)) / n)),V0),T) + dot(dot(dot(dot(dot(4,theta),gamma ** 2),T),exp(dot(T,kappa) / n)),kappa) - dot(dot(dot(dot(dot(4,V0),gamma ** 2),T),exp(dot(T,kappa) / n)),kappa) - dot(dot(dot(dot(4,gamma ** 2),exp(dot(- T,kappa))),n),theta) - dot(dot(dot(dot(dot(4,gamma ** 2),exp(dot(- T,kappa))),theta),T),kappa) - dot(dot(dot(dot(dot(4,n),theta),V0),kappa),exp(dot(dot(2,T),kappa) / n)) + dot(dot(dot(dot(dot(4,theta),V0),T),kappa ** 2),exp(dot(dot(2,T),kappa) / n)) + dot(dot(dot(dot(dot(8,kappa ** 3),n),theta),T),exp(dot(dot(2,T),kappa) / n)) + dot(dot(dot(2,n ** 2),theta),gamma ** 2) - dot(dot(dot(dot(dot(dot(8,rho),kappa),gamma),V0),n),exp(dot(dot(2,T),kappa) / n)) + dot(dot(dot(dot(8,kappa ** 3),T ** 2),r),theta) - dot(dot(dot(dot(8,kappa ** 2),T),r),theta) - dot(dot(dot(dot(dot(dot(8,rho),kappa),gamma),theta),exp(dot(T,kappa) / n)),n ** 2) + dot(dot(dot(dot(8,kappa ** 2),T),r),V0) - dot(dot(dot(dot(dot(dot(dot(8,rho),kappa ** 2),gamma),theta),exp(dot(dot(2,T),kappa) / n)),T),n) + dot(dot(dot(dot(4,exp(dot(dot(- T,kappa),(dot(2,n) - 1)) / n)),n),theta ** 2),kappa) + dot(dot(dot(dot(8,kappa ** 2),exp(dot(dot(- T,kappa),(n - 2)) / n)),theta),n) - dot(dot(dot(dot(2,exp(dot(dot(- 2,T),kappa))),n),V0 ** 2),kappa) - dot(dot(dot(dot(2,exp(dot(dot(dot(- 2,T),kappa),(n - 1)) / n)),n),V0 ** 2),kappa) - dot(dot(dot(dot(2,exp(dot(dot(dot(- 2,T),kappa),(n - 1)) / n)),n),kappa),theta ** 2) + dot(dot(dot(dot(4,V0),gamma ** 2),n),exp(dot(T,kappa) / n)) - dot(dot(dot(dot(2,theta),gamma ** 2),n),exp(dot(T,kappa) / n)) - dot(dot(dot(dot(2,exp(dot(dot(- 2,T),kappa))),n),kappa),theta ** 2) - dot(dot(dot(dot(2,gamma ** 2),theta),exp(dot(- T,kappa) / n)),n ** 2) + dot(dot(dot(dot(2,n),kappa),theta ** 2),exp(dot(dot(2,T),kappa) / n)) + dot(dot(dot(dot(2,V0),gamma ** 2),n),exp(dot(dot(2,T),kappa) / n)) + dot(dot(dot(dot(4,gamma ** 2),exp(dot(dot(- T,kappa),(n - 2)) / n)),theta),n) - dot(dot(dot(dot(dot(dot(8,rho),kappa),gamma),exp(dot(dot(- T,kappa),(n - 2)) / n)),theta),n) - dot(dot(dot(dot(dot(8,rho),kappa),gamma),n),theta) - dot(dot(dot(dot(4,gamma ** 2),exp(dot(dot(- T,kappa),(dot(2,n) - 1)) / n)),n),V0) + dot(dot(dot(dot(dot(4,gamma ** 2),exp(dot(dot(- T,kappa),(n - 1)) / n)),V0),T),kappa) + dot(dot(dot(dot(2,gamma ** 2),exp(dot(dot(dot(- 2,T),kappa),(n - 1)) / n)),n),V0) - dot(dot(dot(gamma ** 2,exp(dot(dot(- 2,T),kappa))),n),theta) + dot(dot(dot(dot(dot(dot(8,rho),kappa ** 2),gamma),V0),T),exp(dot(T,kappa) / n)) - dot(dot(dot(dot(dot(dot(8,rho),kappa ** 2),gamma),exp(dot(- T,kappa))),V0),T) - dot(dot(dot(dot(dot(8,kappa ** 2),T),r),V0),exp(dot(- T,kappa))) - dot(dot(dot(dot(dot(dot(8,rho),kappa ** 2),gamma),theta),T),exp(dot(T,kappa) / n)) - dot(dot(dot(dot(dot(8,rho),kappa ** 2),gamma),theta),T) + dot(dot(dot(dot(dot(8,rho),kappa ** 2),gamma),V0),T) + dot(dot(dot(4,theta ** 2),T),kappa ** 2) + dot(dot(dot(dot(4,gamma ** 2),exp(dot(- T,kappa))),n),V0) - dot(dot(dot(8,T ** 2),kappa ** 3),r ** 2) - dot(dot(dot(dot(dot(8,kappa ** 3),T ** 2),r),theta),exp(dot(dot(2,T),kappa) / n)) + dot(dot(dot(dot(2,n ** 2),theta),gamma ** 2),exp(dot(T,kappa) / n)) + dot(dot(dot(dot(2,theta ** 2),exp(dot(dot(2,T),kappa) / n)),T ** 2),kappa ** 3) - dot(dot(dot(dot(8,kappa ** 3),n),theta),T) + dot(dot(dot(dot(dot(8,exp(dot(T,kappa) / n)),theta),V0),n),kappa) + dot(dot(dot(2,theta ** 2),n),kappa) - dot(dot(dot(dot(dot(4,gamma ** 2),exp(dot(dot(- T,kappa),(n - 1)) / n)),theta),T),kappa) + dot(dot(dot(dot(dot(8,kappa ** 2),T),r),theta),exp(dot(dot(2,T),kappa) / n)) + dot(dot(dot(dot(dot(dot(8,rho),kappa),gamma),theta),exp(dot(- T,kappa) / n)),n ** 2) - dot(dot(dot(dot(dot(2,n),theta),gamma ** 2),kappa),T) + dot(dot(dot(dot(8,T ** 2),kappa ** 3),r ** 2),exp(dot(dot(2,T),kappa) / n)) + dot(dot(dot(2,n),V0 ** 2),kappa) + dot(dot(dot(5,n),theta),gamma ** 2) - dot(dot(dot(6,n),V0),gamma ** 2) + dot(dot(dot(dot(dot(4,exp(dot(dot(dot(- 2,T),kappa),(n - 1)) / n)),n),theta),V0),kappa) + dot(dot(dot(dot(dot(dot(8,rho),kappa),gamma),exp(dot(- T,kappa))),n),theta) - dot(dot(dot(dot(dot(8,exp(dot(dot(- T,kappa),(dot(2,n) - 1)) / n)),n),theta),V0),kappa) + dot(dot(dot(dot(dot(4,exp(dot(dot(- 2,T),kappa))),n),theta),V0),kappa) - dot(dot(dot(dot(dot(8,kappa ** 2),T),r),theta),exp(dot(dot(- T,kappa),(n - 2)) / n)) + dot(dot(dot(dot(4,theta),gamma ** 2),T),kappa) - dot(dot(dot(dot(4,gamma ** 2),exp(dot(dot(- T,kappa),(n - 2)) / n)),V0),n) + dot(dot(dot(dot(dot(dot(8,rho),kappa),gamma),theta),exp(dot(dot(2,T),kappa) / n)),n ** 2)) / (dot(dot(kappa ** 3,n),(exp(dot(dot(2,T),kappa) / n) - 1)))))
# hestonfairstrike.m:18
    return Kd
    
if __name__ == '__main__':
    pass
    
    return Kd
    
if __name__ == '__main__':
    pass
    