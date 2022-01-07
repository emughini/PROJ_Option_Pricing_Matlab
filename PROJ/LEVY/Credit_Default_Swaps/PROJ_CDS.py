# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_CDS.m

    
@function
def PROJ_CDS(R=None,L=None,M=None,T=None,r=None,N=None,alph=None,mult=None,rnCHF=None,*args,**kwargs):
    varargin = PROJ_CDS.varargin
    nargin = PROJ_CDS.nargin

    #########################################################
# About: Calc Fair Spread of Credit Default Swaps (and default probabilities) using PROJ method
# Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Returns: prob = probability of default on [0,T]
#          spread = fair (par) CDS spread in basis points (ie *10000)
# Author: Justin Lars Kirkby
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# r     = interest rate (e.g. 0.05)
# T     = time remaining until maturity (in years, e.g. T=1)
# M     = number of subintervals of [0,T] (total of M+1 monitoring points in time grid, including initial time)
# R     = recovery rate, 0<R<1
# L     = percentage of initial firm value that leads to default, 0<L<1
# rnCHF = risk netural characteristic function (function handle with single argument)
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# alph  = grid with is 2*alph
# N     = number of grid/basis points (power of 2, e.g. 2^12), resolution = 2*alph/(N-1)
#########################################################
    dt=T / M
# PROJ_CDS.m:25
    l=log(L)
# PROJ_CDS.m:26
    K=N / 2
# PROJ_CDS.m:28
    dx=dot(2,alph) / (N - 1)
# PROJ_CDS.m:29
    a=1 / dx
# PROJ_CDS.m:29
    xmin=copy(l)
# PROJ_CDS.m:31
    nnot=floor(1 - dot(xmin,a))
# PROJ_CDS.m:32
    
    dx=l / (1 - nnot)
# PROJ_CDS.m:33
    a=1 / dx
# PROJ_CDS.m:34
    zmin=dot((1 - K),dx)
# PROJ_CDS.m:36
    Nmult=dot(mult,N)
# PROJ_CDS.m:37
    dw=dot(dot(2,pi),a) / Nmult
# PROJ_CDS.m:38
    grand=dot(dw,(arange(1,Nmult - 1)))
# PROJ_CDS.m:39
    Thet=ones(K,1)
# PROJ_CDS.m:41
    Thet[1]=0.5
# PROJ_CDS.m:41
    b1=1 / 48
# PROJ_CDS.m:42
    b2=1 / 12
# PROJ_CDS.m:42
    a2=a ** 2
# PROJ_CDS.m:44
    Cons=dot(24,a2) / Nmult
# PROJ_CDS.m:45
    grand=multiply(multiply(exp(dot(dot(- 1j,zmin),grand)),rnCHF(grand)),(sin(grand / (dot(2,a))) / grand) ** 2.0) / (2 + cos(grand / a))
# PROJ_CDS.m:47
    beta=dot(Cons,real(fft(concat([1 / (dot(24,a2)),grand]))))
# PROJ_CDS.m:48
    toepM=concat([[beta(arange(K,1,- 1)).T],[0],[beta(arange(dot(2,K) - 1,K,- 1),+ 1).T]])
# PROJ_CDS.m:49
    toepM=fft(toepM)
# PROJ_CDS.m:49
    Thetbar1=cumsum(beta(arange(dot(2,K),K + 1,- 1))).T
# PROJ_CDS.m:51
    p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_CDS.m:53
    Val=p(arange(1,K)) + Thetbar1
# PROJ_CDS.m:54
    Probs=zeros(1,M)
# PROJ_CDS.m:56
    Probs[1]=Val(nnot)
# PROJ_CDS.m:57
    for m in arange(M - 2,0,- 1).reshape(-1):
        Thet[1]=dot(b1,(dot(13,Val(1)) + dot(15,Val(2)) - dot(5,Val(3)) + Val(4)))
# PROJ_CDS.m:60
        Thet[K]=dot(b1,(dot(13,Val(K)) + dot(15,Val(K - 1)) - dot(5,Val(K - 2)) + Val(K - 3)))
# PROJ_CDS.m:61
        Thet[arange(2,K - 1)]=dot(b2,(Val(arange(1,K - 2)) + dot(10,Val(arange(2,K - 1))) + Val(arange(3,K))))
# PROJ_CDS.m:62
        p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_CDS.m:64
        Val[arange(1,K)]=p(arange(1,K)) + Thetbar1
# PROJ_CDS.m:65
        Probs[M - m]=Val(nnot)
# PROJ_CDS.m:66
    
    prob=Val(nnot)
# PROJ_CDS.m:69
    denom=dot(dt,(0.5 + sum(multiply(exp(dot(dot(- r,dt),(arange(1,M - 1)))),Probs(arange(1,M - 1)))) + dot(dot(0.5,Probs(M)),exp(dot(- r,T)))))
# PROJ_CDS.m:70
    
    spread=dot(dot(10000,(1 - R)),((1 - dot(exp(dot(- r,T)),Probs(M))) / denom - r))
# PROJ_CDS.m:71
    return prob,spread
    
if __name__ == '__main__':
    pass
    