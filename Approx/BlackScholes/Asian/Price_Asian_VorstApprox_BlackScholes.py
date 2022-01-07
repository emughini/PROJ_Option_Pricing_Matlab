# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Price_Asian_VorstApprox_BlackScholes.m

    
@function
def Price_Asian_VorstApprox_BlackScholes(S_0=None,sigma=None,M=None,W=None,call=None,T=None,r=None,q=None,enforce_convention=None,*args,**kwargs):
    varargin = Price_Asian_VorstApprox_BlackScholes.varargin
    nargin = Price_Asian_VorstApprox_BlackScholes.nargin

    #########################################################
# About: Pricing Function for Arithmetic Asian Options using Vorst Approximation Method
# Models Supported: Black-Scholes
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# S_0   = initial stock price (e.g. 100)
# sigma = volatility of diffusion (e.g. 0.2)
# W     = strike  (e.g. 100)
# r     = interest rate (e.g. 0.05)
# q     = dividend yield (e.g. 0.05)
# T     = time remaining until maturity (in years, e.g. T=1)
# M     = number of subintervals of [0,T] (total of M+1 monitoring points in time grid, including S_0)
# call  = 1 for call (else put)
# enforce_convention  =  true by default, enforces convention that S_0 is included in the average, else averaging starts at S_1
    
    #########################################################
# NOTE: we do an adjustment so that the formula is in terms of Avg(S_0,S_1,...,S_M) instead of Avg(S_1,...,S_M)
    
    dt=T / M
# Price_Asian_VorstApprox_BlackScholes.m:24
    if nargin < 9:
        enforce_convention=1
# Price_Asian_VorstApprox_BlackScholes.m:27
    
    if enforce_convention:
        W=dot((M + 1) / M,W) - S_0 / M
# Price_Asian_VorstApprox_BlackScholes.m:31
    
    mu_G=log(S_0) + dot((r - q - dot(0.5,sigma ** 2)),(T + dt)) / 2
# Price_Asian_VorstApprox_BlackScholes.m:34
    sigma_G=sqrt(dot(sigma ** 2,(dt + dot((T - dt),(dot(2,M) - 1)) / (dot(6,M)))))
# Price_Asian_VorstApprox_BlackScholes.m:35
    if r - q == 0:
        mult=copy(M)
# Price_Asian_VorstApprox_BlackScholes.m:38
    else:
        mult=dot(exp(dot((r - q),dt)),(1 - exp(dot(dot((r - q),M),dt)))) / (1 - exp(dot((r - q),dt)))
# Price_Asian_VorstApprox_BlackScholes.m:40
    
    E_A=dot((S_0 / M),mult)
# Price_Asian_VorstApprox_BlackScholes.m:43
    E_G=exp(mu_G + dot(0.5,sigma_G ** 2))
# Price_Asian_VorstApprox_BlackScholes.m:44
    K=W - (E_A - E_G)
# Price_Asian_VorstApprox_BlackScholes.m:45
    
    d1=(mu_G - log(K) + sigma_G ** 2) / sigma_G
# Price_Asian_VorstApprox_BlackScholes.m:47
    d2=d1 - sigma_G
# Price_Asian_VorstApprox_BlackScholes.m:48
    price=dot(exp(dot(- r,T)),(dot(exp(mu_G + dot(0.5,sigma_G ** 2)),normcdf(d1)) - dot(K,normcdf(d2))))
# Price_Asian_VorstApprox_BlackScholes.m:50
    # Final adjustment so due to different averagin convention,  Avg(S_0,S_1,...,S_M) instead of Avg(S_1,...,S_M)
    if enforce_convention:
        price=dot(price,(M / (M + 1)))
# Price_Asian_VorstApprox_BlackScholes.m:54
    
    if call != 1:
        if enforce_convention:
            if r - q == 0:
                mult=M + 1
# Price_Asian_VorstApprox_BlackScholes.m:60
            else:
                mult=(exp(dot(dot((r - q),T),(1 + 1 / M))) - 1) / (exp(dot((r - q),dt)) - 1)
# Price_Asian_VorstApprox_BlackScholes.m:62
            price=price - dot(dot(S_0 / (M + 1),exp(dot(- r,T))),mult) + dot(W,exp(dot(- r,T)))
# Price_Asian_VorstApprox_BlackScholes.m:64
        else:
            price=price - dot(dot(S_0 / (M),exp(dot(- r,T))),mult) + dot(W,exp(dot(- r,T)))
# Price_Asian_VorstApprox_BlackScholes.m:66
    
    return price
    
if __name__ == '__main__':
    pass
    