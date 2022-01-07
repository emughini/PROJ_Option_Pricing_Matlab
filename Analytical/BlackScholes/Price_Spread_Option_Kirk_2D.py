# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Price_Spread_Option_Kirk_2D.m

    
@function
def Price_Spread_Option_Kirk_2D(K=None,S0_1=None,S0_2=None,T=None,r=None,rho=None,sigma_1=None,sigma_2=None,q_1=None,q_2=None,*args,**kwargs):
    varargin = Price_Spread_Option_Kirk_2D.varargin
    nargin = Price_Spread_Option_Kirk_2D.nargin

    #######################################################
# About: calcuates Price of 2D Spread option, (S_1(T) - S_2(T) - K)+, using Kirks approximation
#        Note: when K = 0, this agrees with Magrabes exact formula
# Author: Justin Lars Kirkby
    
    # Reference: Kirk, E. (1995): "Correlation in the energy markets," In Managing Energy Price
#               Risk (First Edition). London: Risk Publications and Enron, pp. 71-78.
    
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
# Price_Spread_Option_Kirk_2D.m:25
    F2=dot(S0_2,exp(dot((r - q_2),T)))
# Price_Spread_Option_Kirk_2D.m:26
    f2k=F2 / (F2 + K)
# Price_Spread_Option_Kirk_2D.m:28
    sig=sqrt(sigma_1 ** 2 - dot(dot(dot(dot(2,rho),sigma_1),sigma_2),f2k) + dot(f2k ** 2,sigma_2 ** 2))
# Price_Spread_Option_Kirk_2D.m:29
    d1=(log(F1 / (F1 + K)) + dot(dot(0.5,sig ** 2),T)) / (dot(sig,sqrt(T)))
# Price_Spread_Option_Kirk_2D.m:31
    d2=d1 - dot(sig,sqrt(T))
# Price_Spread_Option_Kirk_2D.m:32
    price=dot(exp(dot(- r,T)),(dot(F1,normcdf(d1)) - dot((F2 + K),normcdf(d2))))
# Price_Spread_Option_Kirk_2D.m:34
    return price
    
if __name__ == '__main__':
    pass
    