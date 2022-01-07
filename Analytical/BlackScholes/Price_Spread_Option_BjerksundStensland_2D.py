# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Price_Spread_Option_BjerksundStensland_2D.m

    
@function
def Price_Spread_Option_BjerksundStensland_2D(K=None,S0_1=None,S0_2=None,T=None,r=None,rho=None,sigma_1=None,sigma_2=None,q_1=None,q_2=None,*args,**kwargs):
    varargin = Price_Spread_Option_BjerksundStensland_2D.varargin
    nargin = Price_Spread_Option_BjerksundStensland_2D.nargin

    #######################################################
# About: calcuates Price of 2D Spread option, (S_1(T) - S_2(T) - K)+, using Bjerksund & Stensland approximation
#        Note: when K = 0, this agrees with Magrabes exact formula
# Author: Justin Lars Kirkby
    
    # Reference: Bjerksund, P. and Stensland, G. (2006): "Closed form spread option valuation"
    
    # -----------------
# Params
# -----------------
# S0_1    = initial asset price of first asset, e.g. S0_1 = 100
# S0_2    = initial asset price of second asset, e.g. S0_2 = 100
# T       = time to maturity in years (e.g. T=1)
# r       = interest rate
# rho     = instantaneous correlation between S_1 and S_2
# sigma_1 = volatility of first asset (annualized), e.g. sigma = 0.2
# sigma_2 = volatility of second asset (annualized), e.g. sigma = 0.2
# q_1     = dividend yield of first asset, e.g. q_1 = 0.02
# q_2     = dividend yield of second asset, e.g. q_2 = 0.02
#  
#######################################################
    
    F1=dot(S0_1,exp(dot((r - q_1),T)))
# Price_Spread_Option_BjerksundStensland_2D.m:24
    F2=dot(S0_2,exp(dot((r - q_2),T)))
# Price_Spread_Option_BjerksundStensland_2D.m:25
    a=F2 + K
# Price_Spread_Option_BjerksundStensland_2D.m:27
    b=F2 / a
# Price_Spread_Option_BjerksundStensland_2D.m:28
    rhosigs=dot(dot(rho,sigma_1),sigma_2)
# Price_Spread_Option_BjerksundStensland_2D.m:29
    sig=sqrt(sigma_1 ** 2 - dot(dot(2,rhosigs),b) + dot(b ** 2,sigma_2 ** 2))
# Price_Spread_Option_BjerksundStensland_2D.m:30
    sigst=dot(sig,sqrt(T))
# Price_Spread_Option_BjerksundStensland_2D.m:31
    d1=(log(F1 / a) + dot((dot(0.5,sigma_1 ** 2) - dot(b,rhosigs) + dot(dot(0.5,b ** 2),sigma_2 ** 2)),T)) / sigst
# Price_Spread_Option_BjerksundStensland_2D.m:34
    d2=(log(F1 / a) + dot((dot(- 0.5,sigma_1 ** 2) + rhosigs + dot((dot(0.5,b ** 2) - b),sigma_2 ** 2)),T)) / sigst
# Price_Spread_Option_BjerksundStensland_2D.m:35
    d3=(log(F1 / a) + dot((dot(- 0.5,sigma_1 ** 2) + dot(dot(0.5,b ** 2),sigma_2 ** 2)),T)) / sigst
# Price_Spread_Option_BjerksundStensland_2D.m:36
    price=dot(exp(dot(- r,T)),(dot(F1,normcdf(d1)) - dot(F2,normcdf(d2)) - dot(K,normcdf(d3))))
# Price_Spread_Option_BjerksundStensland_2D.m:38
    return price
    
if __name__ == '__main__':
    pass
    