# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Lewis_European_Price.m

    
@function
def Lewis_European_Price(S_0=None,W=None,rnCHF=None,T=None,r=None,q=None,call=None,max_u=None,*args,**kwargs):
    varargin = Lewis_European_Price.varargin
    nargin = Lewis_European_Price.nargin

    #########################################################
# About: Pricing Function for European Options using the method of Lewis (2001)
# Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# S_0 = initial stock price (e.g. 100)
# W   = strike  (e.g. 100)
# r   = interest rate (e.g. 0.05)
# q   = dividend yield (e.g. 0.05)
# T   = time remaining until maturity (in years, e.g. T=1)
# call  = 1 for call (else put)
# rnCHF = risk netural characteristic function (function handle with single argument)
# 
# ----------------------
# Numerical Params 
# ----------------------
# max_u = upper limit of fourier integral for numerical integration
    
    #########################################################
    if nargin < 8:
        max_u=400
# Lewis_European_Price.m:26
    
    k=log(S_0 / W)
# Lewis_European_Price.m:29
    # Integrate the complex integral
    grand=lambda u=None: real(multiply(exp(dot(dot(1j,u),k)),rnCHF(u - dot(0.5,1j))) / (multiply(u,u) + 0.25))
# Lewis_European_Price.m:32
    z=integral(grand,0,max_u)
# Lewis_European_Price.m:33
    # Call Price
    price=dot(S_0,exp(dot(- q,T))) - dot(dot(dot((1 / pi),sqrt(dot(S_0,W))),exp(dot(- r,T))),z)
# Lewis_European_Price.m:36
    if call != 1:
        price=price - (dot(S_0,exp(dot(- q,T))) - dot(W,exp(dot(- r,T))))
# Lewis_European_Price.m:39
    
    return price
    
if __name__ == '__main__':
    pass
    