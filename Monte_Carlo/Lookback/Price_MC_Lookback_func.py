# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Price_MC_Lookback_func.m

    
@function
def Price_MC_Lookback_func(Spath=None,call=None,M=None,mult=None,disc=None,*args,**kwargs):
    varargin = Price_MC_Lookback_func.varargin
    nargin = Price_MC_Lookback_func.nargin

    #######################################################
# About: Calculates Looback option price, given the simulatd paths 
# Author: Justin Lars Kirkby
    
    # -----------------
# Params
# -----------------
# Contract Types
# Floating Strike (Lookback) Put:  max{S_m: 0<=m<=M} - S_T
# Floating Strike (Lookback) Call: S_T - min{S_m: 0<=m<=M}
    
    # Spath = paths of underlying, dimension N_sim x M+1, where M = number of time steps (since includes S_0)
# call = 1 for call (else put)
# M = number of monitoring points, e.g. 252 for "daily" monitoring
# mult = time partitioning multiplier to reduce bias (e.g. mult = 2 or 5)
# S_0 = initial price
# disc = discount factor (e.g. exp(-r*T))
# T = Time (in years)
#######################################################
    
    N_sim=size(Spath,1)
# Price_MC_Lookback_func.m:22
    
    M_mult=dot(M,mult)
# Price_MC_Lookback_func.m:24
    
    if call != 1:
        curr_max=zeros(N_sim,1)
# Price_MC_Lookback_func.m:28
        for n in arange(1,N_sim).reshape(-1):
            curr_max[n]=max(Spath(n,arange(1,M_mult + 1,mult)))
# Price_MC_Lookback_func.m:30
    else:
        curr_min=zeros(N_sim,1)
# Price_MC_Lookback_func.m:33
        for n in arange(1,N_sim).reshape(-1):
            curr_min[n]=min(Spath(n,arange(1,M_mult + 1,mult)))
# Price_MC_Lookback_func.m:35
    
    if call == 1:
        payoffs=Spath(arange(),M_mult + 1) - curr_min
# Price_MC_Lookback_func.m:41
    else:
        payoffs=curr_max - Spath(arange(),M_mult + 1)
# Price_MC_Lookback_func.m:44
    
    price=dot(disc,mean(payoffs))
# Price_MC_Lookback_func.m:46
    stdErr=dot(disc,std(payoffs)) / sqrt(N_sim)
# Price_MC_Lookback_func.m:47
    return price,stdErr
    
if __name__ == '__main__':
    pass
    