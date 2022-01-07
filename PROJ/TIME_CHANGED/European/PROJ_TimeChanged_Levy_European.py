# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_TimeChanged_Levy_European.m

    
@function
def PROJ_TimeChanged_Levy_European(r=None,q=None,S_0=None,T=None,W=None,call=None,levyExponent=None,hFunc=None,n=None,ParamsDiffus=None,ParamsCtmc=None,ParamsProj=None,*args,**kwargs):
    varargin = PROJ_TimeChanged_Levy_European.varargin
    nargin = PROJ_TimeChanged_Levy_European.nargin

    #########################################################
# About: Pricing Function for European Options under time-changed Levy Models,
#        using Markov-Chain Approximation + PROJ method
# Models Supported: Time Changed Levy Processes, such as Heston's Model (with rho=0)
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # References:   1) A General Framework for Time-Changed Markov Processes and Applications. 
#                  European J. Operational Research (2018), Cui, Z., Kirkby, J.L., and Nguyen, D.
    
    #               2) Efficient Option Pricing by Frame Duality with the Fast Fourier Transform. 
#                  SIAM J. Financial Math (2015), Kirkby, J.L
# ----------------------
# Contract/Model Params 
# ----------------------
# S_0 = initial stock price (e.g. 100)
# W   = strike  (e.g. 100)
# r   = interest rate (e.g. 0.05)
# q   = dividend yield (e.g. 0.05)
# T   = time remaining until maturity (in years, e.g. T=1)
# call  = 1 for call (else put)
# hFunc = function handle, the integrand in time change, tau = int_0^T h(X_s)ds
# levyExponent = function handle: e.g. -1/2*i*xi - 1/2*xi^2 for case of Heston as time changed levy process
# n = number of discrete points for the discrete version, set n = 0 for continuous
# ParamsDiffus =  diffusion parameters of X_s, where tau = int_0^T h(X_s)ds
    
    # ----------------------
# Numerical (CTMC/PROJ) Params 
# ----------------------
# ParamsCtmc = container of CTMC approximation params
# ParamsProj = container of PROJ params
#########################################################
    
    # Martingale Adjustment for exponent: ensure the driving Levy process itself is a martingale
# Note, we model the RN drift (r-q)*T separately... then price using PROJ
    levyExponentRN=lambda u=None: levyExponent(u) - dot(dot(1j,levyExponent(- 1j)),u)
# PROJ_TimeChanged_Levy_European.m:37
    ### Set CTMC Parameters (CTMC approximates the diffusion)
    gridMethod=6
# PROJ_TimeChanged_Levy_European.m:41
    
    varGridMult=ParamsCtmc.varGridMult
# PROJ_TimeChanged_Levy_European.m:42
    gamma=ParamsCtmc.gamma
# PROJ_TimeChanged_Levy_European.m:43
    Nx=ParamsCtmc.Nx
# PROJ_TimeChanged_Levy_European.m:44
    
    ### The time change driver process X_t is approximated by CTMC
    if ParamsDiffus.model == 1:
        t=copy(T)
# PROJ_TimeChanged_Levy_European.m:48
        eta=ParamsDiffus.eta
# PROJ_TimeChanged_Levy_European.m:49
        theta=ParamsDiffus.theta
# PROJ_TimeChanged_Levy_European.m:49
        Sigmav=ParamsDiffus.Sigmav
# PROJ_TimeChanged_Levy_European.m:49
        v0=ParamsDiffus.v0
# PROJ_TimeChanged_Levy_European.m:49
        mu_func=lambda v=None: dot(eta,(theta - v))
# PROJ_TimeChanged_Levy_European.m:50
        sig_func=lambda v=None: dot(Sigmav,sqrt(v))
# PROJ_TimeChanged_Levy_European.m:51
        mu_H=dot(exp(dot(- eta,t)),v0) + dot(theta,(1 - exp(dot(- eta,t))))
# PROJ_TimeChanged_Levy_European.m:53
        sig2_H=dot(dot(Sigmav ** 2 / eta,v0),(exp(dot(- eta,t)) - exp(dot(dot(- 2,eta),t)))) + dot(dot(theta,Sigmav ** 2) / (dot(2,eta)),(1 - exp(dot(- eta,t)) + exp(dot(dot(- 2,eta),t))))
# PROJ_TimeChanged_Levy_European.m:54
        lx=max(1e-05,mu_H - dot(gamma,sqrt(sig2_H)))
# PROJ_TimeChanged_Levy_European.m:56
        ux=mu_H + dot(gamma,sqrt(sig2_H))
# PROJ_TimeChanged_Levy_European.m:57
    
    center=copy(v0)
# PROJ_TimeChanged_Levy_European.m:60
    G,stateGrid=Q_Matrix_AllForms(Nx,mu_func,sig_func,lx,ux,gridMethod,varGridMult,center,nargout=2)
# PROJ_TimeChanged_Levy_European.m:61
    H=hFunc(stateGrid)
# PROJ_TimeChanged_Levy_European.m:63
    
    ####////////////////////////////////////////////////////////
#### Find bracketing states
####////////////////////////////////////////////////////////
    k_0=2
# PROJ_TimeChanged_Levy_European.m:68
    
    while v0 >= stateGrid(k_0) and k_0 < Nx:

        k_0=k_0 + 1
# PROJ_TimeChanged_Levy_European.m:70

    
    k_0=k_0 - 1
# PROJ_TimeChanged_Levy_European.m:72
    ####////////////////////////////////////////////////////////
# Risk Neutral CHF of Log Return: ln(S_T/S_0)
####////////////////////////////////////////////////////////
    if n == 0:
        rnCHF=lambda z=None: multiply(exp(dot(dot(dot(1j,(r - q)),T),z)),rnCHF_cont_single(z,levyExponentRN,H,G,T,k_0,stateGrid))
# PROJ_TimeChanged_Levy_European.m:78
    else:
        rnCHF=lambda z=None: multiply(exp(dot(dot(dot(1j,(r - q)),T),z)),rnCHF_disc_single(z,levyExponentRN,H,G,T,n,k_0,stateGrid))
# PROJ_TimeChanged_Levy_European.m:80
    
    c1=0
# PROJ_TimeChanged_Levy_European.m:83
    order=ParamsProj.order
# PROJ_TimeChanged_Levy_European.m:84
    alph=ParamsProj.alph
# PROJ_TimeChanged_Levy_European.m:85
    N_proj=ParamsProj.N_proj
# PROJ_TimeChanged_Levy_European.m:86
    price=PROJ_European(order,N_proj,alph,r,q,T,S_0,W,call,rnCHF,c1)
# PROJ_TimeChanged_Levy_European.m:88
    return price
    
if __name__ == '__main__':
    pass
    
    
@function
def rnCHF_cont_single(z=None,levyExponentRN=None,H=None,G=None,T=None,k_0=None,stateGrid=None,*args,**kwargs):
    varargin = rnCHF_cont_single.varargin
    nargin = rnCHF_cont_single.nargin

    numStates=length(stateGrid)
# PROJ_TimeChanged_Levy_European.m:93
    numZ=length(z)
# PROJ_TimeChanged_Levy_European.m:94
    ones_=ones(numStates,1)
# PROJ_TimeChanged_Levy_European.m:96
    
    chf=zeros(numStates,numZ)
# PROJ_TimeChanged_Levy_European.m:97
    
    
    for j in arange(1,numZ).reshape(-1):
        chf[arange(),j]=dot(expm(dot(T,(G + diag(dot(levyExponentRN(z(j)),H))))),ones_)
# PROJ_TimeChanged_Levy_European.m:100
    
    
    chf=chf(k_0,arange())
# PROJ_TimeChanged_Levy_European.m:103
    return chf
    
if __name__ == '__main__':
    pass
    
    
@function
def rnCHF_disc_single(z=None,levyExponentRN=None,H=None,G=None,T=None,n=None,k_0=None,stateGrid=None,*args,**kwargs):
    varargin = rnCHF_disc_single.varargin
    nargin = rnCHF_disc_single.nargin

    # k_0 is the bracketing index: grid(k_0) <= v0 < grid(k_0+1)
    #Returns the chf with is linear interpolation of the two bracketing chfs
    dt=T / n
# PROJ_TimeChanged_Levy_European.m:109
    P=expm(dot(dt,G))
# PROJ_TimeChanged_Levy_European.m:110
    numStates=length(stateGrid)
# PROJ_TimeChanged_Levy_European.m:112
    numZ=length(z)
# PROJ_TimeChanged_Levy_European.m:113
    ones_=ones(numStates,1)
# PROJ_TimeChanged_Levy_European.m:115
    
    chf=zeros(numStates,numZ)
# PROJ_TimeChanged_Levy_European.m:116
    
    for j in arange(1,numZ).reshape(-1):
        E=diag(exp(dot(dot(levyExponentRN(z(j)),H),dt)))
# PROJ_TimeChanged_Levy_European.m:119
        chf[arange(),j]=dot(E,ones_)
# PROJ_TimeChanged_Levy_European.m:120
        EP=dot(E,P)
# PROJ_TimeChanged_Levy_European.m:121
        for k in arange(1,n).reshape(-1):
            chf[arange(),j]=dot(EP,chf(arange(),j))
# PROJ_TimeChanged_Levy_European.m:123
    
    
    chf=chf(k_0,arange())
# PROJ_TimeChanged_Levy_European.m:128
    return chf
    
if __name__ == '__main__':
    pass
    