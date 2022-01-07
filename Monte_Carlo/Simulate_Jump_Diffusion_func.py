# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Simulate_Jump_Diffusion_func.m

    
@function
def Simulate_Jump_Diffusion_func(N_sim=None,M=None,T=None,S_0=None,r=None,q=None,sigma=None,jumpModel=None,jumpParams=None,*args,**kwargs):
    varargin = Simulate_Jump_Diffusion_func.varargin
    nargin = Simulate_Jump_Diffusion_func.nargin

    #######################################################
# About: Simulates Paths of Jump Diffusion Models with jumps (including simple Black-Scholes, no jumps)
#        Uses log-Euler scheme
# Returns: paths of dimension (N_sim, M+1), since they include S_0 
#          ... Simulates N_sim paths, each row is a full path starting from S_0, ending with S_M (M+1 points in path)
# Author: Justin Lars Kirkby
    
    # -----------------
# Params
# -----------------
# N_sim = # paths
# M = #time steps on [0,T], time step is dt=T/M, so each path has M+1 points
# T = time to maturity, ie path is on [0,T]
# S_0 = initial underlying value (e.g. S_0=100)
# r = interst rate (e.g. r = 0.05)
# q = dividend yield (e.g. q = 0.05)
# sigma = diffusion parameter (e.g. sigma = 0.2)
    
    #===================================
# jumpModel: 0 = NoJumps, 1 = NormalJumps, 2 = DEJumps, 3 = MixedNormalJumps
#===================================
# jumpParams = paramters container containing all necessary params for models,
#            : if jumpModel = 0, no jump params are needed
#            : if jumpModel > 0, jumpParams must contain lambda, kappa, and any other model specific params (see below)
    
    #######################################################
    if nargin < 8:
        jumpModel=0
# Simulate_Jump_Diffusion_func.m:29
        jumpParams=cellarray([])
# Simulate_Jump_Diffusion_func.m:29
    
    dt=T / M
# Simulate_Jump_Diffusion_func.m:32
    #==============================
# Initialize Jump Model Params and JumpFunc (function handle)
#==============================
### NOTE:  Jump Model is of the form in LOG space
### X(m+1) = X(m) + drift + Brownian Component + sum(Jumps on [m,m+1])
### By Jump we mean log(Y), e.g. in Merton Model, Jump ~ Normal (since we are in log space )
    
    if jumpModel > 0:
        lambda_=jumpParams.lambda
# Simulate_Jump_Diffusion_func.m:42
        kappa=jumpParams.kappa
# Simulate_Jump_Diffusion_func.m:43
        Zeta=r - q - dot(lambda_,kappa)
# Simulate_Jump_Diffusion_func.m:45
        lamdt=dot(lambda_,dt)
# Simulate_Jump_Diffusion_func.m:46
        if jumpModel == 1:
            muJ=jumpParams.muJ
# Simulate_Jump_Diffusion_func.m:49
            sigJ=jumpParams.sigJ
# Simulate_Jump_Diffusion_func.m:50
            JumpFunc=lambda n=None: sum(muJ + dot(sigJ,randn(n,1)))
# Simulate_Jump_Diffusion_func.m:51
        else:
            if jumpModel == 2:
                p_up=jumpParams.p_up
# Simulate_Jump_Diffusion_func.m:54
                eta1=jumpParams.eta1
# Simulate_Jump_Diffusion_func.m:55
                eta2=jumpParams.eta2
# Simulate_Jump_Diffusion_func.m:56
                JumpFunc=lambda n=None: sum(DoubleExpoRnd(n,p_up,eta1,eta2))
# Simulate_Jump_Diffusion_func.m:57
            else:
                if jumpModel == 3:
                    p_up=jumpParams.p_up
# Simulate_Jump_Diffusion_func.m:60
                    a1=jumpParams.a1
# Simulate_Jump_Diffusion_func.m:61
                    b1=jumpParams.b1
# Simulate_Jump_Diffusion_func.m:61
                    a2=jumpParams.a2
# Simulate_Jump_Diffusion_func.m:62
                    b2=jumpParams.b2
# Simulate_Jump_Diffusion_func.m:62
                    JumpFunc=lambda n=None: sum(MixedNormalRnd(n,p_up,a1,b1,a2,b2))
# Simulate_Jump_Diffusion_func.m:63
    else:
        Zeta=r - q
# Simulate_Jump_Diffusion_func.m:66
    
    ##################################################################################
    
    Spath=zeros(N_sim,M + 1)
# Simulate_Jump_Diffusion_func.m:71
    Spath[arange(),1]=S_0
# Simulate_Jump_Diffusion_func.m:72
    Sigsqdt=dot(sigma,sqrt(dt))
# Simulate_Jump_Diffusion_func.m:73
    drift=dot((Zeta - dot(0.5,sigma ** 2)),dt)
# Simulate_Jump_Diffusion_func.m:74
    if jumpModel == 0:
        for m in arange(1,M).reshape(-1):
            W1=randn(N_sim,1)
# Simulate_Jump_Diffusion_func.m:78
            Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(drift + dot(Sigsqdt,W1)))
# Simulate_Jump_Diffusion_func.m:79
    else:
        for m in arange(1,M).reshape(-1):
            Poi=PoissonRnd(N_sim,lamdt)
# Simulate_Jump_Diffusion_func.m:83
            sumJumpsVec=zeros(N_sim,1)
# Simulate_Jump_Diffusion_func.m:84
            for n in arange(1,N_sim).reshape(-1):
                if Poi(n) > 0:
                    sumJumpsVec[n]=JumpFunc(Poi(n))
# Simulate_Jump_Diffusion_func.m:87
            W1=randn(N_sim,1)
# Simulate_Jump_Diffusion_func.m:91
            Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(drift + sumJumpsVec + dot(Sigsqdt,W1)))
# Simulate_Jump_Diffusion_func.m:92
    
    return Spath
    
if __name__ == '__main__':
    pass
    