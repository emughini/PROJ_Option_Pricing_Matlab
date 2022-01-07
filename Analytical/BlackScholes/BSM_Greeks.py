# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# BSM_Greeks.m

    
@function
def BSM_Greeks(G=None,S_0=None,sigma=None,r=None,q=None,T=None,K=None,call=None,*args,**kwargs):
    varargin = BSM_Greeks.varargin
    nargin = BSM_Greeks.nargin

    #######################################################
# About: calcuates prices and Greeks for Black Scholes Model (for strike or vector of strikes)
# Author: Justin Lars Kirkby
    
    # -----------------
# Params
# -----------------
# S_0   = initial asset price, e.g. S_0 = 100
# sigma = volatility (annualized), e.g. sigma = 0.2
# r     = interest rate, e.g. r = 0.05
# q     = dividend yeild, e.g. q = 0.02
# K     = strike (or vector of strikes)
# call  = 1 for call option (else put)
    
    # G = Greek: 
#         0:Price
#         1:Delta, 2:Gamma, 3:Theta
#         4:Vega,  5:Rho,   6:Vanna
#         7:Vomma
#  
#######################################################
    sig=copy(sigma)
# BSM_Greeks.m:23
    eqT=exp(dot(- q,T))
# BSM_Greeks.m:25
    erT=exp(dot(- r,T))
# BSM_Greeks.m:26
    sqT=sqrt(T)
# BSM_Greeks.m:27
    d1=dot(1 / (dot(sig,sqT)),(log(S_0 / K) + dot((r - q + sig ** 2 / 2),T)))
# BSM_Greeks.m:29
    d2=d1 - dot(sig,sqT)
# BSM_Greeks.m:30
    if G == 0:
        if call == 1:
            Greeks=multiply(dot(eqT,S_0),normcdf(d1)) - multiply(dot(erT,K),normcdf(d2))
# BSM_Greeks.m:34
        else:
            Greeks=multiply(dot(erT,K),normcdf(- d2)) - multiply(dot(eqT,S_0),normcdf(- d1))
# BSM_Greeks.m:36
    else:
        if G == 1:
            if call == 1:
                Greeks=dot(eqT,normcdf(d1))
# BSM_Greeks.m:41
            else:
                Greeks=dot(- eqT,normcdf(- d1))
# BSM_Greeks.m:43
        else:
            if G == 2:
                Greeks=exp(dot(- 0.5,d1 ** 2)) / (dot(dot(sqrt(dot(dot(2,pi),T)),sig),S_0))
# BSM_Greeks.m:47
            else:
                if G == 3:
                    if call == 1:
                        Greeks=dot(multiply(dot(- eqT,S_0),normpdf(d1)),sig) / (dot(2,sqT)) - multiply(dot(dot(r,erT),K),normcdf(d2)) + multiply(dot(dot(q,eqT),S_0),normcdf(d1))
# BSM_Greeks.m:51
                    else:
                        Greeks=dot(multiply(dot(- eqT,S_0),normpdf(d1)),sig) / (dot(2,sqT)) + multiply(dot(dot(r,erT),K),normcdf(- d2)) - multiply(dot(dot(q,eqT),S_0),normcdf(- d1))
# BSM_Greeks.m:54
                else:
                    if G == 4:
                        Greeks=dot(dot(multiply(S_0,normpdf(d1)),eqT),sqT)
# BSM_Greeks.m:59
                    else:
                        if G == 5:
                            if call == 1:
                                Greeks=multiply(dot(dot(T,erT),K),normcdf(d2))
# BSM_Greeks.m:63
                            else:
                                Greeks=multiply(dot(dot(- T,erT),K),normcdf(- d2))
# BSM_Greeks.m:65
                        else:
                            if G == 6:
                                Greeks=multiply(dot(- eqT,normpdf(d1)),d2) / sig
# BSM_Greeks.m:69
                            else:
                                if G == 7:
                                    Greeks=multiply(multiply(multiply(dot(dot(eqT,sqT),S_0),normpdf(d1)),d1),d2) / sig
# BSM_Greeks.m:72
    
    return Greeks
    
if __name__ == '__main__':
    pass
    