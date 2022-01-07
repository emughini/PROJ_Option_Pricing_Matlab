# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# CarrMadan_European_Price_Strikes.m

    
@function
def CarrMadan_European_Price_Strikes(S_0=None,W=None,rnCHF=None,N=None,T=None,r=None,q=None,call=None,alpha=None,*args,**kwargs):
    varargin = CarrMadan_European_Price_Strikes.varargin
    nargin = CarrMadan_European_Price_Strikes.nargin

    #########################################################
# About: Pricing Function for European Options using Method of Carr-Madan (1999)
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
    
    # ----------------------
# Numerical Params 
# ----------------------
# N     = number of FFT grid points (power of 2, e.g. 2^12)
#########################################################
    disc=exp(dot(- r,T))
# CarrMadan_European_Price_Strikes.m:24
    logK=log(W)
# CarrMadan_European_Price_Strikes.m:26
    
    logS=log(S_0)
# CarrMadan_European_Price_Strikes.m:27
    if nargin < 9:
        alpha=0.75
# CarrMadan_European_Price_Strikes.m:30
    
    eta=0.1
# CarrMadan_European_Price_Strikes.m:32
    lam=dot(2,pi) / (dot(N,eta))
# CarrMadan_European_Price_Strikes.m:34
    
    b=dot(N,lam) / 2
# CarrMadan_European_Price_Strikes.m:35
    uv=arange(1,N)
# CarrMadan_European_Price_Strikes.m:37
    ku=- b + dot(lam,(uv - 1))
# CarrMadan_European_Price_Strikes.m:38
    vj=dot((uv - 1),eta)
# CarrMadan_European_Price_Strikes.m:39
    rnCHF=lambda z=None: multiply(rnCHF(z),exp(dot(dot(1j,z),logS)))
# CarrMadan_European_Price_Strikes.m:40
    
    Psij=feval(rnCHF,vj - dot((alpha + 1),1j)) / (alpha ** 2 + alpha - vj ** 2 + multiply(dot(1j,(dot(2,alpha) + 1)),vj))
# CarrMadan_European_Price_Strikes.m:41
    temp=multiply(dot((dot(disc,eta) / 3),exp(dot(dot(1j,vj),b))),Psij)
# CarrMadan_European_Price_Strikes.m:43
    temp=multiply(temp,(3 + (- 1) ** uv - ((uv - 1) == 0)))
# CarrMadan_European_Price_Strikes.m:44
    Cku=real(multiply(exp(dot(- alpha,ku)),fft(temp)) / pi)
# CarrMadan_European_Price_Strikes.m:46
    istrike=floor((logK + b) / lam + 1)
# CarrMadan_European_Price_Strikes.m:48
    xp=concat([ku(istrike),ku(istrike,+ 1)])
# CarrMadan_European_Price_Strikes.m:49
    yp=concat([Cku(istrike),Cku(istrike,+ 1)])
# CarrMadan_European_Price_Strikes.m:50
    price=real(interp1(xp,yp,logK))
# CarrMadan_European_Price_Strikes.m:51
    if call != 1:
        price=price - (dot(S_0,exp(dot(- q,T))) - dot(W,disc))
# CarrMadan_European_Price_Strikes.m:54
    
    return price
    
if __name__ == '__main__':
    pass
    