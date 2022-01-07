# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Price_MC_Var_Swaps_func.m

    
@function
def Price_MC_Var_Swaps_func(Spath=None,disc=None,M=None,mult=None,*args,**kwargs):
    varargin = Price_MC_Var_Swaps_func.varargin
    nargin = Price_MC_Var_Swaps_func.nargin

    #######################################################
# About: Calculates Variance Swap prices (fair strike) for vector of strikes, given the simulated paths 
#           Uses Prices of Underlying for Control Variate
# Returns: prices and standard errors for each of the supplied strikes
# Author: Justin Lars Kirkby
    
    # -----------------
# Params
# -----------------
# Spath = paths of underlying, dimension N_sim x M+1, where M = number of time steps (since includes S_0)
# M = number of monitoring points, e.g. 252 for "daily" monitoring
# mult = time partitioning multiplier to reduce bias (e.g. mult = 2 or 5)
# disc = discount factor, e.g. exp(-r*T), where T = Time (in years)
#######################################################
    
    N_sim=size(Spath,1)
# Price_MC_Var_Swaps_func.m:18
    
    M_mult=dot(M,mult)
# Price_MC_Var_Swaps_func.m:19
    
    S_0=Spath(1,1)
# Price_MC_Var_Swaps_func.m:20
    RV=zeros(N_sim,1)
# Price_MC_Var_Swaps_func.m:22
    
    for n in arange(1,N_sim).reshape(-1):
        RV[n]=sum(log(Spath(n,arange(1 + mult,M_mult + 1,mult)) / Spath(n,arange(1,M_mult,mult))) ** 2)
# Price_MC_Var_Swaps_func.m:24
    
    # Use S_T as Control Variate (CV) since E[S_T] = S_0/disc ... not great but provides a small reduction in std err
    
    meanRV=mean(RV)
# Price_MC_Var_Swaps_func.m:29
    price_NoCV=dot(disc,meanRV)
# Price_MC_Var_Swaps_func.m:30
    CV=Spath(arange(),M_mult + 1)
# Price_MC_Var_Swaps_func.m:32
    Ref=S_0 / disc
# Price_MC_Var_Swaps_func.m:34
    meanCV=mean(CV)
# Price_MC_Var_Swaps_func.m:35
    covXY=dot(1 / (N_sim - 1),sum(multiply((CV - meanCV),(RV - meanRV))))
# Price_MC_Var_Swaps_func.m:36
    cstar=- covXY / var(CV)
# Price_MC_Var_Swaps_func.m:37
    price=price_NoCV + dot(cstar,(meanCV - Ref))
# Price_MC_Var_Swaps_func.m:39
    stdErr=std(dot(disc,RV) + dot(cstar,(CV - Ref))) / sqrt(N_sim)
# Price_MC_Var_Swaps_func.m:41
    return price,stdErr
    
if __name__ == '__main__':
    pass
    