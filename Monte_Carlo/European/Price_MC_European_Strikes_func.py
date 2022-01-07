# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Price_MC_European_Strikes_func.m

    
@function
def Price_MC_European_Strikes_func(Spath=None,disc=None,call=None,Kvec=None,*args,**kwargs):
    varargin = Price_MC_European_Strikes_func.varargin
    nargin = Price_MC_European_Strikes_func.nargin

    #######################################################
# About: Calculates European option prices for vector of strikes, given the simulatd paths 
# Returns: prices and standard errors for each of the supplied strikes
# Author: Justin Lars Kirkby
    
    # -----------------
# Params
# -----------------
# Spath = paths of underlying, dimension N_sim x M+1, where M = number of time steps (since includes S_0)
# disc = discount factor, e.g. exp(-r*T)
# call = 1 for call (else put)
# Kvec = strike vector
#######################################################
    
    prices=zeros(length(Kvec),1)
# Price_MC_European_Strikes_func.m:16
    stdErrs=zeros(length(Kvec),1)
# Price_MC_European_Strikes_func.m:17
    N_sim=size(Spath,1)
# Price_MC_European_Strikes_func.m:18
    
    for k in arange(1,length(Kvec)).reshape(-1):
        K=Kvec(k)
# Price_MC_European_Strikes_func.m:21
        if call == 1:
            payoffs=max(0,Spath(arange(),end()) - K)
# Price_MC_European_Strikes_func.m:23
        else:
            payoffs=max(0,K - Spath(arange(),end()))
# Price_MC_European_Strikes_func.m:25
        prices[k]=dot(disc,mean(payoffs))
# Price_MC_European_Strikes_func.m:27
        stdErrs[k]=dot(disc,std(payoffs)) / sqrt(N_sim)
# Price_MC_European_Strikes_func.m:28
    
    return prices,stdErrs
    
if __name__ == '__main__':
    pass
    