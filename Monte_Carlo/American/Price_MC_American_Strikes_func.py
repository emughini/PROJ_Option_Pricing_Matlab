# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Price_MC_American_Strikes_func.m

    
@function
def Price_MC_American_Strikes_func(Spath=None,disc=None,call=None,Kvec=None,polyOrder=None,*args,**kwargs):
    varargin = Price_MC_American_Strikes_func.varargin
    nargin = Price_MC_American_Strikes_func.nargin

    #######################################################
# About: Longstaff-Schwartz Algo: Calculates American option prices for vector of strikes, given the simulatd paths 
# Returns: prices and standard errors for each of the supplied strikes
# Author: Justin Lars Kirkby
    
    # -----------------
# Params
# -----------------
# Spath = paths of underlying, dimension N_sim x M+1, where M = number of time steps (since includes S_0)
# disc = discount factor for each time step, e.g. exp(-r*dt), where dt is time step, and r is interest rate
# call = 1 for call (else put)
# Kvec = strike vector
# polyOrder = order of polynomial regression of continuation val, e.g. 3
#######################################################
    if nargin < 5:
        polyOrder=3
# Price_MC_American_Strikes_func.m:17
    
    prices=zeros(length(Kvec),1)
# Price_MC_American_Strikes_func.m:20
    stdErrs=zeros(length(Kvec),1)
# Price_MC_American_Strikes_func.m:21
    for k in arange(1,length(Kvec)).reshape(-1):
        K=Kvec(k)
# Price_MC_American_Strikes_func.m:24
        prices(k),stdErrs(k)=Price_MC_American_func(Spath,disc,call,K,polyOrder,nargout=2)
# Price_MC_American_Strikes_func.m:25
    
    return prices,stdErrs
    
if __name__ == '__main__':
    pass
    
    
@function
def Price_MC_American_func(Spath=None,disc=None,call=None,K=None,polyOrder=None,*args,**kwargs):
    varargin = Price_MC_American_func.varargin
    nargin = Price_MC_American_func.nargin

    M=size(Spath,2) - 1
# Price_MC_American_Strikes_func.m:31
    
    N_sim=size(Spath,1)
# Price_MC_American_Strikes_func.m:32
    
    
    if call == 1:
        payoff=max(Spath(arange(),M + 1) - K,0)
# Price_MC_American_Strikes_func.m:35
    else:
        payoff=max(K - Spath(arange(),M + 1),0)
# Price_MC_American_Strikes_func.m:37
    
    
    for m in arange(M,2,- 1).reshape(-1):
        payoff=dot(payoff,disc)
# Price_MC_American_Strikes_func.m:41
        if call == 1:
            EV=max(Spath(arange(),m) - K,0)
# Price_MC_American_Strikes_func.m:44
        else:
            EV=max(K - Spath(arange(),m),0)
# Price_MC_American_Strikes_func.m:46
        index=find(EV > 0)
# Price_MC_American_Strikes_func.m:49
        regression=polyfit(Spath(index,m),payoff(index),polyOrder)
# Price_MC_American_Strikes_func.m:51
        EHV=polyval(regression,Spath(index,m))
# Price_MC_American_Strikes_func.m:52
        si=size(index)
# Price_MC_American_Strikes_func.m:54
        for j in arange(1,si(1)).reshape(-1):
            index_j=index(j)
# Price_MC_American_Strikes_func.m:57
            if EHV(j) < EV(index_j):
                payoff[index_j]=EV(index_j)
# Price_MC_American_Strikes_func.m:59
    
    
    price=dot(mean(payoff),disc)
# Price_MC_American_Strikes_func.m:64
    stdErr=dot(disc,std(payoff)) / sqrt(N_sim)
# Price_MC_American_Strikes_func.m:65
    return price,stdErr
    
if __name__ == '__main__':
    pass
    