# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_ForwardStarting.m

    
@function
def PROJ_ForwardStarting(N=None,alph=None,r=None,q=None,T1=None,T2=None,S_0=None,call=None,rnCHF1=None,rnCHF2=None,*args,**kwargs):
    varargin = PROJ_ForwardStarting.varargin
    nargin = PROJ_ForwardStarting.nargin

    #########################################################
# About: Pricing Function for Forward Starting Options using PROJ method (uses cubic B-splines)
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
# T1  =  time to maturity (in years), e.g. T1=1
# T2  = T - T1, how much time remains in contract after the forward start date (choose 0 < T2 < T1)
# call  = 1 for call (else put)
# rnCHF1 = risk netural characteristic function of process up to T1 (function handle with single argument)
# rnCHF2 = risk netural characteristic function of process with T2 = T - T1 remaining time to maturity after forward start date
# ----------------------
# Numerical (PROJ) Params 
# ----------------------
# alph  = grid with is 2*alph
# N     = budget: resolution = 2*alph/(N-1), where support is of length 2*alph
#########################################################
    
    T=T1 + T2
# PROJ_ForwardStarting.m:27
    dx=dot(2,alph) / (N - 1)
# PROJ_ForwardStarting.m:29
    a=1 / dx
# PROJ_ForwardStarting.m:29
    dw=dot(2,pi) / (dot(N,dx))
# PROJ_ForwardStarting.m:30
    omega=dot(dw,(arange(1,N - 1)))
# PROJ_ForwardStarting.m:32
    
    nbar=N / 2
# PROJ_ForwardStarting.m:33
    xmin=dot((1 - N / 2),dx)
# PROJ_ForwardStarting.m:34
    #### Cubic Spline
    b0=1208 / 2520
# PROJ_ForwardStarting.m:37
    b1=1191 / 2520
# PROJ_ForwardStarting.m:37
    b2=120 / 2520
# PROJ_ForwardStarting.m:37
    b3=1 / 2520
# PROJ_ForwardStarting.m:37
    grand=lambda w=None: multiply(rnCHF2(w),(sin(w / (dot(2,a))) / w) ** 4.0) / (b0 + dot(b1,cos(w / a)) + dot(b2,cos(dot(2,w) / a)) + dot(b3,cos(dot(3,w) / a)))
# PROJ_ForwardStarting.m:38
    beta=real(fft(concat([1 / (dot(32,a ** 4)),multiply(exp(dot(dot(- 1j,xmin),omega)),feval(grand,omega))])))
# PROJ_ForwardStarting.m:39
    #FIND Value of E[(1 - exp(X_tau))^+]
    G=zeros(1,N)
# PROJ_ForwardStarting.m:42
    G[nbar + 1]=dot(1,(1 / 24 - dot(dot(1 / 20,exp(dx)),(exp(dot(- 7 / 4,dx)) / 54 + exp(dot(- 1.5,dx)) / 18 + exp(dot(- 1.25,dx)) / 2 + dot(7,exp(- dx)) / 27))))
# PROJ_ForwardStarting.m:44
    G[nbar]=dot(1,(0.5 - dot(0.05,(28 / 27 + exp(dot(- 7 / 4,dx)) / 54 + exp(dot(- 1.5,dx)) / 18 + exp(dot(- 1.25,dx)) / 2 + dot(14,exp(- dx)) / 27 + dot(121 / 54,exp(dot(- 0.75,dx))) + dot(23 / 18,exp(dot(- 0.5,dx))) + dot(235 / 54,exp(dot(- 0.25,dx)))))))
# PROJ_ForwardStarting.m:46
    G[nbar - 1]=dot(1,(23 / 24 - dot(exp(- dx) / 90,((28 + dot(7,exp(- dx))) / 3 + (dot(14,exp(dx)) + exp(dot(- 7 / 4,dx)) + dot(242,cosh(dot(0.75,dx))) + dot(470,cosh(dot(0.25,dx)))) / 12 + dot(0.25,(exp(dot(- 1.5,dx)) + dot(9,exp(dot(- 1.25,dx))) + dot(46,cosh(dot(0.5,dx)))))))))
# PROJ_ForwardStarting.m:49
    vartheta_star=dot(1 / 90,(dot(14 / 3,(2 + cosh(dx))) + dot(0.5,(cosh(dot(1.5,dx)) + dot(9,cosh(dot(1.25,dx))) + dot(23,cosh(dot(0.5,dx))))) + dot(1 / 6,(cosh(dot(7 / 4,dx)) + dot(121,cosh(dot(0.75,dx))) + dot(235,cosh(dot(0.25,dx)))))))
# PROJ_ForwardStarting.m:53
    G[arange(1,nbar - 2)]=1 - dot(dot(1,exp(xmin + dot(dx,(arange(0,nbar - 3))))),vartheta_star)
# PROJ_ForwardStarting.m:57
    Cons=dot(32,a ** 4)
# PROJ_ForwardStarting.m:58
    Vbar2=dot(dot(Cons / N,G(1,arange(1,(nbar + 1)))),(beta(1,arange(1,(nbar + 1))).T))
# PROJ_ForwardStarting.m:60
    ### Find Second Expansion
    grand=lambda w=None: multiply(rnCHF1(w),(sin(w / (dot(2,a))) / w) ** 4.0) / (b0 + dot(b1,cos(w / a)) + dot(b2,cos(dot(2,w) / a)) + dot(b3,cos(dot(3,w) / a)))
# PROJ_ForwardStarting.m:63
    beta=real(fft(concat([1 / (dot(32,a ** 4)),multiply(exp(dot(dot(- 1j,xmin),omega)),feval(grand,omega))])))
# PROJ_ForwardStarting.m:64
    G[arange(1,N)]=exp(xmin + dot((arange(0,(N - 1))),dx))
# PROJ_ForwardStarting.m:66
    Vbar1=dot(dot(Cons / N,G),beta.T)
# PROJ_ForwardStarting.m:67
    Val_put=dot(dot(dot(dot(exp(dot(- r,T)),Vbar2),Vbar1),S_0),vartheta_star)
# PROJ_ForwardStarting.m:68
    ####  PUT CALL PARITY/PRICING FORMULA
    if call == 1:
        Val_Proj=dot(S_0,(exp(dot(- q,T)) - dot(exp(dot(- r,T2)),exp(dot(- q,T1))))) + Val_put
# PROJ_ForwardStarting.m:73
    else:
        Val_Proj=copy(Val_put)
# PROJ_ForwardStarting.m:75
    
    price=copy(Val_Proj)
# PROJ_ForwardStarting.m:78
    return price
    
if __name__ == '__main__':
    pass
    