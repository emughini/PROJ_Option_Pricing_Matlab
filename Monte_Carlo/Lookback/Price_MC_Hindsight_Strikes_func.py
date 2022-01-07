# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Price_MC_Hindsight_Strikes_func.m

    
@function
def Price_MC_Hindsight_Strikes_func(Spath=None,call=None,strikes=None,M=None,mult=None,disc=None,*args,**kwargs):
    varargin = Price_MC_Hindsight_Strikes_func.varargin
    nargin = Price_MC_Hindsight_Strikes_func.nargin

    #######################################################
# About: Calculates Hindsight option prices for vector of strikes, given the simulatd paths 
# Author: Justin Lars Kirkby
    
    # -----------------
# Params
# -----------------
# Contract Types
# Fixed Strike (Hindsight) Put: (W - min{S_m: 0<=m<=M})^+
# Fixed Strike (Hindsight) Call: (max{S_m: 0<=m<=M} - W)^+
    
    # Spath = paths of underlying, dimension N_sim x M+1, where M = number of time steps (since includes S_0)
# call = 1 for call (else put)
# Kvec = strike vector
# M = number of monitoring points, e.g. 252 for "daily" monitoring
# mult = time partitioning multiplier to reduce bias (e.g. mult = 2 or 5)
# S_0 = initial price
# disc = discount factor (e.g. exp(-r*T))
# T = Time (in years)
#######################################################
    
    N_sim=size(Spath,1)
# Price_MC_Hindsight_Strikes_func.m:23
    
    M_mult=dot(M,mult)
# Price_MC_Hindsight_Strikes_func.m:25
    
    prices=zeros(length(strikes),1)
# Price_MC_Hindsight_Strikes_func.m:27
    stdErrs=zeros(length(strikes),1)
# Price_MC_Hindsight_Strikes_func.m:28
    
    if call == 1:
        curr_max=zeros(N_sim,1)
# Price_MC_Hindsight_Strikes_func.m:31
        for n in arange(1,N_sim).reshape(-1):
            curr_max[n]=max(Spath(n,arange(1,M_mult + 1,mult)))
# Price_MC_Hindsight_Strikes_func.m:33
    else:
        curr_min=zeros(N_sim,1)
# Price_MC_Hindsight_Strikes_func.m:36
        for n in arange(1,N_sim).reshape(-1):
            curr_min[n]=min(Spath(n,arange(1,M_mult + 1,mult)))
# Price_MC_Hindsight_Strikes_func.m:38
    
    for k in arange(1,length(strikes)).reshape(-1):
        K=strikes(k)
# Price_MC_Hindsight_Strikes_func.m:43
        if call == 1:
            payoffs=max(0,curr_max - K)
# Price_MC_Hindsight_Strikes_func.m:45
        else:
            payoffs=max(0,K - curr_min)
# Price_MC_Hindsight_Strikes_func.m:48
        prices[k]=dot(disc,mean(payoffs))
# Price_MC_Hindsight_Strikes_func.m:50
        stdErrs[k]=dot(disc,std(payoffs)) / sqrt(N_sim)
# Price_MC_Hindsight_Strikes_func.m:51
    
    return prices,stdErrs
    
if __name__ == '__main__':
    pass
    