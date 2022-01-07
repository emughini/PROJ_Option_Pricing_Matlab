# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# TC_Levy_VarianceSwap.m

    
@function
def TC_Levy_VarianceSwap(r=None,q=None,T=None,M=None,levyExponent=None,hFunc=None,n=None,ParamsDiffus=None,ParamsCtmc=None,*args,**kwargs):
    varargin = TC_Levy_VarianceSwap.varargin
    nargin = TC_Levy_VarianceSwap.nargin

    # levyExponent is function handle: e.g. -1/2*i*xi - 1/2*xi^2 for case of Heston as time changed levy process
# hFunc is function handle: tau = int_0^T h(X_s)ds
# n is number of discrete points for the discrete version, set n = 0 for continuous
# ParamsDiffus are the diffusion parameters of X_s, where tau = int_0^T h(X_s)ds
    
    # Martingale Adjustment for exponent: ensure the driving Levy process itself is a martingale
# Note, we model the RN drift (r-q)*T separately... then price using PROJ
    levyExponentRN=lambda u=None: levyExponent(u) - dot(dot(1j,levyExponent(- 1j)),u)
# TC_Levy_VarianceSwap.m:9
    dt=T / M
# TC_Levy_VarianceSwap.m:11
    ### Set CTMC Parameters (CTMC approximates the diffusion)
    gridMethod=6
# TC_Levy_VarianceSwap.m:14
    
    varGridMult=ParamsCtmc.varGridMult
# TC_Levy_VarianceSwap.m:15
    gamma=ParamsCtmc.gamma
# TC_Levy_VarianceSwap.m:16
    Nx=ParamsCtmc.Nx
# TC_Levy_VarianceSwap.m:17
    
    ### The time change driver process X_t is approximated by CTMC
    if ParamsDiffus.model == 1:
        t=copy(T)
# TC_Levy_VarianceSwap.m:21
        eta=ParamsDiffus.eta
# TC_Levy_VarianceSwap.m:22
        theta=ParamsDiffus.theta
# TC_Levy_VarianceSwap.m:22
        Sigmav=ParamsDiffus.Sigmav
# TC_Levy_VarianceSwap.m:22
        v0=ParamsDiffus.v0
# TC_Levy_VarianceSwap.m:22
        mu_func=lambda v=None: dot(eta,(theta - v))
# TC_Levy_VarianceSwap.m:23
        sig_func=lambda v=None: dot(Sigmav,sqrt(v))
# TC_Levy_VarianceSwap.m:24
        mu_H=dot(exp(dot(- eta,t)),v0) + dot(theta,(1 - exp(dot(- eta,t))))
# TC_Levy_VarianceSwap.m:26
        sig2_H=dot(dot(Sigmav ** 2 / eta,v0),(exp(dot(- eta,t)) - exp(dot(dot(- 2,eta),t)))) + dot(dot(theta,Sigmav ** 2) / (dot(2,eta)),(1 - exp(dot(- eta,t)) + exp(dot(dot(- 2,eta),t))))
# TC_Levy_VarianceSwap.m:27
        lx=max(1e-05,mu_H - dot(gamma,sqrt(sig2_H)))
# TC_Levy_VarianceSwap.m:29
        ux=mu_H + dot(gamma,sqrt(sig2_H))
# TC_Levy_VarianceSwap.m:30
    
    center=copy(v0)
# TC_Levy_VarianceSwap.m:33
    boundaryMethod=1
# TC_Levy_VarianceSwap.m:34
    G,stateGrid=Q_Matrix_AllForms(Nx,mu_func,sig_func,lx,ux,gridMethod,varGridMult,center,boundaryMethod,nargout=2)
# TC_Levy_VarianceSwap.m:35
    H=hFunc(stateGrid)
# TC_Levy_VarianceSwap.m:37
    
    ####////////////////////////////////////////////////////////
#### Find bracketing states
####////////////////////////////////////////////////////////
    j_0=2
# TC_Levy_VarianceSwap.m:42
    
    while v0 >= stateGrid(j_0) and j_0 < Nx:

        j_0=j_0 + 1
# TC_Levy_VarianceSwap.m:44

    
    j_0=j_0 - 1
# TC_Levy_VarianceSwap.m:46
    ####////////////////////////////////////////////////////////
# Risk Neutral CHF of Log Return: ln(S_T/S_0)
####////////////////////////////////////////////////////////
    RNdrift=dot((r - q),dt)
# TC_Levy_VarianceSwap.m:51
    delt=0.005
# TC_Levy_VarianceSwap.m:52
    z=concat([- delt,delt])
# TC_Levy_VarianceSwap.m:53
    
    if n == 0:
        chf=rnCHF_cont(z,levyExponentRN,H,G,dt,stateGrid,RNdrift)
# TC_Levy_VarianceSwap.m:56
    else:
        chf=rnCHF_disc(z,levyExponentRN,H,G,dt,n,stateGrid,RNdrift)
# TC_Levy_VarianceSwap.m:58
    
    Evec=zeros(Nx,1)
# TC_Levy_VarianceSwap.m:61
    for j in arange(1,Nx).reshape(-1):
        M_mh=chf(j,1)
# TC_Levy_VarianceSwap.m:64
        M_0=1
# TC_Levy_VarianceSwap.m:65
        M_ph=chf(j,2)
# TC_Levy_VarianceSwap.m:66
        Evec[j]=- (M_ph - dot(2,M_0) + M_mh) / delt ** 2
# TC_Levy_VarianceSwap.m:67
    
    Pm=expm(dot(dt,G))
# TC_Levy_VarianceSwap.m:70
    PmPm=copy(Pm)
# TC_Levy_VarianceSwap.m:71
    sumPm=eye(Nx,Nx)
# TC_Levy_VarianceSwap.m:72
    for m in arange(2,M).reshape(-1):
        sumPm=sumPm + PmPm
# TC_Levy_VarianceSwap.m:74
        if m < M:
            PmPm=dot(Pm,PmPm)
# TC_Levy_VarianceSwap.m:76
    
    prices=dot(sumPm,Evec)
# TC_Levy_VarianceSwap.m:80
    price=prices(j_0) / T
# TC_Levy_VarianceSwap.m:81
    return price
    
if __name__ == '__main__':
    pass
    