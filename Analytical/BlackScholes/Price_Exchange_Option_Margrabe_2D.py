# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Price_Exchange_Option_Margrabe_2D.m

    
@function
def Price_Exchange_Option_Margrabe_2D(S0_1=None,S0_2=None,T=None,rho=None,sigma_1=None,sigma_2=None,q_1=None,q_2=None,*args,**kwargs):
    varargin = Price_Exchange_Option_Margrabe_2D.varargin
    nargin = Price_Exchange_Option_Margrabe_2D.nargin

    #######################################################
# About: calcuates Price of 2D Exchange option, (S_1(T) - S_2(T)), using Magrabe Formula Under 2D Diffusion
# Author: Justin Lars Kirkby
    
    # -----------------
# Params
# -----------------
# S0_1    = initial asset price of first asset, e.g. S0_1 = 100
# S0_2    = initial asset price of second asset, e.g. S0_2 = 100
# T       = time to maturity in years (e.g. T=1)
# rho     = instantaneous correlation between S_1 and S_2
# sigma_1 = volatility of first asset (annualized), e.g. sigma = 0.2
# sigma_2 = volatility of second asset (annualized), e.g. sigma = 0.2
# q_1     = dividend yield of first asset, e.g. q_1 = 0.02
# q_2     = dividend yield of second asset, e.g. q_2 = 0.02
#  
#######################################################
    
    sig=sqrt(sigma_1 ** 2 - dot(dot(dot(2,rho),sigma_1),sigma_2) + sigma_2 ** 2)
# Price_Exchange_Option_Margrabe_2D.m:20
    d1=(log(S0_1 / S0_2) + dot(dot(0.5,sig ** 2),T)) / (dot(sig,sqrt(T)))
# Price_Exchange_Option_Margrabe_2D.m:21
    d2=d1 - dot(sig,sqrt(T))
# Price_Exchange_Option_Margrabe_2D.m:22
    price=dot(dot(exp(dot(- q_1,T)),S0_1),normcdf(d1)) - dot(dot(exp(dot(- q_2,T)),S0_2),normcdf(d2))
# Price_Exchange_Option_Margrabe_2D.m:23
    return price
    
if __name__ == '__main__':
    pass
    