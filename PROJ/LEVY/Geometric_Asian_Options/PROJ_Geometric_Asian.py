# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_Geometric_Asian.m

    
@function
def PROJ_Geometric_Asian(N=None,alph=None,S_0=None,M=None,W=None,call=None,T=None,r=None,q=None,rnSYMB=None,*args,**kwargs):
    varargin = PROJ_Geometric_Asian.varargin
    nargin = PROJ_Geometric_Asian.nargin

    #########################################################
# About: Pricing Function for Geometric Asian Options using PROJ method
# Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # Reference:   (1) An Efficient Transform Method For Asian Option Pricing, SIAM J. Financial Math., 2016
#              (2) Efficient Option Pricing by Frame Duality with the Fast Fourier Transform. 
#                  SIAM J. Financial Math (2015), Kirkby, J.L
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# S_0 = initial stock price (e.g. 100)
# W   = strike  (e.g. 100)
# r   = interest rate (e.g. 0.05)
# q   = dividend yield (e.g. 0.05)
# T   = time remaining until maturity (in years, e.g. T=1)
# M   = number of subintervals of [0,T] (total of M+1 monitoring points in time grid, including S_0)
# call = 1 for call (else put)
# rnSYMB =  risk neutral symbol of log return over time step dt = 1/M (function handle with single argument)
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# alph  = grid with is 2*alph
# N     = number of grid/basis points (power of 2, e.g. 2^12), resolution = 2*alph/(N-1)
#########################################################
    
    Psi=lambda u=None: rnSYMB(u) - dot((r - q - rnSYMB(- 1j)),u)
# PROJ_Geometric_Asian.m:32
    
    dx=dot(2,alph) / (N - 1)
# PROJ_Geometric_Asian.m:34
    a=1 / dx
# PROJ_Geometric_Asian.m:34
    dt=T / M
# PROJ_Geometric_Asian.m:35
    xmin=log(W) - dx
# PROJ_Geometric_Asian.m:37
    if abs(xmin) > dot(1.01,alph):
        alph=dot(1.01,abs(xmin))
# PROJ_Geometric_Asian.m:39
        price=PROJ_Geometric_Asian(N,alph,S_0,M,W,call,T,r,q,rnSYMB)
# PROJ_Geometric_Asian.m:40
        return price
    
    dw=dot(dot(2,pi),a) / N
# PROJ_Geometric_Asian.m:44
    omega=(arange(dw,dot((N - 1),dw),dw))
# PROJ_Geometric_Asian.m:45
    
    gran=zeros(1,N - 1)
# PROJ_Geometric_Asian.m:46
    for j in arange(1,(N - 1)).reshape(-1):
        gran[j]=sum(Psi(dot(omega(j),(1 - (arange(1,M)) / (M + 1)))))
# PROJ_Geometric_Asian.m:49
    
    a2=a ** 2
# PROJ_Geometric_Asian.m:52
    a3=dot(a,a2)
# PROJ_Geometric_Asian.m:52
    gg=lambda w=None: (sin(w / (dot(2,a))) / w) ** 3.0 / (dot(26,cos(w / a)) + cos(dot(2,w) / a) + 33)
# PROJ_Geometric_Asian.m:54
    gran=multiply(exp(dot(dot(1j,(log(S_0) + dot(dot(0.5,T),(r - q - Psi(- 1j))))),omega) + dot(dt,gran)),gg(omega))
# PROJ_Geometric_Asian.m:55
    beta=real(fft(concat([1 / (dot(960,a3)),multiply(exp(dot(dot(- 1j,xmin),omega)),gran)])))
# PROJ_Geometric_Asian.m:56
    x1=xmin + dx
# PROJ_Geometric_Asian.m:58
    ex1=exp(x1)
# PROJ_Geometric_Asian.m:59
    G=zeros(1,N / 2)
# PROJ_Geometric_Asian.m:60
    G[1]=dot(ex1,(dot(a3,exp(dot(0.5,dx))) - dot(a,(1 / 8 + a / 2 + a2)))) - W / 48
# PROJ_Geometric_Asian.m:61
    G[2]=dot(ex1,(dot(a3,(2 + exp(dot(1.5,dx)) - dot(3,exp(dot(0.5,dx))))) - dot(0.75,a))) - dot(0.5,W)
# PROJ_Geometric_Asian.m:62
    G[3]=dot(ex1,(dot(0.5,a2) - a / 8 + dot(a3,(exp(dot(2.5,dx)) + dot(3,(exp(dot(0.5,dx)) - exp(dot(1.5,dx)))) - 1)))) - dot(47 / 48,W)
# PROJ_Geometric_Asian.m:63
    G[arange(4,N / 2)]=dot(dot(exp(x1 + dot(dx,(arange(2,N / 2 - 2)))),a3),(dot(2,sinh(dot(1.5,dx))) - dot(6,sinh(dot(0.5,dx))))) - W
# PROJ_Geometric_Asian.m:64
    price=dot(dot(dot(dot(960,a ** (3)),exp(dot(- r,T))) / N,G),beta(arange(1,N / 2)).T)
# PROJ_Geometric_Asian.m:67
    price=max(0,price)
# PROJ_Geometric_Asian.m:68
    if logical_not(call) == 1:
        error('Sorry, havent yet added the put option... just use PCP')
    
    return price
    
if __name__ == '__main__':
    pass
    