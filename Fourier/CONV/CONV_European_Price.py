# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# CONV_European_Price.m

    
@function
def CONV_European_Price(S_0=None,W=None,rnCHF=None,T=None,r=None,call=None,N=None,alph=None,damp_alpha=None,*args,**kwargs):
    varargin = CONV_European_Price.varargin
    nargin = CONV_European_Price.nargin

    #########################################################
# About: Pricing Function for European Options using the CONV method of Lord, Fang, Bervoets, and Oosterlee (2008)
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
# N  = number of FFT grid points (power of 2, e.g. 2^12)
# alpha = gridwidth param, density centered on [-alph, alph], determined e.g. using cumulants
#########################################################
    
    if call != 1:
        call=- 1
# CONV_European_Price.m:27
    
    if nargin < 9:
        damp_alpha=dot(- call,0.5)
# CONV_European_Price.m:31
    
    
    dx=(dot(2,alph)) / N
# CONV_European_Price.m:34
    
    du=dot(2,pi) / (dot(2,alph))
# CONV_European_Price.m:35
    grid1=(arange(0,N - 1)).T
# CONV_European_Price.m:37
    grid2=(- 1) ** grid1
# CONV_European_Price.m:38
    x=(multiply(grid1,dx)) - (dot(N / 2,dx))
# CONV_European_Price.m:40
    y=log(W / S_0) + (multiply(grid1,dx)) - (dot(N / 2,dx))
# CONV_European_Price.m:41
    u=(multiply(grid1,du)) - (dot(N / 2,du))
# CONV_European_Price.m:43
    payoff=max(dot(call,(dot(S_0,exp(y)) - W)),0)
# CONV_European_Price.m:45
    damped=multiply(payoff,exp(multiply(damp_alpha,y)))
# CONV_European_Price.m:46
    w=ones(N,1)
# CONV_European_Price.m:47
    w[1]=0.5
# CONV_European_Price.m:47
    w[N]=0.5
# CONV_European_Price.m:47
    
    f=ifft(multiply(multiply((grid2),w),damped))
# CONV_European_Price.m:48
    chfval=rnCHF(- (u - (dot(1j,damp_alpha))))
# CONV_European_Price.m:50
    f=multiply(multiply(exp(multiply(multiply(multiply(1j,grid1),(y(1) - x(1))),du)),chfval),f)
# CONV_European_Price.m:52
    # Final Valuation Step
    C=abs(multiply(multiply(exp(- (dot(r,T)) - (multiply(damp_alpha,x)) + (multiply(multiply(1j,u),(y(1) - x(1))))),grid2),fft(f)))
# CONV_European_Price.m:55
    price=double(C(N / 2 + 1,1))
# CONV_European_Price.m:56
    return price
    
if __name__ == '__main__':
    pass
    